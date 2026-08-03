"""
convergence_plot.py
===================
Measures rank stability (Kendall's tau correlation) across scenario sub-samples
N in [20, 40, 60, 80, 100] to identify the scenario count where model rankings
stabilize.

Usage:
    python scripts/convergence_plot.py
"""

from __future__ import annotations

import glob
import json
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import kendalltau


def compute_ipir_from_df(df: pd.DataFrame) -> float:
    if df.empty or 'score' not in df.columns:
        return 0.0
    scores = pd.to_numeric(df['score'], errors='coerce').fillna(0.5)
    return float(np.mean(1.0 - scores) * 100.0)


def run_convergence_study(csv_dir: str, num_trials: int = 50) -> dict:
    csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
    model_dfs = {}
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        if filename in ('.gitkeep', 'results.csv'):
            continue
        try:
            df = pd.read_csv(filepath)
            if df.empty or 'score' not in df.columns or 'test_id' not in df.columns:
                continue
            if 'defense_mode' in df.columns:
                baseline_df = df[df['defense_mode'].astype(str).str.lower() == 'none'].copy()
                if not baseline_df.empty:
                    df = baseline_df
            m_name = df['model_name'].iloc[0] if 'model_name' in df.columns else filename.replace('.csv', '')
            model_dfs[m_name] = df
        except Exception:
            pass

    if not model_dfs:
        print("No valid CSV files found.")
        return {}

    all_test_ids = set()
    for df in model_dfs.values():
        all_test_ids.update(df['test_id'].unique())
    test_ids_list = list(all_test_ids)
    max_scenarios = len(test_ids_list)

    # Compute full dataset ranking
    full_scores = {m: compute_ipir_from_df(df) for m, df in model_dfs.items()}
    full_models = sorted(full_scores.keys(), key=lambda m: full_scores[m], reverse=True)
    full_ranks = {m: r for r, m in enumerate(full_models, start=1)}

    sample_sizes = [20, 40, 60, 80, min(100, max_scenarios)]
    sample_sizes = sorted(list(set(sample_sizes)))

    results = {}
    np.random.seed(42)

    for n in sample_sizes:
        taus = []
        for _ in range(num_trials):
            sampled_ids = np.random.choice(test_ids_list, size=n, replace=False)
            iter_scores = {}
            for m_name, df in model_dfs.items():
                sub_df = df[df['test_id'].isin(sampled_ids)]
                iter_scores[m_name] = compute_ipir_from_df(sub_df)

            sorted_iter = sorted(iter_scores.keys(), key=lambda m: iter_scores[m], reverse=True)
            iter_ranks = {m: r for r, m in enumerate(sorted_iter, start=1)}

            # Compare iter_ranks with full_ranks
            y_full = [full_ranks[m] for m in full_models]
            y_iter = [iter_ranks[m] for m in full_models]

            tau, _ = kendalltau(y_full, y_iter)
            if not np.isnan(tau):
                taus.append(tau)

        mean_tau = float(np.mean(taus)) if taus else 0.0
        std_tau = float(np.std(taus)) if taus else 0.0
        results[str(n)] = {
            "n_scenarios": n,
            "mean_kendall_tau": round(mean_tau, 4),
            "std_kendall_tau": round(std_tau, 4)
        }

    return results


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_dir = os.path.join(base_dir, "results", "csv")
    out_json = os.path.join(base_dir, "results", "convergence_study.json")
    out_png = os.path.join(base_dir, "results", "convergence_plot.png")

    results = run_convergence_study(csv_dir, num_trials=50)

    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Convergence study complete. Results written to {out_json}")
    print(f"\n{'Scenario Count (N)':<20} {'Kendall Tau (mean ± std)':<30}")
    print("-" * 50)
    stabilization_n = None
    for n_str, data in results.items():
        mean_tau = data['mean_kendall_tau']
        std_tau = data['std_kendall_tau']
        print(f"{n_str:<20} {mean_tau:.4f} ± {std_tau:.4f}")
        if mean_tau >= 0.95 and stabilization_n is None:
            stabilization_n = n_str

    if stabilization_n:
        print(f"\nRankings stabilize at approximately N={stabilization_n} scenarios (Kendall's tau >= 0.95).")

    # Plot if matplotlib is installed
    try:
        import matplotlib.pyplot as plt
        ns = [int(k) for k in results.keys()]
        taus = [v['mean_kendall_tau'] for v in results.values()]
        stds = [v['std_kendall_tau'] for v in results.values()]

        plt.figure(figsize=(8, 5))
        plt.plot(ns, taus, 'o-', color='#2b5c8f', linewidth=2, label="Kendall's Tau")
        plt.fill_between(ns, np.array(taus) - np.array(stds), np.array(taus) + np.array(stds), color='#2b5c8f', alpha=0.2)
        plt.axhline(0.95, color='crimson', linestyle='--', label='Stabilization Threshold (0.95)')
        plt.xlabel('Number of Scenarios (N)', fontsize=12)
        plt.ylabel("Kendall's Tau Rank Correlation", fontsize=12)
        plt.title('IPIBench Ranking Convergence vs. Scenario Sample Size', fontsize=14)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.savefig(out_png, dpi=300)
        print(f"Plot saved to {out_png}")
    except ImportError:
        print("matplotlib not installed; skipping plot generation.")


if __name__ == "__main__":
    main()
