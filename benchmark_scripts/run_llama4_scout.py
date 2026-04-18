"""
run_llama4_scout.py  —  Llama 4 Scout 17B 16E via Groq
Provider : Groq
Model ID : meta-llama/llama-4-scout-17b-16e-instruct
Rate limit: Check console.groq.com — MoE model, limits vary

Usage:
    python run_llama4_scout.py
    python run_llama4_scout.py --dry-run
    python run_llama4_scout.py --validate
"""

import os
from groq import Groq
from _core import run_benchmark

MODEL_NAME    = "llama4_scout"
MODEL_ID      = "meta-llama/llama-4-scout-17b-16e-instruct"
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