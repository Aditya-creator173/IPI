"""Merge per-model CSV files from results/csv into one final CSV."""

from __future__ import annotations

import csv
from pathlib import Path


def merge_results(
    input_dir: Path = Path("results/csv"),
    output_file: Path = Path("results/results_final.csv"),
) -> None:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    csv_files = sorted(p for p in input_dir.glob("*.csv") if p.is_file())
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {input_dir}")

    rows = []
    fieldnames = None

    for path in csv_files:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                continue
            if fieldnames is None:
                fieldnames = reader.fieldnames
            for row in reader:
                rows.append(row)

    if fieldnames is None:
        raise ValueError("Unable to infer CSV header from input files.")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Merged {len(csv_files)} files into {output_file}")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    merge_results()
