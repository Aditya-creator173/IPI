"""
run_cohere_command_a.py  —  Cohere Command A via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : Cohere-command-a
Rate tier : LOW — 150 RPD, 15 RPM

Usage:
    python run_cohere_command_a.py
    python run_cohere_command_a.py --dry-run
    python run_cohere_command_a.py --validate
"""

from _core import run_benchmark
from _github import call_github, client

MODEL_NAME    = "cohere_command_a"
MODEL_ID      = "Cohere-command-a"
PAUSE_SECONDS = 6.5

def call(prompt: str, system_prompt: str) -> str:
    return call_github(MODEL_ID, prompt, system_prompt, timeout=60)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)