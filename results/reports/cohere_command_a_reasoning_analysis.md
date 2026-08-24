# IPIBench Automated Analysis: cohere_command_a_reasoning

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **57.0%** | 0.0pp |
| input_filter | **56.0%** | -1.0pp |
| prompt_warning | **52.0%** | -5.0pp |
| spotlighting | **42.0%** | -15.0pp |

## 2. Reads From The Data

- **Input_filter: -1.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: -5.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Spotlighting: -15.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 87.5% |
| fake_metadata | 73.4% |
| disguised | 50.0% |
| direct | 46.2% |
| split | 0.0% |
