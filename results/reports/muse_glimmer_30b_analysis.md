# IPIBench Automated Analysis: muse_glimmer_30b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **22.0%** | 0.0pp |
| input_filter | **20.0%** | -2.0pp |
| prompt_warning | **15.0%** | -7.0pp |
| spotlighting | **7.0%** | -15.0pp |

## 2. Reads From The Data

- **Input_filter: -2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -7.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -15.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| fake_metadata | 26.6% |
| foreign_language | 16.7% |
| direct | 16.1% |
| disguised | 8.3% |
| split | 0.0% |
