"""
run_qwq_plus.py  —  QwQ Plus via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : qwq-plus
Role      : Axis B hosted CoT reasoning model
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "qwq_plus"
MODEL_ID      = "qwq-plus"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
