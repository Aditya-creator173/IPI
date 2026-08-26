import glob
import os
import pandas as pd
import json

with open('benchmark.json', 'r', encoding='utf-8') as f:
    bench = json.load(f)
expected_test_ids = set(c['id'] for c in (bench if isinstance(bench, list) else bench.get('test_cases', [])))
expected_defenses = {'none', 'prompt_warning', 'spotlighting', 'input_filter'}

csv_files = sorted(glob.glob('results/csv/*.csv'))

print(f"Auditing all {len(csv_files)} CSV files in results/csv/ against benchmark ({len(expected_test_ids)} test cases x 4 defenses = 400 rows)...\n")

passed_models = []
imperfect_models = []

for f in csv_files:
    fname = os.path.basename(f)
    model_key = fname.replace('.csv', '')
    df = pd.read_csv(f)
    total_rows = len(df)
    
    issues = []
    
    if total_rows != 400:
        issues.append(f"Row count is {total_rows}, expected 400")
        
    # Check defense mode distribution
    dm_counts = df['defense_mode'].value_counts().to_dict() if 'defense_mode' in df.columns else {}
    for dm in expected_defenses:
        cnt = dm_counts.get(dm, 0)
        if cnt != 100:
            issues.append(f"Defense '{dm}' has {cnt} rows (expected 100)")
            
    # Check test_id coverage
    if 'test_id' in df.columns:
        present_tids = set(df['test_id'].dropna().astype(str))
        missing_tids = expected_test_ids - present_tids
        if missing_tids:
            issues.append(f"Missing {len(missing_tids)} test IDs: {sorted(list(missing_tids))[:5]}...")
            
    # Check API errors or nulls
    if 'response_received' in df.columns:
        api_err_count = df['response_received'].astype(str).str.startswith('API_ERROR:').sum()
        if api_err_count > 0:
            issues.append(f"Contains {api_err_count} API_ERROR rows")
            
    if 'score' in df.columns:
        nan_scores = df['score'].isna().sum()
        if nan_scores > 0:
            issues.append(f"Contains {nan_scores} NaN scores")
            
    # Check duplicates
    if 'test_id' in df.columns and 'defense_mode' in df.columns:
        dupes = df.duplicated(subset=['test_id', 'defense_mode']).sum()
        if dupes > 0:
            issues.append(f"Contains {dupes} duplicate (test_id, defense_mode) pairs")

    if not issues:
        asr = round(df['score'].mean() * 100, 1) if 'score' in df.columns else 0.0
        passed_models.append((model_key, total_rows, asr))
    else:
        imperfect_models.append((model_key, total_rows, issues))

print(f"=== PASSED PERFECT 400/400 AUDIT ({len(passed_models)} models) ===")
print(f"{'Model':32} | {'Rows':8} | {'ASR':7} | {'Integrity'}")
print("-" * 65)
for m, n, asr in passed_models:
    print(f"{m:32} | {n:3}/400   | {asr:5.1f}% | 100% CLEAN (0 errors, 0 duplicates, 4x100)")

if imperfect_models:
    print(f"\n=== INCOMPLETE OR WITH ISSUES ({len(imperfect_models)} models) ===")
    for m, n, issues in imperfect_models:
        print(f"\n[{m}] ({n}/400 rows):")
        for iss in issues:
            print(f"  - {iss}")
