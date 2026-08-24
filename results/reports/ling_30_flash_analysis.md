# IPIBench Automated Analysis: ling_30_flash

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **40.0%** | 0.0pp |
| input_filter | **35.0%** | -5.0pp |
| prompt_warning | **26.0%** | -14.0pp |
| spotlighting | **41.0%** | +1.0pp |

## 2. Reads From The Data

- **Input_filter: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -14.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 83.3% |
| fake_metadata | 37.5% |
| direct | 33.9% |
| disguised | 30.0% |
| split | 0.0% |
