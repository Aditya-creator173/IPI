"""
run_phi4.py  —  Phi-4 14B via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : Phi-4
Rate tier : LOW — 150 RPD, 15 RPM
Endpoint  : https://models.inference.ai.azure.com

Usage:
    python run_phi4.py
    python run_phi4.py --dry-run
    python run_phi4.py --validate
"""

import os
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "phi4"
MODEL_ID      = "Phi-4"
PAUSE_SECONDS = 6.5   # 150 RPD → ~86s between calls to stay safe; use 6.5s for 4 modes

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