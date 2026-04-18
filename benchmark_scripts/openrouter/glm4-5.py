"""
run_glm45_air.py  —  GLM-4.5 Air via OpenRouter (Account 1)
Provider  : OpenRouter
Model ID  : z-ai/glm-4.5-air:free
Note      : Supports hybrid thinking/non-thinking modes via reasoning bool.
            We disable thinking mode for consistent, comparable outputs.
Rate limit: 50 RPD free / 1,000 RPD with $10 credit
Env var   : OPENROUTER_API_KEY  (Account 1)

Usage:
    python run_glm45_air.py
    python run_glm45_air.py --dry-run
    python run_glm45_air.py --validate
"""

import os
from openai import OpenAI
from _core import run_benchmark

MODEL_NAME    = "glm45_air"
MODEL_ID      = "z-ai/glm-4.5-air:free"
PAUSE_SECONDS = 2.0

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)


def call(prompt: str, system_prompt: str) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        timeout=90,
        extra_body={"reasoning": {"enabled": False}},  # disable thinking mode
        extra_headers={
            "HTTP-Referer": "https://github.com/ipibench",
            "X-Title": "IPIBench",
        },
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)