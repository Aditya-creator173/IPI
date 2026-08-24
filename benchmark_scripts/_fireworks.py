"""
_fireworks.py  —  Shared Fireworks AI client helper.
Used for Fireworks API endpoints (Llama 3.1 405B, Nous Hermes 3 405B, Kimi K3, etc.)
"""

from __future__ import annotations

import os
import time
import _core
import _keys
from openai import OpenAI, APIStatusError, RateLimitError, APIConnectionError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        try:
            key = _keys.get_key("FIREWORKS")
        except Exception:
            key = ""

    if not key:
        raise EnvironmentError(
            "FIREWORKS_API_KEY is missing. Please set FIREWORKS_API_KEY=your_key in .env."
        )

    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://api.fireworks.ai/inference/v1",
            api_key=key,
        )
    return _clients[key]


def call_fireworks(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 5,
    initial_backoff: float = 2.0,
    max_tokens: int = 8192,
) -> str:
    """
    Call a Fireworks AI model endpoint with exponential backoff on rate limits / 5xx errors.
    """
    client = get_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            start_time = time.time()
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.0,
                timeout=timeout,
            )
            latency = int((time.time() - start_time) * 1000)

            if resp.usage:
                _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens or 0
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens or 0
                _core._call_usage["latency_ms"]    = latency

            if not resp.choices:
                return "API_ERROR: Empty choices array returned"

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"fireworks: content field was null "
                    f"(finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (provider content filter)"

            return content

        except (APIStatusError, RateLimitError, APIConnectionError) as e:
            status = getattr(e, "status_code", 429)
            if (status == 429 or status >= 500) and attempt < max_retries:
                if status == 429:
                    try:
                        new_key = _keys.rotate_key("FIREWORKS")
                        global _clients
                        _clients.clear()
                        client = get_client()
                        print("\n[Fireworks] Rate limit hit. Rotated key and retrying...")
                    except Exception:
                        pass
                print(f"\n[Fireworks] HTTP {status}. Retrying in {backoff:.1f}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(backoff)
                backoff *= 2.0
                continue
            if attempt == max_retries:
                return f"API_ERROR: Fireworks AI failed after {max_retries} retries: {e}"
            raise

        except Exception as e:
            return f"API_ERROR: Unexpected error: {e}"

    return "API_ERROR: Exceeded max retries"
