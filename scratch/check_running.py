import os
import pandas as pd

models = {
    'Gemini 3.7 Flash (Google AI Studio)': 'gemini37_flash',
    'LiquidAI LFM 2.5 (OpenRouter)': 'liquid_lfm25'
}

for label, fname in models.items():
    p = os.path.join('results', 'csv', f'{fname}.csv')
    if os.path.exists(p):
        df = pd.read_csv(p)
        n = len(df)
        pct = (n / 400.0) * 100
        asr = round(df['score'].mean() * 100, 1) if 'score' in df.columns and n > 0 else 0.0
        print(f"=== {label} ===")
        print(f"Total Rows Completed : {n}/400 ({pct:.1f}%)")
        print(f"Current ASR          : {asr}%\n")
        
        if 'defense_mode' in df.columns and n > 0:
            print("Row Counts per Defense Mode:")
            for dm, cnt in df['defense_mode'].value_counts().items():
                dm_asr = round(df[df['defense_mode'] == dm]['score'].mean() * 100, 1)
                print(f"  - {dm:15}: {cnt:3}/100 rows (ASR: {dm_asr}%)")
            
            print("\nScore Distribution:")
            counts = df['score'].value_counts(normalize=True).sort_index() * 100
            for score_val, pcent in counts.items():
                print(f"  - Score {score_val:3.1f} : {pcent:5.1f}%")
        print("-" * 50)
