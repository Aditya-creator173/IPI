# IPIBench: A Cross-Model and Cross-Architecture Indirect Prompt Injection Benchmark

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

## Abstract
IPIBench is a systematic empirical framework for evaluating Indirect Prompt Injection vulnerabilities across frontier Large Language Models. The benchmark evaluates 28 models against 100 distinct attack scenarios and 4 structural defense configurations, tracking 14 quantitative execution metrics and 8 taxonomic dimensions per evaluation. 

## 1. Introduction
When a language model retrieves external content like web pages or user documents, an attacker can embed adversarial instructions within that content. Current autoregressive architectures lack native mechanisms to decouple data intended for processing from instructions intended for execution. This causes the model to treat injected text as command tokens. 

This attack vector allows for scalable and privileged exploitation. A single compromised external source can execute payloads across any model that retrieves it. It can potentially co-opt tool use for unauthorized data exfiltration or state modification. 

## 2. Benchmark Design and Taxonomy
The dataset comprises 100 scenarios. Each scenario is classified across 8 analytical dimensions to facilitate granular vulnerability mapping. 

These dimensions capture the delivery context (webpage, file, tool output), the attack objective (from task hijacking to identity corruption), and the specific obfuscation technique used. They also track placement, impersonated authority, the target action type, linguistic register, and overall harm severity. A boolean persistence flag denotes whether a payload is engineered to corrupt subsequent turns or modify future session states.

## 3. Defense Configurations
Each attack scenario is evaluated against four structural defense modes. The baseline processes the prompt without modification. The prompt warning adds a system instruction explicitly ordering the model to treat external content as untrusted data. Spotlighting wraps external data in structural XML delimiters combined with system directives instructing the model to ignore command tokens within the tags. Finally, the input filter uses a pre-processing layer to replace common injection triggers with a filtered string before inference.

## 4. Experimental Setup
To ensure evaluation reliability and provenance, inference is restricted to verified enterprise API channels (such as AWS Bedrock, GitHub Models, and NVIDIA NIM). Unofficial endpoints and third-party resellers are excluded.

The evaluation cohort includes 28 models. It features four controlled pairs designed to isolate specific architectural and alignment variables. These isolate the effect of deliberate safety removal (LLaMA 3.1 405B vs. Nous Hermes 3 405B), the impact of visible chain-of-thought traces on security (DeepSeek R1 vs. DeepSeek V4 Pro), the transition from dense to mixture-of-experts (Gemma 4 31B Dense vs. Gemma 4 26B MoE), and capability enhancements across consecutive model releases (GLM 5.1 vs. GLM 5.2).

The execution architecture processes these evaluations through a custom pipeline that tracks 14 execution metrics per run. These include latency, token consumption, semantic similarity scores computed via sentence-transformers, and quantitative compliance flags.

## 5. Empirical Observations
Analysis of the evaluation data revealed several consistent alignment limitations across the frontier cohort.

In reasoning models, the exposed chain-of-thought frequently demonstrates that the model comprehends it is reading an adversarial injection. The model explicitly documents the security risk but proceeds to execute the malicious commands regardless. This indicates that introspection does not equate to steering control.

Models that successfully reject impersonated prompts from third parties will often comply when the payload claims to be a directive from the model's parent operations team. Furthermore, translating an injection payload into low-resource languages often bypasses safety guardrails on models that successfully blocked the English equivalent.

Injected instructions can also modify future session behavior without outputting anomalous strings during the current turn. This significantly complicates detection in multi-turn environments. During edge-case probing, models even affirmed unverified prompt configurations attributed to non-existent internal versions under user confidence pressure, demonstrating measurable sycophantic alignment drift.

## 6. Reproducibility and Execution

Dependency Installation:
```bash
pip install -r requirements.txt
```

Environment Configuration:
```bash
cp .env.example .env
```
Edit the `.env` file to insert your API keys.

Schema Validation:
```bash
python migrate_benchmark.py
```

Evaluation Execution:
```bash
python benchmark_scripts/run_gpt5.py --dry-run
python benchmark_scripts/run_gpt5.py --v1-only
python benchmark_scripts/run_gpt5.py
```

Result Compilation:
```bash
python merge_results.py
```

Automated Security Protocol:
The repository utilizes a strict pre-commit hook to prevent credential leakage. Running `git commit` automatically scans the filesystem and staged diffs for API keys, unencrypted result files, and forbidden paths.

## 7. Contributors
Aditya L (SRMIST)

## 8. Citation
```bibtex
@misc{ipibench2026,
  title   = {IPIBench: A Cross-Model and Cross-Architecture Benchmark for Indirect Prompt Injection Attacks and Defences in Large Language Models},
  author  = {Aditya L},
  year    = {2026},
  note    = {arXiv preprint in preparation},
  url     = {https://github.com/Aditya-creator173/IPI}
}
```
