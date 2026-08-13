"""
run_gpt56_luna.py  —  GPT-5.6 Luna via Azure UAE North (Azure OpenAI)
Provider  : Azure UAE North (Azure OpenAI / Foundry)
Model ID  : gpt-5.6-luna
Role      : OpenAI 5th-gen flagship Luna variant
"""

from _core import run_benchmark
from _azure_openai import call_azure_openai

MODEL_NAME    = "gpt56_luna"
MODEL_ID      = "gpt-5.6-luna"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_azure_openai(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print(f"Sampling config: default (gpt-5 family compatibility — no temperature/top_p)")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
