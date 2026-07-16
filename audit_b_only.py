import os
import subprocess
import re

print("Starting audit script...", flush=True)

# Find all run_*.py scripts using exact find command
result = subprocess.run(['C:/Program Files/Git/bin/sh.exe', '-c', 'find . -name "run_*.py"'], capture_output=True, text=True)
scripts = [x for x in result.stdout.split('\n') if x.strip()]
scripts.sort()

# SECTION B
b_output = "| Script | B1 (MODEL_NAME) | B2 (MODEL_ID) | B3 (def call() | B4 (run_benchmark() | B5 ([MANUAL ONLY]) | B6 (PENDING) | B7 (Provider Import) | B8 (os.environ[) | B9 (try/except) |\n"
b_output += "|---|---|---|---|---|---|---|---|---|---|\n"

for s in scripts:
    try:
        with open(s, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        b_output += f"| {s} | ERROR READING FILE | | | | | | | | |\n"
        continue
    
    b1_ans = "NO"
    b2_ans = "NO"
    b3_ans = "NO"
    b4_ans = "NO"
    b5_ans = "NO"
    b6_ans = "NO"
    b7_ans = "NO PROVIDER IMPORT FOUND."
    b8_ans = "NONE FOUND."
    b9_ans = "NO"
    
    b8_lines = []
    
    for i, line in enumerate(lines):
        # B1
        if 'MODEL_NAME' in line and b1_ans == "NO":
            b1_ans = f"YES — {line.strip()}"
        # B2
        if 'MODEL_ID' in line and b2_ans == "NO":
            b2_ans = f"YES — {line.strip()}"
        # B3
        if 'def call(' in line: b3_ans = "YES"
        # B4
        if 'run_benchmark(' in line: b4_ans = "YES"
        # B5
        if '[MANUAL ONLY]' in line: b5_ans = "YES"
        # B6
        if 'PENDING' in line: b6_ans = "YES"
        # B7 - provider import
        if line.strip().startswith('from _') and 'import call_' in line:
            b7_ans = line.strip()
        # B8
        if 'os.environ[' in line:
            b8_lines.append(str(i+1))
    
    if b8_lines:
        b8_ans = ", ".join(b8_lines)
        
    # B9 try/except
    for i, line in enumerate(lines):
        if 'try:' in line:
            for j in range(1, 16):
                if i+j < len(lines) and 'except' in lines[i+j]:
                    b9_ans = "YES"
                    break
            if b9_ans == "YES":
                break
                
    b_output += f"| {s} | {b1_ans} | {b2_ans} | {b3_ans} | {b4_ans} | {b5_ans} | {b6_ans} | {b7_ans} | {b8_ans} | {b9_ans} |\n"

print("SECTION B TABLE:")
print(b_output)

