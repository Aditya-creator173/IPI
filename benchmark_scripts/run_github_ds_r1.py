"""
run_github_ds_r1.py  —  DeepSeek R1-0528 via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : DeepSeek-R1-0528
Rate tier : LOW — 150 RPD, 15 RPM

Usage:
    python run_github_ds_r1.py
    python run_github_ds_r1.py --dry-run
    python run_github_ds_r1.py --validate
"""

from _core import run_benchmark
from _github import call_github, client

MODEL_NAME    = "github_ds_r1"
MODEL_ID      = "DeepSeek-R1-0528"
PAUSE_SECONDS = 6.5

def call(prompt: str, system_prompt: str) -> str:
    return call_github(MODEL_ID, prompt, system_prompt, temperature=0.6, fold_system_prompt=True, timeout=90)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)