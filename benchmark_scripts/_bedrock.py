"""
_bedrock.py — Shared AWS Bedrock API client helper.

Routing:
  - bedrock-runtime (Converse API): Claude, Jamba 1.5, DeepSeek R1
  - bedrock-mantle  (OpenAI-compat): Grok 4.3, GPT-5.x (future)

Credential rotation:
  - mantle  : rotates AWS_BEARER_TOKEN_BEDROCK via _keys pool, clears client cache
  - runtime : exponential backoff only (boto3 IAM creds don't rotate per-call)
"""

from __future__ import annotations

import os
import time
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import _core
import _keys

try:
    import boto3
    from botocore.exceptions import ClientError
    _BOTO3_AVAILABLE = True
except ImportError:
    _BOTO3_AVAILABLE = False
    ClientError = Exception  # fallback so isinstance checks don't crash

try:
    from openai import OpenAI, RateLimitError as OpenAIRateLimitError
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False
    OpenAIRateLimitError = Exception  # fallback

# ── Model routing ──────────────────────────────────────────────────────────────
# "mantle_openai"    = OpenAI-compatible bedrock-mantle (Grok 4.3, GPT-5.x)
# "mantle_anthropic" = Anthropic-compatible bedrock-mantle (Claude models)
# "runtime"          = Converse API bedrock-runtime (DeepSeek R1, Jamba)

_MANTLE_OPENAI_MODELS: dict[str, bool] = {
    "xai.grok-4.3":          True,
    "openai.gpt-5.4":        True,
    "openai.gpt-5.6-sol":    True,
    "openai.gpt-5.6-terra":  True,
    "openai.gpt-5.6-luna":   True,
}

_MANTLE_ANTHROPIC_MODELS: dict[str, bool] = {
    "anthropic.claude-haiku-4-5":                 True,
    "anthropic.claude-sonnet-4-6":                True,
    "anthropic.claude-opus-4-6":                  True,
    "us.anthropic.claude-haiku-4-5-20251001-v1:0": True,
    "us.anthropic.claude-sonnet-4-6":             True,
    "us.anthropic.claude-opus-4-6-v1":            True,
}

# ── Client caches ──────────────────────────────────────────────────────────────
# Keyed by region for runtime, by (region, key_prefix) for mantle.
# IMPORTANT: must be cleared after credential rotation so fresh clients are built.

_runtime_clients: dict[str, object] = {}
_mantle_clients:  dict[str, OpenAI] = {}


def _get_region() -> str:
    return os.environ.get("AWS_REGION", "us-east-1").strip() or "us-east-1"


def _clear_mantle_cache() -> None:
    """Wipe mantle client cache so next call builds a fresh client with new key."""
    _mantle_clients.clear()


def _clear_runtime_cache() -> None:
    """Wipe runtime client cache so next call rebuilds with current IAM creds."""
    _runtime_clients.clear()


def _get_runtime_client():
    """boto3 bedrock-runtime client, cached by region."""
    if not _BOTO3_AVAILABLE:
        raise ImportError("boto3 is required. Install with: pip install boto3")
    region = _get_region()
    if region not in _runtime_clients:
        _runtime_clients[region] = boto3.client(
            "bedrock-runtime",
            region_name=region,
        )
    return _runtime_clients[region]


def _get_mantle_client() -> OpenAI:
    """OpenAI-compatible client for bedrock-mantle, cached by (region, key prefix)."""
    if not _OPENAI_AVAILABLE:
        raise ImportError(
            "openai package is required for Grok/GPT models. "
            "Install with: pip install openai"
        )
    region = _get_region()

    api_key = os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "").strip()
    if not api_key:
        try:
            api_key = _keys.get_key("BEDROCK")
        except EnvironmentError:
            api_key = ""

    if not api_key:
        raise ValueError(
            "No Bedrock bearer token found. Set AWS_BEARER_TOKEN_BEDROCK "
            "or BEDROCK_API_KEY_1 in your .env file."
        )

    cache_key = f"{region}:{api_key[:8]}"
    if cache_key not in _mantle_clients:
        _mantle_clients[cache_key] = OpenAI(
            base_url=f"https://bedrock-mantle.{region}.api.aws/openai/v1",
            api_key=api_key,
        )
    return _mantle_clients[cache_key]


# ── Internal callers ───────────────────────────────────────────────────────────

def _call_mantle(
    model_id: str,
    prompt: str,
    system_prompt: str,
    max_tokens: int,
) -> str:
    client = _get_mantle_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.0,
    )
    if resp.usage:
        _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens or 0
        _core._call_usage["output_tokens"] = resp.usage.completion_tokens or 0

    return resp.choices[0].message.content or ""


def _call_converse(
    model_id: str,
    prompt: str,
    system_prompt: str,
    max_tokens: int,
) -> str:
    client = _get_runtime_client()
    # Jamba 1.5 doesn't support Converse system parameter — prepend to user prompt
    if "ai21" in model_id:
        if system_prompt:
            prompt = f"{system_prompt}\n\n{prompt}"
        kwargs: dict = {
            "modelId": model_id,
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": max_tokens, "temperature": 0.0},
        }
    else:
        kwargs: dict = {
            "modelId": model_id,
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": max_tokens, "temperature": 0.0},
        }
        if system_prompt:
            kwargs["system"] = [{"text": system_prompt}]

    resp = client.converse(**kwargs)
    usage = resp.get("usage", {})
    if usage:
        _core._call_usage["input_tokens"]  = usage.get("inputTokens", 0)
        _core._call_usage["output_tokens"] = usage.get("outputTokens", 0)

    output = resp.get("output", {}).get("message", {}).get("content", [])
    return "".join(part["text"] for part in output if "text" in part)


def _call_mantle_anthropic(
    model_id: str,
    prompt: str,
    system_prompt: str,
    max_tokens: int,
) -> str:
    import requests
    region = _get_region()
    api_key = os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "").strip()
    if not api_key:
        try:
            api_key = _keys.get_key("BEDROCK")
        except EnvironmentError:
            api_key = ""

    if not api_key:
        raise ValueError(
            "No Bedrock bearer token found. Set AWS_BEARER_TOKEN_BEDROCK "
            "or BEDROCK_API_KEY_1 in your .env file."
        )

    url = f"https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": model_id,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        payload["system"] = system_prompt

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    if resp.status_code != 200:
        raise Exception(f"Bedrock Mantle Anthropic API Error {resp.status_code}: {resp.text}")

    data = resp.json()
    usage = data.get("usage", {})
    if usage:
        _core._call_usage["input_tokens"] = usage.get("input_tokens", 0)
        _core._call_usage["output_tokens"] = usage.get("output_tokens", 0)

    content_list = data.get("content", [])
    return "".join([c.get("text", "") for c in content_list if c.get("type") == "text"])


# ── Error classification ───────────────────────────────────────────────────────

def _is_rate_limit(e: Exception) -> bool:
    """True if the error is a 429 / throttling error."""
    err_str = str(e).lower()
    if "throttling" in err_str or "toomanyrequests" in err_str or "429" in err_str:
        return True
    if _BOTO3_AVAILABLE and isinstance(e, ClientError):
        code = e.response.get("Error", {}).get("Code", "")
        return code in ("ThrottlingException", "TooManyRequestsException")
    if _OPENAI_AVAILABLE and isinstance(e, OpenAIRateLimitError):
        return True
    return False


def _is_hard_error(e: Exception) -> bool:
    """True if the error is unrecoverable — don't retry."""
    err_str = str(e).lower()
    hard = [
        "accessdenied", "validationexception",
        "resourcenotfound", "not found",
        "modelnotfound", "unsupportedoperation",
    ]
    return any(x in err_str for x in hard)


# ── Public API ─────────────────────────────────────────────────────────────────

def call_bedrock(
    model_id: str,
    prompt: str,
    system_prompt: str = "",
    max_tokens: int = 1024,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    """
    Universal Bedrock caller. Routes automatically:
      bedrock-mantle (OpenAI)    → Grok 4.3, GPT-5.x  (bearer token auth)
      bedrock-mantle (Anthropic) → Claude Haiku, Sonnet, Opus  (bearer token auth)
      bedrock-runtime (Converse) → DeepSeek R1, Jamba  (IAM auth)
    """
    use_mantle_openai = _MANTLE_OPENAI_MODELS.get(model_id, False)
    use_mantle_anthropic = _MANTLE_ANTHROPIC_MODELS.get(model_id, False) or "anthropic" in model_id.lower() or "claude" in model_id.lower()
    use_mantle = use_mantle_openai or use_mantle_anthropic
    backoff = initial_backoff

    for attempt in range(max_retries + 1):
        try:
            if use_mantle_anthropic:
                return _call_mantle_anthropic(model_id, prompt, system_prompt, max_tokens)
            elif use_mantle_openai:
                return _call_mantle(model_id, prompt, system_prompt, max_tokens)
            else:
                return _call_converse(model_id, prompt, system_prompt, max_tokens)

        except Exception as e:

            # Never retry hard errors
            if _is_hard_error(e):
                raise

            if attempt >= max_retries:
                raise

            is_429 = _is_rate_limit(e)

            if is_429 and use_mantle:
                # ── Rotate bearer token + bust cache so fresh client is built ──
                try:
                    new_key = _keys.rotate_key("BEDROCK")
                    # Sync the new key back into env so _get_mantle_client picks it up
                    os.environ["AWS_BEARER_TOKEN_BEDROCK"] = new_key
                    _clear_mantle_cache()   # ← this is the critical fix
                    print(
                        f"[Bedrock] 429 on mantle attempt {attempt+1}. "
                        f"Rotated bearer token, cleared client cache. "
                        f"Retrying in {backoff}s..."
                    )
                except Exception as rot_err:
                    print(f"[Bedrock] Key rotation failed ({rot_err}), backing off anyway.")

            elif is_429 and not use_mantle:
                # boto3 runtime: just backoff, no key rotation
                print(
                    f"[Bedrock] 429 on runtime attempt {attempt+1} for {model_id}. "
                    f"Backing off {backoff}s..."
                )

            else:
                # Non-429 transient error
                print(f"[Bedrock] Error on attempt {attempt+1}: {e}. Retrying in {backoff}s...")

            time.sleep(backoff)
            backoff *= 2
