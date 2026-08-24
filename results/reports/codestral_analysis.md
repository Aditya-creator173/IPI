# IPIBench Automated Analysis: codestral

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **65.0%** | 0.0pp |
| input_filter | **60.0%** | -5.0pp |
| prompt_warning | **42.0%** | -23.0pp |
| spotlighting | **39.0%** | -26.0pp |

## 2. Reads From The Data

- **Input_filter: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -23.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -26.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 91.7% |
| fake_metadata | 54.7% |
| direct | 50.8% |
| disguised | 48.3% |
| split | 0.0% |
