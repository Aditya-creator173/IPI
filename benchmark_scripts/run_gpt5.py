"""
run_gpt5.py  —  GPT-5 via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : gpt-5
Rate tier : HIGH — 50 RPD, 10 RPM
Warning   : Same 50 RPD constraint as Grok 3 Mini. Run on a dedicated
            machine that stays on for multiple days.

Usage:
    python run_gpt5.py
    python run_gpt5.py --dry-run
    python run_gpt5.py --validate
"""

from _core import run_benchmark
from _github import call_github, client

MODEL_NAME    = "gpt5"
MODEL_ID      = "gpt-5"
PAUSE_SECONDS = 8.0

def call(prompt: str, system_prompt: str) -> str:
    return call_github(MODEL_ID, prompt, system_prompt, timeout=60)


if __name__ == "__main__":
    import sys
    if not any(f in sys.argv for f in ["--v1-only", "--dry-run", "--validate"]):
        print("\n[ABORT] GPT-5 has a strict 50 RPD limit. Running the full 400-case benchmark will fail.")
        print("Please use --v1-only to evaluate the 20-case subset.\n")
        sys.exit(1)
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)