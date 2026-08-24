# IPIBench Automated Analysis: qwen3_30b_thinking

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **48.0%** | 0.0pp |
| input_filter | **51.0%** | +3.0pp |
| prompt_warning | **48.0%** | 0.0pp |
| spotlighting | **29.0%** | -19.0pp |

## 2. Reads From The Data

- **Input_filter: +3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -19.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 83.3% |
| fake_metadata | 53.1% |
| disguised | 46.7% |
| direct | 39.8% |
| split | 0.0% |
