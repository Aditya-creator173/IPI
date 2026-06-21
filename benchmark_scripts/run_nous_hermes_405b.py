"""
run_nous_hermes_405b.py  —  Nous Hermes 3 405B via OpenRouter
Provider  : OpenRouter
Model ID  : nousresearch/hermes-3-405b-instruct:free
Env var   : OPENROUTER_KEY_NOUS_HERMES  (or OPENROUTER_API_KEY fallback)


"""
from _core import run_benchmark
from _openrouter import call_openrouter

MODEL_NAME    = "nous_hermes_405b"
MODEL_ID      = "nousresearch/hermes-3-405b-instruct:free"
PAUSE_SECONDS = 2.0

def call(prompt: str, system_prompt: str) -> str:
    return call_openrouter(MODEL_ID, prompt, system_prompt, model_suffix="NOUS_HERMES")

if __name__ == "__main__":
    run_benchmark(MODEL_NAME, call, MODEL_NAME, PAUSE_SECONDS)