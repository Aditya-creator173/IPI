"""
rescore_all.py — Re-score all benchmark CSV files using scoring_v2 v3.

Backs up all CSVs to results/csv/backup_pre_v3/ first, then updates score,
score_confidence, attack_succeeded, detection_reason, and needs_review columns.
Prints before/after summary per model.
"""

import os
import glob
import csv
import json
import shutil
import sys

sys.path.insert(0, "benchmark_scripts")
from scoring_v2 import _score_attack

BENCHMARK_PATH = "benchmark_v2.json"
CSV_DIR = "results/csv"
BACKUP_DIR = os.path.join(CSV_DIR, "backup_pre_v3")


def main():
    if not os.path.exists(BENCHMARK_PATH):
        print(f"ERROR: {BENCHMARK_PATH} not found.")
        sys.exit(1)

    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        bench_data = json.load(f)

    if isinstance(bench_data, list):
        bench_map = {tc["id"]: tc for tc in bench_data}
    else:
        bench_map = {tc["id"]: tc for tc in bench_data.get("test_cases", [])}

    # Step 1: Create backup directory
    os.makedirs(BACKUP_DIR, exist_ok=True)
    csv_files = sorted(glob.glob(os.path.join(CSV_DIR, "*.csv")))

    valid_csv_files = []
    for filepath in csv_files:
        basename = os.path.basename(filepath)
        if basename.startswith(".") or "_rescored" in basename or "_disagreement" in basename:
            continue
        valid_csv_files.append(filepath)

    print(f"Backing up {len(valid_csv_files)} CSV files to {BACKUP_DIR}...")
    for filepath in valid_csv_files:
        dest = os.path.join(BACKUP_DIR, os.path.basename(filepath))
        shutil.copy2(filepath, dest)

    print("\n" + "=" * 95)
    print(f"{'MODEL NAME':<25} | {'OLD ASR':<8} | {'NEW ASR':<8} | {'OLD REV':<7} | {'NEW REV':<7} | {'SCORE MIX (0 / 0.5 / 1)'}")
    print("=" * 95)

    summary_rows = []

    for filepath in valid_csv_files:
        model_name = os.path.splitext(os.path.basename(filepath))[0]

        with open(filepath, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))

        if not reader:
            continue

        fieldnames = list(reader[0].keys())

        # Track old stats
        old_rows = len(reader)
        old_asr_count = sum(1 for r in reader if str(r.get("attack_succeeded", "")).strip() in ("1", "1.0", "True"))
        old_asr = (old_asr_count / old_rows * 100) if old_rows else 0.0
        old_rev = sum(1 for r in reader if str(r.get("needs_review", "")).strip() in ("1", "1.0", "True"))

        new_scores = {0.0: 0, 0.5: 0, 1.0: 0}
        new_asr_count = 0
        new_rev_count = 0

        rescored_rows = []
        for r in reader:
            cid = r.get("test_id", "")
            tc = bench_map.get(cid, {})

            # Retrieve phrases / behavior / prompt
            phrases = tc.get("attack_success_phrases", [])
            cb = tc.get("correct_behavior", "")
            inj = tc.get("injected_text", "")

            resp = r.get("response_received")
            if resp is None:
                resp = r.get("model_raw_output", "")

            src = r.get("prompt_sent")
            if not src:
                src = r.get("prompt", "")

            res = _score_attack(
                response_text=resp,
                success_phrases=phrases,
                correct_behavior=cb,
                injected_text=inj,
                source_text=src,
            )

            # Update row fields
            r["score"] = res.score
            r["score_confidence"] = res.confidence
            r["attack_succeeded"] = res.attack_succeeded
            r["detection_reason"] = res.reason

            needs_rev = 1 if (res.confidence < 0.60 or "manual review" in res.reason.lower()) else 0
            r["needs_review"] = needs_rev

            # Track new stats
            new_scores[res.score] = new_scores.get(res.score, 0) + 1
            if res.attack_succeeded == 1:
                new_asr_count += 1
            if needs_rev == 1:
                new_rev_count += 1

            rescored_rows.append(r)

        # Overwrite CSV file in-place
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rescored_rows)

        new_asr = (new_asr_count / len(rescored_rows) * 100) if rescored_rows else 0.0
        mix_str = f"{{{new_scores.get(0.0,0)} / {new_scores.get(0.5,0)} / {new_scores.get(1.0,0)}}}"

        print(f"{model_name:<25} | {old_asr:>6.1f}%  | {new_asr:>6.1f}%  | {old_rev:>7} | {new_rev_count:>7} | {mix_str}")
        summary_rows.append((model_name, old_asr, new_asr, old_rev, new_rev_count, new_scores))

    print("=" * 95)
    print(f"Re-scored {len(valid_csv_files)} CSV files successfully.")


if __name__ == "__main__":
    main()
