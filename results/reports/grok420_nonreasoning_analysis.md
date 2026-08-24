# IPIBench Automated Analysis: grok420_nonreasoning

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **50.0%** | 0.0pp |
| input_filter | **48.0%** | -2.0pp |
| prompt_warning | **53.0%** | +3.0pp |
| spotlighting | **53.0%** | +3.0pp |

## 2. Reads From The Data

- **Input_filter: -2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: +3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 100.0% |
| fake_metadata | 78.1% |
| disguised | 71.7% |
| direct | 36.9% |
| split | 0.0% |
