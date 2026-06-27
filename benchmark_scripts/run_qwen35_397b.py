"""
run_qwen35_397b.py  —  Qwen 3.5 397B MoE via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : qwen/qwen3.5-397b-a17b  (override via NIM_QWEN35_397B_MODEL_ID)
Params    : 397B total / 17B active (MoE)
Env var   : NVIDIA_KEY_QWEN35_397B  (or NVIDIA_API_KEY fallback)

Research role:
  Alibaba's flagship MoE model. Replaces Qwen3-Next-80B — larger, better
  provider (NIM vs OpenRouter), same Alibaba alignment story.
  Standard RLHF paradigm. Third-largest Chinese AI company.

⚠️  NIM model IDs shift weekly. Verify at build.nvidia.com before running.
    Set NIM_QWEN35_397B_MODEL_ID env var to override without editing this file.

Usage:
    python run_qwen35_397b.py
    python run_qwen35_397b.py --dry-run
    python run_qwen35_397b.py --validate
    python run_qwen35_397b.py --v1-only
"""

import os
import _core
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "qwen35_397b"
MODEL_ID      = os.environ.get("NIM_QWEN35_397B_MODEL_ID", "qwen/qwen3.5-397b-a17b")
PAUSE_SECONDS = 2.0

_key = os.environ.get("NVIDIA_KEY_QWEN35_397B") or os.environ["NVIDIA_API_KEY"]

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
