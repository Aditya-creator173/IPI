# IPIBench Automated Analysis: gemma4_26b_moe

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **22.0%** | 0.0pp |
| input_filter | **23.0%** | +1.0pp |
| prompt_warning | **10.0%** | -12.0pp |
| spotlighting | **3.0%** | -19.0pp |

## 2. Reads From The Data

- **Input_filter: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -12.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -19.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 41.7% |
| direct | 18.6% |
| fake_metadata | 6.2% |
| disguised | 0.0% |
| split | 0.0% |
