"""
[RETIRED — July 12 2026]
run_gpt5.py  —  GPT-5 via GitHub Models

Retired because:
  - 50 RPD cap forces --v1-only (20 cases only); cannot produce a full result.
  - Replaced by two-entry strategy:
      run_gpt4o.py   →  GPT-4o via GitHub Models (150 RPD, full 400-case run, Tier B)
      run_gpt55.py   →  GPT-5.5 via TokenBay (full run, Tier C, free trial credits)
    Together these provide the cross-generation OpenAI pair without the rate-limit wall.

  Script kept on disk for historical reference. Do not include in automated benchmark runs.

Original provider  : GitHub Models (PAT)
Original model ID  : gpt-5
Original rate tier : HIGH — 50 RPD, 10 RPM
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