"""
run_llama4_scout.py  —  Llama 4 Scout via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : Llama-4-Scout-17B-16E
Rate tier : LOW — 150 RPD, 15 RPM

Usage:
    python run_llama4_scout.py
    python run_llama4_scout.py --dry-run
    python run_llama4_scout.py --validate
"""

from _core import run_benchmark
from _github import call_github

MODEL_NAME    = "llama4_scout"
MODEL_ID      = "Llama-4-Scout-17B-16E"
PAUSE_SECONDS = 6.5

def call(prompt: str, system_prompt: str) -> str:
    return call_github(MODEL_ID, prompt, system_prompt, timeout=60)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)