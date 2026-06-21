"""
run_grok4.py  —  Grok 4 via xAI API
Provider  : xAI (OpenAI-compatible)
Model ID  : grok-4  (override via XAI_MODEL_ID)
Env var   : XAI_API_KEY
Rate tier : Based on your xAI credit balance.

Usage:
    python run_grok4.py
    python run_grok4.py --dry-run
    python run_grok4.py --validate
"""

import os
import _core
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "grok4"
MODEL_ID      = os.environ.get("XAI_MODEL_ID", "grok-4")
PAUSE_SECONDS = 2.0

client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key=os.environ["XAI_API_KEY"],
)


def call(prompt: str, system_prompt: str) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        timeout=60,
    )
    if resp.usage:
        _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
        _core._call_usage["output_tokens"] = resp.usage.completion_tokens
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
