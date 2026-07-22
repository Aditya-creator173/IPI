# IPIBench Automated Analysis: gpt_oss_120b

**Dataset:** 292 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **33.0%** | 0.0pp |
| prompt_warning | **22.0%** | -11.0pp |
| spotlighting | **4.3%** | -28.7pp |

## 2. Reads From The Data

- **Prompt_warning: -11.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -28.7pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 52.9% |
| fake_metadata | 42.2% |
| disguised | 26.7% |
| direct | 10.9% |
| split | 0.0% |
