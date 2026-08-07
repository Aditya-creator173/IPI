"""
_cloudflare.py — Shared Cloudflare Workers AI client helper.
Uses OpenAI-compatible client endpoint: https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1
Dynamically loads CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_KEY from environment.
"""

from __future__ import annotations

import os
import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APITimeoutError, APIConnectionError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = _keys.get_key("CLOUDFLARE")
    account_id = (
        os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip() or
        os.environ.get("CLOUDFLARE_ACCOUNT_ID_1", "").strip() or
        os.environ.get("CLOUDFLARE_ACCOUNT", "").strip() or
        os.environ.get("CF_ACCOUNT_ID", "").strip() or
        os.environ.get("ACCOUNT_ID", "").strip()
    )

    if not account_id:
        raise EnvironmentError(
            "CLOUDFLARE_ACCOUNT_ID not found in environment. "
            "Please set CLOUDFLARE_ACCOUNT_ID in your .env file."
        )

    client_key = f"{key}_{account_id}"
    if client_key not in _clients:
        _clients[client_key] = OpenAI(
            base_url=f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
            api_key=key,
        )
    return _clients[client_key]

def call_cloudflare(
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
                    f"cloudflare: content field was null (finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null"
            return content

        except (APITimeoutError, APIConnectionError) as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("CLOUDFLARE")
                    print(f"\n[Cloudflare] Connection/Timeout error. Rotated key and retrying...")
                except Exception:
                    print(f"\n[Cloudflare] Timeout retry attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                if e.status_code == 429:
                    try:
                        _keys.rotate_key("CLOUDFLARE")
                        print(f"\n[Cloudflare] Rate limit hit. Rotated key and retrying...")
                        continue
                    except Exception as ex:
                        print(f"\n[Cloudflare] Failed to rotate key: {ex}")

                print(f"\n[Cloudflare] HTTP {e.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
