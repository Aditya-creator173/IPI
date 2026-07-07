"""
run_nous_hermes_405b.py  —  Nous Hermes 3 405B via OpenRouter
Provider  : OpenRouter
Model ID  : nousresearch/hermes-3-405b-instruct:free
Env var   : OPENROUTER_KEY_NOUS_HERMES  (or OPENROUTER_API_KEY fallback)

Research role:
  Deliberately safety-reduced fine-tune of LLaMA 3.1 405B (Llama 3.1 405B
  Instruct base, confirmed via Nous Research technical report and HuggingFace
  model card). Serves as the upper-bound vulnerability ceiling: shows what
  IPI vulnerability looks like when alignment fine-tuning is stripped away.

  CONTROLLED PAIR with run_llama31_405b.py (SambaNova):
    - Identical base weights: Meta-Llama-3.1-405B-Instruct
    - Changed variable: safety-reduction fine-tuning (Hermes) vs. standard
      Meta RLHF alignment (LLaMA 3.1 405B baseline)
    - Any vulnerability difference is attributable to fine-tuning, not scale

  Expected to be the most vulnerable model in the benchmark. Results provide
  the calibration ceiling against which all other models' resistance is compared.

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