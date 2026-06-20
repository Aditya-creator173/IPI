"""
run_deepseek_r1_0528.py  —  DeepSeek R1-0528 via OpenRouter (Account 1)
Provider  : OpenRouter
Model ID  : deepseek/deepseek-r1-0528:free
Rate limit: 50 RPD free / 1,000 RPD with $10 credit
Env var   : OPENROUTER_API_KEY  (Account 1)

Note: This is the CURRENT DeepSeek R1 model (May 2028 release).
Distinct from run_deepseek_r1_distill_qwen32b.py (Groq — distilled variant).
Produces visible <think>...</think> reasoning traces.
Attack detection runs on full response including think blocks —
this lets us observe how the model reasons through injections.

Usage:
    python run_deepseek_r1_0528.py
    python run_deepseek_r1_0528.py --dry-run
    python run_deepseek_r1_0528.py --validate
    python run_deepseek_r1_0528.py --full
"""

from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "deepseek_r1_0528"
MODEL_ID      = "deepseek/deepseek-r1-0528:free"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)