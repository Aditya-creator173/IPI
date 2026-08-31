"""
embed_canaries.py — Step 3.1.1
Embeds [CANARY:ipibench-v1-<guid>] marker into injected_text for every scenario
in benchmark.json. The marker is appended after the injected instruction text
as a trailing inert marker, so a model that fully complies with the injection
will reproduce the canary string in its output.

The canary_guid field in metadata is the authoritative source; this script
reads from it and writes the formatted string into injected_text.

Idempotent: if [CANARY:ipibench-v1-<guid>] is already present, it is not added again.

Run:
    python embed_canaries.py
"""

import json
import sys

BENCHMARK_FILE = "benchmark.json"
CANARY_PREFIX = "ipibench-v1-"


def main():
    with open(BENCHMARK_FILE, encoding="utf-8") as f:
        data = json.load(f)

    already_embedded = 0
    newly_embedded = 0
    missing_guid = 0

    for scenario in data:
        guid = scenario.get("canary_guid")
        if not guid:
            print(f"  WARNING: {scenario['id']} has no canary_guid — skipping", file=sys.stderr)
            missing_guid += 1
            continue

        canary_tag = f"[CANARY:{CANARY_PREFIX}{guid}]"

        injected = scenario.get("injected_text", "")
        if canary_tag in injected:
            already_embedded += 1
            continue

        # Append canary after the injected instruction.
        # A single space separator — keeps it semantically inert but reproducible.
        scenario["injected_text"] = injected + " " + canary_tag
        newly_embedded += 1

    print(f"Already embedded:  {already_embedded}")
    print(f"Newly embedded:    {newly_embedded}")
    print(f"Missing guid:      {missing_guid}")
    print(f"Total scenarios:   {len(data)}")

    if missing_guid > 0:
        print("ERROR: Some scenarios had no canary_guid. Fix before proceeding.", file=sys.stderr)
        sys.exit(1)

    with open(BENCHMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nbenchmark.json written — {newly_embedded} canaries embedded.")

    # Verification: spot-check 3 scenarios
    print("\n=== SPOT-CHECK (first 3 scenarios) ===")
    with open(BENCHMARK_FILE, encoding="utf-8") as f:
        verify = json.load(f)
    for s in verify[:3]:
        it = s["injected_text"]
        tag = f"[CANARY:{CANARY_PREFIX}{s['canary_guid']}]"
        found = tag in it
        print(f"  {s['id']}: canary present={found}  injected_text tail: ...{it[-60:]}")

    # Verify the full_prompt field does NOT need updating —
    # injected_text is embedded inside full_prompt for most scenarios.
    # Check if full_prompt already contains injected_text (it should).
    mismatches = 0
    for s in verify:
        if s.get("injected_text") and s.get("full_prompt"):
            tag = f"[CANARY:{CANARY_PREFIX}{s['canary_guid']}]"
            if tag not in s["full_prompt"]:
                # full_prompt was built from injected_text before canary embedding
                # This is expected — full_prompt is the static test prompt, not live.
                mismatches += 1
    print(f"\nfull_prompt fields missing canary tag: {mismatches}/100")
    print("(This is expected — full_prompt is static; injected_text is the live field.)")


if __name__ == "__main__":
    main()
