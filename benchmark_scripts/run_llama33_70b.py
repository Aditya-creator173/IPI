"""
run_llama33_70b.py  —  LLaMA 3.3 70B via Groq
Provider : Groq
Model ID : llama-3.3-70b-versatile
Rate limit: ~1,000 RPD — run overnight, do not saturate in one session

Usage:
    python run_llama33_70b.py
    python run_llama33_70b.py --dry-run
    python run_llama33_70b.py --validate
"""

import os
from groq import Groq
from _core import run_benchmark

MODEL_NAME    = "llama33_70b"
MODEL_ID      = "llama-3.3-70b-versatile"
PAUSE_SECONDS = 4.0   # 70B has tighter limits; pace to stay under 1000/day

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
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)