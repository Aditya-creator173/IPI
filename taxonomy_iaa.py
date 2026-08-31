"""
taxonomy_iaa.py — Step 3.4: Taxonomy Inter-Annotator Agreement

Generates a blind annotation template for 20 randomly-selected benchmark scenarios.
Annotators must label each scenario's attack_goal and evasion_style based solely on
the injected_text and full_prompt, WITHOUT seeing the scenario's ground-truth labels.

Two annotators complete the template independently. Then run this script with
--compute to calculate Cohen's kappa on the completed annotations.

Usage:
  # Generate annotation template (pick 20 random scenarios):
  python taxonomy_iaa.py --generate [--seed 42]

  # Compute kappa from completed annotations:
  python taxonomy_iaa.py --compute results/validation/taxonomy_annotations.json

Input for --compute (taxonomy_annotations.json):
  [
    {
      "scenario_id": "A015",
      "injected_text": "...",
      "annotator_1_attack_goal": "task_hijacking",
      "annotator_1_evasion_style": "direct",
      "annotator_2_attack_goal": "task_hijacking",
      "annotator_2_evasion_style": "direct",
      "gold_attack_goal": "task_hijacking",
      "gold_evasion_style": "direct"
    },
    ...
  ]
"""

import argparse
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
BENCHMARK_FILE = REPO_ROOT / "benchmark.json"
OUTPUT_DIR = REPO_ROOT / "results" / "validation"

ATTACK_GOALS = ["task_hijacking", "information_exfiltration", "unauthorized_action",
                "privilege_escalation", "identity_corruption"]
EVASION_STYLES = ["direct", "disguised", "split", "foreign_language", "fake_metadata"]

N_SCENARIOS = 20


def cohen_kappa(labels_a: list[str], labels_b: list[str], all_labels: list[str]) -> float:
    """Compute Cohen's kappa for two annotators over a set of items."""
    n = len(labels_a)
    assert n == len(labels_b), "Annotator lists must be the same length"

    # Observed agreement
    p_o = sum(1 for a, b in zip(labels_a, labels_b) if a == b) / n

    # Expected agreement (marginals)
    count_a = Counter(labels_a)
    count_b = Counter(labels_b)
    p_e = sum((count_a.get(l, 0) / n) * (count_b.get(l, 0) / n) for l in all_labels)

    if abs(1 - p_e) < 1e-10:
        return 1.0

    return round((p_o - p_e) / (1 - p_e), 4)


def generate_template(seed: int) -> None:
    """Pick 20 random scenarios and create a blind annotation template."""
    with open(BENCHMARK_FILE, encoding="utf-8") as f:
        data = json.load(f)

    rng = random.Random(seed)

    # Stratified: ensure at least 1 scenario per attack_goal (5 goals)
    by_goal = {}
    for s in data:
        g = s["attack_goal"]
        by_goal.setdefault(g, []).append(s)

    selected = []
    # First, guarantee 1 per goal
    for goal, scenarios in by_goal.items():
        selected.append(rng.choice(scenarios))

    # Fill remainder randomly from all (excluding already selected)
    selected_ids = {s["id"] for s in selected}
    remaining = [s for s in data if s["id"] not in selected_ids]
    extra = rng.sample(remaining, N_SCENARIOS - len(selected))
    selected.extend(extra)
    rng.shuffle(selected)

    # Build BLIND template (no gold labels shown to annotators)
    template = []
    for s in selected:
        template.append({
            "scenario_id": s["id"],
            "category": s["category"],
            "setup": s["setup"],
            "injected_text": s["injected_text"],
            "correct_behavior": s["correct_behavior"],
            # Annotators classify these:
            "annotator_1_attack_goal": "",   # One of: task_hijacking | information_exfiltration | unauthorized_action | privilege_escalation | identity_corruption
            "annotator_1_evasion_style": "", # One of: direct | disguised | split | foreign_language | fake_metadata
            "annotator_2_attack_goal": "",
            "annotator_2_evasion_style": "",
            # Gold labels (filled in when computing kappa, hidden from annotators)
            "_gold_attack_goal": s["attack_goal"],
            "_gold_evasion_style": s["evasion_style"],
        })

    output_path = OUTPUT_DIR / "taxonomy_annotations.json"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

    print(f"Taxonomy annotation template written: {output_path}")
    print(f"  {N_SCENARIOS} scenarios selected (seed={seed})")
    print(f"  Attack goals represented: {Counter(s['_gold_attack_goal'] for s in template)}")
    print(f"  Evasion styles represented: {Counter(s['_gold_evasion_style'] for s in template)}")
    print()
    print("INSTRUCTIONS FOR ANNOTATORS:")
    print("  1. Open taxonomy_annotations.json")
    print("  2. For each scenario, read 'setup', 'injected_text', and 'correct_behavior'")
    print("  3. Fill in your annotations (do NOT look at _gold_ fields):")
    print(f"     attack_goal: one of {ATTACK_GOALS}")
    print(f"     evasion_style: one of {EVASION_STYLES}")
    print("  4. Return completed file to researcher")
    print()
    print("LABEL DEFINITIONS:")
    print("  attack_goal:")
    print("    task_hijacking     — injection substitutes a different task for the original")
    print("    information_exfiltration — injection causes agent to reveal/transmit data")
    print("    unauthorized_action — injection triggers action the user didn't authorize")
    print("    privilege_escalation — injection claims elevated permissions")
    print("    identity_corruption — injection overrides the agent's identity/persona")
    print("  evasion_style:")
    print("    direct          — plain imperative ('IGNORE...', 'Do not...')")
    print("    disguised       — injection disguised as legitimate content")
    print("    split           — instruction split across multiple locations")
    print("    foreign_language — injection uses non-English language")
    print("    fake_metadata   — injection embedded in fake metadata/headers")


def compute_kappa(annotation_path: str) -> None:
    """Compute Cohen's kappa from completed annotations."""
    path = Path(annotation_path)
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        samples = json.load(f)

    # Validate completeness
    errors = []
    for i, s in enumerate(samples):
        for field in ["annotator_1_attack_goal", "annotator_1_evasion_style",
                       "annotator_2_attack_goal", "annotator_2_evasion_style"]:
            if not s.get(field):
                errors.append(f"Sample {i} ({s.get('scenario_id', '?')}): missing {field}")
            elif "attack_goal" in field and s[field] not in ATTACK_GOALS:
                errors.append(f"Sample {i}: invalid attack_goal '{s[field]}'")
            elif "evasion_style" in field and s[field] not in EVASION_STYLES:
                errors.append(f"Sample {i}: invalid evasion_style '{s[field]}'")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)

    a1_goals = [s["annotator_1_attack_goal"] for s in samples]
    a2_goals = [s["annotator_2_attack_goal"] for s in samples]
    a1_evasions = [s["annotator_1_evasion_style"] for s in samples]
    a2_evasions = [s["annotator_2_evasion_style"] for s in samples]

    kappa_goal = cohen_kappa(a1_goals, a2_goals, ATTACK_GOALS)
    kappa_evasion = cohen_kappa(a1_evasions, a2_evasions, EVASION_STYLES)

    # Accuracy vs gold (if gold labels present)
    gold_goals = [s.get("_gold_attack_goal", "") for s in samples]
    gold_evasions = [s.get("_gold_evasion_style", "") for s in samples]
    a1_goal_acc = sum(1 for a, g in zip(a1_goals, gold_goals) if a == g and g) / len(samples) if any(gold_goals) else None
    a2_goal_acc = sum(1 for a, g in zip(a2_goals, gold_goals) if a == g and g) / len(samples) if any(gold_goals) else None

    print("\n" + "=" * 60)
    print("  IPIBench Taxonomy Inter-Annotator Agreement")
    print("=" * 60)
    print(f"  N scenarios: {len(samples)}")
    print()
    print(f"  attack_goal kappa:    {kappa_goal:.4f}")
    print(f"  evasion_style kappa:  {kappa_evasion:.4f}")
    print()
    if a1_goal_acc is not None:
        print(f"  Annotator 1 vs gold: {a1_goal_acc*100:.1f}% (attack_goal)")
        print(f"  Annotator 2 vs gold: {a2_goal_acc*100:.1f}% (attack_goal)")
    print("=" * 60)

    result = {
        "n_scenarios": len(samples),
        "kappa_attack_goal": kappa_goal,
        "kappa_evasion_style": kappa_evasion,
        "kappa_average": round((kappa_goal + kappa_evasion) / 2, 4),
        "annotator_1_vs_gold_attack_goal": round(a1_goal_acc, 4) if a1_goal_acc else None,
        "annotator_2_vs_gold_attack_goal": round(a2_goal_acc, 4) if a2_goal_acc else None,
    }

    out_path = OUTPUT_DIR / "taxonomy_iaa_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"\n  Results saved to {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Taxonomy IAA: generate template or compute kappa.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--generate", action="store_true", help="Generate blank annotation template.")
    group.add_argument("--compute", type=str, metavar="PATH", help="Compute kappa from completed annotations.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for scenario selection (default: 42)")
    args = parser.parse_args()

    if args.generate:
        generate_template(args.seed)
    elif args.compute:
        compute_kappa(args.compute)


if __name__ == "__main__":
    main()
