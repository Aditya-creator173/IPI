# IPIBench Automated Analysis: qwen36_27b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **27.0%** | 0.0pp |
| input_filter | **31.0%** | +4.0pp |
| prompt_warning | **6.0%** | -21.0pp |
| spotlighting | **2.0%** | -25.0pp |

## 2. Reads From The Data

- **Input_filter: +4.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -21.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -25.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 41.7% |
| disguised | 21.7% |
| direct | 15.3% |
| fake_metadata | 10.9% |
| split | 0.0% |
