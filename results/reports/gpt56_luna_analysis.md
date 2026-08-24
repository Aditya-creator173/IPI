# IPIBench Automated Analysis: gpt56_luna

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **21.0%** | 0.0pp |
| input_filter | **25.0%** | +4.0pp |
| prompt_warning | **13.0%** | -8.0pp |
| spotlighting | **6.0%** | -15.0pp |

## 2. Reads From The Data

- **Input_filter: +4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -8.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -15.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 25.0% |
| direct | 21.2% |
| fake_metadata | 12.5% |
| disguised | 1.7% |
| split | 0.0% |
