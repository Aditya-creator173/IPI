# IPIBench Automated Analysis: qwen37_max

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **35.0%** | 0.0pp |
| input_filter | **32.0%** | -3.0pp |
| prompt_warning | **11.0%** | -24.0pp |
| spotlighting | **7.0%** | -28.0pp |

## 2. Reads From The Data

- **Input_filter: -3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -24.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -28.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 41.7% |
| direct | 24.6% |
| fake_metadata | 14.1% |
| disguised | 13.3% |
| split | 0.0% |
