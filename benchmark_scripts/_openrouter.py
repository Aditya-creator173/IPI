"""
Shared OpenRouter client helper.
Resolves keys automatically based on calling script filename.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import _core
import _keys
from openai import OpenAI, APIStatusError

_clients: dict[str, OpenAI] = {}


def get_client() -> OpenAI:
    key = _keys.get_key("OPENROUTER")
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
    model_suffix: str | None = None, # Kept for backward compatibility
    timeout: int = 90,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    """
    Call an OpenRouter model with exponential backoff retry on 429/5xx errors.
    """
    client = get_client()
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

            # Handle provider-side content filter (content=None)
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
                if e.status_code == 429:
                    try:
                        new_key = _keys.rotate_key("OPENROUTER")
                        client = get_client()
                        print(f"\n[OpenRouter] Rate limit hit. Rotating key and retrying immediately...")
                        continue
                    except Exception as ex:
                        print(f"\n[OpenRouter] Failed to rotate key: {ex}")
                print(f"\n[OpenRouter] HTTP {e.status_code}. Retrying in {backoff:.0f}s "
                      f"(attempt {attempt + 1}/{max_retries})...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise