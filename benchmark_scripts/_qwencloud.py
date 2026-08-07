"""
_qwencloud.py — Shared QwenCloud (DashScope) API client helper.
Uses OpenAI-compatible client endpoint: https://dashscope.aliyuncs.com/compatible-mode/v1
Handles key rotation (QWEN_API_KEY, DASHSCOPE_API_KEY) and exponential backoff.
"""

from __future__ import annotations

import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APITimeoutError, APIConnectionError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = _keys.get_key("QWENCLOUD")
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=key,
        )
    return _clients[key]

def call_qwencloud(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        client = get_client()
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=timeout,
            )
            if resp.usage:
                _core._call_usage["input_tokens"] = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"qwencloud: content field was null (finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null"
            return content

        except (APITimeoutError, APIConnectionError) as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("QWENCLOUD")
                    print(f"\n[QwenCloud] Connection/Timeout error. Rotated key and retrying...")
                except Exception:
                    print(f"\n[QwenCloud] Timeout retry attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                if e.status_code == 429:
                    try:
                        _keys.rotate_key("QWENCLOUD")
                        print(f"\n[QwenCloud] Rate limit hit. Rotated key and retrying...")
                        continue
                    except Exception as ex:
                        print(f"\n[QwenCloud] Failed to rotate key: {ex}")

                print(f"\n[QwenCloud] HTTP {e.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
