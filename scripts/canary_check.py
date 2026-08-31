"""
canary_check.py — IPIBench Contamination Detection Tool (Step 3.1.1)

Screens model responses for known IPIBench canary strings.
A canary string found in a model response — without that scenario being in the
model's evaluation prompt — indicates potential training-data contamination.

Usage:
    # Screen a single response string
    python scripts/canary_check.py --text "...model response..."

    # Screen all responses in a CSV file
    python scripts/canary_check.py --csv results/csv/some_model.csv

    # Screen all CSVs (full contamination audit)
    python scripts/canary_check.py --all

    # List all known canary strings
    python scripts/canary_check.py --list

The canary format is: [CANARY:ipibench-v1-<128-bit-hex-guid>]
where guid matches the canary_guid field in benchmark.json metadata.
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
from pathlib import Path

# Resolve benchmark.json relative to repo root (one level up from scripts/)
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
BENCHMARK_FILE = REPO_ROOT / "benchmark.json"
RESULTS_CSV_DIR = REPO_ROOT / "results" / "csv"

CANARY_PATTERN = re.compile(r"\[CANARY:ipibench-v1-[0-9a-f\-]+\]", re.IGNORECASE)


def load_canary_map() -> dict[str, dict]:
    """
    Returns {canary_tag: scenario_dict} for all scenarios with a canary_guid.
    canary_tag format: [CANARY:ipibench-v1-<guid>]
    """
    with open(BENCHMARK_FILE, encoding="utf-8") as f:
        data = json.load(f)

    canary_map = {}
    for scenario in data:
        guid = scenario.get("canary_guid")
        if guid:
            tag = f"[CANARY:ipibench-v1-{guid}]"
            canary_map[tag] = scenario
    return canary_map


def check_response(response_text: str, canary_map: dict) -> list[tuple[str, dict]]:
    """
    Given a model response string, return list of (canary_tag, scenario) found.
    An empty list means no contamination signal detected.
    """
    found = []
    # Fast path: check if ANY canary-pattern substring is present first
    if "[CANARY:" not in response_text.upper():
        return found
    for canary_tag, scenario in canary_map.items():
        if canary_tag in response_text:
            found.append((canary_tag, scenario))
    return found


def screen_text(text: str, canary_map: dict) -> int:
    """Screen a raw text string. Returns count of hits."""
    hits = check_response(text, canary_map)
    if hits:
        print(f"  [WARN] CONTAMINATION SIGNAL: {len(hits)} canary(s) found")
        for tag, scenario in hits:
            print(f"     Canary: {tag}")
            print(f"     Scenario: {scenario['id']} | split={scenario.get('split','?')} | attack_goal={scenario['attack_goal']}")
    else:
        print("  [OK] No canary strings detected.")
    return len(hits)


def screen_csv(csv_path: str, canary_map: dict, verbose: bool = True) -> dict:
    """
    Screen all model_response values in a CSV file.
    Returns {total_rows, hits, contaminated_rows}.
    """
    total = 0
    hit_count = 0
    contaminated = []

    with open(csv_path, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            response = row.get("model_response", "")
            hits = check_response(response, canary_map)
            if hits:
                hit_count += 1
                contaminated.append({
                    "row": total,
                    "scenario_id": row.get("scenario_id", "?"),
                    "hits": [(tag, sc["id"]) for tag, sc in hits],
                })

    result = {"total_rows": total, "hits": hit_count, "contaminated_rows": contaminated}

    model_name = os.path.basename(csv_path)
    if verbose:
        if hit_count == 0:
            print(f"  [OK] {model_name}: clean ({total} rows)")
        else:
            print(f"  [HIT] {model_name}: {hit_count} contamination hit(s) in {total} rows")
            for c in contaminated:
                print(f"       Row {c['row']}, scenario {c['scenario_id']}: {c['hits']}")

    return result


def screen_all_csvs(canary_map: dict) -> None:
    """Screen all CSV files in results/csv/."""
    csvs = sorted(glob.glob(str(RESULTS_CSV_DIR / "*.csv")))
    if not csvs:
        print(f"No CSVs found in {RESULTS_CSV_DIR}", file=sys.stderr)
        return

    print(f"Screening {len(csvs)} CSV files for canary contamination...\n")
    total_hits = 0
    for csv_path in csvs:
        result = screen_csv(csv_path, canary_map, verbose=True)
        total_hits += result["hits"]

    print(f"\n{'='*60}")
    if total_hits == 0:
        print("[OK] CLEAN: No contamination signals found across all CSVs.")
    else:
        print(f"[WARN] WARNING: {total_hits} contamination signal(s) detected. Investigate immediately.")
    print(f"{'='*60}")


def list_canaries(canary_map: dict) -> None:
    """Print all known canary strings with their scenario metadata."""
    print(f"{'ID':<8} {'Split':<10} {'Attack Goal':<30} {'Canary Tag'}")
    print("-" * 100)
    for tag, scenario in sorted(canary_map.items(), key=lambda x: x[1]["id"]):
        sid = scenario["id"]
        split = scenario.get("split", "?")
        goal = scenario.get("attack_goal", "?")
        print(f"{sid:<8} {split:<10} {goal:<30} {tag}")


def main():
    parser = argparse.ArgumentParser(
        description="IPIBench canary contamination detection tool.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Screen a raw text string for canary hits.")
    group.add_argument("--csv", type=str, help="Screen all responses in a CSV file.")
    group.add_argument("--all", action="store_true", help="Screen all CSVs in results/csv/.")
    group.add_argument("--list", action="store_true", help="List all known canary strings.")

    args = parser.parse_args()

    if not BENCHMARK_FILE.exists():
        print(f"ERROR: benchmark.json not found at {BENCHMARK_FILE}", file=sys.stderr)
        sys.exit(1)

    canary_map = load_canary_map()
    print(f"Loaded {len(canary_map)} canary strings from {BENCHMARK_FILE.name}\n")

    if args.list:
        list_canaries(canary_map)
    elif args.text:
        print(f"Screening text ({len(args.text)} chars)...")
        hits = screen_text(args.text, canary_map)
        sys.exit(1 if hits > 0 else 0)
    elif args.csv:
        print(f"Screening CSV: {args.csv}")
        result = screen_csv(args.csv, canary_map, verbose=True)
        sys.exit(1 if result["hits"] > 0 else 0)
    elif args.all:
        screen_all_csvs(canary_map)


if __name__ == "__main__":
    main()
