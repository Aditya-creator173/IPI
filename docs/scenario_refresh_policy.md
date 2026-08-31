# IPIBench Scenario Refresh Policy

> **Document version:** 1.0  
> **Created:** 2026-08-31  
> **Applies to:** IPIBench v1.0+

This document defines the policies for scenario versioning, contamination detection,
scenario retirement, drift tracking, and release cadence for the IPIBench benchmark.

---

## 1. Versioning

IPIBench uses semantic versioning scoped to scenario-set changes:

| Version type | When used | Example |
|---|---|---|
| **Major (v2.0)** | Full scenario replacement or schema breaking change | New 100-scenario cohort |
| **Minor (v1.1, v1.2)** | Individual scenario swaps due to contamination or quality issues | 3 scenarios retired, 3 replacements validated |
| **Patch (v1.0.1)** | Metadata-only or tooling fixes with no scenario content change | canary_guid backfill, split re-stratification |

Scenario content (injected_text, full_prompt, attack_success_phrases) is considered
**frozen** from the moment of a major or minor release. No in-place edits to live
scenario content after release.

---

## 2. Canary Architecture

### 2.1 Canary Format

Each scenario carries a unique 128-bit UUID canary in two locations:

1. **`canary_guid` field (metadata):** The raw UUID string. Used by detection tooling.
2. **`injected_text` (embedded):** Formatted as `[CANARY:ipibench-v1-<guid>]`, appended
   after the injected instruction. A model that fully complies with the injection will
   reproduce the canary string verbatim in its output.

The canary is **semantically inert** — it does not alter the attack's meaning, effectiveness,
or correct defense behavior. It is a trailing opaque marker.

### 2.2 Canary Uniqueness

Canaries are **unique per scenario**, not per dataset version. This means:
- The same scenario carries the same canary across v1.0, v1.0.1, v1.1 (unless retired).
- A retired scenario's canary is never reused.

### 2.3 Detection Tool

`scripts/canary_check.py` is the authoritative contamination detection tool.

```bash
# Screen a new model's response CSV before scoring
python scripts/canary_check.py --csv results/csv/<new_model>.csv

# Full audit across all CSVs
python scripts/canary_check.py --all

# Screen a single response string
python scripts/canary_check.py --text "...model response text..."
```

A canary hit means the model reproduced the exact `[CANARY:ipibench-v1-<guid>]` string
in its output **without that string appearing in the user-visible prompt**. This is a
strong signal of training data memorization.

---

## 3. Contamination Detection

### 3.1 Screening Schedule

- **New frontier model release:** Screen the model's CSV output with `canary_check.py`
  within **2 weeks** of public release, before reporting its IPI-R score.
- **Monthly audit:** Run `python scripts/canary_check.py --all` against all finished CSVs
  on the first Monday of each month.
- **Incident response:** If a canary string is detected in any public training corpus
  crawl or open-source dataset, immediately run a full audit and flag the affected scenario.

### 3.2 Interpreting a Canary Hit

A canary hit in a model response requires investigation:

| Finding | Interpretation | Action |
|---|---|---|
| Canary in response **and** model was prompted with that scenario | Model complied with the injection (expected for high-ASR models). Not contamination. | No action. |
| Canary in response **but** model was NOT prompted with that scenario | Strong contamination signal. | Flag immediately, begin retirement process. |
| Canary appears as a substring of a longer token/word (false positive) | Regex artifact. | Inspect manually; if spurious, document and dismiss. |

---

## 4. Scenario Retirement

A scenario is **retired** when:
1. Its canary is detected in any public training corpus or model output without direct exposure, **OR**
2. Its ASR drops >10 percentage points across 3 consecutive frontier-model generations
   (drift signal indicating memorized refusal patterns), **OR**
3. A quality issue is discovered that makes the scenario unfit for fair evaluation.

### 4.1 Retirement Process

1. Flag the scenario in `split_assignment.json` (private): set `"status": "retired"`.
2. Exclude the scenario from leaderboard scoring in the **next release**.
3. Historical scores on the retired scenario remain in the archive but are marked
   `"retired_scenario": true` in their metadata.
4. A replacement scenario is authored targeting the **same attack_goal and evasion_style**
   as the retired scenario, with a fresh canary_guid.
5. The replacement is validated against the existing model cohort (≥3 models) before release.
6. The minor version is bumped on release containing the replacement.

---

## 5. Drift Tracking

Per-scenario Attack Success Rate (ASR) is tracked across model cohorts to detect:

- **Memorization drift:** Scenario ASR drops monotonically as newer models are tested.
  Threshold: >10pp drop over 3 consecutive frontier-generation releases.
- **Distribution shift:** Scenario ASR increases unexpectedly (new attack variant going viral
  in training data).

### 5.1 Drift Reporting

The `model_eval.md` session log records per-generation ASR summaries. Drift flags are
added to the scenario's metadata in `split_assignment.json` as:

```json
{
  "scenario_id": "A015",
  "drift_flag": true,
  "drift_note": "ASR dropped 12pp across GPT-5→5.4→5.5 generations. Retirement candidate.",
  "drift_first_flagged": "2026-09-01"
}
```

---

## 6. Release Cadence

| Activity | Target cadence |
|---|---|
| New frontier model IPI-R score | Within **2 weeks** of public API availability |
| Contamination audit (canary_check --all) | **Monthly** (first Monday) |
| Scenario review (quality + drift audit) | **Annually** (minimum) |
| Minor version release (scenario swaps) | **As needed**, triggered by retirement events |
| Major version release (full cohort replacement) | **Every 2 years** or when >20% of scenarios are retired |

---

## 7. Deprecation Policy

When a canary string appears in a publicly crawled training corpus or model output
without prompt exposure:

1. The affected scenario is **immediately flagged** in `split_assignment.json`.
2. The scenario is **excluded from leaderboard scoring** in the next release.
3. Historical scores are marked `"retired_scenario": true` in the result archive.
4. A validated replacement is authored and released in the next **minor version**.
5. The paper's leaderboard page notes: *"Scenario <ID> retired in v<X.Y> due to
   contamination detection. Historical scores preserved in archive."*

---

## 8. Held-Out Split Governance

The 20 held-out scenarios (`"split": "held_out"` in `benchmark.json`) are governed by
additional restrictions:

- **Not published** in the public GitHub repository or paper appendix.
- Used **exclusively** for leaderboard scoring and contamination-resistant evaluation.
- The private `split_assignment.json` file (gitignored) is the authoritative record
  of held-out scenario assignments.
- Held-out scenarios are subject to the same retirement and replacement process as
  public scenarios.

If a held-out scenario is contaminated, it is retired and replaced **without public
announcement** (to preserve the integrity of the held-out set).

---

## 9. Stratification Requirements for Held-Out Set

The 20 held-out scenarios must maintain coverage across:

| Dimension | Requirement |
|---|---|
| Content categories | All 3 (webpage, file, tool_output) represented |
| Attack goals | All 5 represented (task_hijacking, information_exfiltration, identity_corruption, unauthorized_action, privilege_escalation) |
| Evasion styles | ≥3 of 5 styles represented |
| Thin cells | `identity_corruption` (5 total scenarios) must have ≥1 held-out |

When replacing retired held-out scenarios, stratification must be re-verified and
documented in `split_assignment.json`.

---

*This document is part of the IPIBench methodology. Cite as: IPIBench v1.0 Scenario Refresh Policy (2026).*
