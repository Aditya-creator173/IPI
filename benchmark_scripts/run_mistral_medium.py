"""
run_mistral_medium.py  —  Mistral Medium 3.5 128B via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : mistralai/mistral-medium-3.5-128b  (override via NIM_MISTRAL_MEDIUM_MODEL_ID)
Params    : 128B dense
Env var   : NVIDIA_KEY_MISTRAL_MEDIUM  (or NVIDIA_API_KEY fallback)

Research role:
  Only European-origin architecture in the benchmark. Built under EU AI Act
  cultural and regulatory pressure. 128B frontier-tier. Replaces Mistral Small
  3.1 24B (GitHub Models) — larger model, better provider, same research story.
  Tests whether regulatory pressure produces different IPI resistance than
  voluntary safety training.

⚠️  NIM model IDs shift weekly. Verify at build.nvidia.com before running.
    Set NIM_MISTRAL_MEDIUM_MODEL_ID env var to override without editing this file.

Usage:
    python run_mistral_medium.py
    python run_mistral_medium.py --dry-run
    python run_mistral_medium.py --validate
    python run_mistral_medium.py --v1-only
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "mistral_medium"
MODEL_ID      = os.environ.get("NIM_MISTRAL_MEDIUM_MODEL_ID", "mistralai/mistral-medium-3.5-128b")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="MISTRAL_MEDIUM")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
