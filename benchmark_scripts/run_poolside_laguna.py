"""
Runner for Poolside Laguna M.1 via OpenRouter
"""

import os
import sys

# Add the parent directory to the path so we can import _core and _openrouter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark_scripts import _core
from benchmark_scripts import _openrouter

MODEL_NAME = "poolside_laguna_m1"
OPENROUTER_SLUG = "poolside/laguna-m.1:free"
PAUSE_SECONDS = 3  # Add a small pause for free tiers to avoid 429s

def call(prompt: str, system_prompt: str) -> str:
    """Wrapper to pass the specific model slug to the shared OpenRouter client."""
    return _openrouter.call_openrouter(
        model_id=OPENROUTER_SLUG,
        prompt=prompt,
        system_prompt=system_prompt
    )

if __name__ == "__main__":
    _core.run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
