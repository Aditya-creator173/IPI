"""
run_sarvam_m.py  —  Sarvam-M via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : sarvamai/sarvam-m  (override via NIM_SARVAM_M_MODEL_ID)
Params    : ~8B dense
Env var   : NVIDIA_KEY_SARVAM_M  (or NVIDIA_API_KEY fallback)

Research role:
  Only Indian model in any IPI benchmark. Natively trained on Hindi, Tamil,
  Telugu, Kannada, and other Indian languages. Directly intersects A027
  (Hindi bypass attack). Native-language training may produce fundamentally
  different resistance profile for multilingual injection attacks.
  Only model from India in the entire set.

⚠️  NIM model IDs shift weekly. Verify at build.nvidia.com before running.
    Set NIM_SARVAM_M_MODEL_ID env var to override without editing this file.

Usage:
    python run_sarvam_m.py
    python run_sarvam_m.py --dry-run
    python run_sarvam_m.py --validate
    python run_sarvam_m.py --v1-only
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "sarvam_m"
MODEL_ID      = os.environ.get("NIM_SARVAM_M_MODEL_ID", "sarvamai/sarvam-m")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="SARVAM_M")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
