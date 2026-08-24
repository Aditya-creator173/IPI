import glob
import os
import pandas as pd

files = sorted(glob.glob('results/csv/*.csv'))
print(f"=== POST-RESCORE ASR & MEAN SCORE SUMMARY ({len(files)} files) ===\n")
print(f"{'MODEL':<30} | {'COUNT':>5} | {'ATTACK_SUCC %':>13} | {'MEAN SCORE %':>12} | {'SCORE MIX (0 / 0.5 / 1)'}")
print('-' * 85)

for f in files:
    try:
        df = pd.read_csv(f)
    except Exception:
        continue
    if len(df) == 0 or 'score' not in df.columns:
        continue
    c0 = (df['score'] == 0.0).sum()
    c05 = (df['score'] == 0.5).sum()
    c1 = (df['score'] == 1.0).sum()
    succ_rate = (df['attack_succeeded'] == 1).mean() * 100
    mean_score = df['score'].mean() * 100
    print(f"{os.path.basename(f):<30} | {len(df):>5} | {succ_rate:>12.1f}% | {mean_score:>11.1f}% | {{{c0} / {c05} / {c1}}}")
