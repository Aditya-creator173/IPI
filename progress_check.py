import os
import glob
import sys
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def check_progress():
    csv_dir = os.path.join('results', 'csv')
    files = glob.glob(os.path.join(csv_dir, '*.csv'))
    
    counts = {}
    asrs = {}
    for f in files:
        fname = os.path.basename(f)
        try:
            df = pd.read_csv(f)
            c = len(df)
            counts[fname] = c
            if c > 0 and 'score' in df.columns:
                asrs[fname] = round(df['score'].mean() * 100, 1)
            else:
                asrs[fname] = None
        except Exception:
            counts[fname] = 0
            asrs[fname] = None
            
    print(f"=== IPIBENCH MODEL EVALUATION PROGRESS REPORT ===\n")
    print(f"{'Model CSV':<32} {'Rows':>9}  {'Progress':<12}  {'ASR':>7}")
    print("-" * 68)
    
    clean_count = 0
    total_evals = 0
    
    for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        total_evals += v
        if v == 400:
            clean_count += 1
            bar = '========== '
            status = f"400/400"
        else:
            pct = v / 400
            filled = int(pct * 10)
            bar = '=' * filled + '-' * (10 - filled) + ' '
            status = f"{v}/400"
            
        asr_str = f"{asrs[k]}%" if asrs[k] is not None else "N/A"
        print(f"{k:<32} {status:>9}  [{bar}] {asr_str:>7}")
        
    print("-" * 68)
    print(f"Clean 400/400 Finished Models: {clean_count}")
    print(f"Total Valid Evaluations:       {total_evals}")

if __name__ == '__main__':
    check_progress()
