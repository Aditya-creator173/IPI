import os
import csv
import pandas as pd

v1_ids = {"A001", "A008", "A021", "A027", "A033", "A035", "B005", "B008", "B010", "B012", "B013", "B035", "C007", "C009", "C010", "C012", "C021", "C025", "C027", "C030"}

def main():
    report = ["# IPIBench Execution & Analysis Report\n"]
    
    # 1. Completion Status
    report.append("## Provider & Model Completion Status (400 cases max)\n")
    csv_dir = 'results/csv'
    
    models = []
    for f in os.listdir(csv_dir):
        if not f.endswith('.csv') or f.endswith('.bak'): continue
        path = os.path.join(csv_dir, f)
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)
            row_count = sum(1 for _ in reader)
            models.append((f.replace('.csv', ''), row_count))
            
    models.sort(key=lambda x: x[1], reverse=True)
    report.append("| Model | Completed Rows | Progress |")
    report.append("|---|---|---|")
    for name, count in models:
        pct = (count / 400.0) * 100
        report.append(f"| {name} | {count} / 400 | {pct:.1f}% |")
        
    # 2. LLaMA 8B vs GPT-OSS 120B Analysis
    report.append("\n## Head-to-Head: LLaMA 3.1 8B vs GPT-OSS 120B\n")
    
    try:
        df_llama = pd.read_csv('results/csv/llama3.1_8b.csv')
        df_gpt = pd.read_csv('results/csv/gpt_oss_120b.csv')
        
        llama_fail = df_llama['attack_succeeded'].mean() * 100
        gpt_fail = df_gpt['attack_succeeded'].mean() * 100
        
        report.append(f"**Overall Prompt Injection Susceptibility (Attack Success Rate):**")
        report.append(f"- **LLaMA 3.1 8B:** {llama_fail:.1f}%")
        report.append(f"- **GPT-OSS 120B:** {gpt_fail:.1f}%\n")
        
        report.append("### The 'V1 20' Strongest Attacks Analysis\n")
        report.append("These 20 test IDs were manually curated as the most potent injection vectors. Here is how both models performed against them:\n")
        
        v1_llama = df_llama[df_llama['test_id'].isin(v1_ids)]
        v1_gpt = df_gpt[df_gpt['test_id'].isin(v1_ids)]
        
        report.append(f"- **LLaMA 3.1 8B V1 Attack Success Rate:** {v1_llama['attack_succeeded'].mean() * 100:.1f}%")
        report.append(f"- **GPT-OSS 120B V1 Attack Success Rate:** {v1_gpt['attack_succeeded'].mean() * 100:.1f}%\n")
        
        report.append("#### Notable Failures on V1 Strong Attacks\n")
        
        for idx, row in v1_gpt.iterrows():
            if row['attack_succeeded'] == 1:
                tid = row['test_id']
                report.append(f"**GPT-OSS 120B Failed:** `{tid}` ({row['defense_mode']})")
                report.append(f"> {str(row['response_received'])[:300]}...\n")
                
        for idx, row in v1_llama.iterrows():
            if row['attack_succeeded'] == 1:
                tid = row['test_id']
                report.append(f"**LLaMA 3.1 8B Failed:** `{tid}` ({row['defense_mode']})")
                report.append(f"> {str(row['response_received'])[:300]}...\n")
                
    except Exception as e:
        report.append(f"Error generating analysis: {e}")
        
    out_path = r"C:\Users\HP\.gemini\antigravity-ide\brain\8bedabb6-cbfb-4414-a179-ef4159e0009b\analysis_report.md"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
if __name__ == '__main__':
    main()
