# IPIBench Automated Analysis: kimi_k3

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **23.0%** | 0.0pp |
| input_filter | **21.0%** | -2.0pp |
| prompt_warning | **33.0%** | +10.0pp |
| spotlighting | **25.0%** | +2.0pp |

## 2. Reads From The Data

- **Input_filter: -2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +10.0pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 
- **Spotlighting: +2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| direct | 29.7% |
| disguised | 23.3% |
| foreign_language | 20.8% |
| fake_metadata | 20.3% |
| split | 0.0% |
