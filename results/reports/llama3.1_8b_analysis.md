# IPIBench Automated Analysis: llama3.1_8b

**Dataset:** 400 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **50.0%** | 0.0pp |
| False | **23172.6%** | +23122.6pp |
| True | **23544.1%** | +23494.1pp |
| input_filter | **50.0%** | 0.0pp |
| prompt_warning | **60.0%** | +10.0pp |
| spotlighting | **20.0%** | -30.0pp |

## 2. Reads From The Data

- **False: +23122.6pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 
- **True: +23494.1pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 
- **Input_filter: +0.0pp** 
  - *Negligible effect. This defense did not significantly alter the model's vulnerability profile.* 
- **Prompt_warning: +10.0pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 
- **Spotlighting: -30.0pp** 
  - *Strong defensive effect detected. Model effectively utilized this safeguard to block injections.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| split | 25706.2% |
| disguised | 23138.3% |
| foreign_language | 20920.8% |
| fake_metadata | 20707.8% |
| direct | 15964.0% |
