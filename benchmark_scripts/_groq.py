"""
_groq.py  —  Shared Groq client helper.
All Groq model scripts import from here to reduce boilerplate.
"""

import os
import _core
from groq import Groq

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    return _client

def call_groq(model_id: str, prompt: str, system_prompt: str) -> str:
    client = get_client()
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
