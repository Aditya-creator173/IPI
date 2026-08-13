"""
run_claude_haiku.py  —  Claude Haiku 4.5 via AWS Bedrock
Provider  : AWS Bedrock
Model ID  : anthropic.claude-3-5-haiku-20241022-v1:0
"""

from _core import run_benchmark
from _bedrock import call_bedrock

MODEL_NAME    = "claude_haiku"
MODEL_ID      = "anthropic.claude-haiku-4-5"
PAUSE_SECONDS = 1.5

def call(prompt: str, system_prompt: str) -> str:
    return call_bedrock(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
