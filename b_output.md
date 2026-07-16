Starting audit script...
SECTION B TABLE:
| Script | B1 (MODEL_NAME) | B2 (MODEL_ID) | B3 (def call() | B4 (run_benchmark() | B5 ([MANUAL ONLY]) | B6 (PENDING) | B7 (Provider Import) | B8 (os.environ[) | B9 (try/except) |
|---|---|---|---|---|---|---|---|---|---|
| ./.venv/Lib/site-packages/openai/types/beta/threads/run_create_params.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/run_list_params.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/run_status.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/run_submit_tool_outputs_params.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/run_update_params.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/runs/run_step.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/runs/run_step_delta.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/runs/run_step_delta_event.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/runs/run_step_delta_message_delta.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/beta/threads/runs/run_step_include.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/evals/run_cancel_response.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/evals/run_create_params.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/evals/run_create_response.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/evals/run_delete_response.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/evals/run_list_params.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/evals/run_list_response.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./.venv/Lib/site-packages/openai/types/evals/run_retrieve_response.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./benchmark_scripts/legacy_models/run_github_ds_r1.py | YES â€” MODEL_NAME    = "github_ds_r1" | YES â€” MODEL_ID      = "DeepSeek-R1-0528" | YES | YES | NO | NO | from _github import call_github, client | NONE FOUND. | NO |
| ./benchmark_scripts/legacy_models/run_llama4_maverick.py | YES â€” MODEL_NAME    = "llama4_maverick" | YES â€” MODEL_ID      = os.environ.get("NIM_MAVERICK_MODEL_ID", "meta/llama-4-maverick-17b-128e-instruct") | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/legacy_models/run_mistral_medium.py | YES â€” MODEL_NAME    = "mistral_medium" | YES â€” Model ID  : mistralai/mistral-medium-3.5-128b  (override via NIM_MISTRAL_MEDIUM_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/legacy_models/run_sarvam_m.py | YES â€” MODEL_NAME    = "sarvam_m" | YES â€” Model ID  : sarvamai/sarvam-m  (override via NIM_SARVAM_M_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_claude_haiku.py | YES â€” MODEL_NAME    = "claude_haiku" | YES â€” MODEL_ID      = "claude-haiku-4-5-20251001"   # update if 4.8 ID confirmed | YES | YES | NO | NO | NO PROVIDER IMPORT FOUND. | 37 | NO |
| ./benchmark_scripts/run_claude_opus.py | YES â€” MODEL_NAME    = "claude_opus" | YES â€” MODEL_ID      = "claude-opus-4-8"    # verify at console.anthropic.com | YES | YES | NO | NO | NO PROVIDER IMPORT FOUND. | 31 | NO |
| ./benchmark_scripts/run_claude_sonnet.py | YES â€” MODEL_NAME    = "claude_sonnet" | YES â€” MODEL_ID      = "claude-sonnet-4-6"   # update if newer string confirmed | YES | YES | NO | NO | NO PROVIDER IMPORT FOUND. | 30 | NO |
| ./benchmark_scripts/run_cohere_command_a.py | YES â€” MODEL_NAME    = "cohere_command_a" | YES â€” MODEL_ID      = "Cohere-command-a" | YES | YES | NO | NO | from _github import call_github, client | NONE FOUND. | NO |
| ./benchmark_scripts/run_deepseek_r1.py | YES â€” MODEL_NAME    = "deepseek_r1" | YES â€” MODEL_ID      = "deepseek/deepseek-r1-0528:free" | YES | YES | NO | NO | from _openrouter import call_openrouter | NONE FOUND. | NO |
| ./benchmark_scripts/run_deepseek_v4_pro.py | YES â€” MODEL_NAME    = "deepseek_v4_pro" | YES â€” Model ID  : deepseek/deepseek-v4-pro  (override via NIM_DEEPSEEK_V4_PRO_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_diffusiongemma.py | YES â€” MODEL_NAME    = "diffusiongemma" | YES â€” Model ID  : google/diffusiongemma-26b-a4b-it  (override via NIM_DIFFUSIONGEMMA_MODEL_ID) | YES | YES | NO | YES | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_gemini35_flash.py | YES â€” MODEL_NAME    = "gemini35_flash" | YES â€” MODEL_ID      = "gemini-3.5-flash" | YES | YES | NO | NO | from _google import call_google | NONE FOUND. | NO |
| ./benchmark_scripts/run_gemma4_26b_moe.py | YES â€” MODEL_NAME    = "gemma4_26b_moe" | YES â€” MODEL_ID      = "gemma-4-26b-a4b-it" | YES | YES | NO | NO | from _google import call_google | NONE FOUND. | NO |
| ./benchmark_scripts/run_gemma4_31b.py | YES â€” MODEL_NAME    = "gemma4_31b" | YES â€” MODEL_ID      = "gemma-4-31b-it" | YES | YES | NO | NO | from _google import call_google | NONE FOUND. | NO |
| ./benchmark_scripts/run_glm51.py | YES â€” MODEL_NAME    = "glm51" | YES â€” Model ID  : z-ai/glm-5.1  (override via NIM_GLM51_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_glm52.py | YES â€” MODEL_NAME    = "glm52" | YES â€” Model ID  : z-ai/glm-5.2  (override via NIM_GLM52_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_gpt4o.py | YES â€” MODEL_NAME    = "gpt4o" | YES â€” MODEL_ID      = "gpt-4o" | YES | YES | NO | NO | from _github import call_github, client | NONE FOUND. | NO |
| ./benchmark_scripts/run_gpt5.py | YES â€” MODEL_NAME    = "gpt5" | YES â€” MODEL_ID      = "gpt-5" | YES | YES | NO | NO | from _github import call_github, client | NONE FOUND. | NO |
| ./benchmark_scripts/run_gpt_oss_120b.py | YES â€” MODEL_NAME    = "gpt_oss_120b" | YES â€” MODEL_ID      = "openai/gpt-oss-120b" | YES | YES | NO | NO | from _groq import call_groq | NONE FOUND. | NO |
| ./benchmark_scripts/run_grok4.py | YES â€” MODEL_NAME    = "grok4" | YES â€” Model ID  : grok-4  (override via XAI_MODEL_ID) | YES | YES | NO | NO | NO PROVIDER IMPORT FOUND. | 37 | NO |
| ./benchmark_scripts/run_kimi_k2.py | YES â€” MODEL_NAME    = "kimi_k2" | YES â€” Model ID  : moonshotai/kimi-k2.6  (override via NIM_KIMI_K2_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_liquidai_lfm.py | YES â€” MODEL_NAME    = "liquidai_lfm" | YES â€” MODEL_ID      = "liquid/lfm-7b:free" | YES | YES | NO | NO | from _openrouter import call_openrouter | NONE FOUND. | NO |
| ./benchmark_scripts/run_llama31_405b.py | YES â€” MODEL_NAME    = "llama31_405b" | YES â€” MODEL_ID      = os.environ.get("SAMBANOVA_MODEL_405B", "Meta-Llama-3.1-405B-Instruct") | YES | YES | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | NO |
| ./benchmark_scripts/run_llama31_8b.py | YES â€” MODEL_NAME     = "llama3.1_8b" | YES â€” MODEL_ID       = "llama-3.1-8b-instant" | YES | YES | NO | NO | from _groq import call_groq | NONE FOUND. | NO |
| ./benchmark_scripts/run_llama32_3b.py | YES â€” MODEL_NAME    = "llama32_3b" | YES â€” MODEL_ID      = "meta-llama/llama-3.2-3b-instruct:free" | YES | YES | NO | NO | from _openrouter import call_openrouter | NONE FOUND. | NO |
| ./benchmark_scripts/run_llama33_70b.py | YES â€” MODEL_NAME    = "llama33_70b" | YES â€” MODEL_ID      = "llama-3.3-70b-versatile" | YES | YES | NO | NO | from _groq import call_groq | NONE FOUND. | NO |
| ./benchmark_scripts/run_llama4_scout.py | YES â€” MODEL_NAME    = "llama4_scout" | YES â€” MODEL_ID      = "meta-llama/llama-4-scout-17b-16e-instruct" | YES | YES | NO | NO | from _groq import call_groq | NONE FOUND. | NO |
| ./benchmark_scripts/run_minimax_m2.py | YES â€” MODEL_NAME    = "minimax_m2" | YES â€” Model ID  : minimax/minimax-m2.7  (override via NIM_MINIMAX_M2_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_mistral_large3.py | YES â€” MODEL_NAME    = "mistral_large3" | YES â€” Model ID  : mistralai/mistral-large-3  (override via NIM_MISTRAL_LARGE3_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_nemotron_ultra.py | YES â€” MODEL_NAME    = "nemotron_ultra" | YES â€” Model ID  : nvidia/nemotron-3-ultra-550b-a55b  (override via NIM_NEMOTRON_ULTRA_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./benchmark_scripts/run_nous_hermes_405b.py | YES â€” MODEL_NAME    = "nous_hermes_405b" | YES â€” MODEL_ID      = "nousresearch/hermes-3-405b-instruct:free" | YES | YES | NO | NO | from _openrouter import call_openrouter | NONE FOUND. | NO |
| ./benchmark_scripts/run_phi4.py | YES â€” MODEL_NAME    = "phi4" | YES â€” MODEL_ID      = "Phi-4" | YES | YES | NO | NO | from _github import call_github, client | NONE FOUND. | NO |
| ./benchmark_scripts/run_qwen35_397b.py | YES â€” MODEL_NAME    = "qwen35_397b" | YES â€” Model ID  : qwen/qwen3.5-397b-a17b  (override via NIM_QWEN35_397B_MODEL_ID) | YES | YES | NO | NO | from _nim import call_nim | NONE FOUND. | NO |
| ./run_benchmark.py | NO | NO | NO | NO | NO | NO | NO PROVIDER IMPORT FOUND. | NONE FOUND. | YES |

