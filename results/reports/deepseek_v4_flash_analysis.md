# IPIBench Automated Analysis: deepseek_v4_flash

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **53.0%** | 0.0pp |
| input_filter | **43.0%** | -10.0pp |
| prompt_warning | **31.0%** | -22.0pp |
| spotlighting | **13.0%** | -40.0pp |

## 2. Reads From The Data

- **Input_filter: -10.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -22.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -40.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 58.3% |
| fake_metadata | 48.4% |
| direct | 32.2% |
| disguised | 31.7% |
| split | 0.0% |
