"""
run_llama31_405b.py  —  LLaMA 3.1 405B Instruct via SambaNova Cloud
Provider  : SambaNova Cloud
Model ID  : Meta-Llama-3.1-405B-Instruct
Env var   : SAMBANOVA_API_KEY
"""

import os
from _core import run_benchmark
from _sambanova import call_sambanova

MODEL_NAME    = "llama31_405b"
MODEL_ID      = os.environ.get("SAMBANOVA_MODEL_405B", "Meta-Llama-3.1-405B-Instruct")
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_sambanova(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
