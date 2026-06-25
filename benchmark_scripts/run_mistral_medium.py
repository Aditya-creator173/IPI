"""
run_mistral_medium.py  —  Mistral Medium 3.5 128B via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : mistralai/mistral-medium-3.5-128b  (override via NIM_MISTRAL_MEDIUM_MODEL_ID)
Env var   : NVIDIA_KEY_MISTRAL_MEDIUM  (or NVIDIA_API_KEY fallback)

Usage:
    python run_mistral_medium.py
    python run_mistral_medium.py --dry-run
    python run_mistral_medium.py --validate
"""

import os
import _core
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "mistral_medium"
MODEL_ID      = os.environ.get("NIM_MISTRAL_MEDIUM_MODEL_ID", "mistralai/mistral-medium-3.5-128b")
PAUSE_SECONDS = 2.0

_key = os.environ.get("NVIDIA_KEY_MISTRAL_MEDIUM") or os.environ["NVIDIA_API_KEY"]

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=_key,
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
