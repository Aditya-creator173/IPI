import os
import glob
import pandas as pd
import datetime

# 1. Check file timestamps
print("=== 1. FILE TIMESTAMPS ===")
files = [
    'results/csv/gpt56_sol.csv',
    'results/csv/gpt56_terra.csv',
    'results/csv/gpt56_luna.csv',
    'results/csv/gpt55.csv',
    'results/csv/gpt54.csv',
    'results/csv/gpt5.csv',
    'benchmark_scripts/_core.py',
    'rescore_all.py',
    'rescore.py'
]
for f in files:
    if os.path.exists(f):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(f))
        print(f"{f:<35}: {mtime}")
    else:
        print(f"{f:<35}: NOT FOUND")

# 2. Check schema and population in GPT CSVs
print("\n=== 2. SCHEMA & POPULATION IN GPT CSVs ===")
gpt_files = glob.glob('results/csv/gpt*.csv')
for gf in sorted(gpt_files):
    df = pd.read_csv(gf)
    has_src = 'source_text' in df.columns
    has_ps = 'prompt_sent' in df.columns
    pop_src = df['source_text'].notna().mean() if has_src else 'N/A'
    pop_ps = df['prompt_sent'].notna().mean() if has_ps else 'N/A'
    print(f"{os.path.basename(gf):<20} | source_text col: {has_src} ({pop_src}) | prompt_sent col: {has_ps} ({pop_ps})")

# 3. Check A003 rows in original GPT CSVs
print("\n=== 3. A003-CLASS ROWS IN ORIGINAL GPT CSVs ===")
for gf in sorted(gpt_files):
    df = pd.read_csv(gf)
    a003 = df[df['test_id'] == 'A003'] if 'test_id' in df.columns else pd.DataFrame()
    if not a003.empty:
        scores = a003['score'].tolist() if 'score' in a003.columns else []
        reasons = a003['detection_reason'].tolist() if 'detection_reason' in a003.columns else []
        print(f"{os.path.basename(gf):<20} | A003 rows: {len(a003)} | scores: {scores}")
        for s, r in zip(scores, reasons):
            print(f"   score={s} | reason={r}")
