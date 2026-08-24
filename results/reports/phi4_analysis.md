# IPIBench Automated Analysis: phi4

**Dataset:** 97 evaluations (across 4 defense modes)

## 1. Attack Success Rate by Defense Mode (%)

| Defense Mode | ASR (%) | Delta from Baseline (pp) |
| :--- | :--- | :--- |
| No Defense | **22.6%** | 0.0pp |
| input_filter | **34.1%** | +11.4pp |

## 2. Reads From The Data

- **Input_filter: +11.4pp** 
  - *Negative effect detected. The model treated the warning as extra context confirming the injection should be processed.* 

## 3. Top Evasion Styles (Bypass Effectiveness)

| Evasion Style | ASR (%) |
| :--- | :--- |
| foreign_language | 80.0% |
| fake_metadata | 31.2% |
| direct | 26.3% |
| disguised | 20.0% |
| split | 0.0% |
