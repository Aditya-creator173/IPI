"""
run_deepseek_v4_pro.py  —  DeepSeek V4 Pro via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : deepseek/deepseek-v4-pro  (override via NIM_DEEPSEEK_V4_PRO_MODEL_ID)
Env var   : NVIDIA_KEY_DEEPSEEK_V4_PRO  (or NVIDIA_API_KEY fallback)

Usage:
    python run_deepseek_v4_pro.py
    python run_deepseek_v4_pro.py --dry-run
    python run_deepseek_v4_pro.py --validate
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "deepseek_v4_pro"
MODEL_ID      = os.environ.get("NIM_DEEPSEEK_V4_PRO_MODEL_ID", "deepseek/deepseek-v4-pro")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="DEEPSEEK_V4_PRO")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
