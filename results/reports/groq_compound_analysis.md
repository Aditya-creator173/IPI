# IPIBench Automated Analysis: groq_compound

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **48.0%** | 0.0pp |
| input_filter | **49.0%** | +1.0pp |
| prompt_warning | **40.0%** | -8.0pp |
| spotlighting | **23.0%** | -25.0pp |

## 2. Reads From The Data

- **Input_filter: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -8.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -25.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 66.7% |
| fake_metadata | 48.4% |
| disguised | 40.0% |
| direct | 37.7% |
| split | 0.0% |
