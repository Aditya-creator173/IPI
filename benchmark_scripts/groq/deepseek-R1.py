"""
run_deepseek_r1_distill_qwen32b.py  —  DeepSeek R1 Distill Qwen 32B via Groq
Provider : Groq
Model ID : deepseek-r1-distill-qwen-32b
Note     : Reasoning model — produces <think>...</think> tags before answer.
           The response includes the full reasoning trace. attack detection
           runs on the FULL response including think blocks, which means
           we can observe how the model reasons through injections.
Rate limit: Check console.groq.com

Usage:
    python run_deepseek_r1_distill_qwen32b.py
    python run_deepseek_r1_distill_qwen32b.py --dry-run
    python run_deepseek_r1_distill_qwen32b.py --validate
"""

import os
from groq import Groq
from _core import run_benchmark

MODEL_NAME    = "deepseek_r1_distill_qwen32b"
MODEL_ID      = "deepseek-r1-distill-qwen-32b"
PAUSE_SECONDS = 3.0   # reasoning model — longer generation, pace accordingly

client = Groq(api_key=os.environ["GROQ_API_KEY"])


def call(prompt: str, system_prompt: str) -> str:
    # DeepSeek R1 distill models perform best without a system prompt.
    # All context including security notices are folded into the user message.
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n---\n\n{prompt}"
    else:
        full_prompt = prompt

    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.6,   # recommended for R1 distill series
        timeout=90,        # reasoning traces can be long
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)