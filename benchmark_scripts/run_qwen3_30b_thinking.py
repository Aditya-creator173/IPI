"""
run_qwen3_30b_thinking.py  —  Qwen 3 30B Thinking via QwenCloud / DashScope
Provider  : QwenCloud / DashScope
Model ID  : qwen3-30b-a3b-thinking-2507
Role      : Axis 2 same-arch CoT pair UPDATED (reasoning counterpart) & Axis 3 dense control
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "qwen3_30b_thinking"
MODEL_ID      = "qwen3-30b-a3b-thinking-2507"
PAUSE_SECONDS = 1.0


def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
