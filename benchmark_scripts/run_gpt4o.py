"""
run_gpt4o.py  —  GPT-4o via GitHub Models
Provider  : GitHub Models (PAT)
Model ID  : gpt-4o
Rate tier : HIGH — 150 RPD, 15 RPM   (more generous than GPT-5's 50 RPD)

Research role:
  Community-standard flagship. GPT-4o is the most widely used OpenAI model
  by the research and developer community — it is the de-facto reference point
  against which newer OpenAI models are compared. Replacing GPT-5 (v1-only,
  50 RPD) with GPT-4o gives:

  1. Full 400-case automated run (150 RPD covers the benchmark in ~3 days at
     PAUSE_SECONDS=6.5 without hitting rate limits).

  2. Cross-generation pair with GPT-5.5 (TokenBay):
       GPT-4o  →  pre-GPT-5 OpenAI RLHF baseline
       GPT-5.5 →  current OpenAI flagship
     The ASR delta isolates two generations of OpenAI alignment progress.

  3. Community reproducibility: GPT-4o is Tier B (GitHub Models — Microsoft
     hosted, well-established), while GPT-5.5 is Tier C (TokenBay). Having
     GPT-4o in Tier B anchors the OpenAI cross-generation comparison in a
     higher-confidence result.

Provider note:
  GitHub Models hosts GPT-4o via Microsoft Azure OpenAI Service — this is the
  same backend as Azure OpenAI, not a promotional trial. Model identity is
  substantially more verifiable than Tier C providers.

Usage:
    python run_gpt4o.py
    python run_gpt4o.py --dry-run
    python run_gpt4o.py --validate
    python run_gpt4o.py --v1-only
"""

from _core import run_benchmark
from _github import call_github, client

MODEL_NAME    = "gpt4o"
MODEL_ID      = "gpt-4o"
PAUSE_SECONDS = 6.5   # 150 RPD ÷ 400 calls = ~2.7 days at 6.5s pause — safe

def call(prompt: str, system_prompt: str) -> str:
    return call_github(MODEL_ID, prompt, system_prompt, timeout=60)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
