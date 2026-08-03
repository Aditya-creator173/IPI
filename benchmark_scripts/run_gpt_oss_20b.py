"""
run_gpt_oss_20b.py  —  GPT-OSS 20B via Groq
Provider : Groq
Model ID : openai/gpt-oss-20b
Rate limit: ~14,400 RPD (Groq)

Research role:
  OpenAI's compact open-weight Mixture-of-Experts (MoE) model with 20B total
  parameters (3.6B active per forward pass). Tests cost-efficient MoE scaling
  and agentic reasoning on Groq's high-speed LPU infrastructure.

Usage:
    python run_gpt_oss_20b.py              # full run
    python run_gpt_oss_20b.py --dry-run    # first 3 cases, mode=none
    python run_gpt_oss_20b.py --validate   # A001 x 4 modes, phrase check
"""

from _core import run_benchmark
from _groq import call_groq

MODEL_NAME     = "gpt_oss_20b"
MODEL_ID       = "openai/gpt-oss-20b"
PAUSE_SECONDS  = 1.5

def call(prompt: str, system_prompt: str) -> str:
    return call_groq(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
