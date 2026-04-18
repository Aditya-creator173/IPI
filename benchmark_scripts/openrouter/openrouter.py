"""
_openrouter.py  —  Shared OpenRouter client helper.
All OpenRouter model scripts import call_openrouter() from here.
"""

import os
from openai import OpenAI

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )
    return _client


def call_openrouter(model_id: str, prompt: str, system_prompt: str, timeout: int = 90) -> str:
    client = get_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=model_id,
        messages=messages,
        timeout=timeout,
        extra_headers={
            "HTTP-Referer": "https://github.com/ipibench",
            "X-Title": "IPIBench",
        },
    )
    return resp.choices[0].message.content