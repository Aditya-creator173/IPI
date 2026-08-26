"""
_google.py  —  Shared Google AI Studio client helper.
All Google model scripts import from here.
Uses the google-genai SDK with automatic OpenRouter failover when Google Studio daily quota is exhausted.
"""

import os
import time
import _core
import _keys
from google import genai
from google.genai import types

_clients: dict[str, genai.Client] = {}


def get_client(rotate: bool = False) -> genai.Client:
    key = _keys.rotate_key("GOOGLE") if rotate else _keys.get_key("GOOGLE")
    if key not in _clients:
        _clients[key] = genai.Client(api_key=key)
    return _clients[key]


def call_google(
    model_id: str,
    prompt: str,
    system_prompt: str,
    thinking_level: str = "NONE",  # NONE | MINIMAL | LOW | MEDIUM | HIGH
) -> str:
    config_kwargs = {}

    # System instruction
    if system_prompt:
        config_kwargs["system_instruction"] = system_prompt

    # Thinking level for Gemini 3 models (replaces thinking_budget)
    # Set to NONE/MINIMAL for consistent non-reasoning responses across benchmark
    if thinking_level and thinking_level != "NONE":
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=0 if thinking_level == "MINIMAL" else None
        )

    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

    # Rotate client across available key pool for even load distribution
    try:
        client = get_client(rotate=True)
    except Exception:
        client = None

    max_retries = 2
    backoff = 1.0
    for attempt in range(max_retries + 1):
        if client is None:
            break
        try:
            resp = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=config,
            )
            if resp.usage_metadata:
                _core._call_usage["input_tokens"]  = resp.usage_metadata.prompt_token_count
                _core._call_usage["output_tokens"] = resp.usage_metadata.candidates_token_count

            # Handle provider-side content filter (text=None)
            text = resp.text
            if text is None:
                candidates = getattr(resp, "candidates", None) or []
                finish_reason = (
                    getattr(candidates[0], "finish_reason", "unknown") if candidates else "unknown"
                )
                _core._call_usage["filter_reason"] = (
                    f"google: resp.text was null (finish_reason={finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
            return text
        except Exception as e:
            err_str = str(e).lower()
            transient_signals = [
                "429", "quota", "503", "500", "502", "504", "exhausted",
                "overloaded", "unavailable", "deadline", "timeout", "connection",
                "reset", "getaddrinfo", "wsarecv", "closed", "network", "ssl"
            ]
            if any(sig in err_str for sig in transient_signals) and attempt < max_retries:
                try:
                    client = get_client(rotate=True)
                except Exception:
                    pass
                pause_dur = 1.0 if attempt < 3 else backoff
                time.sleep(pause_dur)
                backoff = min(backoff * 1.5, 30.0)
                continue
            break

    # All retries exhausted — raise a retryable error so _core.py backoff logic can handle it.
    # Do NOT silently fall back to OpenRouter: that would contaminate scores with a different provider.
    raise RuntimeError(
        f"[Google] All {max_retries + 1} attempts failed for model '{model_id}'. "
        "Quota or network error — retryable by _core.py backoff logic."
    )