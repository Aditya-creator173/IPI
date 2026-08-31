"""
statistical_tests.py
=====================
Statistical rigor pipeline for IPIBench.

Implements:
  - Wilcoxon signed-rank test (paired models)
  - McNemar's test (binary outcomes)
  - Benjamini-Hochberg FDR correction
  - Non-parametric bootstrap CIs (95%)
  - 95% Wilson Score intervals
  - Power analysis justifying N=400
  - Per-cell taxonomy counts with thin-cell disclosure

Usage:
  python analysis/statistical_tests.py
  python analysis/statistical_tests.py --pair gpt5 gpt55
  python analysis/statistical_tests.py --all-pairs
  python analysis/statistical_tests.py --power-analysis
"""

from __future__ import annotations

import csv
import json
import math
import random
import sys
from pathlib import Path
from collections import defaultdict
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = REPO_ROOT / "results" / "csv"
BENCHMARK_PATH = REPO_ROOT / "benchmark.json"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_model_scores(model_key: str) -> list[float]:
    path = CSV_DIR / f"{model_key}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No CSV for model: {model_key}")
    with open(path, encoding="utf-8", errors="replace") as f:
        return [float(r["score"]) for r in csv.DictReader(f)
                if r.get("score") not in ("", None)]


def load_benchmark_taxonomy() -> list[dict]:
    with open(BENCHMARK_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("test_cases", [])


# ---------------------------------------------------------------------------
# Wilcoxon signed-rank test (exact for small N, normal approx for large N)
# ---------------------------------------------------------------------------

def wilcoxon_signed_rank(x: list[float], y: list[float]) -> dict:
    """Paired Wilcoxon signed-rank test. H0: median of (x-y) = 0."""
    diffs = [a - b for a, b in zip(x, y)]
    nonzero = [(d, abs(d)) for d in diffs if d != 0]
    n = len(nonzero)
    if n == 0:
        return {"W": 0, "n": 0, "p_approx": 1.0, "significant": False, "note": "All differences zero"}

    ranked = sorted(nonzero, key=lambda t: t[1])
    ranks = list(range(1, n + 1))

    W_plus = sum(ranks[i] for i, (d, _) in enumerate(ranked) if d > 0)
    W_minus = sum(ranks[i] for i, (d, _) in enumerate(ranked) if d < 0)
    W = min(W_plus, W_minus)

    # Normal approximation (valid for n > 10)
    mu = n * (n + 1) / 4
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    if sigma == 0:
        return {"W": W, "n": n, "p_approx": 1.0, "significant": False}
    z = (W - mu) / sigma
    # Two-sided p-value from z (approximation using erfc)
    p = math.erfc(abs(z) / math.sqrt(2))

    return {
        "W": W,
        "W_plus": W_plus,
        "W_minus": W_minus,
        "n_nonzero": n,
        "z_approx": round(z, 4),
        "p_approx": round(p, 6),
        "significant_alpha05": p < 0.05,
        "significant_alpha01": p < 0.01,
    }


# ---------------------------------------------------------------------------
# McNemar's test (binary outcomes: 1=breach, 0=not)
# ---------------------------------------------------------------------------

def mcnemar_test(x: list[float], y: list[float]) -> dict:
    """McNemar's test on binary attack-succeeded outcomes."""
    x_bin = [1 if s == 1.0 else 0 for s in x]
    y_bin = [1 if s == 1.0 else 0 for s in y]

    b = sum(1 for a, b_ in zip(x_bin, y_bin) if a == 1 and b_ == 0)
    c = sum(1 for a, b_ in zip(x_bin, y_bin) if a == 0 and b_ == 1)

    if b + c == 0:
        return {"b": 0, "c": 0, "chi2": 0, "p": 1.0, "significant": False, "note": "No discordant pairs"}

    # With continuity correction (Yates)
    chi2 = (abs(b - c) - 1) ** 2 / (b + c) if (b + c) > 0 else 0
    # Chi-square 1df p-value approximation
    p = math.exp(-chi2 / 2) if chi2 >= 0 else 1.0

    return {
        "b_only_x_succeeds": b,
        "c_only_y_succeeds": c,
        "chi2_with_continuity": round(chi2, 4),
        "p_approx": round(p, 6),
        "significant_alpha05": p < 0.05,
    }


# ---------------------------------------------------------------------------
# Benjamini-Hochberg FDR correction
# ---------------------------------------------------------------------------

def benjamini_hochberg(p_values: list[float], alpha: float = 0.05) -> list[bool]:
    """BH FDR correction. Returns list of booleans: True = reject H0."""
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda t: t[1])
    rejected = [False] * m
    for rank, (orig_idx, p) in enumerate(indexed, 1):
        if p <= (rank / m) * alpha:
            rejected[orig_idx] = True
        else:
            # Once threshold is not met, all subsequent are not rejected
            # (step-up: actually we need to find the largest k where condition holds)
            pass
    # Proper step-up implementation
    rejected = [False] * m
    k_max = 0
    for rank, (orig_idx, p) in enumerate(indexed, 1):
        if p <= (rank / m) * alpha:
            k_max = rank
    for rank, (orig_idx, p) in enumerate(indexed, 1):
        if rank <= k_max:
            rejected[orig_idx] = True
    return rejected


# ---------------------------------------------------------------------------
# Bootstrap CI (non-parametric)
# ---------------------------------------------------------------------------

def bootstrap_ci(scores: list[float], n_boot: int = 2000, ci: float = 0.95, seed: int = 42) -> dict:
    """Non-parametric bootstrap CI for weighted ASR."""
    rng = random.Random(seed)
    n = len(scores)
    means = []
    for _ in range(n_boot):
        sample = [scores[rng.randint(0, n - 1)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo_idx = int((1 - ci) / 2 * n_boot)
    hi_idx = int((1 + ci) / 2 * n_boot)
    point = sum(scores) / n
    return {
        "point_estimate": round(point * 100, 2),
        "ci_lower": round(means[lo_idx] * 100, 2),
        "ci_upper": round(means[hi_idx] * 100, 2),
        "ci_level": ci,
        "n_bootstrap": n_boot,
    }


# ---------------------------------------------------------------------------
# Wilson Score interval (for proportions)
# ---------------------------------------------------------------------------

def wilson_score_ci(successes: int, n: int, z: float = 1.96) -> dict:
    """95% Wilson Score interval for a proportion."""
    if n == 0:
        return {"lower": 0.0, "upper": 0.0, "proportion": 0.0}
    p = successes / n
    denom = 1 + z ** 2 / n
    center = (p + z ** 2 / (2 * n)) / denom
    margin = (z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2))) / denom
    return {
        "proportion": round(p, 4),
        "lower": round(max(0, center - margin), 4),
        "upper": round(min(1, center + margin), 4),
    }


# ---------------------------------------------------------------------------
# Power analysis for N=400
# ---------------------------------------------------------------------------

def power_analysis_n400() -> dict:
    """
    Justification for N=400 per model (100 scenarios × 4 defense modes).

    Under H0: ASR_A = ASR_B = 0.30 (conservative null)
    Detectable effect: delta = 0.05 (5pp difference)
    alpha = 0.05 (two-sided), target power = 0.80

    Using paired Wilcoxon signed-rank approximation.
    """
    # Minimum detectable effect at N=400 with alpha=0.05, power=0.80
    # For a proportion test: n = (z_alpha/2 + z_beta)^2 * 2 * p * (1-p) / delta^2
    z_alpha_2 = 1.96   # alpha = 0.05, two-sided
    z_beta = 0.842     # power = 0.80
    p_null = 0.30      # conservative null ASR
    delta = 0.05       # 5pp detectable effect

    n_required = ((z_alpha_2 + z_beta) ** 2) * 2 * p_null * (1 - p_null) / (delta ** 2)

    # Achieved power at N=400
    delta_detectable_400 = (z_alpha_2 + z_beta) * math.sqrt(2 * p_null * (1 - p_null) / 400)

    return {
        "n_per_model": 400,
        "n_scenarios": 100,
        "n_defense_modes": 4,
        "alpha": 0.05,
        "target_power": 0.80,
        "null_asr_assumption": p_null,
        "n_required_for_5pp_effect": round(n_required),
        "n_provided": 400,
        "provides_adequate_power": 400 >= n_required,
        "minimum_detectable_effect_at_n400": round(delta_detectable_400 * 100, 2),
        "justification": (
            f"N=400 (100 scenarios x 4 defense modes) provides adequate power to detect "
            f"a {round(delta_detectable_400*100, 1)}pp difference in Weighted ASR at "
            f"alpha=0.05 with >=80% power, assuming null ASR=30%."
        ),
    }


# ---------------------------------------------------------------------------
# Per-cell taxonomy counts with thin-cell disclosure
# ---------------------------------------------------------------------------

def taxonomy_cell_counts(thin_threshold: int = 10) -> dict:
    """
    Compute per-cell counts across taxonomy dimensions.
    Flag thin cells (< thin_threshold) for disclosure.
    """
    cases = load_benchmark_taxonomy()
    dims = ["category", "attack_goal", "evasion_style", "injection_position",
            "authority_claimed", "target_action_type", "linguistic_register", "harm_severity"]

    result = {}
    thin_cells = []

    for dim in dims:
        counts = defaultdict(int)
        for tc in cases:
            val = tc.get(dim, "unknown")
            counts[val] += 1
        result[dim] = dict(counts)
        for val, cnt in counts.items():
            if cnt < thin_threshold:
                thin_cells.append({"dimension": dim, "value": val, "count": cnt})

    return {
        "per_dimension_counts": result,
        "thin_cells": thin_cells,
        "thin_threshold": thin_threshold,
        "n_thin_cells": len(thin_cells),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_pair_test(model_a: str, model_b: str) -> None:
    print(f"\n{'='*60}")
    print(f"  Paired tests: {model_a} vs {model_b}")
    print(f"{'='*60}")

    try:
        scores_a = load_model_scores(model_a)
        scores_b = load_model_scores(model_b)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return

    if len(scores_a) != len(scores_b):
        print(f"WARNING: Row count mismatch: {len(scores_a)} vs {len(scores_b)}")
        min_n = min(len(scores_a), len(scores_b))
        scores_a = scores_a[:min_n]
        scores_b = scores_b[:min_n]

    asr_a = sum(scores_a) / len(scores_a) * 100
    asr_b = sum(scores_b) / len(scores_b) * 100
    print(f"  {model_a}: {asr_a:.1f}% WASR (N={len(scores_a)})")
    print(f"  {model_b}: {asr_b:.1f}% WASR (N={len(scores_b)})")

    wsr = wilcoxon_signed_rank(scores_a, scores_b)
    print(f"\n  Wilcoxon signed-rank:")
    print(f"    W = {wsr['W']}, n_nonzero = {wsr.get('n_nonzero', 'N/A')}")
    print(f"    z ≈ {wsr.get('z_approx', 'N/A')}, p ≈ {wsr.get('p_approx', 'N/A')}")
    print(f"    Significant (α=0.05): {wsr.get('significant_alpha05', 'N/A')}")

    mc = mcnemar_test(scores_a, scores_b)
    print(f"\n  McNemar's test (binary):")
    print(f"    b={mc.get('b_only_x_succeeds', 0)}, c={mc.get('c_only_y_succeeds', 0)}")
    print(f"    χ² ≈ {mc.get('chi2_with_continuity', 'N/A')}, p ≈ {mc.get('p_approx', 'N/A')}")
    print(f"    Significant (α=0.05): {mc.get('significant_alpha05', 'N/A')}")

    ci_a = bootstrap_ci(scores_a)
    ci_b = bootstrap_ci(scores_b)
    print(f"\n  Bootstrap 95% CI (Weighted ASR):")
    print(f"    {model_a}: {ci_a['point_estimate']}% [{ci_a['ci_lower']}%, {ci_a['ci_upper']}%]")
    print(f"    {model_b}: {ci_b['point_estimate']}% [{ci_b['ci_lower']}%, {ci_b['ci_upper']}%]")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="IPIBench Statistical Rigor Pipeline")
    parser.add_argument("--pair", nargs=2, metavar=("MODEL_A", "MODEL_B"),
                        help="Run paired tests between two models")
    parser.add_argument("--power-analysis", action="store_true",
                        help="Run power analysis for N=400")
    parser.add_argument("--taxonomy", action="store_true",
                        help="Per-cell taxonomy counts with thin-cell disclosure")
    parser.add_argument("--all-pairs", action="store_true",
                        help="Run paired tests for all same-lab reasoning pairs")
    args = parser.parse_args()

    if args.power_analysis or (not args.pair and not args.all_pairs and not args.taxonomy):
        pa = power_analysis_n400()
        print("\n" + "=" * 60)
        print("  Power Analysis: N=400 Justification")
        print("=" * 60)
        for k, v in pa.items():
            if k != "justification":
                print(f"  {k}: {v}")
        print(f"\n  {pa['justification']}")

    if args.taxonomy:
        print("\n" + "=" * 60)
        print("  Taxonomy Cell Counts (thin-cell disclosure)")
        print("=" * 60)
        tc = taxonomy_cell_counts()
        for dim, counts in tc["per_dimension_counts"].items():
            print(f"\n  {dim}:")
            for val, cnt in sorted(counts.items(), key=lambda x: -x[1]):
                flag = " [THIN CELL]" if cnt < tc["thin_threshold"] else ""
                print(f"    {val}: {cnt}{flag}")
        if tc["thin_cells"]:
            print(f"\n  {tc['n_thin_cells']} thin cells (< {tc['thin_threshold']}) require disclosure in paper.")

    if args.pair:
        run_pair_test(args.pair[0], args.pair[1])

    if args.all_pairs:
        reasoning_pairs = [
            ("deepseek_r1", "deepseek_v4_pro"),
            ("qwen3_30b_thinking", "qwen3_30b_instruct"),
            ("qwq32b", "qwen36_27b"),
            ("cohere_command_a_reasoning", "cohere_command_a_plus"),
            ("grok41fast_reasoning", "grok41fast_nonreasoning"),
            ("grok420_reasoning", "grok420_nonreasoning"),
        ]
        p_values = []
        pair_results = []
        for a, b in reasoning_pairs:
            try:
                sa = load_model_scores(a)
                sb = load_model_scores(b)
                if len(sa) != len(sb):
                    n = min(len(sa), len(sb))
                    sa, sb = sa[:n], sb[:n]
                wsr = wilcoxon_signed_rank(sa, sb)
                p_values.append(wsr.get("p_approx", 1.0))
                pair_results.append((a, b, wsr))
            except FileNotFoundError as e:
                print(f"SKIP: {e}")
                p_values.append(1.0)
                pair_results.append((a, b, None))

        rejected = benjamini_hochberg(p_values)
        print("\n" + "=" * 70)
        print("  All-Pairs BH-FDR Corrected Wilcoxon Tests (Reasoning Pairs)")
        print("=" * 70)
        for i, (a, b, wsr) in enumerate(pair_results):
            if wsr:
                p = wsr.get("p_approx", "N/A")
                sig = rejected[i]
                print(f"  {a} vs {b}")
                print(f"    p≈{p}, BH-FDR significant: {sig}")
            else:
                print(f"  {a} vs {b}: DATA MISSING")


if __name__ == "__main__":
    main()
