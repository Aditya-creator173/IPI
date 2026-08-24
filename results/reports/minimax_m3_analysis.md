# IPIBench Automated Analysis: minimax_m3

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **22.0%** | 0.0pp |
| input_filter | **18.0%** | -4.0pp |
| prompt_warning | **24.0%** | +2.0pp |
| spotlighting | **24.0%** | +2.0pp |

## 2. Reads From The Data

- **Input_filter: -4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: +2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 62.5% |
| fake_metadata | 21.9% |
| direct | 20.8% |
| disguised | 16.7% |
| split | 0.0% |
