# IPIBench Automated Analysis: qwen36_27b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **40.0%** | 0.0pp |
| input_filter | **43.0%** | +3.0pp |
| prompt_warning | **18.0%** | -22.0pp |
| spotlighting | **8.0%** | -32.0pp |

## 2. Reads From The Data

- **Input_filter: +3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -22.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -32.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 45.8% |
| direct | 30.1% |
| disguised | 26.7% |
| fake_metadata | 17.2% |
| split | 0.0% |
