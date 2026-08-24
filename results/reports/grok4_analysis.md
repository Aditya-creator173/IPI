# IPIBench Automated Analysis: grok4

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **56.0%** | 0.0pp |
| input_filter | **52.0%** | -4.0pp |
| prompt_warning | **10.0%** | -46.0pp |
| spotlighting | **6.0%** | -50.0pp |

## 2. Reads From The Data

- **Input_filter: -4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -46.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -50.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 37.5% |
| fake_metadata | 37.5% |
| disguised | 33.3% |
| direct | 30.1% |
| split | 0.0% |
