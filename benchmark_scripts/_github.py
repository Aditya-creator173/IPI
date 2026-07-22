"""
_github.py  —  Shared GitHub Models client helper.
All GitHub Models scripts import from here to reduce boilerplate.
"""

import time
import _core
import _keys
from openai import OpenAI, APIStatusError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = _keys.get_key("GITHUB")
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=key,
        )
    return _clients[key]

def call_github(
    model_id: str,
    prompt: str,
    system_prompt: str,
    temperature: float = None,
    fold_system_prompt: bool = False,
    timeout: int = 60,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    client = get_client()
    
    if fold_system_prompt:
        if system_prompt:
            prompt = f"{system_prompt}\n\n---\n\n{prompt}"
        messages = [{"role": "user", "content": prompt}]
    else:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
    kwargs = {
        "model": model_id,
        "messages": messages,
        "timeout": timeout,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
        
    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        try:
            resp = client.chat.completions.create(**kwargs)
            if resp.usage:
                _core._call_usage["input_tokens"]  = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            # Handle provider-side content filter (content=None)
            content = resp.choices[0].message.content
            if content is None:
                return "PROVIDER_FILTERED: content field was null (likely provider-side content filter)"
            return content
        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                if e.status_code == 429:
                    try:
                        new_key = _keys.rotate_key("GITHUB")
                        client = get_client()
                        print(f"\n[GitHub] Rate limit hit. Rotating key and retrying immediately...")
                        continue
                    except Exception as ex:
                        print(f"\n[GitHub] Failed to rotate key: {ex}")
                print(f"\n[GitHub] HTTP {e.status_code}. Retrying in {backoff:.0f}s "
                      f"(attempt {attempt + 1}/{max_retries})...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
