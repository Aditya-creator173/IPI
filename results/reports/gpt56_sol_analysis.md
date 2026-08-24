# IPIBench Automated Analysis: gpt56_sol

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **13.0%** | 0.0pp |
| input_filter | **16.0%** | +3.0pp |
| prompt_warning | **6.0%** | -7.0pp |
| spotlighting | **6.0%** | -7.0pp |

## 2. Reads From The Data

- **Input_filter: +3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -7.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -7.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| direct | 15.7% |
| disguised | 3.3% |
| fake_metadata | 3.1% |
| split | 0.0% |
| foreign_language | 0.0% |
