# IPIBench Automated Analysis: gemma4_26b_moe

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **13.0%** | 0.0pp |
| input_filter | **16.0%** | +3.0pp |
| prompt_warning | **4.0%** | -9.0pp |
| spotlighting | **2.0%** | -11.0pp |

## 2. Reads From The Data

- **Input_filter: +3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -9.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -11.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 41.7% |
| direct | 9.7% |
| fake_metadata | 3.1% |
| disguised | 0.0% |
| split | 0.0% |
