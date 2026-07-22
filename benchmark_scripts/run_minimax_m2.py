"""
run_minimax_m2.py  —  MiniMax M2.7 via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : minimax/minimax-m2.7  (override via NIM_MINIMAX_M2_MODEL_ID)
Env var   : NVIDIA_KEY_MINIMAX_M2  (or NVIDIA_API_KEY fallback)

Usage:
    python run_minimax_m2.py
    python run_minimax_m2.py --dry-run
    python run_minimax_m2.py --validate
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "minimax_m2"
MODEL_ID      = os.environ.get("NIM_MINIMAX_M2_MODEL_ID", "minimaxai/minimax-m2.7")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="MINIMAX_M2")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
