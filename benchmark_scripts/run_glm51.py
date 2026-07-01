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
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "glm51"
MODEL_ID      = os.environ.get("NIM_GLM51_MODEL_ID", "z-ai/glm-5.1")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="GLM51")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
