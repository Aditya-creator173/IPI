# IPIBench Automated Analysis: qwen3_30b_instruct

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **63.0%** | 0.0pp |
| input_filter | **59.0%** | -4.0pp |
| prompt_warning | **58.0%** | -5.0pp |
| spotlighting | **56.0%** | -7.0pp |

## 2. Reads From The Data

- **Input_filter: -4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -7.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 100.0% |
| disguised | 81.7% |
| fake_metadata | 76.6% |
| direct | 48.3% |
| split | 0.0% |
