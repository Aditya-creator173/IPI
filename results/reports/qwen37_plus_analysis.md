# IPIBench Automated Analysis: qwen37_plus

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **43.0%** | 0.0pp |
| input_filter | **44.0%** | +1.0pp |
| prompt_warning | **13.0%** | -30.0pp |
| spotlighting | **8.0%** | -35.0pp |

## 2. Reads From The Data

- **Input_filter: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -30.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -35.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 45.8% |
| direct | 29.7% |
| fake_metadata | 21.9% |
| disguised | 21.7% |
| split | 0.0% |
