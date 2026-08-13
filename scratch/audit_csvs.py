import os
import glob
import csv
import re

csv_dir = 'results/csv'
csv_files = sorted(glob.glob(os.path.join(csv_dir, '*.csv')))

print(f"=== AUDIT OF ALL CSV FILES IN {csv_dir} ===\n")
header_str = f"{'CSV Filename':<30} | {'Total Rows':<10} | {'Valid Rows':<10} | {'API Errors':<10} | {'Unique Pairs':<15}"
print(header_str)
print("-" * len(header_str))

total_valid_evals = 0
models_400 = []
models_partial = []
models_empty = []

for fpath in csv_files:
    fname = os.path.basename(fpath)
    if fname.startswith('.'):
        continue
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    total = len(rows)
    valid = 0
    errs = 0
    pairs = set()
    for r in rows:
        tid = r.get('test_id')
        dm = r.get('defense_mode')
        resp = r.get('response_received', '')
        if tid and dm:
            pairs.add((tid, dm))
        if resp.startswith('API_ERROR:'):
            errs += 1
        elif resp != '':
            valid += 1
            
    print(f"{fname:<30} | {total:<10} | {valid:<10} | {errs:<10} | {len(pairs):<15}")
    total_valid_evals += valid
    if valid == 400:
        models_400.append(fname)
    elif valid > 0:
        models_partial.append((fname, valid))
    else:
        models_empty.append(fname)

print("\n" + "=" * 80)
print(f"Total Valid Evaluations across all CSVs: {total_valid_evals}")
print(f"Models with exactly 400/400 valid rows ({len(models_400)}):")
for m in models_400:
    print(f"  - {m}")

print(f"\nModels with partial valid rows ({len(models_partial)}):")
for m, v in models_partial:
    print(f"  - {m}: {v} valid rows")

print(f"\nEmpty/0-row CSV placeholders ({len(models_empty)}):")
for m in models_empty:
    print(f"  - {m}")
