"""
run_grok3_mini.py  —  Grok 3 Mini via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : Grok-3-Mini
Rate tier : HIGH — 50 RPD, 10 RPM
Warning   : 50 RPD means 400 calls takes 8 days at full run.
            Start this script early. It will resume automatically.

Usage:
    python run_grok3_mini.py
    python run_grok3_mini.py --dry-run
    python run_grok3_mini.py --validate
"""

import os
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "grok3_mini"
MODEL_ID      = "Grok-3-Mini"
PAUSE_SECONDS = 8.0   # HIGH tier: 50 RPD — pace to ~7.2s between calls

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