# IPIBench Automated Analysis: qwen3_coder_480b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **46.0%** | 0.0pp |
| input_filter | **45.0%** | -1.0pp |
| prompt_warning | **44.0%** | -2.0pp |
| spotlighting | **54.0%** | +8.0pp |

## 2. Reads From The Data

- **Input_filter: -1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -2.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: +8.0pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 91.7% |
| disguised | 65.0% |
| fake_metadata | 62.5% |
| direct | 37.3% |
| split | 0.0% |
