"""
run_seed_oss_36b.py  —  ByteDance Seed OSS 36B via NVIDIA NIM
Provider  : NVIDIA NIM (OpenAI-compatible)
Model ID  : bytedance/seed-oss-36b-instruct  (override via NIM_SEED_OSS_36B_MODEL_ID)
Params    : 36B dense
Env var   : NVIDIA_KEY_SEED_OSS  (or NVIDIA_API_KEY fallback)

Research role:
  ByteDance's open-weights baseline. Testing ByteDance's safety-alignment
  against prompt injections. Expiring soon on NVIDIA NIM catalog.

Usage:
    python run_seed_oss_36b.py
    python run_seed_oss_36b.py --dry-run
    python run_seed_oss_36b.py --validate
"""

import os
from _core import run_benchmark
from _nim import call_nim

MODEL_NAME    = "seed_oss_36b"
MODEL_ID      = os.environ.get("NIM_SEED_OSS_36B_MODEL_ID", "bytedance/seed-oss-36b-instruct")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="SEED_OSS")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
