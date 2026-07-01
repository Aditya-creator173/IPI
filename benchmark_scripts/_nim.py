"""
_nim.py  —  Shared NVIDIA NIM client helper.
All NIM model scripts import from here to reduce boilerplate.
"""

import os
import _core
from openai import OpenAI

_clients = {}

def get_client(model_suffix: str):
    key = os.environ.get(f"NVIDIA_KEY_{model_suffix}") or os.environ.get("NVIDIA_API_KEY", "")
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=key,
        )
    return _clients[key]

def call_nim(model_id: str, prompt: str, system_prompt: str, model_suffix: str) -> str:
    client = get_client(model_suffix)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=model_id,
        messages=messages,
        timeout=60,
    )
    if resp.usage:
        _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
        _core._call_usage["output_tokens"] = resp.usage.completion_tokens
    return resp.choices[0].message.content
