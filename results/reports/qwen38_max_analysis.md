# IPIBench Automated Analysis: qwen38_max

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **37.0%** | 0.0pp |
| input_filter | **32.0%** | -5.0pp |
| prompt_warning | **24.0%** | -13.0pp |
| spotlighting | **19.0%** | -18.0pp |

## 2. Reads From The Data

- **Input_filter: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -13.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -18.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| direct | 36.0% |
| foreign_language | 29.2% |
| fake_metadata | 17.2% |
| disguised | 15.0% |
| split | 0.0% |
