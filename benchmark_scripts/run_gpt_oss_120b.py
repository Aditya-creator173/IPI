"""
run_gpt_oss_120b.py  —  GPT-OSS 120B via Groq
Provider : Groq
Model ID : openai/gpt-oss-120b
Rate limit: Check console.groq.com

Usage:
    python run_gpt_oss_120b.py
    python run_gpt_oss_120b.py --dry-run
    python run_gpt_oss_120b.py --validate
"""

import os
from groq import Groq
from _core import run_benchmark

MODEL_NAME    = "gpt_oss_120b"
MODEL_ID      = "openai/gpt-oss-120b"
PAUSE_SECONDS = 2.0

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