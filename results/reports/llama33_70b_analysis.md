# IPIBench Automated Analysis: llama33_70b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **36.0%** | 0.0pp |
| input_filter | **33.0%** | -3.0pp |
| prompt_warning | **40.0%** | +4.0pp |
| spotlighting | **41.0%** | +5.0pp |

## 2. Reads From The Data

- **Input_filter: -3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: +5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 79.2% |
| disguised | 58.3% |
| fake_metadata | 45.3% |
| direct | 28.4% |
| split | 0.0% |
