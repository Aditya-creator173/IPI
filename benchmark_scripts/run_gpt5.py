"""
run_gpt5.py  —  GPT-5 via Azure OpenAI / Azure Foundry
Provider  : Azure UAE North / Azure Foundry
Model ID  : gpt-5 (configurable via AZURE_GPT5_DEPLOYMENT)
Role      : OpenAI 5th-gen flagship anchor & Axis 4/12 frontier baseline
"""

import os
from _core import run_benchmark
from _azure_openai import call_azure_openai

MODEL_NAME    = "gpt5"
MODEL_ID      = os.environ.get("AZURE_GPT5_DEPLOYMENT", "gpt-5")
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_azure_openai(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print("Provider: Azure OpenAI / Azure Foundry")
    print("Sampling config: default (gpt-5 family compatibility — no temperature/top_p)")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)