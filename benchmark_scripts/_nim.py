"""
_nim.py  —  Shared NVIDIA NIM client helper.
All NIM model scripts import from here to reduce boilerplate.

Key resolution order (most specific wins):
  1. NVIDIA_KEY_<MODEL_SUFFIX>  (e.g. NVIDIA_KEY_NEMOTRON_ULTRA)
  2. NVIDIA_API_KEY             (fallback — single-key setups)

If neither is set, raises EnvironmentError immediately (fail-fast) rather
than caching OpenAI(api_key="") and producing a silent 401 later.
"""

from __future__ import annotations

import os
import time
import _core
from openai import OpenAI, APIStatusError

_clients: dict[str, OpenAI] = {}


def _get_key(model_suffix: str) -> str:
    """
    Resolve NVIDIA API key. Raises EnvironmentError with an explicit message
    naming the missing variable(s) if no key is found — avoids the silent
    OpenAI(api_key="") path that caches a broken client under the "" dict key.
    """
    key = os.environ.get(f"NVIDIA_KEY_{model_suffix}") or os.environ.get("NVIDIA_API_KEY", "")
    if not key:
        raise EnvironmentError(
            f"No NVIDIA API key found. Set NVIDIA_KEY_{model_suffix} or "
            "NVIDIA_API_KEY in your .env file."
        )
    return key


def get_client(model_suffix: str) -> OpenAI:
    key = _get_key(model_suffix)
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=key,
        )
    return _clients[key]


def call_nim(
    model_id: str,
    prompt: str,
    system_prompt: str,
    model_suffix: str,
    timeout: int = 60,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    """
    Call a NIM model with exponential backoff retry on 429/5xx errors.

    NIM has a documented 40 RPM hard cap; transient rate-limit hits should be
    retried rather than written as API_ERROR rows. Model IDs also drift weekly
    (see script comments) — 404s are NOT retried (they indicate a stale model
    ID, not a transient error).
    """
    client = get_client(model_suffix)
    messages = []
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
                    f"nim: content field was null "
                    f"(finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
            return content

        except APIStatusError as e:
            # Retry on 429 (rate limits) and 5xx (server errors).
            # Do NOT retry 404 — stale model IDs should surface immediately.
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                print(
                    f"\n[NIM] HTTP {e.status_code}. Retrying in {backoff:.0f}s "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
