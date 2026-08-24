# IPIBench Automated Analysis: liquid_lfm25

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **44.0%** | 0.0pp |
| input_filter | **48.0%** | +4.0pp |
| prompt_warning | **35.0%** | -9.0pp |
| spotlighting | **39.0%** | -5.0pp |

## 2. Reads From The Data

- **Input_filter: +4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -9.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 70.8% |
| fake_metadata | 43.8% |
| direct | 42.4% |
| disguised | 35.0% |
| split | 0.0% |
