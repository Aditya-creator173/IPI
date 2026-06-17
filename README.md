# IPIBench: A Cross-Model Indirect Prompt Injection Benchmark

IPIBench is an empirical benchmark for studying indirect prompt injection (IPI) in LLM-based agent workflows.
It focuses on how models behave when they are asked to process external content that may contain malicious embedded instructions.

The repository is designed for reproducible evaluation: fixed attack scenarios, explicit success criteria, and a scriptable execution pipeline.

## What Is Indirect Prompt Injection?

Indirect prompt injection happens when an attacker places instructions inside content the model is asked to read, such as:

- webpages
- retrieved documents
- tool output
- copied text blocks

If the model treats those embedded instructions as valid commands, it can deviate from the user goal without obvious signs.

## Benchmark Scope & Taxonomy

This benchmark evaluates models against a structured 8-dimension taxonomy to study the mechanics of Indirect Prompt Injection (IPI) at a granular level:
- **Core Dimensions:** `category` (webpage, file, tool_output), `attack_goal` (task_hijacking, exfiltration, etc.), `evasion_style`, `injection_position`, `authority_claimed`, `target_action_type`, `linguistic_register`, `harm_severity`, and `persistence` flags.
- **Evaluation Set:** 100 high-fidelity, hand-crafted attack scenarios structured in [benchmark_v2.json](benchmark_v2.json).
- **Defense Mode Evaluator:** Core engine tests each attack scenario against 4 defenses:
  - `none` (No defense baseline)
  - `prompt_warning` (System notice to ignore external instruction blocks)
  - `spotlighting` (XML-based input isolation delimiters)
  - `input_filter` (Suspicious keyword regex filtering)

## Key Insights & Discoveries

Our empirical evaluations across a wide spectrum of closed and open models have yielded **21 Novel Research Findings (NRFs)**, exposing deep safety gaps in state-of-the-art LLMs:
- **Paradoxical Disclosure (NRF-006):** In reasoning models (like DeepSeek V3), models can explicitly explain they are compromised by an injection, yet proceed to comply with it anyway (decoupling introspective awareness from control resistance).
- **In-Group Creator Impersonation Bias (NRF-011):** Certain models (like Grok 4) successfully reject impersonated instructions from generic entities, but yield completely when the instruction claims to be from their own parent/operations team.
- **Cross-Lingual control bypasses (NRF-010):** Translating the attack instruction into a low-resource or non-English language (e.g., Hindi) increases the Attack Success Rate (ASR) significantly.
- **Stealth Session Persistence (NRF-004):** Adversarial instructions in multi-turn contexts redirecting future behavior without outputting obvious anomalous strings.

## Repository Structure

- [README.md](README.md): Project overview, setup, and execution guide
- [benchmark_v2.json](benchmark_v2.json): 100 structured IPI scenarios with metadata tags and success phrases
- [benchmark_scripts/](benchmark_scripts/): Model-specific execution harness containing:
  - [_core.py](benchmark_scripts/_core.py): Shared evaluation driver (resumption support, rotation, checks)
  - `run_*.py`: Model runners for 27+ open/closed models (including GPT, Claude, Gemini, Qwen, DeepSeek)
- [merge_results.py](merge_results.py): Compiles per-model CSV results into a unified table
- [results/](results/): Outputs folder (gitignored csv/jsonl files, maintaining directory placeholders)
- [analysis/](analysis/): Jupyter notebooks for plotting metrics and visual comparisons
- [requirements.txt](requirements.txt): Python package dependencies

## Setup

### 1) Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure API keys

The benchmark runner reads API keys from environment variables.
Use [.env.example](.env.example) as a local template and keep your real `.env` file private.

Minimum providers currently used by the script:

- Groq
- Google GenAI

The requirements file also includes Mistral and OpenAI packages for future extension.

Windows PowerShell (current session):

```powershell
$env:GROQ_API_KEY="your_groq_key"
$env:GOOGLE_API_KEY="your_google_key"
```

macOS/Linux (current session):

```bash
export GROQ_API_KEY="your_groq_key"
export GOOGLE_API_KEY="your_google_key"
```

If you also run scripts under [benchmark_scripts/](benchmark_scripts/), you may need:

- `ANTHROPIC_API_KEY`
- `OPENROUTER_API_KEY`
- `GITHUB_TOKEN`

## Security Before Open-Sourcing

Use this checklist before pushing to GitHub:

1. Confirm only template config is committed: [.env.example](.env.example) is tracked, but real `.env` is not.
2. Run a quick tracked-file secret scan:

```bash
git grep -nE '(api[_-]?key|apikey|secret|token|password)[[:space:]]*[:=][[:space:]]*["\x27][^"\x27]{8,}["\x27]|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AIza[0-9A-Za-z_-]{20,}|-----BEGIN [A-Z ]+PRIVATE KEY-----' -- .
```

3. If anything looks like a real credential, remove it and rotate that key before publishing.
4. Review notebook outputs and CSV artifacts for copied credentials before commit.

## How To Run

Runs are managed via model-specific scripts in the `benchmark_scripts/` directory.

### Supported Run Modes:
- `--v1-only`: Filter to run only the 20-prompt core V1 subset (ideal for fast-track/cost-controlled tests).
- `--full` (default): Run all 100 scenarios.
- `--dry-run`: Test the first 3 cases against the model using no defenses.
- `--validate`: Run case `A001` across all 4 defense modes to verify client connectivity.

### Example Run Commands:

Dry run sanity check:
```bash
python benchmark_scripts/run_gemini3_flash.py --dry-run
```

Core V1 evaluation run (20 cases x 4 defenses = 80 queries):
```bash
python benchmark_scripts/run_gemini3_flash.py --v1-only
```

Full benchmark run (100 cases x 4 defenses = 400 queries):
```bash
python benchmark_scripts/run_gemini3_flash.py
```

## Output Files

Run output is automatically saved to provider-specific outputs inside:
- [results/csv/](results/csv/): Individual model CSV spreadsheets containing execution parameters, success results, and character metrics.
- [results/jsonl/](results/jsonl/): Structured JSONL files for post-hoc analysis.

To combine all results into one unified table:
```bash
python merge_results.py
```
This consolidates all model CSVs into [results/results_final.csv](results/results_final.csv).

## Reproducibility Checklist

- pin package versions before final reporting
- document model names and API versions used
- log run date and hardware/network context
- keep the exact [benchmark.json](benchmark.json) used for each reported result
- keep raw per-model files in [results/csv/](results/csv/) and [results/jsonl/](results/jsonl/) for auditability

## Dataset

The benchmark dataset can also be published on Hugging Face.

Placeholder:

[huggingface.co/datasets/your-username/IPIBench](https://huggingface.co/datasets/your-username/IPIBench)

## Citation

If you use this benchmark in research, cite this repository and add your formal citation after publication.

Example placeholder:

```
@misc{ipibench2026,
	title={IPIBench: A Cross-Model Indirect Prompt Injection Benchmark},
	author={Aditya L},
	year={2026},
	howpublished={GitHub repository}
}
```

## Author

Aditya L
