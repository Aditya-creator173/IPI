"""
run_mai_ds_r1.py  —  MAI-DS-R1 via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : MAI-DS-R1
Rate tier : LOW — 150 RPD, 15 RPM

Usage:
    python run_mai_ds_r1.py
    python run_mai_ds_r1.py --dry-run
    python run_mai_ds_r1.py --validate
"""

import os
import _core
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "mai_ds_r1"
MODEL_ID      = "MAI-DS-R1"
PAUSE_SECONDS = 6.5

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)


def call(prompt: str, system_prompt: str) -> str:
    # R1-based model — fold system prompt into user message
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n---\n\n{prompt}"
    else:
        full_prompt = prompt

    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.6,
        timeout=90,
    )
    if resp.usage:
        _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
        _core._call_usage["output_tokens"] = resp.usage.completion_tokens
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)