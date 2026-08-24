import os
import pandas as pd

models = {
    'Gemini 3.7 Flash (Google AI Studio)': 'gemini37_flash',
    'Qwen 3 30B Thinking (QwenCloud)': 'qwen3_30b_thinking',
    'LiquidAI LFM 2.5 (OpenRouter)': 'liquid_lfm25',
    'IBM Granite 4.0 (Cloudflare)': 'ibm_granite'
}

print(f"{'Model':40} | {'Progress':14} | {'ASR':7} | {'Status'}")
print("-" * 75)
for label, fname in models.items():
    csv_path = os.path.join('results', 'csv', f'{fname}.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        rows = len(df)
        pct = (rows / 400.0) * 100
        asr = f"{df['score'].mean()*100:.1f}%" if 'score' in df.columns and rows > 0 else "N/A"
        status = "COMPLETED" if rows >= 400 else "RUNNING"
        print(f"{label:40} | {rows:3}/400 ({pct:5.1f}%) | {asr:7} | {status}")
    else:
        print(f"{label:40} |   0/400 (  0.0%) | N/A     | PENDING / PAUSED")
