"""
_openrouter.py  —  Shared OpenRouter client helper.
All OpenRouter model scripts import call_openrouter() from here.

Key resolution order (most specific wins):
  1. OPENROUTER_KEY_<MODEL_SUFFIX>  (e.g. OPENROUTER_KEY_DEEPSEEK_V3)
  2. OPENROUTER_API_KEY             (fallback — single-key setups)

If model_suffix is not passed explicitly, it is auto-detected from the
calling script's filename (e.g. run_deepseek_v3.py -> DEEPSEEK_V3).
This allows per-model key isolation with zero code changes per script.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import _core
from openai import OpenAI, APIStatusError

_clients: dict[str, OpenAI] = {}


def _get_key(model_suffix: str | None = None) -> str:
    """
    Resolve API key.

    If model_suffix is None, auto-detects from the running script filename:
        run_deepseek_v3.py  ->  DEEPSEEK_V3  ->  OPENROUTER_KEY_DEEPSEEK_V3

    Falls back to OPENROUTER_API_KEY if no per-model key is found.
    """
    if not model_suffix:
        script_name = Path(sys.argv[0]).stem
        if script_name.startswith("run_"):
            model_suffix = script_name[4:].upper()  # e.g. "DEEPSEEK_V3"

    if model_suffix:
        specific = os.environ.get(f"OPENROUTER_KEY_{model_suffix.upper()}")
        if specific:
            return specific

    generic = os.environ.get("OPENROUTER_API_KEY", "")
    if not generic:
        raise EnvironmentError(
            "No OpenRouter API key found. Set OPENROUTER_API_KEY or "
            f"OPENROUTER_KEY_{(model_suffix or 'MODEL').upper()} in your .env file."
        )
    return generic


def get_client(model_suffix: str | None = None) -> OpenAI:
    key = _get_key(model_suffix)
    # Cache client per key — avoids re-initialising on every call
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=key,
        )
    return _clients[key]


def call_openrouter(
    model_id: str,
    prompt: str,
    system_prompt: str,
    model_suffix: str | None = None,
    timeout: int = 90,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    """
    Call an OpenRouter model with exponential backoff retry on 429/5xx errors.

    model_suffix: uppercase suffix matching the env var, e.g. "DEEPSEEK_V3".
    If None, auto-detected from the calling script's filename.
    """
    client = get_client(model_suffix)
    messages: list[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=timeout,
                extra_headers={
                    "HTTP-Referer": "https://github.com/ipibench",
                    "X-Title":      "IPIBench",
                },
            )
            if resp.usage:
                _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            # Guard: provider-side content filters set content=None.
            # Write filter_reason into _call_usage so _core.py can persist
            # provider-specific diagnostic detail into the CSV filter_reason column.
            # The definitive sentinel substitution is also applied in _core.py
            # (covers all providers); this guard is extra defence-in-depth.
            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"openrouter: content field was null "
                    f"(finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
            return content
        except APIStatusError as e:
            # Retry on 429 (rate limits) and 5xx (server/concurrency issues)
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                print(f"\n[OpenRouter] HTTP {e.status_code}. Retrying in {backoff:.0f}s "
                      f"(attempt {attempt + 1}/{max_retries})...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise