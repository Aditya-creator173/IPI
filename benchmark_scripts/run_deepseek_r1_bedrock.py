"""
run_deepseek_r1_bedrock.py  —  DeepSeek R1 via AWS Bedrock (Converse API)
Provider  : AWS Bedrock
Model ID  : us.deepseek.r1-v1:0
Role      : Axis 2 (Chain-of-Thought Reasoning Subject) & Axis 4 DeepSeek generational flagship
Auth      : AWS IAM (boto3 standard credentials)
"""

import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))

from _core import run_benchmark
from _bedrock import call_bedrock

MODEL_NAME    = "deepseek_r1"
MODEL_ID      = "us.deepseek.r1-v1:0"
PAUSE_SECONDS = 2.0

def strip_thinking(text: str) -> str:
    """Remove <think>...</think> CoT block from DeepSeek R1 output before scoring."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def call(prompt: str, system_prompt: str) -> str:
    raw_response = call_bedrock(MODEL_ID, prompt, system_prompt)
    return strip_thinking(raw_response)

if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    print("Provider: AWS Bedrock (Converse API) | Role: Axis 2 CoT Reasoning Subject")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
