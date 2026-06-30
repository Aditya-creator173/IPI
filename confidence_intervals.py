"""
confidence_intervals.py
=======================
Statistical utilities for IPIBench analysis notebook.

Provides:
  - Wilson confidence intervals for ASR proportions
  - McNemar's test for pairwise defense mode comparison
  - Cohen's h effect size for proportion differences
  - Formatted output helpers for paper tables

Usage in analysis.ipynb:
  from confidence_intervals import wilson_ci, defense_comparison_table, cohens_h
"""

from __future__ import annotations

import math
from typing import Optional


# ---------------------------------------------------------------------------
# Wilson confidence interval
# ---------------------------------------------------------------------------

def wilson_ci(
    n_success: int,
    n_total: int,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """
    Wilson score confidence interval for a proportion.

    Parameters
    ----------
    n_success : number of successes (attacks succeeded)
    n_total   : total observations
    alpha     : significance level (default 0.05 -> 95% CI)

    Returns
    -------
    (lower, upper) as proportions in [0, 1]

    References
    ----------
    Wilson (1927). "Probable inference, the law of succession, and
    statistical inference." JASA 22(158):209-212.
    """
    if n_total == 0:
        return (0.0, 0.0)

    from scipy import stats  # type: ignore
    z = stats.norm.ppf(1 - alpha / 2)

    p_hat = n_success / n_total
    denominator = 1 + z**2 / n_total
    center = (p_hat + z**2 / (2 * n_total)) / denominator
    spread = (
        z
        * math.sqrt(p_hat * (1 - p_hat) / n_total + z**2 / (4 * n_total**2))
        / denominator
    )

    lower = max(0.0, center - spread)
    upper = min(1.0, center + spread)
    return lower, upper


def wilson_ci_pct(
    n_success: int,
    n_total: int,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """Same as wilson_ci but returns percentages (0-100)."""
    lo, hi = wilson_ci(n_success, n_total, alpha)
    return lo * 100, hi * 100


# ---------------------------------------------------------------------------
# Cohen's h effect size
# ---------------------------------------------------------------------------

def cohens_h(p1: float, p2: float) -> float:
    """
    Cohen's h effect size for the difference between two proportions.

    h = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))

    Interpretation:
      |h| < 0.2  : small
      |h| < 0.5  : medium
      |h| >= 0.5 : large
    """
    return 2 * math.asin(math.sqrt(max(0.0, min(1.0, p1)))) - 2 * math.asin(
        math.sqrt(max(0.0, min(1.0, p2)))
    )


# ---------------------------------------------------------------------------
# McNemar's test (paired defense-mode comparison)
# ---------------------------------------------------------------------------

def mcnemar_test(
    results_a: list[int],
    results_b: list[int],
) -> tuple[float, float]:
    """
    McNemar's test for paired binary data.

    Use to compare attack success rates between two defense modes on the
    SAME set of prompts (paired observations).

    Parameters
    ----------
    results_a : list of 0/1 for defense mode A (length N)
    results_b : list of 0/1 for defense mode B (length N)

    Returns
    -------
    (chi2, p_value)

    Notes
    -----
    Uses the exact binomial test when b + c < 25 (small sample correction).
    """
    from scipy import stats  # type: ignore

    if len(results_a) != len(results_b):
        raise ValueError("results_a and results_b must have the same length")

    # Build 2x2 contingency table
    # b = A success, B fail  (A found something B missed)
    # c = A fail, B success  (B found something A missed)
    b = sum(1 for a, bb in zip(results_a, results_b) if a == 1 and bb == 0)
    c = sum(1 for a, bb in zip(results_a, results_b) if a == 0 and bb == 1)

    if b + c == 0:
        return (0.0, 1.0)  # no discordant pairs -- modes are identical

    if b + c < 25:
        # Exact binomial
        result = stats.binomtest(b, b + c, p=0.5)
        return (float("nan"), result.pvalue)
    else:
        # McNemar chi-square with continuity correction
        chi2 = (abs(b - c) - 1) ** 2 / (b + c)
        p = 1 - stats.chi2.cdf(chi2, df=1)
        return chi2, p


# ---------------------------------------------------------------------------
# Defense comparison table
# ---------------------------------------------------------------------------

def defense_comparison_table(
    df,
    mode_order: Optional[list[str]] = None,
    baseline_mode: str = "none",
    alpha: float = 0.05,
):
    """
    Build the defense summary table with ASR, Wilson CI, and McNemar p-value
    vs. the baseline defense mode.

    Parameters
    ----------
    df           : pandas DataFrame (must have defense_mode + attack_succeeded)
    mode_order   : list of defense modes in display order
    baseline_mode: defense mode to compare against (default "none")
    alpha        : confidence level for Wilson CI

    Returns
    -------
    DataFrame with columns:
      defense_mode | n | n_success | asr_pct | ci_low_pct | ci_high_pct |
      abs_reduction_pp | mcnemar_p | effect_h | significant
    """
    import pandas as pd  # type: ignore

    if mode_order is None:
        mode_order = ["none", "prompt_warning", "spotlighting", "input_filter"]

    rows = []
    baseline_results = None
    baseline_asr = 0.0

    for mode in mode_order:
        subset = df[df["defense_mode"] == mode]
        n = len(subset)
        n_success = int(subset["attack_succeeded"].sum())
        asr = n_success / n if n > 0 else 0.0
        ci_lo, ci_hi = wilson_ci_pct(n_success, n)

        row: dict = {
            "defense_mode":     mode,
            "n":                n,
            "n_success":        n_success,
            "asr_pct":          round(asr * 100, 2),
            "ci_low_pct":       round(ci_lo, 2),
            "ci_high_pct":      round(ci_hi, 2),
            "abs_reduction_pp": None,
            "mcnemar_p":        None,
            "effect_h":         None,
            "significant":      None,
        }

        if mode == baseline_mode:
            baseline_results = list(subset["attack_succeeded"].astype(int))
            baseline_asr = asr
            row["abs_reduction_pp"] = 0.0
            row["mcnemar_p"]        = 1.0
            row["effect_h"]         = 0.0
            row["significant"]      = False
        else:
            mode_results = list(subset["attack_succeeded"].astype(int))
            if baseline_results is not None and len(mode_results) == len(baseline_results):
                _, p = mcnemar_test(baseline_results, mode_results)
                h = cohens_h(baseline_asr, asr)
                row["abs_reduction_pp"] = round((baseline_asr - asr) * 100, 2)
                row["mcnemar_p"]        = round(p, 4)
                row["effect_h"]         = round(h, 3)
                row["significant"]      = bool(p < alpha)

        rows.append(row)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# ASR with CI -- per-model summary
# ---------------------------------------------------------------------------

def model_asr_table(
    df,
    model_order: Optional[list[str]] = None,
    defense_mode: str = "none",
    alpha: float = 0.05,
):
    """
    Build per-model ASR table with Wilson confidence intervals for a
    specific defense mode.

    Returns DataFrame with columns:
      model_name | n | n_success | asr_pct | ci_low_pct | ci_high_pct
    """
    import pandas as pd  # type: ignore

    subset = df[df["defense_mode"] == defense_mode]

    if model_order is None:
        model_order = sorted(subset["model_name"].unique())

    rows = []
    for model in model_order:
        model_df = subset[subset["model_name"] == model]
        n = len(model_df)
        if n == 0:
            continue
        n_success = int(model_df["attack_succeeded"].sum())
        asr = n_success / n
        ci_lo, ci_hi = wilson_ci_pct(n_success, n)
        rows.append({
            "model_name": model,
            "n":          n,
            "n_success":  n_success,
            "asr_pct":    round(asr * 100, 2),
            "ci_low_pct": round(ci_lo, 2),
            "ci_high_pct":round(ci_hi, 2),
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Paper-ready formatter
# ---------------------------------------------------------------------------

def format_asr_with_ci(asr_pct: float, ci_lo: float, ci_hi: float) -> str:
    """
    Format ASR for paper tables.
    Example: format_asr_with_ci(54.5, 43.1, 65.6) -> "54.5% [43.1-65.6]"
    """
    return f"{asr_pct:.1f}% [{ci_lo:.1f}-{ci_hi:.1f}]"
