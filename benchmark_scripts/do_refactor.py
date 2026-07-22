import os
from pathlib import Path
import re

def refactor():
    base_dir = Path(__file__).resolve().parent
    
    # -------------------------------------------------------------
    # NIM Refactoring
    # -------------------------------------------------------------
    nim_scripts = [
        "run_glm51.py", "run_nemotron_ultra.py", "run_kimi_k2.py", 
        "run_minimax_m2.py", "run_qwen35_397b.py", "run_mistral_medium.py", 
        "run_sarvam_m.py", "run_deepseek_v4_pro.py"
    ]
    
    for script_name in nim_scripts:
        p = base_dir / script_name
        if not p.exists(): continue
        content = p.read_text(encoding="utf-8")
        
        # Replace imports
        content = re.sub(
            r'import os\nimport _core\nfrom openai import OpenAI\nfrom _core import run_benchmark',
            r'from _core import run_benchmark\nfrom _nim import call_nim',
            content
        )
        
        # Remove client initialization
        content = re.sub(
            r'_key\s*=\s*os\.environ\.get\([^)]+\)\s*or\s*os\.environ\["NVIDIA_API_KEY"\]\s*\n+client\s*=\s*OpenAI\(\s*base_url="https://integrate\.api\.nvidia\.com/v1",\s*api_key=_key,\s*\)\s*\n+',
            '',
            content
        )
        
        # Replace call function
        call_func_pattern = r'def call\(prompt: str, system_prompt: str\) -> str:\n(?:.|\n)*?return resp\.choices\[0\]\.message\.content'
        
        # Find the MODEL_NAME to pass to model_suffix
        model_name_match = re.search(r'MODEL_NAME\s*=\s*"([^"]+)"', content)
        suffix = model_name_match.group(1).upper() if model_name_match else "UNKNOWN"
        
        new_call_func = f'def call(prompt: str, system_prompt: str) -> str:\n    return call_nim(MODEL_ID, prompt, system_prompt, model_suffix="{suffix}")'
        content = re.sub(call_func_pattern, new_call_func, content)
        
        p.write_text(content, encoding="utf-8")
        print(f"Refactored {script_name}")


    # -------------------------------------------------------------
    # Groq Refactoring
    # -------------------------------------------------------------
    groq_scripts = [
        "run_llama31_8b.py", "run_llama33_70b.py", "run_llama4_scout.py", "run_gpt_oss_120b.py"
    ]
    
    for script_name in groq_scripts:
        p = base_dir / script_name
        if not p.exists(): continue
        content = p.read_text(encoding="utf-8")
        
        content = re.sub(
            r'import os\nimport _core\nfrom groq import Groq\nfrom _core import run_benchmark',
            r'from _core import run_benchmark\nfrom _groq import call_groq',
            content
        )
        
        content = re.sub(
            r'client\s*=\s*Groq\(api_key=os\.environ\["GROQ_API_KEY"\]\)\s*\n+',
            '',
            content
        )
        
        call_func_pattern = r'def call\(prompt: str, system_prompt: str\) -> str:\n(?:.|\n)*?return resp\.choices\[0\]\.message\.content'
        new_call_func = f'def call(prompt: str, system_prompt: str) -> str:\n    return call_groq(MODEL_ID, prompt, system_prompt)'
        content = re.sub(call_func_pattern, new_call_func, content)
        
        p.write_text(content, encoding="utf-8")
        print(f"Refactored {script_name}")


    # -------------------------------------------------------------
    # GitHub Refactoring
    # -------------------------------------------------------------
    github_scripts = [
        "run_phi4.py", "run_jamba.py", "run_cohere_command_a.py", "run_gpt5.py", "run_mai_ds_r1.py"
    ]
    
    for script_name in github_scripts:
        p = base_dir / script_name
        if not p.exists(): continue
        content = p.read_text(encoding="utf-8")
        
        content = re.sub(
            r'import os\nimport _core\nfrom openai import OpenAI\nfrom _core import run_benchmark',
            r'from _core import run_benchmark\nfrom _github import call_github, client',
            content
        )
        
        content = re.sub(
            r'client\s*=\s*OpenAI\(\s*base_url="https://models\.inference\.ai\.azure\.com",\s*api_key=os\.environ\["GITHUB_TOKEN"\],\s*\)\s*\n+',
            '',
            content
        )
        
        # Check for special parameters in the call
        has_temp = "temperature=0.6" in content
        is_ds_r1 = "run_mai_ds_r1.py" in script_name
        
        extra_args = []
        if has_temp: extra_args.append("temperature=0.6")
        if is_ds_r1: extra_args.append("fold_system_prompt=True")
        extra_args.append("timeout=90" if is_ds_r1 else "timeout=60")
        
        args_str = ", ".join(extra_args)
        if args_str:
            args_str = ", " + args_str
            
        call_func_pattern = r'def call\(prompt: str, system_prompt: str\) -> str:\n(?:.|\n)*?return resp\.choices\[0\]\.message\.content'
        new_call_func = f'def call(prompt: str, system_prompt: str) -> str:\n    return call_github(MODEL_ID, prompt, system_prompt{args_str})'
        content = re.sub(call_func_pattern, new_call_func, content)
        
        p.write_text(content, encoding="utf-8")
        print(f"Refactored {script_name}")


if __name__ == "__main__":
    refactor()
