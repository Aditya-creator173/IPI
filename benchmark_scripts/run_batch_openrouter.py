import os
import sys
import time

# Manually parse .env to load OPENROUTER_API_KEY
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

scripts = [
    "run_nous_hermes_405b.py",
    "run_deepseek_r1.py",
    "run_liquidai_lfm.py"
]

print("Starting OpenRouter Batch Run...")
for script in scripts:
    print(f"\n--- Running {script} ---")
    os.system(f"{sys.executable} {script}")
    time.sleep(2)
        
print("\n=== OpenRouter Batch Complete ===")
