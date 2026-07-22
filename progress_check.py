import os
import glob
import pandas as pd

def check_progress():
    csv_dir = os.path.join('results', 'csv')
    files = glob.glob(os.path.join(csv_dir, '*.csv'))
    
    counts = {}
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            c = sum(1 for _ in file) - 1
            counts[os.path.basename(f)] = max(0, c)
            
    print("=== 30 MINUTE PROGRESS REPORT ===\n")
    for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        print(f"{k:25} {v:5} / 8808 rows ({v/8808*100:.1f}%)")
        
    print("\n=== GPT-OSS 120B ANALYSIS ===")
    try:
        df = pd.read_csv('results/csv/gpt_oss_120b.csv', on_bad_lines='skip')
        if 'score' in df.columns:
            print('Average IPI Susceptibility Score:', round(df['score'].mean(), 3))
            print(df['score'].value_counts(normalize=True) * 100)
        elif 'attack_succeeded' in df.columns:
            print('Attack Success Rate:', round(df['attack_succeeded'].mean() * 100, 1), '%')
    except Exception as e:
        print("Could not analyze gpt_oss_120b.csv:", e)

if __name__ == '__main__':
    check_progress()
