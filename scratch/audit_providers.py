import os
import glob
import csv

provider_map = {
    "Groq": ["gpt_oss_120b.csv", "gpt_oss_20b.csv", "llama3.1_8b.csv", "llama33_70b.csv", "qwen36_27b.csv", "groq_compound.csv"],
    "Google AI Studio": ["gemini35_flash.csv", "gemini36_flash.csv", "gemma4_31b.csv", "gemma4_26b_moe.csv"],
    "NVIDIA NIM": ["nemotron_ultra.csv", "deepseek_v4_pro.csv", "diffusiongemma.csv", "minimax_m3.csv"],
    "Cohere API": ["cohere_command_a_plus.csv", "cohere_command_a_reasoning.csv"],
    "Mistral API": ["mistral_large3.csv", "codestral.csv"],
    "OpenRouter": ["poolside_laguna_m1.csv", "ling_30_flash.csv"],
    "QwenCloud / DashScope": [
        "qwen35_plus.csv", "qwen36_max.csv", "qwen37_max.csv", "qwen37_plus.csv", 
        "qwen37_flash.csv", "qwen38_max.csv", "glm51.csv", "glm52.csv", 
        "deepseek_v4_flash.csv", "qwq_plus.csv", "qwen3_coder_480b.csv", "deepseek_v32.csv"
    ],
    "Cloudflare": ["llama4_scout.csv", "kimi_k2.csv", "qwq32b.csv", "sea_lion_v4.csv", "ibm_granite.csv", "qwen3_30b_moe.csv"],
    "GitHub Models": ["phi4.csv"],
    "Azure UAE North": ["gpt56_sol.csv"],
    "AWS Bedrock": ["claude_haiku.csv", "claude_sonnet.csv", "claude_opus.csv", "grok4.csv", "jamba15_large.csv", "deepseek_r1.csv"]
}

print("=== PROVIDER AUDIT COMPARISON ===\n")
total_all_evals = 0

for provider, csv_list in provider_map.items():
    p_total = 0
    p_finished = 0
    details = []
    for csv_file in csv_list:
        fpath = os.path.join("results/csv", csv_file)
        count = 0
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                count = sum(1 for r in reader if r.get("response_received", "") and not r.get("response_received", "").startswith("API_ERROR:"))
        p_total += count
        if count == 400:
            p_finished += 1
        details.append(f"{csv_file.replace('.csv','')}: {count}")
    
    total_all_evals += p_total
    print(f"{provider:<25} | Finished Models: {p_finished:<2} | Evals: {p_total:<6} | Details: {', '.join(details)}")

print("\nGrand Total Valid Evals across all mapped providers:", total_all_evals)
