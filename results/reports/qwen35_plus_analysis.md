# IPIBench Automated Analysis: qwen35_plus

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **37.0%** | 0.0pp |
| input_filter | **37.0%** | 0.0pp |
| prompt_warning | **16.0%** | -21.0pp |
| spotlighting | **9.0%** | -28.0pp |

## 2. Reads From The Data

- **Input_filter: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -21.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -28.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 45.8% |
| fake_metadata | 26.6% |
| direct | 26.3% |
| disguised | 15.0% |
| split | 0.0% |
