"""
run_glm52.py  —  GLM 5.2 via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : glm-5.2
Role      : Axis D generational CN safety drift
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "glm52"
MODEL_ID      = "glm-5.2"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
