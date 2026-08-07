"""
run_grok4.py  —  Grok 4.3 via AWS Bedrock
Provider  : AWS Bedrock
Model ID  : xai.grok-4-3
"""

from _core import run_benchmark
from _bedrock import call_bedrock

MODEL_NAME    = "grok4"
MODEL_ID      = "xai.grok-4-3"
PAUSE_SECONDS = 1.5

def call(prompt: str, system_prompt: str) -> str:
    return call_bedrock(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
