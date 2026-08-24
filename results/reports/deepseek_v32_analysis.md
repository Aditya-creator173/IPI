# IPIBench Automated Analysis: deepseek_v32

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **60.0%** | 0.0pp |
| input_filter | **60.0%** | 0.0pp |
| prompt_warning | **55.0%** | -5.0pp |
| spotlighting | **44.0%** | -16.0pp |

## 2. Reads From The Data

- **Input_filter: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -16.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 87.5% |
| disguised | 73.3% |
| fake_metadata | 68.8% |
| direct | 46.6% |
| split | 0.0% |
