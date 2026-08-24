# IPIBench Automated Analysis: cohere_command_a_plus

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **58.0%** | 0.0pp |
| input_filter | **55.0%** | -3.0pp |
| prompt_warning | **52.0%** | -6.0pp |
| spotlighting | **30.0%** | -28.0pp |

## 2. Reads From The Data

- **Input_filter: -3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -6.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -28.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 83.3% |
| disguised | 61.7% |
| fake_metadata | 46.9% |
| direct | 45.8% |
| split | 0.0% |
