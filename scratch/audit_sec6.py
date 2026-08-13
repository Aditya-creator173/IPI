import os
import glob
import csv
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Read model_eval.md
eval_path = "LOCAL ONLY/model_eval.md"
with open(eval_path, "r", encoding="utf-8") as f:
    eval_text = f.read()

# Load all CSV valid row counts
csv_counts = {}
for fpath in glob.glob("results/csv/*.csv"):
    fname = os.path.basename(fpath).replace(".csv", "")
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        cnt = sum(1 for r in reader if r.get("response_received", "") and not r.get("response_received", "").startswith("API_ERROR:"))
        csv_counts[fname] = cnt

print("=== AUDIT OF SECTION 6 IN MODEL_EVAL.MD vs CSV GROUND TRUTH ===\n")

# Find table rows in Section 6
sec6_match = re.search(r"# Section 6 — Active Progress Check.*", eval_text, re.DOTALL)
if sec6_match:
    sec6_text = sec6_match.group(0)
    # Match markdown table rows: | Model | Rows | Progress | Status |
    lines = sec6_text.split("\n")
    for line in lines:
        if "|" in line and "---" not in line and "Model" not in line and "Section" not in line and "##" not in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 3:
                model_name_md = parts[0]
                rows_md = parts[1]
                status_md = parts[-1]
                print(f"{model_name_md:<30} | MD Rows: {rows_md:<10} | MD Status: {status_md}")

