# IPIBench Automated Analysis: grok420_reasoning

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **53.0%** | 0.0pp |
| input_filter | **45.0%** | -8.0pp |
| prompt_warning | **21.0%** | -32.0pp |
| spotlighting | **8.0%** | -45.0pp |

## 2. Reads From The Data

- **Input_filter: -8.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -32.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -45.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 45.8% |
| fake_metadata | 45.3% |
| disguised | 36.7% |
| direct | 27.5% |
| split | 0.0% |
