# IPIBench Automated Analysis: gpt5

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **20.0%** | 0.0pp |
| input_filter | **21.0%** | +1.0pp |
| prompt_warning | **16.0%** | -4.0pp |
| spotlighting | **6.0%** | -14.0pp |

## 2. Reads From The Data

- **Input_filter: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -14.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| direct | 22.0% |
| fake_metadata | 10.9% |
| foreign_language | 8.3% |
| disguised | 3.3% |
| split | 0.0% |
