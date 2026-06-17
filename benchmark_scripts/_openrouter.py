"""
_openrouter.py  —  Shared OpenRouter client helper.
All OpenRouter model scripts import call_openrouter() from here.

Key resolution order (most specific wins):
  1. OPENROUTER_KEY_<MODEL_SUFFIX>  (e.g. OPENROUTER_KEY_DEEPSEEK_V3)
  2. OPENROUTER_API_KEY             (fallback — single-key setups)

This allows one key per model (recommended for rate-limit isolation)
while remaining backwards-compatible with a single shared key.
"""

from __future__ import annotations

import os
from openai import OpenAI

_clients: dict[str, OpenAI] = {}


def _get_key(model_suffix: str | None = None) -> str:
    """
    Resolve API key. model_suffix should be the uppercase env var suffix,
    e.g. "DEEPSEEK_V3" for OPENROUTER_KEY_DEEPSEEK_V3.
    Falls back to OPENROUTER_API_KEY.
    """
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
) -> str:
    """
    model_suffix: uppercase suffix matching the env var, e.g. "DEEPSEEK_V3".
    If None, falls back to OPENROUTER_API_KEY.
    """
    client = get_client(model_suffix)
    messages: list[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=model_id,
        messages=messages,
        timeout=timeout,
        extra_headers={
            "HTTP-Referer": "https://github.com/ipibench",
            "X-Title":      "IPIBench",
        },
    )
    return resp.choices[0].message.content