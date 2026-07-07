"""
run_gemini35_flash.py  —  Gemini 3.5 Flash via Google AI Studio
Provider  : Google AI Studio
Model ID  : gemini-3.5-flash
Rate limit: 1,500 RPD (shared pool across all Google models on same key)
Env var   : GOOGLE_API_KEY

Research role:
  Google's closed flagship in the automated cohort. Paired with Gemma 4 31B
  and Gemma 4 26B MoE for open-vs-closed comparison within the same lab.
  Independent inclusion criterion: closes the Google closed-frontier coverage
  gap that Gemma 4 (open-weight) cannot fill alone.

  NOTE: NRF-022 through NRF-028 (behavioral probing findings) were produced
  in a SEPARATE manual session using Gemini 3.1 Pro (web UI, gemini.google.com)
  with a system prompt sourced from Pliny the Liberator's GitHub repository
  (Tier 3 community source). Those findings are qualitative case studies,
  not automated benchmark results, and are NOT attributable to this script.

Usage:
    python run_gemini35_flash.py
    python run_gemini35_flash.py --dry-run
    python run_gemini35_flash.py --validate
    python run_gemini35_flash.py --v1-only
"""

from _core import run_benchmark
from _google import call_google

MODEL_NAME    = "gemini35_flash"
MODEL_ID      = "gemini-3.5-flash"
PAUSE_SECONDS = 1.0   # 1,500 RPD is generous


def call(prompt: str, system_prompt: str) -> str:
    return call_google(MODEL_ID, prompt, system_prompt, thinking_level="NONE")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
