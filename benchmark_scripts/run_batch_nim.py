import os
import sys
import time

# Manually parse .env to load NVIDIA_API_KEY
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

scripts = [
    "run_mistral_large3.py",
    "run_deepseek_v4_pro.py",
    "run_qwen35_397b.py",
    "run_kimi_k2.py",
    "run_glm51.py",
    "run_glm52.py",
    "run_minimax_m2.py",
    "run_nemotron_ultra.py"
]

print("Starting NIM Batch Run...")
for script in scripts:
    print(f"\n--- Running {script} ---")
    os.system(f"{sys.executable} {script}")
    time.sleep(2)
        
print("\n=== NIM Batch Complete ===")
