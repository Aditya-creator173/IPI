import os
import sys
import time

# Manually parse .env to avoid dependency on python-dotenv
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

scripts = [
    # NVIDIA NIM
    "run_mistral_large3.py",
    "run_deepseek_v4_pro.py",
    "run_qwen35_397b.py",
    "run_kimi_k2.py",
    "run_glm51.py",
    "run_glm52.py",
    "run_minimax_m2.py",
    "run_nemotron_ultra.py",
    
    # GitHub Models
    "run_gpt5.py",
    "run_phi4.py",
    "run_cohere_command_a.py",
    
    # OpenRouter
    "run_nous_hermes_405b.py",
    "run_deepseek_r1.py",
    "run_liquidai_lfm.py"
]

print("Starting NIM, GitHub, & OpenRouter Batch Run...")
for script in scripts:
    print(f"\n--- Running {script} ---")
    result = os.system(f"{sys.executable} {script}")
    if result != 0:
        print(f"Error executing {script} (Exit Code: {result})")
    time.sleep(2)
        
print("\n=== Batch Run 2 Complete ===")
