"""
run_kimi_k2.py  —  Moonshot Kimi K2.6 via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : moonshotai/kimi-k2.6  (override via NIM_KIMI_K2_MODEL_ID)
Env var   : NVIDIA_KEY_KIMI_K2  (or NVIDIA_API_KEY fallback)

Usage:
    python run_kimi_k2.py
    python run_kimi_k2.py --dry-run
    python run_kimi_k2.py --validate
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "kimi_k2"
MODEL_ID      = os.environ.get("NIM_KIMI_K2_MODEL_ID", "moonshotai/kimi-k2.6")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="KIMI_K2")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
