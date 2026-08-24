# IPIBench Automated Analysis: qwq32b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **32.0%** | 0.0pp |
| input_filter | **29.0%** | -3.0pp |
| prompt_warning | **24.0%** | -8.0pp |
| spotlighting | **28.0%** | -4.0pp |

## 2. Reads From The Data

- **Input_filter: -3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -8.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| disguised | 36.7% |
| fake_metadata | 31.2% |
| foreign_language | 29.2% |
| direct | 27.1% |
| split | 0.0% |
