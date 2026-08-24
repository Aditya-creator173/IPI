# IPIBench Automated Analysis: qwen3_30b_moe

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **59.0%** | 0.0pp |
| input_filter | **53.0%** | -6.0pp |
| prompt_warning | **50.0%** | -9.0pp |
| spotlighting | **37.0%** | -22.0pp |

## 2. Reads From The Data

- **Input_filter: -6.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -9.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -22.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 87.5% |
| disguised | 60.0% |
| fake_metadata | 59.4% |
| direct | 44.1% |
| split | 0.0% |
