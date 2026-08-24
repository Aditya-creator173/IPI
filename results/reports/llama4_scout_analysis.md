# IPIBench Automated Analysis: llama4_scout

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **50.0%** | 0.0pp |
| input_filter | **51.0%** | +1.0pp |
| prompt_warning | **51.0%** | +1.0pp |
| spotlighting | **52.0%** | +2.0pp |

## 2. Reads From The Data

- **Input_filter: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: +2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 95.8% |
| disguised | 68.3% |
| direct | 47.9% |
| fake_metadata | 42.2% |
| split | 0.0% |
