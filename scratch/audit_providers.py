import os
import glob
import pandas as pd
import json

provider_map = {
    "Groq": [
        "gpt_oss_120b.csv", "gpt_oss_20b.csv", "llama3.1_8b.csv", 
        "llama33_70b.csv", "qwen36_27b.csv", "groq_compound.csv"
    ],
    "Google AI Studio": [
        "gemini35_flash.csv", "gemini36_flash.csv", "gemini37_flash.csv", 
        "gemma4_31b.csv", "gemma4_26b_moe.csv"
    ],
    "NVIDIA NIM": [
        "nemotron_ultra.csv", "deepseek_v4_pro.csv", "diffusiongemma.csv", 
        "minimax_m3.csv", "muse_glimmer_30b.csv"
    ],
    "Cohere API": [
        "cohere_command_a_plus.csv", "cohere_command_a_reasoning.csv"
    ],
    "Mistral API": [
        "mistral_large3.csv", "codestral.csv"
    ],
    "OpenRouter": [
        "poolside_laguna_m1.csv", "ling_30_flash.csv", "liquid_lfm25.csv"
    ],
    "QwenCloud / DashScope": [
        "qwen35_plus.csv", "qwen36_max.csv", "qwen37_max.csv", "qwen37_plus.csv", 
        "qwen37_flash.csv", "qwen38_max.csv", "glm51.csv", "glm52.csv", 
        "deepseek_v4_flash.csv", "qwq_plus.csv", "qwen3_coder_480b.csv", 
        "deepseek_v32.csv", "qwen3_30b_instruct.csv", "qwen3_30b_thinking.csv"
    ],
    "Cloudflare": [
        "llama4_scout.csv", "qwq32b.csv", "sea_lion_v4.csv", 
        "ibm_granite.csv", "qwen3_30b_moe.csv"
    ],
    "Azure UAE North": [
        "gpt56_sol.csv", "gpt56_terra.csv", "gpt56_luna.csv", 
        "gpt55.csv", "gpt54.csv", "gpt5.csv", "phi4.csv"
    ],
    "AWS Bedrock": [
        "deepseek_r1.csv", "grok4.csv"
    ],
    "GCP Vertex AI": [
        "grok41fast_nonreasoning.csv", "grok41fast_reasoning.csv", 
        "grok420_nonreasoning.csv", "grok420_reasoning.csv"
    ],
    "Fireworks AI": [
        "kimi_k3.csv"
    ]
}

print("=== ACCURATE PROVIDER AUDIT REPORT ===\n")
total_clean_models = 0
total_all_evals = 0

for provider, csv_list in provider_map.items():
    p_total = 0
    p_finished = 0
    details = []
    for csv_file in csv_list:
        fpath = os.path.join("results/csv", csv_file)
        count = 0
        asr = 0.0
        if os.path.exists(fpath):
            df = pd.read_csv(fpath)
            count = len(df)
            if count > 0 and 'score' in df.columns:
                asr = round(df['score'].mean() * 100, 1)
        p_total += count
        if count == 400:
            p_finished += 1
            details.append(f"{csv_file.replace('.csv','')}: 400 (ASR {asr}%)")
        elif count > 0:
            details.append(f"{csv_file.replace('.csv','')}: {count}/400 (ASR {asr}%)")
        else:
            details.append(f"{csv_file.replace('.csv','')}: 0/400")
            
    total_clean_models += p_finished
    total_all_evals += p_total
    print(f"{provider:<25} | Finished: {p_finished:<2}/{len(csv_list):<2} | Evals: {p_total:<6} | Models: {', '.join(details)}")

print("-" * 80)
print(f"Grand Total Clean Finished Models (400/400): {total_clean_models}")
print(f"Grand Total Valid Evaluations: {total_all_evals}")
