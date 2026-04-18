"""
run_gpt5.py  —  GPT-5 via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : gpt-5
Rate tier : HIGH — 50 RPD, 10 RPM
Warning   : Same 50 RPD constraint as Grok 3 Mini. Run on a dedicated
            machine that stays on for multiple days.

Usage:
    python run_gpt5.py
    python run_gpt5.py --dry-run
    python run_gpt5.py --validate
"""

import os
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "gpt5"
MODEL_ID      = "gpt-5"
PAUSE_SECONDS = 8.0

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
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)