"""
run_groq_sequential.py — Dedicated sequential runner for Groq models.
Runs one Groq model at a time so all 5 Groq keys and 100% of TPM capacity
are dedicated to a single model script without parallel thread contention.
"""

import os
import sys
import subprocess
import time

GROQ_SCRIPTS = [
    "run_qwen36_27b.py",
    "run_groq_compound.py",
]

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(root_dir, "benchmark_scripts")
    
    print("==================================================")
    print("  DEDICATED SEQUENTIAL GROQ BENCHMARK RUNNER")
    print("==================================================")
    print(f"Scripts queued: {GROQ_SCRIPTS}")
    print("Strategy: 1 script at a time (100% TPM allocation per model)")
    print("==================================================\n")

    for script in GROQ_SCRIPTS:
        script_path = os.path.join(scripts_dir, script)
        print(f"\n[QUEUE] Starting {script}...")
        t0 = time.time()
        
        res = subprocess.run([sys.executable, script_path])
        
        elapsed = time.time() - t0
        if res.returncode == 0:
            print(f"[COMPLETED] {script} finished in {elapsed:.1f}s")
        else:
            print(f"[WARNING] {script} exited with code {res.returncode}")
            
        time.sleep(2)

    print("\n==================================================")
    print("  ALL GROQ MODELS COMPLETED!")
    print("==================================================")

if __name__ == "__main__":
    main()
