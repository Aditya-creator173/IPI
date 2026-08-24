# IPIBench Automated Analysis: sea_lion_v4

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **49.0%** | 0.0pp |
| input_filter | **59.0%** | +10.0pp |
| prompt_warning | **50.0%** | +1.0pp |
| spotlighting | **59.0%** | +10.0pp |

## 2. Reads From The Data

- **Input_filter: +10.0pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 
- **Prompt_warning: +1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: +10.0pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 75.0% |
| disguised | 70.0% |
| fake_metadata | 59.4% |
| direct | 50.4% |
| split | 0.0% |
