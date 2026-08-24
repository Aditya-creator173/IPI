"""
run_phi4.py  —  Phi-4 14B via Azure Foundry / Azure OpenAI
Provider  : Azure UAE North / Azure Foundry
Model ID  : Phi-4 (configurable via AZURE_PHI4_DEPLOYMENT)
Role      : Synthetic pre-training hypothesis & Axis 13 SLM architecture
"""

import os
from _core import run_benchmark
from _azure_openai import call_azure_openai

MODEL_NAME    = "phi4"
MODEL_ID      = os.environ.get("AZURE_PHI4_DEPLOYMENT", "phi-4")
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_azure_openai(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print("Provider: Azure Foundry / Azure OpenAI")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)