"""
run_deepseek_r1.py  —  DeepSeek R1 via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : DeepSeek-R1
Rate tier : LOW — 150 RPD / 50 RPD

Usage:
    python run_deepseek_r1.py
    python run_deepseek_r1.py --dry-run
    python run_deepseek_r1.py --validate
"""

from _core import run_benchmark
from _github import call_github

MODEL_NAME    = "deepseek_r1"
MODEL_ID      = "DeepSeek-R1"
PAUSE_SECONDS = 6.5  # To respect 15 RPM GitHub limits

def call(prompt: str, system_prompt: str) -> str:
    return call_github(MODEL_ID, prompt, system_prompt, timeout=90)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)