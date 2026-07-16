"""
Shared SambaNova Cloud client helper.
"""

from __future__ import annotations

import os
import time
import _core
from openai import OpenAI, APIStatusError

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        key = os.environ.get("SAMBANOVA_API_KEY", "")
        if not key:
            raise EnvironmentError(
                "SAMBANOVA_API_KEY not set. Create a free account at cloud.sambanova.ai "
                "and add the key to your .env file."
            )
        _client = OpenAI(
            base_url="https://api.sambanova.ai/v1",
            api_key=key,
        )
    return _client


def call_sambanova(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 90,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    """Call a SambaNova model with exponential backoff on 429/5xx errors."""
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

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"sambanova: content field was null "
                    f"(finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
            return content

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                print(
                    f"\n[SambaNova] HTTP {e.status_code}. Retrying in {backoff:.0f}s "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
