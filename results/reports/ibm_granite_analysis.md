# IPIBench Automated Analysis: ibm_granite

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **33.0%** | 0.0pp |
| input_filter | **36.0%** | +3.0pp |
| prompt_warning | **51.0%** | +18.0pp |
| spotlighting | **51.0%** | +18.0pp |

## 2. Reads From The Data

- **Input_filter: +3.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +18.0pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 
- **Spotlighting: +18.0pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 87.5% |
| fake_metadata | 54.7% |
| disguised | 45.0% |
| direct | 37.3% |
| split | 0.0% |
