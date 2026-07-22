import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor

def run_script(script_name):
    print(f"Starting {script_name}...")
    subprocess.run([sys.executable, os.path.join("benchmark_scripts", script_name)])
    print(f"Finished {script_name}")

def main():
    groq_google_or_scripts = [
        "run_gpt_oss_120b.py", "run_llama33_70b.py", "run_qwen36_27b.py", "run_groq_compound.py",
        "run_gemini35_flash.py", "run_gemini36_flash.py", "run_gemma4_31b.py", "run_gemma4_26b_moe.py",
        "run_poolside_laguna.py"
    ]
    
    nvidia_scripts = [
        "run_mistral_large3.py", "run_deepseek_v4_pro.py", "run_qwen35_397b.py", "run_kimi_k2.py", 
        "run_glm52.py", "run_minimax_m2.py", "run_nemotron_ultra.py"
    ]
    
    github_scripts = [
        "run_phi4.py", "run_cohere_command_a.py", "run_deepseek_r1.py", "run_llama4_scout.py", "run_gpt5.py"
    ]

    print("Launching all benchmark suites in background worker pools...")

    with ThreadPoolExecutor(max_workers=len(groq_google_or_scripts)) as ex_ggor, \
         ThreadPoolExecutor(max_workers=4) as ex_nvidia, \
         ThreadPoolExecutor(max_workers=1) as ex_github:
         
         for s in groq_google_or_scripts:
             ex_ggor.submit(run_script, s)
         for s in nvidia_scripts:
             ex_nvidia.submit(run_script, s)
         for s in github_scripts:
             ex_github.submit(run_script, s)
             
    print("All background benchmark scripts have completed!")

if __name__ == '__main__':
    main()
