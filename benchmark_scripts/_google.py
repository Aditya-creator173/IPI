"""
_google.py  —  Shared Google AI Studio client helper.
All Google model scripts import from here.
Uses the google-genai SDK.
"""

import os
import time
import _core
import _keys
from google import genai
from google.genai import types

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = _keys.get_key("GOOGLE")
        _client = genai.Client(api_key=api_key)
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

    max_retries = 3
    backoff = 2.0
    for attempt in range(max_retries + 1):
        try:
            resp = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=config,
            )
            if resp.usage_metadata:
                _core._call_usage["input_tokens"]  = resp.usage_metadata.prompt_token_count
                _core._call_usage["output_tokens"] = resp.usage_metadata.candidates_token_count

            # Handle provider-side content filter (text=None)
            text = resp.text
            if text is None:
                candidates = getattr(resp, "candidates", None) or []
                finish_reason = (
                    getattr(candidates[0], "finish_reason", "unknown") if candidates else "unknown"
                )
                _core._call_usage["filter_reason"] = (
                    f"google: resp.text was null (finish_reason={finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
            return text
        except Exception as e:
            err_str = str(e).lower()
            if ("429" in err_str or "quota" in err_str or "503" in err_str) and attempt < max_retries:
                if "429" in err_str or "quota" in err_str:
                    try:
                        new_key = _keys.rotate_key("GOOGLE")
                        global _client
                        _client = genai.Client(api_key=new_key)
                        client = _client
                        print(f"\n[Google] Rate limit hit. Rotating key and retrying immediately...")
                        continue
                    except Exception as ex:
                        print(f"\n[Google] Failed to rotate key: {ex}")
                print(f"\n[Google] API Error. Retrying in {backoff:.0f}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise