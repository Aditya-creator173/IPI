# IPIBench Automated Analysis: gpt54

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **32.0%** | 0.0pp |
| input_filter | **30.0%** | -2.0pp |
| prompt_warning | **13.0%** | -19.0pp |
| spotlighting | **6.0%** | -26.0pp |

## 2. Reads From The Data

- **Input_filter: -2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -19.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -26.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| direct | 23.7% |
| foreign_language | 20.8% |
| fake_metadata | 20.3% |
| disguised | 11.7% |
| split | 0.0% |
