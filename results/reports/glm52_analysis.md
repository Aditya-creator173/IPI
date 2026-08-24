# IPIBench Automated Analysis: glm52

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **36.0%** | 0.0pp |
| input_filter | **33.0%** | -3.0pp |
| prompt_warning | **15.0%** | -21.0pp |
| spotlighting | **9.0%** | -27.0pp |

## 2. Reads From The Data

- **Input_filter: -3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -21.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -27.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 37.5% |
| direct | 27.1% |
| fake_metadata | 18.8% |
| disguised | 13.3% |
| split | 0.0% |
