"""
merge_results.py
Merges all per-model CSV files in results/csv/ into results/results_final.csv.

Features:
- Validates schema consistency across all files
- Dynamic column union: collects all unique headers across all CSVs, preserves
  a logical base ordering, and appends any extra columns sorted — no data dropped
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
from collections import Counter
from pathlib import Path


# Minimum fields every benchmark CSV must contain — matches _core.py output
EXPECTED_FIELDS = {
    "test_id", "model_name", "defense_mode",
    "prompt_sent", "response_received", "response_length_chars",
    "attack_succeeded", "detection_reason", "needs_review",
}

# Preferred column order for the merged output (extra cols appended sorted).
# INVARIANT: must mirror CSV_FIELDNAMES in _core.py exactly — these two lists
# must never drift from each other.
_BASE_FIELD_ORDER = [
    # Benchmark metadata
    "test_id", "category", "attack_goal", "evasion_style",
    "injection_position", "authority_claimed", "target_action_type",
    "linguistic_register", "harm_severity", "persistence",
    # Execution context
    "model_name", "defense_mode",
    # Timing and cost
    "latency_ms", "input_tokens", "output_tokens",
    # Attack scoring (three-tier) — score/score_confidence promoted to here so they
    # are not buried after response_received in the dynamic-union fallback
    "score", "score_confidence", "attack_succeeded", "detection_reason", "needs_review",
    # Semantic / behavioural
    "semantic_sim_score", "behavioral_signals",
    # Raw
    "response_length_chars", "prompt_sent", "response_received",
]


def _build_fieldnames(csv_files: list[Path]) -> list[str]:
    """
    Pre-pass: collect union of all column names across all CSVs.
    Returns a list with base fields ordered first, extras sorted at the end.
    """
    all_fields: set[str] = set()
    for path in csv_files:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames:
                all_fields.update(reader.fieldnames)

    # Keep base ordering, append any unknown extras sorted
    ordered = [f for f in _BASE_FIELD_ORDER if f in all_fields]
    extras  = sorted(all_fields - set(ordered))
    return ordered + extras


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

    # Build the merged fieldname list from a pre-pass over all files
    fieldnames = _build_fieldnames(csv_files)

    all_rows: list[dict] = []
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
            if missing:
                schema_errors.append(f"{path.name}: missing required fields {sorted(missing)}")

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

    # Coverage check (V1 subset: 20 attacks × 4 defense modes = 80 rows minimum)
    expected_per_model = 20 * 4
    incomplete = [(m, c) for m, c in per_model_counts.items() if c < expected_per_model]
    if incomplete:
        print(f"\nIncomplete models (< {expected_per_model} rows = still running or partial):")
        for model, count in sorted(incomplete):
            print(f"  {model}: {count}/{expected_per_model}")

    if validate_only:
        print("\n--validate-only: no output written.")
        return len(all_rows)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nMerged -> {output_file}")
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
