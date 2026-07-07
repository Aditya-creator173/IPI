"""
[MANUAL ONLY — do not use in automated benchmark runs]
run_grok4.py  —  Grok 4 via xAI API
Provider  : xAI (OpenAI-compatible)
Model ID  : grok-4  (override via XAI_MODEL_ID)
Env var   : XAI_API_KEY
Rate tier : Credit-based — $25 free credit on signup, then paid.

Why manual-only:
  xAI billing is credit-based. A full 100-case automated run across all
  defense modes would consume credits at an unpredictable rate. Grok 4
  findings (NRF-003, NRF-011 — creator-authority hijacking, in-group
  impersonation) were captured in dedicated manual sessions and are
  already documented. Script kept on disk for ad-hoc probing only.

Research role:
  Source of NRF-003 (creator authority hijacking) and NRF-011
  (in-group creator impersonation). Manual case-study model only.

Usage (manual probe sessions only):
    python run_grok4.py --dry-run
    python run_grok4.py --validate
"""


import os
import _core
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "grok4"
MODEL_ID      = os.environ.get("XAI_MODEL_ID", "grok-4")
PAUSE_SECONDS = 2.0

client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key=os.environ["XAI_API_KEY"],
)


def call(prompt: str, system_prompt: str) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        timeout=60,
    )
    if resp.usage:
        _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
        _core._call_usage["output_tokens"] = resp.usage.completion_tokens
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
