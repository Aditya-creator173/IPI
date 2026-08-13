"""
run_sea_lion_v4.py  —  SEA-LION v4 27B via Cloudflare Workers AI
Provider  : Cloudflare Workers AI
Model ID  : gemma-sea-lion-v4-27b-it
Role      : Regional SEA alignment hypothesis
"""

from _core import run_benchmark
from _cloudflare import call_cloudflare

MODEL_NAME    = "sea_lion_v4"
MODEL_ID      = "@cf/aisingapore/gemma-sea-lion-v4-27b-it"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cloudflare(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
