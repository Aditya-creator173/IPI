# IPIBench Automated Analysis: poolside_laguna_m1

**Dataset:** 399 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **36.0%** | 0.0pp |
| input_filter | **37.4%** | +1.4pp |
| prompt_warning | **21.0%** | -15.0pp |
| spotlighting | **29.0%** | -7.0pp |

## 2. Reads From The Data

- **Input_filter: +1.4pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -15.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -7.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 79.2% |
| fake_metadata | 40.6% |
| disguised | 37.3% |
| direct | 23.7% |
| split | 0.0% |
