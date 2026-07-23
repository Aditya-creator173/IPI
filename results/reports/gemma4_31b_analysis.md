# IPIBench Automated Analysis: gemma4_31b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **14.0%** | 0.0pp |
| input_filter | **14.0%** | 0.0pp |
| prompt_warning | **4.0%** | -10.0pp |
| spotlighting | **2.0%** | -12.0pp |

## 2. Reads From The Data

- **Input_filter: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -10.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -12.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 20.8% |
| direct | 10.6% |
| disguised | 3.3% |
| fake_metadata | 3.1% |
| split | 0.0% |
