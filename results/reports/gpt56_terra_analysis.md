# IPIBench Automated Analysis: gpt56_terra

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **22.0%** | 0.0pp |
| input_filter | **16.0%** | -6.0pp |
| prompt_warning | **7.0%** | -15.0pp |
| spotlighting | **4.0%** | -18.0pp |

## 2. Reads From The Data

- **Input_filter: -6.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -15.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -18.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 20.8% |
| direct | 14.8% |
| fake_metadata | 7.8% |
| disguised | 6.7% |
| split | 0.0% |
