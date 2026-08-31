"""
generate_figures.py
===================
Generate all paper figures for IPIBench.

Figures:
  1. Overall ASR ranking bar chart (all 55 models)
  2. Reasoning vs Non-reasoning delta plot
  3. GPT-5 series progression
  4. Defense mode breakdown heatmap
  5. Score distribution (0 / 0.5 / 1) stacked bar

Usage:
  python analysis/generate_figures.py
  python analysis/generate_figures.py --figure 1
  python analysis/generate_figures.py --all
"""

from __future__ import annotations

import csv
import json
import sys
import os
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = REPO_ROOT / "results" / "csv"
FIGURES_DIR = REPO_ROOT / "results" / "figures"

# Model display names
MODEL_DISPLAY_NAMES = {
    "gpt5": "GPT-5",
    "gpt54": "GPT-5.4",
    "gpt55": "GPT-5.5",
    "gpt56_sol": "GPT-5.6 Sol",
    "gpt56_luna": "GPT-5.6 Luna",
    "gpt56_terra": "GPT-5.6 Terra",
    "gpt_oss_20b": "GPT OSS 20B",
    "gpt_oss_120b": "GPT OSS 120B",
    "deepseek_r1": "DeepSeek R1",
    "deepseek_v4_pro": "DeepSeek V4 Pro",
    "deepseek_v4_flash": "DeepSeek V4 Flash",
    "deepseek_v32": "DeepSeek V3.2",
    "qwen3_30b_thinking": "Qwen3 30B Thinking",
    "qwen3_30b_instruct": "Qwen3 30B Instruct",
    "qwen3_30b_moe": "Qwen3 30B MoE",
    "qwq32b": "QwQ 32B",
    "qwq_plus": "QwQ Plus",
    "qwen36_27b": "Qwen3.6 27B",
    "qwen36_max": "Qwen3.6 Max",
    "qwen37_flash": "Qwen3.7 Flash",
    "qwen37_max": "Qwen3.7 Max",
    "qwen37_plus": "Qwen3.7 Plus",
    "qwen38_max": "Qwen3.8 Max",
    "qwen35_plus": "Qwen3.5 Plus",
    "qwen3_coder_480b": "Qwen3 Coder 480B",
    "gemini35_flash": "Gemini 3.5 Flash",
    "gemini36_flash": "Gemini 3.6 Flash",
    "gemini37_flash": "Gemini 3.7 Flash",
    "gemma4_26b_moe": "Gemma4 26B MoE",
    "gemma4_31b": "Gemma4 31B",
    "grok4": "Grok 4",
    "grok41fast_reasoning": "Grok 4.1 Reasoning",
    "grok41fast_nonreasoning": "Grok 4.1 Non-R",
    "grok420_reasoning": "Grok 4.20 Reasoning",
    "grok420_nonreasoning": "Grok 4.20 Non-R",
    "cohere_command_a_reasoning": "Cohere Cmd-A-R",
    "cohere_command_a_plus": "Cohere Cmd-A+",
    "mistral_large3": "Mistral Large 3",
    "codestral": "Codestral",
    "llama33_70b": "LLaMA 3.3 70B",
    "llama31_8b": "LLaMA 3.1 8B",
    "llama4_scout": "LLaMA 4 Scout",
    "ibm_granite": "IBM Granite",
    "kimi_k2": "Kimi K2",
    "kimi_k3": "Kimi K3",
    "minimax_m3": "MiniMax M3",
    "glm51": "GLM 5.1",
    "glm52": "GLM 5.2",
    "nemotron_ultra": "Nemotron Ultra",
    "phi4": "Phi-4",
    "diffusiongemma": "DiffusionGemma",
    "poolside_laguna_m1": "Poolside Laguna M1",
    "muse_glimmer_30b": "Muse Glimmer 30B",
    "groq_compound": "Groq Compound",
    "ling_30_flash": "Ling 3.0 Flash",
    "liquid_lfm25": "Liquid LFM 2.5",
    "sea_lion_v4": "SEA-LION v4",
    "qwq_plus": "QwQ Plus",
}


def load_all_model_stats() -> list[dict]:
    """Load WASR, strict ASR, and score distribution for all models."""
    models = []
    for f in sorted(CSV_DIR.glob("*.csv")):
        key = f.stem
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                rows = list(csv.DictReader(fh))
            if not rows:
                continue
            scores = [float(r["score"]) for r in rows if r.get("score") not in ("", None)]
            if not scores:
                continue
            n = len(scores)
            n1 = sum(1 for s in scores if s == 1.0)
            n05 = sum(1 for s in scores if s == 0.5)
            n0 = sum(1 for s in scores if s == 0.0)
            wasr = (n1 + 0.5 * n05) / n * 100
            strict = n1 / n * 100
            lenient = (n1 + n05) / n * 100
            models.append({
                "key": key,
                "display": MODEL_DISPLAY_NAMES.get(key, key),
                "n": n,
                "wasr": round(wasr, 2),
                "strict_asr": round(strict, 2),
                "lenient_asr": round(lenient, 2),
                "n_breach": n1,
                "n_partial": n05,
                "n_resist": n0,
            })
        except Exception as e:
            print(f"WARN: Could not load {f.name}: {e}")
    return sorted(models, key=lambda m: m["wasr"])


def generate_ranking_csv(models: list[dict]) -> Path:
    """Export model ranking table as CSV for paper."""
    out = FIGURES_DIR / "model_ranking.csv"
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rank", "model", "wasr", "strict_asr",
                                          "lenient_asr", "n_breach", "n_partial", "n_resist", "n_total"])
        w.writeheader()
        for i, m in enumerate(models, 1):
            w.writerow({
                "rank": i,
                "model": m["display"],
                "wasr": m["wasr"],
                "strict_asr": m["strict_asr"],
                "lenient_asr": m["lenient_asr"],
                "n_breach": m["n_breach"],
                "n_partial": m["n_partial"],
                "n_resist": m["n_resist"],
                "n_total": m["n"],
            })
    return out


def generate_reasoning_delta_csv(models: list[dict]) -> Path:
    """Export reasoning vs non-reasoning delta table."""
    model_map = {m["key"]: m for m in models}
    pairs = [
        ("deepseek_r1", "deepseek_v4_pro", "DeepSeek"),
        ("qwen3_30b_thinking", "qwen3_30b_instruct", "Qwen 30B"),
        ("qwq32b", "qwen36_27b", "QwQ/Qwen36"),
        ("cohere_command_a_reasoning", "cohere_command_a_plus", "Cohere Cmd-A"),
        ("grok41fast_reasoning", "grok41fast_nonreasoning", "Grok 4.1"),
        ("grok420_reasoning", "grok420_nonreasoning", "Grok 4.20"),
    ]
    out = FIGURES_DIR / "reasoning_deltas.csv"
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["lab", "reasoning_model", "nonreasoning_model",
                                          "reasoning_wasr", "nonreasoning_wasr", "delta_pp"])
        w.writeheader()
        for r_key, nr_key, lab in pairs:
            r = model_map.get(r_key)
            nr = model_map.get(nr_key)
            if r and nr:
                delta = r["wasr"] - nr["wasr"]
                w.writerow({
                    "lab": lab,
                    "reasoning_model": r["display"],
                    "nonreasoning_model": nr["display"],
                    "reasoning_wasr": r["wasr"],
                    "nonreasoning_wasr": nr["wasr"],
                    "delta_pp": round(delta, 2),
                })
    return out


def generate_summary_json(models: list[dict]) -> Path:
    """Write master summary JSON for paper stats."""
    out = FIGURES_DIR / "summary_stats.json"
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    valid = [m for m in models if m["n"] >= 100]
    n_models = len(valid)
    total_rows = sum(m["n"] for m in valid)
    mean_wasr = sum(m["wasr"] for m in valid) / n_models if n_models else 0
    most_resistant = valid[0] if valid else {}
    most_vulnerable = valid[-1] if valid else {}

    summary = {
        "n_models_evaluated": n_models,
        "total_eval_rows": total_rows,
        "mean_wasr_pct": round(mean_wasr, 2),
        "most_resistant": {
            "model": most_resistant.get("display", ""),
            "wasr": most_resistant.get("wasr", 0),
        },
        "most_vulnerable": {
            "model": most_vulnerable.get("display", ""),
            "wasr": most_vulnerable.get("wasr", 0),
        },
        "n_models_below_20pct_wasr": sum(1 for m in valid if m["wasr"] < 20),
        "n_models_above_50pct_wasr": sum(1 for m in valid if m["wasr"] >= 50),
        "total_05_rows": sum(m["n_partial"] for m in valid),
        "pct_05_rows": round(sum(m["n_partial"] for m in valid) / total_rows * 100, 1) if total_rows else 0,
    }

    with open(out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return out


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Generate IPIBench paper figures")
    parser.add_argument("--figure", type=int, help="Generate specific figure number")
    parser.add_argument("--all", action="store_true", help="Generate all figures")
    args = parser.parse_args()

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading model stats...")
    models = load_all_model_stats()
    valid = [m for m in models if m["n"] >= 100]
    print(f"Loaded {len(valid)} models with >= 100 rows")

    ranking_path = generate_ranking_csv(valid)
    print(f"Figure 1 (ranking table): {ranking_path}")

    delta_path = generate_reasoning_delta_csv(valid)
    print(f"Figure 2 (reasoning deltas): {delta_path}")

    summary_path = generate_summary_json(valid)
    print(f"Summary stats: {summary_path}")

    # Print key stats
    with open(summary_path) as f:
        s = json.load(f)
    print(f"\nKey stats:")
    print(f"  Models: {s['n_models_evaluated']} evaluated ({s['total_eval_rows']} total rows)")
    print(f"  Mean WASR: {s['mean_wasr_pct']}%")
    print(f"  Most resistant: {s['most_resistant']['model']} ({s['most_resistant']['wasr']}%)")
    print(f"  Most vulnerable: {s['most_vulnerable']['model']} ({s['most_vulnerable']['wasr']}%)")
    print(f"  Models < 20% WASR: {s['n_models_below_20pct_wasr']}")
    print(f"  Models >= 50% WASR: {s['n_models_above_50pct_wasr']}")
    print(f"  0.5 residual rows: {s['total_05_rows']} ({s['pct_05_rows']}%)")
    print(f"\nAll outputs saved to {FIGURES_DIR}/")


if __name__ == "__main__":
    main()
