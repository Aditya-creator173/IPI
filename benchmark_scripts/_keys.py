"""
_keys.py  —  Shared API key manager for handling pooled provider keys and rotation.
Supports loading multiple numbered keys from .env (e.g., GROQ_API_KEY_1, GROQ_API_KEY_2)
and cycling them efficiently when rate limits occur.
"""

import os

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
    # Try numbered keys first (e.g. GROQ_API_KEY_1, GROQ_TOKEN_1)
    for i in range(1, 100):
        val = os.environ.get(f"{provider_prefix}_API_KEY_{i}") or os.environ.get(f"{provider_prefix}_TOKEN_{i}")
        if val and val.strip():
            keys.append(val.strip())
            
    # Fallback to singular key if no numbered keys found
    if not keys:
        val = os.environ.get(f"{provider_prefix}_API_KEY") or os.environ.get(f"{provider_prefix}_TOKEN")
        if val and val.strip():
            # Support legacy comma-separated list
            parts = [t.strip() for t in val.split(",") if t.strip()]
            keys.extend(parts)
            
    _provider_keys[provider_prefix] = keys
    _provider_indices[provider_prefix] = 0
