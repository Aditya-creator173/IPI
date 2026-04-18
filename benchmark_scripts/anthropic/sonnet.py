"""
run_claude_sonnet.py  —  Claude Sonnet 4.6 via Anthropic API
Provider  : Anthropic
Model ID  : claude-sonnet-4-6
Rate limit: Depends on credits granted
Env var   : ANTHROPIC_API_KEY

Usage:
    python run_claude_sonnet.py
    python run_claude_sonnet.py --dry-run
    python run_claude_sonnet.py --validate
"""

import os
import anthropic
from _core import run_benchmark

MODEL_NAME    = "claude_sonnet"
MODEL_ID      = "claude-sonnet-4-6"
PAUSE_SECONDS = 2.0

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def call(prompt: str, system_prompt: str) -> str:
    kwargs = {
        "model":      MODEL_ID,
        "max_tokens": 1024,
        "messages":   [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    resp = client.messages.create(**kwargs)
    return "".join(
        block.text for block in resp.content if hasattr(block, "text")
    )


if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)