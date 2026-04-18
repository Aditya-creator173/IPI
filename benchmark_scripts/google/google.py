"""
_google.py  —  Shared Google AI Studio client helper.
All Google model scripts import from here.
Uses the google-genai SDK.
"""

import os
from google import genai
from google.genai import types

_client = None


def get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


def call_google(
    model_id: str,
    prompt: str,
    system_prompt: str,
    thinking_level: str = "NONE",  # NONE | MINIMAL | LOW | MEDIUM | HIGH
) -> str:
    client = get_client()

    config_kwargs = {}

    # System instruction
    if system_prompt:
        config_kwargs["system_instruction"] = system_prompt

    # Thinking level for Gemini 3 models (replaces thinking_budget)
    # Set to NONE/MINIMAL for consistent non-reasoning responses across benchmark
    if thinking_level and thinking_level != "NONE":
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=0 if thinking_level == "MINIMAL" else None
        )

    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

    resp = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=config,
    )
    return resp.text