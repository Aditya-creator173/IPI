# IPIBench Automated Analysis: gpt55

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **14.0%** | 0.0pp |
| input_filter | **15.0%** | +1.0pp |
| prompt_warning | **9.0%** | -5.0pp |
| spotlighting | **9.0%** | -5.0pp |

## 2. Reads From The Data

- **Input_filter: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| fake_metadata | 15.6% |
| direct | 14.4% |
| disguised | 5.0% |
| split | 0.0% |
| foreign_language | 0.0% |
