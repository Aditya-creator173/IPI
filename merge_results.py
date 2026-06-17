"""
merge_results.py
Merges all per-model CSV files in results/csv/ into results/results_final.csv.

Features:
- Validates schema consistency across all files
- Deduplicates on (test_id, model_name, defense_mode) — safe to re-run
- Reports per-model row counts and any schema mismatches
- Exits with non-zero status on critical errors so CI can catch failures

Usage:
    python merge_results.py                  # default paths
    python merge_results.py --input results/csv --output results/results_final.csv
    python merge_results.py --validate-only  # check schema without writing
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path


EXPECTED_FIELDS = {
    "test_id", "model_name", "defense_mode",
    "attack_goal", "evasion_style", "harm_severity",
    "prompt_sent", "response_received", "response_length_chars",
    "attack_succeeded", "detection_reason", "needs_review",
}


def merge(
    input_dir: Path,
    output_file: Path,
    validate_only: bool = False,
) -> int:
    """
    Returns total row count written. Raises on critical errors.
    """
    csv_files = sorted(p for p in input_dir.glob("*.csv") if p.is_file())
    if not csv_files:
        print(f"ERROR: No CSV files found in {input_dir}", file=sys.stderr)
        return 0

    all_rows: list[dict] = []
    fieldnames: list[str] | None = None
    schema_errors: list[str] = []
    per_model_counts: Counter = Counter()
    seen_keys: set[tuple] = set()
    duplicate_count = 0

    print(f"Reading {len(csv_files)} file(s) from {input_dir}...")

    for path in csv_files:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                schema_errors.append(f"{path.name}: no header row")
                continue

            file_fields = set(reader.fieldnames)
            missing = EXPECTED_FIELDS - file_fields
            extra   = file_fields - EXPECTED_FIELDS

            if missing:
                schema_errors.append(f"{path.name}: missing fields {sorted(missing)}")
            if extra:
                # Extra fields are fine — newer schema additions
                pass

            if fieldnames is None:
                fieldnames = reader.fieldnames

            file_rows = 0
            for row in reader:
                key = (row.get("test_id"), row.get("model_name"), row.get("defense_mode"))
                if key in seen_keys:
                    duplicate_count += 1
                    continue
                seen_keys.add(key)
                all_rows.append(row)
                per_model_counts[row.get("model_name", "UNKNOWN")] += 1
                file_rows += 1

        print(f"  {path.name:<45} {file_rows:>5} rows")

    # Schema error report
    if schema_errors:
        print("\nSCHEMA WARNINGS:")
        for err in schema_errors:
            print(f"  {err}")

    if duplicate_count:
        print(f"\nDeduplication: removed {duplicate_count} duplicate (test_id, model_name, defense_mode) rows")

    print(f"\nTotal unique rows: {len(all_rows)}")
    print(f"Models found    : {len(per_model_counts)}")
    print(f"\nPer-model breakdown:")
    for model, count in sorted(per_model_counts.items()):
        print(f"  {model:<45} {count:>5} rows")

    # Coverage check
    expected_per_model = 20 * 4  # 20 V1 attacks × 4 defense modes
    incomplete = [(m, c) for m, c in per_model_counts.items() if c < expected_per_model]
    if incomplete:
        print(f"\nIncomplete models (< {expected_per_model} rows = still running or partial):")
        for model, count in sorted(incomplete):
            print(f"  {model}: {count}/{expected_per_model}")

    if validate_only:
        print("\n--validate-only: no output written.")
        return len(all_rows)

    if fieldnames is None:
        print("ERROR: Could not determine field names.", file=sys.stderr)
        return 0

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nMerged → {output_file}")
    return len(all_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge per-model IPIBench CSVs")
    parser.add_argument("--input",         default="results/csv",            help="Input directory")
    parser.add_argument("--output",        default="results/results_final.csv", help="Output file")
    parser.add_argument("--validate-only", action="store_true",              help="Check schema without writing")
    args = parser.parse_args()

    input_dir   = Path(args.input)
    output_file = Path(args.output)

    if not input_dir.exists():
        print(f"ERROR: {input_dir} does not exist.", file=sys.stderr)
        sys.exit(1)

    count = merge(input_dir, output_file, validate_only=args.validate_only)
    if count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
