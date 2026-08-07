import os
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent

    # -------------------------------------------------------------
    # 1. Helper: _qwencloud.py
    # -------------------------------------------------------------
    qwencloud_code = '''"""
_qwencloud.py — Shared QwenCloud (DashScope) API client helper.
Uses OpenAI-compatible client endpoint: https://dashscope.aliyuncs.com/compatible-mode/v1
Handles key rotation (QWEN_API_KEY, DASHSCOPE_API_KEY) and exponential backoff.
"""

from __future__ import annotations

import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APITimeoutError, APIConnectionError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = _keys.get_key("QWENCLOUD")
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=key,
        )
    return _clients[key]

def call_qwencloud(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        client = get_client()
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=timeout,
            )
            if resp.usage:
                _core._call_usage["input_tokens"] = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"qwencloud: content field was null (finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null"
            return content

        except (APITimeoutError, APIConnectionError) as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("QWENCLOUD")
                    print(f"\\n[QwenCloud] Connection/Timeout error. Rotated key and retrying...")
                except Exception:
                    print(f"\\n[QwenCloud] Timeout retry attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                if e.status_code == 429:
                    try:
                        _keys.rotate_key("QWENCLOUD")
                        print(f"\\n[QwenCloud] Rate limit hit. Rotated key and retrying...")
                        continue
                    except Exception as ex:
                        print(f"\\n[QwenCloud] Failed to rotate key: {ex}")

                print(f"\\n[QwenCloud] HTTP {e.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
'''
    (base_dir / "_qwencloud.py").write_text(qwencloud_code, encoding="utf-8")
    print("Created _qwencloud.py")

    # -------------------------------------------------------------
    # 2. Helper: _cloudflare.py
    # -------------------------------------------------------------
    cloudflare_code = '''"""
_cloudflare.py — Shared Cloudflare Workers AI client helper.
Uses OpenAI-compatible client endpoint: https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1
Dynamically loads CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_KEY from environment.
"""

from __future__ import annotations

import os
import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APITimeoutError, APIConnectionError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = _keys.get_key("CLOUDFLARE")
    account_id = (
        os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip() or
        os.environ.get("CLOUDFLARE_ACCOUNT_ID_1", "").strip() or
        os.environ.get("CLOUDFLARE_ACCOUNT", "").strip() or
        os.environ.get("CF_ACCOUNT_ID", "").strip() or
        os.environ.get("ACCOUNT_ID", "").strip()
    )

    if not account_id:
        raise EnvironmentError(
            "CLOUDFLARE_ACCOUNT_ID not found in environment. "
            "Please set CLOUDFLARE_ACCOUNT_ID in your .env file."
        )

    client_key = f"{key}_{account_id}"
    if client_key not in _clients:
        _clients[client_key] = OpenAI(
            base_url=f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1",
            api_key=key,
        )
    return _clients[client_key]

def call_cloudflare(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        client = get_client()
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=timeout,
            )
            if resp.usage:
                _core._call_usage["input_tokens"] = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"cloudflare: content field was null (finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null"
            return content

        except (APITimeoutError, APIConnectionError) as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("CLOUDFLARE")
                    print(f"\\n[Cloudflare] Connection/Timeout error. Rotated key and retrying...")
                except Exception:
                    print(f"\\n[Cloudflare] Timeout retry attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                if e.status_code == 429:
                    try:
                        _keys.rotate_key("CLOUDFLARE")
                        print(f"\\n[Cloudflare] Rate limit hit. Rotated key and retrying...")
                        continue
                    except Exception as ex:
                        print(f"\\n[Cloudflare] Failed to rotate key: {ex}")

                print(f"\\n[Cloudflare] HTTP {e.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
'''
    (base_dir / "_cloudflare.py").write_text(cloudflare_code, encoding="utf-8")
    print("Created _cloudflare.py")

    # -------------------------------------------------------------
    # 3. Helper: _mistral.py
    # -------------------------------------------------------------
    mistral_code = '''"""
_mistral.py — Shared Mistral API client helper.
Uses OpenAI-compatible client endpoint: https://api.mistral.ai/v1
Handles key rotation (MISTRAL_API_KEY) and exponential backoff.
"""

from __future__ import annotations

import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APITimeoutError, APIConnectionError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = _keys.get_key("MISTRAL")
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://api.mistral.ai/v1",
            api_key=key,
        )
    return _clients[key]

def call_mistral(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        client = get_client()
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=timeout,
            )
            if resp.usage:
                _core._call_usage["input_tokens"] = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"mistral: content field was null (finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null"
            return content

        except (APITimeoutError, APIConnectionError) as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("MISTRAL")
                    print(f"\\n[Mistral] Connection/Timeout error. Rotated key and retrying...")
                except Exception:
                    print(f"\\n[Mistral] Timeout retry attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                if e.status_code == 429:
                    try:
                        _keys.rotate_key("MISTRAL")
                        print(f"\\n[Mistral] Rate limit hit. Rotated key and retrying...")
                        continue
                    except Exception as ex:
                        print(f"\\n[Mistral] Failed to rotate key: {ex}")

                print(f"\\n[Mistral] HTTP {e.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
'''
    (base_dir / "_mistral.py").write_text(mistral_code, encoding="utf-8")
    print("Created _mistral.py")

    # -------------------------------------------------------------
    # 4. Helper: _cohere.py
    # -------------------------------------------------------------
    cohere_code = '''"""
_cohere.py — Shared Cohere API client helper.
Uses OpenAI-compatible client endpoint: https://api.cohere.com/v2
Handles key rotation (COHERE_API_KEY) and exponential backoff on 429/5xx errors.
"""

from __future__ import annotations

import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APITimeoutError, APIConnectionError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = _keys.get_key("COHERE")
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://api.cohere.com/v2",
            api_key=key,
        )
    return _clients[key]

def call_cohere(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        client = get_client()
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=timeout,
            )
            if resp.usage:
                _core._call_usage["input_tokens"] = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"cohere: content field null (finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null"
            return content

        except (APITimeoutError, APIConnectionError) as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("COHERE")
                    print(f"\\n[Cohere] Connection/Timeout error. Rotated key and retrying...")
                except Exception:
                    print(f"\\n[Cohere] Timeout retry attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                if e.status_code == 429:
                    try:
                        _keys.rotate_key("COHERE")
                        print(f"\\n[Cohere] Rate limit hit. Rotated key and retrying...")
                        continue
                    except Exception as ex:
                        print(f"\\n[Cohere] Failed to rotate key: {ex}")

                print(f"\\n[Cohere] HTTP {e.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
'''
    (base_dir / "_cohere.py").write_text(cohere_code, encoding="utf-8")
    print("Created _cohere.py")

    # -------------------------------------------------------------
    # 5. Helper: _sambanova.py
    # -------------------------------------------------------------
    sambanova_code = '''"""
_sambanova.py — Shared SambaNova Systems API client helper.
Uses OpenAI-compatible client endpoint: https://api.sambanova.ai/v1
Handles key rotation (SAMBANOVA_API_KEY) and exponential backoff on 429/5xx errors.
"""

from __future__ import annotations

import time
import _core
import _keys
from openai import OpenAI, APIStatusError, APITimeoutError, APIConnectionError

_clients: dict[str, OpenAI] = {}

def get_client() -> OpenAI:
    key = _keys.get_key("SAMBANOVA")
    if key not in _clients:
        _clients[key] = OpenAI(
            base_url="https://api.sambanova.ai/v1",
            api_key=key,
        )
    return _clients[key]

def call_sambanova(
    model_id: str,
    prompt: str,
    system_prompt: str,
    timeout: int = 120,
    max_retries: int = 3,
    initial_backoff: float = 2.0,
) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    backoff = initial_backoff
    for attempt in range(max_retries + 1):
        client = get_client()
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=messages,
                timeout=timeout,
            )
            if resp.usage:
                _core._call_usage["input_tokens"] = resp.usage.prompt_tokens
                _core._call_usage["output_tokens"] = resp.usage.completion_tokens

            content = resp.choices[0].message.content
            if content is None:
                _core._call_usage["filter_reason"] = (
                    f"sambanova: content field null (finish_reason={resp.choices[0].finish_reason!r})"
                )
                return "PROVIDER_FILTERED: content field was null"
            return content

        except (APITimeoutError, APIConnectionError) as e:
            if attempt < max_retries:
                try:
                    _keys.rotate_key("SAMBANOVA")
                    print(f"\\n[SambaNova] Connection/Timeout error. Rotated key and retrying...")
                except Exception:
                    print(f"\\n[SambaNova] Timeout retry attempt {attempt + 1}/{max_retries}: {e}")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise

        except APIStatusError as e:
            if (e.status_code == 429 or e.status_code >= 500) and attempt < max_retries:
                if e.status_code == 429:
                    try:
                        _keys.rotate_key("SAMBANOVA")
                        print(f"\\n[SambaNova] Rate limit hit. Rotated key and retrying...")
                        continue
                    except Exception as ex:
                        print(f"\\n[SambaNova] Failed to rotate key: {ex}")

                print(f"\\n[SambaNova] HTTP {e.status_code}. Retrying in {backoff:.0f}s...")
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
'''
    (base_dir / "_sambanova.py").write_text(sambanova_code, encoding="utf-8")
    print("Created _sambanova.py")

    # -------------------------------------------------------------
    # 6. QwenCloud Model Runner Scripts
    # -------------------------------------------------------------
    qwencloud_models = [
        ("deepseek_v4_flash", "deepseek-v4-flash-0731", "DeepSeek V4 Flash", "run_deepseek_v4_flash.py", "Axis I student arm distillation test"),
        ("qwen37_max", "qwen3.7-max", "Qwen 3.7 Max", "run_qwen37_max.py", "Axis D 4th-gen Qwen flagship MoE"),
        ("qwen38_max", "qwen3.8-max", "Qwen 3.8 Max", "run_qwen38_max.py", "Axis D 5th-gen Qwen flagship 2.4T MoE"),
        ("qwq_plus", "qwq-plus", "QwQ Plus", "run_qwq_plus.py", "Axis B hosted CoT reasoning model"),
        ("qwen35_397b", "qwen3.5-plus", "Qwen 3.5 397B", "run_qwen35_397b.py", "Multilingual pre-training & cross-lingual evasion"),
        ("qwen35_27b", "qwen3.5-27b", "Qwen 3.5 27B", "run_qwen35_27b.py", "Finding 7 open-vs-closed within-lab pair"),
        ("qwen36_27b", "qwen3.6-27b", "Qwen 3.6 27B", "run_qwen36_27b.py", "Finding 7 open-vs-closed within-lab pair"),
        ("glm52", "glm-5.2", "GLM 5.2", "run_glm52.py", "Axis D generational CN safety drift"),
        ("qwen3_coder_480b", "qwen3-coder-480b-a35b-instruct", "Qwen 3 Coder 480B MoE", "run_qwen3_coder_480b.py", "Axis G Chinese lab code-specialized model"),
    ]

    for model_name, model_id, display_name, filename, desc in qwencloud_models:
        code = f'''"""
{filename}  —  {display_name} via QwenCloud (DashScope)
Provider  : QwenCloud (DashScope)
Model ID  : {model_id}
Role      : {desc}
"""

from _core import run_benchmark
from _qwencloud import call_qwencloud

MODEL_NAME    = "{model_name}"
MODEL_ID      = "{model_id}"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_qwencloud(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
'''
        (base_dir / filename).write_text(code, encoding="utf-8")
        print(f"Created {filename}")

    # -------------------------------------------------------------
    # 7. Cloudflare Model Runner Scripts
    # -------------------------------------------------------------
    cloudflare_models = [
        ("sea_lion_v4", "gemma-sea-lion-v4-27b-it", "SEA-LION v4 27B", "run_sea_lion_v4.py", "Regional SEA alignment hypothesis"),
        ("ibm_granite", "granite-4.0-h-micro", "IBM Granite 4.0 H Micro", "run_ibm_granite.py", "Axis J Mamba-2 / Transformer+MoE hybrid"),
        ("qwq32b", "qwq-32b", "QwQ 32B", "run_qwq32b.py", "Axis B cross-lab CoT replication"),
        ("qwen3_30b_moe", "qwen3-30b-a3b-fp8", "Qwen 3 30B MoE", "run_qwen3_30b_moe.py", "Axis C non-Google MoE replication"),
        ("llama4_scout", "llama-4-scout-17b-16e-instruct", "LLaMA 4 Scout", "run_llama4_scout.py", "Axis F scale midpoint & Axis H compound constituent"),
        ("kimi_k2", "kimi-k2-6", "Kimi K2.6", "run_kimi_k2.py", "Extreme long-context MoE"),
    ]

    for model_name, model_id, display_name, filename, desc in cloudflare_models:
        code = f'''"""
{filename}  —  {display_name} via Cloudflare Workers AI
Provider  : Cloudflare Workers AI
Model ID  : {model_id}
Role      : {desc}
"""

from _core import run_benchmark
from _cloudflare import call_cloudflare

MODEL_NAME    = "{model_name}"
MODEL_ID      = "{model_id}"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return call_cloudflare(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
'''
        (base_dir / filename).write_text(code, encoding="utf-8")
        print(f"Created {filename}")

    # -------------------------------------------------------------
    # 8. Mistral, Cohere, SambaNova Runner Scripts
    # -------------------------------------------------------------
    other_runner_configs = [
        ("codestral", "codestral-2508", "Codestral 2508", "run_codestral.py", "_mistral", "call_mistral", "Axis G European code-specialized model"),
        ("mistral_large3", "mistral-large-2512", "Mistral Large 3", "run_mistral_large3.py", "_mistral", "call_mistral", "High-throughput European flagship MoE"),
        ("cohere_command_a_plus", "command-a-plus", "Cohere Command A+", "run_cohere_command_a_plus.py", "_cohere", "call_cohere", "Primary Cohere premium RAG flagship"),
        ("cohere_command_a_reasoning", "command-a-reasoning", "Cohere Command A Reasoning", "run_cohere_command_a_reasoning.py", "_cohere", "call_cohere", "Axis B reasoning variant within Cohere"),
        ("minimax_m2", "minimax-m2.7", "MiniMax M2.7", "run_minimax_m2.py", "_sambanova", "call_sambanova", "High-speed CN MoE inference test"),
        ("deepseek_v32", "deepseek-v3.2", "DeepSeek V3.2", "run_deepseek_v32.py", "_sambanova", "call_sambanova", "Axis D DeepSeek generational trajectory"),
        ("sarvam8b", "sarvam/sarvam-8b", "Sarvam 8B", "run_sarvam8b.py", "_nim", "call_nim", "Regional Hindi specialization vs safety hierarchy"),
    ]

    for model_name, model_id, display_name, filename, helper, func, desc in other_runner_configs:
        code = f'''"""
{filename}  —  {display_name}
Model ID  : {model_id}
Role      : {desc}
"""

from _core import run_benchmark
from {helper} import {func}

MODEL_NAME    = "{model_name}"
MODEL_ID      = "{model_id}"
PAUSE_SECONDS = 1.0

def call(prompt: str, system_prompt: str) -> str:
    return {func}(MODEL_ID, prompt, system_prompt)

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)
'''
        (base_dir / filename).write_text(code, encoding="utf-8")
        print(f"Created {filename}")

    print("All benchmark provider helpers and runner scripts generated successfully!")

if __name__ == "__main__":
    main()


