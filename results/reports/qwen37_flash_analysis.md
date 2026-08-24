# IPIBench Automated Analysis: qwen37_flash

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **47.0%** | 0.0pp |
| input_filter | **45.0%** | -2.0pp |
| prompt_warning | **23.0%** | -24.0pp |
| spotlighting | **34.0%** | -13.0pp |

## 2. Reads From The Data

- **Input_filter: -2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -24.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -13.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 75.0% |
| fake_metadata | 43.8% |
| disguised | 40.0% |
| direct | 33.5% |
| split | 0.0% |
