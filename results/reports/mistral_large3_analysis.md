# IPIBench Automated Analysis: mistral_large3

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **62.0%** | 0.0pp |
| input_filter | **61.0%** | -1.0pp |
| prompt_warning | **48.0%** | -14.0pp |
| spotlighting | **53.0%** | -9.0pp |

## 2. Reads From The Data

- **Input_filter: -1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -14.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -9.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 91.7% |
| fake_metadata | 68.8% |
| disguised | 58.3% |
| direct | 52.1% |
| split | 0.0% |
