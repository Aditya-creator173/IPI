# IPIBench Automated Analysis: glm51

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **41.0%** | 0.0pp |
| input_filter | **36.0%** | -5.0pp |
| prompt_warning | **9.0%** | -32.0pp |
| spotlighting | **4.0%** | -37.0pp |

## 2. Reads From The Data

- **Input_filter: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -32.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -37.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 45.8% |
| direct | 24.2% |
| disguised | 20.0% |
| fake_metadata | 15.6% |
| split | 0.0% |
