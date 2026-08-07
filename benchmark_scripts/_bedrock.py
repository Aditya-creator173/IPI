"""
_bedrock.py — Shared AWS Bedrock API client helper.
Uses boto3 bedrock-runtime client or key rotation (BEDROCK_API_KEY_1).
"""

from __future__ import annotations

import os
import time
import json
import _core
import _keys

try:
    import boto3
    _BOTO3_AVAILABLE = True
except ImportError:
    _BOTO3_AVAILABLE = False

_clients: dict[str, object] = {}

def get_client():
    if not _BOTO3_AVAILABLE:
        raise ImportError("boto3 is required for AWS Bedrock API calls. Install with: pip install boto3")
    key = _keys.get_key("BEDROCK")
    region = os.environ.get("AWS_REGION", "us-east-1")
    if key not in _clients:
        _clients[key] = boto3.client("bedrock-runtime", region_name=region)
    return _clients[key]

def call_bedrock(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    messages = [{"role": "user", "content": prompt}]
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": messages,
    }
    if system_prompt:
        body["system"] = system_prompt

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            client = get_client()
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            response_body = json.loads(response.get("body").read())
            usage = response_body.get("usage", {})
            if usage:
                _core._call_usage["input_tokens"] = usage.get("input_tokens", 0)
                _core._call_usage["output_tokens"] = usage.get("output_tokens", 0)

            content = response_body.get("content", [])
            text_parts = [item["text"] for item in content if item.get("type") == "text"]
            return "".join(text_parts)

        except Exception as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("BEDROCK")
                    print(f"\n[Bedrock] Error ({e}). Rotated key and retrying...")
                except Exception:
                    pass
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
