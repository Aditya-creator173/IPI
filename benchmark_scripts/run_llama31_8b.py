"""
run_llama31_8b.py  —  LLaMA 3.1 8B via Groq
Provider : Groq
Model ID : llama-3.1-8b-instant
Rate limit: ~14,400 RPD (most generous on Groq)

Usage:
    python run_llama31_8b.py              # full run
    python run_llama31_8b.py --dry-run    # first 3 cases, mode=none
    python run_llama31_8b.py --validate   # A001 x 4 modes, phrase check
"""

import os
import _core
from groq import Groq
from _core import run_benchmark

MODEL_NAME     = "llama3.1_8b"
MODEL_ID       = "llama-3.1-8b-instant"
PAUSE_SECONDS  = 1.5   # conservative; 8B has the highest limit on Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])


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