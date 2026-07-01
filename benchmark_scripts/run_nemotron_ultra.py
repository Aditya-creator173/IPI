"""
run_nemotron_ultra.py  —  NVIDIA Nemotron 3 Ultra via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : nvidia/nemotron-3-ultra-550b-a55b  (override via NIM_NEMOTRON_ULTRA_MODEL_ID)
Env var   : NVIDIA_KEY_NEMOTRON_ULTRA  (or NVIDIA_API_KEY fallback)

Usage:
    python run_nemotron_ultra.py
    python run_nemotron_ultra.py --dry-run
    python run_nemotron_ultra.py --validate
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "nemotron_ultra"
MODEL_ID      = os.environ.get("NIM_NEMOTRON_ULTRA_MODEL_ID", "nvidia/nemotron-3-ultra-550b-a55b")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="NEMOTRON_ULTRA")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
