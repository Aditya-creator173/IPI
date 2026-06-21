"""
run_glm51.py  —  GLM 5.1 via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : z-ai/glm-5.1  (override via NIM_GLM51_MODEL_ID)
Env var   : NVIDIA_KEY_GLM51  (or NVIDIA_API_KEY fallback)

Usage:
    python run_glm51.py
    python run_glm51.py --dry-run
    python run_glm51.py --validate
"""

import os
import _core
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "glm51"
MODEL_ID      = os.environ.get("NIM_GLM51_MODEL_ID", "z-ai/glm-5.1")
PAUSE_SECONDS = 2.0

_key = os.environ.get("NVIDIA_KEY_GLM51") or os.environ["NVIDIA_API_KEY"]

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
