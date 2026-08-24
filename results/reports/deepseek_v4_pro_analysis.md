# IPIBench Automated Analysis: deepseek_v4_pro

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **55.0%** | 0.0pp |
| input_filter | **55.0%** | 0.0pp |
| prompt_warning | **57.0%** | +2.0pp |
| spotlighting | **55.0%** | 0.0pp |

## 2. Reads From The Data

- **Input_filter: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 95.8% |
| fake_metadata | 70.3% |
| disguised | 70.0% |
| direct | 47.5% |
| split | 0.0% |
