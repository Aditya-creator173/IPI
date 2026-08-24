# IPIBench Automated Analysis: diffusiongemma

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **54.0%** | 0.0pp |
| input_filter | **56.0%** | +2.0pp |
| prompt_warning | **34.0%** | -20.0pp |
| spotlighting | **35.0%** | -19.0pp |

## 2. Reads From The Data

- **Input_filter: +2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -20.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -19.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 75.0% |
| fake_metadata | 56.2% |
| disguised | 53.3% |
| direct | 39.4% |
| split | 0.0% |
