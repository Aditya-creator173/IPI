"""
_keys.py  —  Shared API key manager for handling pooled provider keys and rotation.
Supports loading multiple numbered keys from .env (e.g., GROQ_API_KEY_1, GROQ_API_KEY_2)
and cycling them efficiently when rate limits occur.
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_provider_keys: dict[str, list[str]] = {}
_provider_indices: dict[str, int] = {}


def get_key(provider_prefix: str) -> str:
    """
    Get the currently active key for the provider.
    provider_prefix: e.g., "GROQ", "NVIDIA", "GITHUB", "OPENROUTER", "GOOGLE"
    """
    if provider_prefix not in _provider_keys:
        _init_provider(provider_prefix)
    
    keys = _provider_keys[provider_prefix]
    if not keys:
        raise EnvironmentError(
            f"No API keys found for {provider_prefix}. "
            f"Set {provider_prefix}_API_KEY_1 in your .env file."
        )
    
    idx = _provider_indices[provider_prefix]
    return keys[idx]


def rotate_key(provider_prefix: str) -> str:
    """
    Rotate to the next key for the provider and return it.
    """
    if provider_prefix not in _provider_keys:
        _init_provider(provider_prefix)
        
    keys = _provider_keys[provider_prefix]
    if not keys:
        raise EnvironmentError(f"No API keys found for {provider_prefix}.")
        
    idx = (_provider_indices[provider_prefix] + 1) % len(keys)
    _provider_indices[provider_prefix] = idx
    print(f"\n[KeyManager] Rotated {provider_prefix} key to index {idx+1}/{len(keys)}.")
    return keys[idx]


def _init_provider(provider_prefix: str):
    keys = []
    # Known aliases for provider prefixes
    prefixes = [provider_prefix]
    if provider_prefix == "QWENCLOUD":
        prefixes.extend(["QWEN", "DASHSCOPE"])
    elif provider_prefix == "BEDROCK":
        prefixes.extend(["AWS", "AWS_BEDROCK"])

    # Try numbered keys first (e.g. QWEN_API_KEY_1, GROQ_API_KEY_1)
    for pfx in prefixes:
        for i in range(1, 100):
            val = (
                os.environ.get(f"{pfx}_API_KEY_{i}") or 
                os.environ.get(f"{pfx}_TOKEN_{i}") or
                os.environ.get(f"{pfx}_KEY_{i}")
            )
            if val and val.strip() and val.strip() not in keys:
                keys.append(val.strip())
            
    # Fallback to unnumbered keys if no numbered keys found (e.g. QWEN_API_KEY, SAMBANOVA_API_KEY)
    if not keys:
        for pfx in prefixes:
            val = (
                os.environ.get(f"{pfx}_API_KEY") or 
                os.environ.get(f"{pfx}_TOKEN") or
                os.environ.get(f"{pfx}_KEY") or
                (os.environ.get("AWS_BEARER_TOKEN_BEDROCK") if pfx in ("BEDROCK", "AWS") else None) or
                (os.environ.get("AWS_ACCESS_KEY_ID") if pfx == "AWS" else None)
            )
            if val and val.strip():
                parts = [t.strip() for t in val.split(",") if t.strip()]
                for part in parts:
                    if part not in keys:
                        keys.append(part)
            
    _provider_keys[provider_prefix] = keys
    _provider_indices[provider_prefix] = 0


