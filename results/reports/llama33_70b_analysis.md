# IPIBench Automated Analysis: llama33_70b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **56.0%** | 0.0pp |
| input_filter | **53.0%** | -3.0pp |
| prompt_warning | **60.0%** | +4.0pp |
| spotlighting | **54.0%** | -2.0pp |

## 2. Reads From The Data

- **Input_filter: -3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 95.8% |
| disguised | 75.0% |
| fake_metadata | 53.1% |
| direct | 51.3% |
| split | 0.0% |
