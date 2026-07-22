"""
run_gemini36_flash.py  —  Gemini 3.6 Flash via Google AI Studio
Provider  : Google AI Studio
Model ID  : gemini-3.6-flash (verified live)
Rate limit: 1,500 RPD (shared pool across Google keys)
Env var   : GOOGLE_API_KEY

Research role:
  Google's next-generation Flash model. Paired with Gemini 3.5 Flash
  for intra-lab generational safety comparison (Gemini 3.5 Flash <-> Gemini 3.6 Flash),
  replacing the dropped GLM 5.1 <-> 5.2 axis gap.
"""

from _core import run_benchmark
from _google import call_google

MODEL_NAME    = "gemini36_flash"
MODEL_ID      = "gemini-3.6-flash"
PAUSE_SECONDS = 1.0


def call(prompt: str, system_prompt: str) -> str:
    return call_google(MODEL_ID, prompt, system_prompt, thinking_level="NONE")


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
