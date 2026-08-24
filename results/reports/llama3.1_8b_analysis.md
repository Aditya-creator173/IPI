# IPIBench Automated Analysis: llama3.1_8b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **56.0%** | 0.0pp |
| input_filter | **51.0%** | -5.0pp |
| prompt_warning | **50.0%** | -6.0pp |
| spotlighting | **27.0%** | -29.0pp |

## 2. Reads From The Data

- **Input_filter: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -6.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -29.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 83.3% |
| disguised | 48.3% |
| fake_metadata | 45.3% |
| direct | 44.9% |
| split | 0.0% |
