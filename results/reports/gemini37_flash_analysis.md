# IPIBench Automated Analysis: gemini37_flash

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **7.0%** | 0.0pp |
| input_filter | **7.0%** | 0.0pp |
| prompt_warning | **9.0%** | +2.0pp |
| spotlighting | **3.0%** | -4.0pp |

## 2. Reads From The Data

- **Input_filter: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| direct | 10.2% |
| disguised | 3.3% |
| split | 0.0% |
| foreign_language | 0.0% |
| fake_metadata | 0.0% |
