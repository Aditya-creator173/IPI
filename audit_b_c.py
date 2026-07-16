import os
import glob
import re

print("Starting audit script...", flush=True)

# Find all run_*.py scripts
scripts = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.startswith('run_') and f.endswith('.py'):
            if '.git' not in root:
                scripts.append(os.path.join(root, f).replace('\\', '/'))

scripts.sort()

# SECTION B
b_output = "| Script | B1 (MODEL_NAME) | B2 (MODEL_ID) | B3 (def call() | B4 (run_benchmark() | B5 ([MANUAL ONLY]) | B6 (PENDING) | B7 (Provider Import) | B8 (os.environ[) | B9 (try/except) |\n"
b_output += "|---|---|---|---|---|---|---|---|---|---|\n"

model_names = []

for s in scripts:
    with open(s, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
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
            m = re.search(r'MODEL_NAME\s*=\s*["\']([^"\']+)["\']', line)
            if m:
                model_names.append(m.group(1))
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

print("SECTION C:")

model_names.sort()

# C2 was: deepseek_r1, gemini3_flash, llama3.1_8b, llama33_70b, results
c2_list = ["deepseek_r1", "gemini3_flash", "llama3.1_8b", "llama33_70b", "results"]

c3_mismatches = []
for m in model_names:
    if m not in c2_list:
        c3_mismatches.append(f"+ {m} (in C1 only)")
for m in c2_list:
    if m not in model_names:
        c3_mismatches.append(f"- {m} (in C2 only)")

print("C1 Model Names:", model_names)
print("C3 Mismatches:")
if not c3_mismatches:
    print("NO MISMATCHES")
else:
    for m in sorted(c3_mismatches):
        print(m)

# C4 and C5
c4_list = []
with open('./benchmark_scripts/_core.py', 'r', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'CSV_FIELDNAMES\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if m:
        c4_list = [x.strip(" '\"\n\r") for x in m.group(1).split(',') if x.strip(" '\"\n\r")]

c5_list = []
with open('./merge_results.py', 'r', encoding='utf-8') as f:
    content = f.read()
    m = re.search(r'_BASE_FIELD_ORDER\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if m:
        c5_list = [x.strip(" '\"\n\r") for x in m.group(1).split(',') if x.strip(" '\"\n\r")]

print("C4 fields:", c4_list)
print("C5 fields:", c5_list)

c6_mismatches = []
for f in c4_list:
    if f not in c5_list:
        c6_mismatches.append(f"+ {f} (in C4 only)")
for f in c5_list:
    if f not in c4_list:
        c6_mismatches.append(f"- {f} (in C5 only)")

print("C6 Mismatches:")
if not c6_mismatches:
    print("NO MISMATCHES")
else:
    for m in sorted(c6_mismatches):
        print(m)

# C7
print("C7:")
with open('./benchmark_scripts/scoring_v2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
def print_context(target_str):
    count = 0
    print(f"Target: {target_str}")
    for i, line in enumerate(lines):
        if target_str in line:
            count += 1
            print(f"Occurrence {count}:")
            if i > 0: print(f"  {lines[i-1].rstrip()}")
            print(f"  {line.rstrip()}")
            if i < len(lines)-1: print(f"  {lines[i+1].rstrip()}")
            print()
    print(f"Total count for '{target_str}': {count}\n")

print_context("attack_succeeded=0")
print_context("attack_succeeded=1")

