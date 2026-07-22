import os
import sys
import time

# Manually parse .env to load GITHUB_TOKEN
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

scripts = [
    "run_gpt5.py",
    "run_phi4.py",
    "run_cohere_command_a.py"
]

print("Starting GitHub Models Batch Run...")
for script in scripts:
    print(f"\n--- Running {script} ---")
    os.system(f"{sys.executable} {script}")
    time.sleep(2)
        
print("\n=== GitHub Models Batch Complete ===")
