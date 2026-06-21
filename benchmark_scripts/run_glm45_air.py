"""
run_glm45_air.py  —  GLM-4.5 Air via OpenRouter
Provider  : OpenRouter
Model ID  : z-ai/glm-4.5-air:free
Env var   : OPENROUTER_KEY_GLM45_AIR  (or OPENROUTER_API_KEY fallback)

"""
from _core import run_benchmark
from _openrouter import call_openrouter
from openai import OpenAI
import os

MODEL_NAME    = "glm45_air"
MODEL_ID      = "z-ai/glm-4.5-air:free"
PAUSE_SECONDS = 2.0


def call(prompt: str, system_prompt: str) -> str:
    # GLM requires reasoning disabled explicitly via extra_body
    # Cannot use the shared call_openrouter helper for this model
    from _openrouter import get_client
    client = get_client("GLM45_AIR")
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        timeout=90,
        extra_body={"reasoning": {"enabled": False}},
        extra_headers={
            "HTTP-Referer": "https://github.com/ipibench",
            "X-Title":      "IPIBench",
        },
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)