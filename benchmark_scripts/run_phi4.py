"""
run_phi4.py  —  Phi-4 14B via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : Phi-4
Rate tier : LOW — 150 RPD, 15 RPM
Endpoint  : https://models.inference.ai.azure.com

Usage:
    python run_phi4.py
    python run_phi4.py --dry-run
    python run_phi4.py --validate
"""

from _core import run_benchmark
from _github import call_github, client

MODEL_NAME    = "phi4"
MODEL_ID      = "Phi-4"
PAUSE_SECONDS = 6.5   # 150 RPD → ~86s between calls to stay safe; use 6.5s for 4 modes

def call(prompt: str, system_prompt: str) -> str:
    return call_github(MODEL_ID, prompt, system_prompt, timeout=60)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)