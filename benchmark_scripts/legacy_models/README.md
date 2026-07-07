# legacy_models/

Scripts in this directory were considered for the IPIBench automated cohort but were **deliberately excluded** through one or more explicit decisions. They are retained here to show the decision trail — that these models were evaluated and rejected, not overlooked.

> **Do not run any script in this directory in an automated benchmark loop without re-reading the decision trail in its docstring and confirming it is still valid.**

---

## Contents

| Script | Model | Reason for Exclusion | Decision Date |
|---|---|---|---|
| `run_llama4_maverick.py` | Llama 4 Maverick 17B 128E (NIM) | **Dropped three times.** Scout (16E) covers the Llama 4 MoE research question independently. Expert-count scaling pair hypothesis was never independently made — the model kept re-entering through compiled summaries without a stated justification checked against Scout's coverage. | July 7, 2026 (3rd rejection) |
| `run_mistral_medium.py` | Mistral Medium 3.5 128B (NIM) | Superseded by Mistral Large 3 (~675B) per the each-lab-flagship principle. Same European-origin research role, larger model. | July 6, 2026 (Phase 4) |
| `run_github_ds_r1.py` | DeepSeek R1-0528 (GitHub Models) | Duplicate coverage. OpenRouter free-tier version (`run_deepseek_r1.py`) is the canonical R1 script. GitHub Models version adds no isolated variable beyond provider. | July 6, 2026 |
| `run_sarvam_m.py` | Sarvam-M 8B (NIM) | Supplementary only. Indian-language native alignment is relevant if cross-lingual IPI becomes a research dimension. Not in the core automated cohort for this paper. | July 6, 2026 (Phase 4) |

---

*Note: Other retired scripts from earlier phases (`run_deepseek_r1_distill_qwen32b.py`, `run_qwen3_80b.py`, `run_mai_ds_r1.py`, `run_jamba.py`, `run_mistral_small.py`) remain in the parent `benchmark_scripts/` directory with `[RETIRED]` headers in their docstrings, as they were excluded before the `legacy_models/` folder existed. They should be considered equivalent legacy artifacts.*
