"""
run_auto_pipeline.py — Automated Sequential Execution Pipeline
Runs all active provider models in structured stages with automatic failover,
logging, and support for --dry-run and --validate flags.
"""

import sys
import subprocess
from pathlib import Path

SCRIPTS = [
    # --- Stage 1: Google AI Studio ---
    ("Gemini 3.5 Flash", "run_gemini35_flash.py"),
    ("Gemini 3.6 Flash", "run_gemini36_flash.py"),
    ("Gemma 4 31B Dense", "run_gemma4_31b.py"),
    ("Gemma 4 26B MoE", "run_gemma4_26b_moe.py"),

    # --- Stage 2: Groq ---
    ("GPT-OSS 120B", "run_gpt_oss_120b.py"),
    ("GPT-OSS 20B", "run_gpt_oss_20b.py"),
    ("LLaMA 3.1 8B", "run_llama31_8b.py"),
    ("LLaMA 3.3 70B", "run_llama33_70b.py"),
    ("Groq Compound", "run_groq_compound.py"),

    # --- Stage 3: Mistral API ---
    ("Mistral Large 3", "run_mistral_large3.py"),
    ("Codestral 2508", "run_codestral.py"),

    # --- Stage 4: Cohere API ---
    ("Cohere Command A+", "run_cohere_command_a_plus.py"),
    ("Cohere Command A Reasoning", "run_cohere_command_a_reasoning.py"),

    # --- Stage 5: QwenCloud (DashScope) ---
    ("Qwen 3.5 Plus", "run_qwen35_plus.py"),
    ("Qwen 3.6 Max Preview", "run_qwen36_max.py"),
    ("Qwen 3.7 Max", "run_qwen37_max.py"),
    ("Qwen 3.7 Plus", "run_qwen37_plus.py"),
    ("Qwen 3.7 Flash", "run_qwen37_flash.py"),
    ("Qwen 3.8 Max", "run_qwen38_max.py"),
    ("QwQ Plus", "run_qwq_plus.py"),
    ("GLM 5.1", "run_glm51.py"),
    ("GLM 5.2", "run_glm52.py"),
    ("DeepSeek V4 Flash", "run_deepseek_v4_flash.py"),
    ("Qwen 3 Coder 480B", "run_qwen3_coder_480b.py"),

    # --- Stage 6: Cloudflare Workers AI ---
    ("LLaMA 4 Scout", "run_llama4_scout.py"),
    ("Kimi K2.6", "run_kimi_k2.py"),
    ("SEA-LION v4 27B", "run_sea_lion_v4.py"),
    ("IBM Granite 4.0 H Micro", "run_ibm_granite.py"),
    ("QwQ 32B", "run_qwq32b.py"),
    ("Qwen 3 30B MoE", "run_qwen3_30b_moe.py"),

    # --- Stage 7: NVIDIA NIM ---
    ("Nemotron Ultra 550B", "run_nemotron_ultra.py"),
    ("DeepSeek V4 Pro", "run_deepseek_v4_pro.py"),
    ("DiffusionGemma 26B", "run_diffusiongemma.py"),
    ("Sarvam 8B", "run_sarvam8b.py"),

    # --- Stage 8: NVIDIA NIM ---
    ("MiniMax M3", "run_minimax_m3.py"),
    ("DeepSeek V3.2", "run_deepseek_v32.py"),

    # --- Stage 9: OpenRouter ---
    ("Poolside Laguna M.1", "run_poolside_laguna.py"),
    ("Ling 3.0 Flash", "run_ling_30_flash.py"),

    # --- Stage 10: AWS Bedrock ---
    ("Claude Haiku 4.5", "run_claude_haiku.py"),
    ("Claude Sonnet 4.6", "run_claude_sonnet.py"),
    ("Claude Opus 4.6", "run_claude_opus.py"),
    ("Grok 4.3", "run_grok4.py"),
    ("Jamba 1.5 Large", "run_jamba15_large.py"),
    ("DeepSeek R1 (Bedrock)", "run_deepseek_r1_bedrock.py"),
]

def main():
    script_dir = Path(__file__).parent.resolve()
    extra_args = sys.argv[1:]

    print("=" * 60)
    print("AUTOMATED BENCHMARK PIPELINE STARTING")
    print(f"Working Directory : {script_dir}")
    if extra_args:
        print(f"Forwarding Flags  : {' '.join(extra_args)}")
    print("=" * 60)

    for idx, (name, filename) in enumerate(SCRIPTS, 1):
        script_path = script_dir / filename
        if not script_path.exists():
            print(f"\n[{idx}/{len(SCRIPTS)}] [SKIP] {name} ({filename}) file not found.")
            continue

        print(f"\n[{idx}/{len(SCRIPTS)}] STAGE STARTING: {name} ({filename})")
        print("-" * 60)

        cmd = [sys.executable, str(script_path)] + extra_args
        try:
            res = subprocess.run(
                cmd,
                cwd=str(script_dir),
                check=False
            )
            if res.returncode == 0:
                print(f"\n[SUCCESS] {name} stage finished with exit code 0.")
            else:
                print(f"\n[PIVOT] {name} exited with code {res.returncode}. Transitioning to next stage...")
        except Exception as e:
            print(f"\n[ERROR] Exception in {name}: {e}. Pivoting to next stage...")

    print("\n" + "=" * 60)
    print("AUTOMATED PIPELINE FINISHED ALL STAGES")
    print("=" * 60)

if __name__ == "__main__":
    main()

