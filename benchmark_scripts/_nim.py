"""
Shared NVIDIA NIM client helper.
Resolves model-specific keys with a fallback to NVIDIA_API_KEY.
"""

from __future__ import annotations

import time
import _core
import _keys
from openai import OpenAI, APIStatusError

_clients: dict[str, OpenAI] = {}


def get_client() -> OpenAI:
    key = _keys.get_key("NVIDIA")
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
    model_suffix: str, # Kept for backward compatibility
    timeout: int = 60,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    """Call a NIM model with exponential backoff on 429/5xx errors. Do not retry 404s."""
    client = get_client()
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

            # Handle provider-side content filter (content=None)
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
                if e.status_code == 429:
                    try:
                        new_key = _keys.rotate_key("NVIDIA")
                        client = get_client()
                        print(f"\n[NIM] Rate limit hit. Rotating key and retrying immediately...")
                        continue
                    except Exception as ex:
                        print(f"\n[NIM] Failed to rotate key: {ex}")

                print(
                    f"\n[NIM] HTTP {e.status_code}. Retrying in {backoff:.0f}s "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
