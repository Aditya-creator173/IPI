# IPIBench Automated Analysis: gemini35_flash

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **24.0%** | 0.0pp |
| input_filter | **20.0%** | -4.0pp |
| prompt_warning | **7.0%** | -17.0pp |
| spotlighting | **5.0%** | -19.0pp |

## 2. Reads From The Data

- **Input_filter: -4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -17.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -19.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 25.0% |
| direct | 19.1% |
| fake_metadata | 6.2% |
| disguised | 1.7% |
| split | 0.0% |
