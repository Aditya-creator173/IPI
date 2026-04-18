"""
run_mistral_small.py  —  Mistral Small 3.1 via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : Mistral-Small-3.1-24B-Instruct-2503
Rate tier : LOW — 150 RPD, 15 RPM

Usage:
    python run_mistral_small.py
    python run_mistral_small.py --dry-run
    python run_mistral_small.py --validate
"""

import os
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "mistral_small"
MODEL_ID      = "Mistral-Small-3.1-24B-Instruct-2503"
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
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)