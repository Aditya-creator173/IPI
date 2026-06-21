"""
run_jamba.py  —  AI21 Jamba 1.5 Large via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : AI21-Jamba-1.5-Large
Rate tier : LOW — 150 RPD, 15 RPM

Usage:
    python run_jamba.py
    python run_jamba.py --dry-run
    python run_jamba.py --validate
"""

import os
import _core
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "jamba"
MODEL_ID      = "AI21-Jamba-1.5-Large"
PAUSE_SECONDS = 6.5

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
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