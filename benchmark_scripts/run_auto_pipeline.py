"""
run_auto_pipeline.py — Automated Sequential Execution Pipeline
Sequence:
  1. Gemini 3.5 Flash (run_gemini35_flash.py) -> Complete remaining rows to 400/400
  2. Gemini 3.6 Flash (run_gemini36_flash.py) -> Complete 0 to 400/400
  3. DeepSeek V4 Pro (run_deepseek_v4_pro.py) -> Complete remaining rows to 400/400 (NVIDIA NIM failover)
"""

import sys
import subprocess
from pathlib import Path

SCRIPTS = [
    ("Gemini 3.5 Flash", "run_gemini35_flash.py"),
    ("Gemini 3.6 Flash", "run_gemini36_flash.py"),
    ("DeepSeek V4 Pro", "run_deepseek_v4_pro.py"),
]

def main():
    script_dir = Path(__file__).parent.resolve()
    print("=" * 60)
    print("AUTOMATED PIPELINE STARTING")
    print(f"Working Directory: {script_dir}")
    print("=" * 60)

    for idx, (name, filename) in enumerate(SCRIPTS, 1):
        script_path = script_dir / filename
        print(f"\n[{idx}/{len(SCRIPTS)}] STAGE STARTING: {name} ({filename})")
        print("-" * 60)

        try:
            res = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(script_dir),
                check=False
            )
            if res.returncode == 0:
                print(f"\n[SUCCESS] {name} stage finished with exit code 0.")
            else:
                print(f"\n[PIVOT] {name} exited with code {res.returncode}. Transitioning to next pipeline stage...")
        except Exception as e:
            print(f"\n[ERROR] Exception in {name}: {e}. Pivoting to next stage...")

    print("\n" + "=" * 60)
    print("AUTOMATED PIPELINE FINISHED ALL STAGES")
    print("=" * 60)

if __name__ == "__main__":
    main()
