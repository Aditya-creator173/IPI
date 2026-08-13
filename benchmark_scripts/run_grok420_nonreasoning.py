"""
run_grok420_nonreasoning.py  —  Grok 4.20 Non-Reasoning via GCP Vertex AI
Provider  : GCP Vertex AI
Model ID  : grok-4.20-non-reasoning
Role      : Axis 2 same-model reasoning pair & Axis 4 generational update
"""

from _core import run_benchmark
from _vertex_ai import call_vertex_grok

MODEL_NAME    = "grok420_nonreasoning"
MODEL_ID      = "grok-4.20-non-reasoning"
PAUSE_SECONDS = 21.0


def call(prompt: str, system_prompt: str) -> str:
    return call_vertex_grok(MODEL_ID, prompt, system_prompt)


if __name__ == "__main__":
    print(f"=== Starting IPIBench Runner: {MODEL_NAME} ({MODEL_ID}) ===")
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
