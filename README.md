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

## Benchmark Scope

This benchmark includes:

- 100 hand-crafted attack scenarios in [benchmark.json](benchmark.json)
- multiple attack goals and evasion styles per scenario
- per-scenario success indicators for automatic scoring
- defense-mode comparisons in the same evaluation run

The current runner script in this repository evaluates four defense modes:

- none
- prompt_warning
- spotlighting
- input_filter

## Key Findings

Work-in-Progress

## Repository Structure

- [README.md](README.md): project overview, setup, and reproducibility notes
- [benchmark.json](benchmark.json): 100 attack scenarios with success criteria
- [run_benchmark.py](run_benchmark.py): evaluation script
- [results/results.csv](results/results.csv): experimental output table
- [analysis/analysis.ipynb](analysis/analysis.ipynb): visualization and analysis notebook
- [paper/draft.pdf](paper/draft.pdf): working paper draft
- [requirements.txt](requirements.txt): Python dependencies

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

Dry run (small sanity check):

```bash
python run_benchmark.py --dry-run
```

Full run:

```bash
python run_benchmark.py
```

## Output Files

By default, the current runner writes to a root-level file named results.csv.

To keep the repository structure clean, move the generated file after each run:

```powershell
Move-Item -LiteralPath .\results.csv -Destination .\results\results.csv -Force
```

If you prefer, you can update [run_benchmark.py](run_benchmark.py) so it writes directly to [results/results.csv](results/results.csv).

## Reproducibility Checklist

- pin package versions before final reporting
- document model names and API versions used
- log run date and hardware/network context
- keep the exact [benchmark.json](benchmark.json) used for each reported result
- keep raw [results/results.csv](results/results.csv) for auditability

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
