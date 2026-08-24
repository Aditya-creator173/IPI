import os
import glob
import json
import csv
import pandas as pd
import sys

sys.path.insert(0, "benchmark_scripts")
from scoring_v2 import _score_attack

BENCHMARK_PATH = "benchmark_v2.json"
with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
    bench_data = json.load(f)

bench_map = {tc["id"]: tc for tc in (bench_data if isinstance(bench_data, list) else bench_data.get("test_cases", []))}

os.makedirs("shadow", exist_ok=True)

gpt_files = [
    "results/csv/gpt56_sol.csv",
    "results/csv/gpt56_terra.csv",
    "results/csv/gpt56_luna.csv",
    "results/csv/gpt55.csv",
    "results/csv/gpt54.csv",
    "results/csv/gpt5.csv"
]

print("=== SHADOW RESCORE OF GPT FILES ===\n")
for fpath in gpt_files:
    fname = os.path.basename(fpath)
    shadow_path = os.path.join("shadow", fname)
    
    with open(fpath, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    
    fieldnames = list(reader[0].keys())
    
    rescored_rows = []
    flips = []
    
    for r in reader:
        cid = r.get("test_id", "")
        tc = bench_map.get(cid, {})
        
        phrases = tc.get("attack_success_phrases", [])
        cb = tc.get("correct_behavior", "")
        inj = tc.get("injected_text", "")
        
        resp = r.get("response_received")
        if resp is None:
            resp = r.get("model_raw_output", "")
            
        src = r.get("prompt_sent", "")
        if not src:
            src = r.get("prompt", "")
            
        old_score = float(r.get("score", 0.0))
        
        res = _score_attack(
            response_text=resp,
            success_phrases=phrases,
            correct_behavior=cb,
            injected_text=inj,
            source_text=src,
        )
        
        new_score = res.score
        if old_score != new_score:
            flips.append((cid, r.get("defense_mode"), old_score, new_score, res.reason))
            
        r_new = dict(r)
        r_new["score"] = res.score
        r_new["score_confidence"] = res.confidence
        r_new["attack_succeeded"] = res.attack_succeeded
        r_new["detection_reason"] = res.reason
        rescored_rows.append(r_new)
        
    with open(shadow_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rescored_rows)
        
    print(f"[{fname}] Total rows: {len(reader)} | Score changes: {len(flips)}")
    for cid, dm, os_c, ns_c, reason in flips:
        print(f"   - {cid} ({dm}): {os_c} -> {ns_c} | {reason}")
