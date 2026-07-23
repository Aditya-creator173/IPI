# IPIBench Automated Analysis: groq_compound

**Dataset:** 311 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **33.8%** | 0.0pp |
| input_filter | **32.6%** | -1.2pp |
| prompt_warning | **20.0%** | -13.8pp |
| spotlighting | **8.4%** | -25.3pp |

## 2. Reads From The Data

- **Input_filter: -1.2pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -13.8pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 
- **Spotlighting: -25.3pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 59.1% |
| fake_metadata | 38.0% |
| disguised | 31.1% |
| direct | 14.8% |
| split | 0.0% |
