# IPIBench Automated Analysis: poolside_laguna_m1

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **59.0%** | 0.0pp |
| input_filter | **59.0%** | 0.0pp |
| prompt_warning | **33.0%** | -26.0pp |
| spotlighting | **42.0%** | -17.0pp |

## 2. Reads From The Data

- **Input_filter: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -26.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -17.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 79.2% |
| fake_metadata | 57.8% |
| disguised | 51.7% |
| direct | 44.9% |
| split | 0.0% |
