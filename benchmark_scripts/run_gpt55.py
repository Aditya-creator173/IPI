"""
run_gpt55.py  —  GPT-5.5 via Azure UAE North (Azure OpenAI)
Provider  : Azure UAE North (Azure OpenAI / Foundry)
Model ID  : gpt-5.5
Role      : OpenAI current flagship
"""

from _core import run_benchmark
from _azure_openai import call_azure_openai

MODEL_NAME    = "gpt55"
MODEL_ID      = "gpt-5.5"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_azure_openai(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print(f"Sampling config: default (gpt-5 family compatibility — no temperature/top_p)")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
