"""
_cohere.py — Shared Cohere API client helper.
Uses Cohere v2 API endpoint: https://api.cohere.com/v2/chat
Handles key rotation (COHERE_API_KEY) and exponential backoff on 429/5xx errors.
"""

from __future__ import annotations

import json
import time
import urllib.request
import urllib.error
import _core
import _keys


def call_cohere(
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

    payload = {
        "model": model_id,
        "messages": messages,
    }
    body = json.dumps(payload).encode("utf-8")

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        key = _keys.get_key("COHERE")
        req = urllib.request.Request(
            "https://api.cohere.com/v2/chat",
            data=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                
                # Token usage reporting
                usage = data.get("usage", {})
                tokens = usage.get("tokens", {})
                if tokens:
                    _core._call_usage["input_tokens"] = tokens.get("input_tokens", 0)
                    _core._call_usage["output_tokens"] = tokens.get("output_tokens", 0)

                # Extract text content from Cohere v2 response
                content_items = data.get("message", {}).get("content", [])
                text_parts = [item.get("text", "") for item in content_items if item.get("type") == "text"]
                content = "".join(text_parts) if text_parts else None

                if content is None:
                    finish_reason = data.get("finish_reason", "unknown")
                    _core._call_usage["filter_reason"] = (
                        f"cohere: content field was null (finish_reason={finish_reason!r})"
                    )
                    return "PROVIDER_FILTERED: content field was null"
                return content

        except urllib.error.HTTPError as e:
            status_code = e.code
            error_body = e.read().decode("utf-8", errors="ignore")
            if (status_code == 429 or status_code >= 500) and attempt < max_retries:
                if status_code == 429:
                    try:
                        _keys.rotate_key("COHERE")
                        print(f"\n[Cohere] Rate limit hit. Rotated key and retrying...")
                        continue
                    except Exception as ex:
                        print(f"\n[Cohere] Failed to rotate key: {ex}")

                print(f"\n[Cohere] HTTP {status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise RuntimeError(f"Cohere API HTTP {status_code}: {error_body}")
        except urllib.error.URLError as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("COHERE")
                    print(f"\n[Cohere] Connection error. Rotated key and retrying...")
                except Exception:
                    print(f"\n[Cohere] Timeout retry attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
