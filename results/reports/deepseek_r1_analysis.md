# IPIBench Automated Analysis: deepseek_r1

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **51.0%** | 0.0pp |
| input_filter | **46.0%** | -5.0pp |
| prompt_warning | **34.0%** | -17.0pp |
| spotlighting | **29.0%** | -22.0pp |

## 2. Reads From The Data

- **Input_filter: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -17.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -22.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 62.5% |
| fake_metadata | 48.4% |
| direct | 39.8% |
| disguised | 33.3% |
| split | 0.0% |
