import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # Set up styling
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "legend.frameon": False,
    })
    
    out_dir = r"C:\Users\HP\.gemini\antigravity-ide\brain\8bedabb6-cbfb-4414-a179-ef4159e0009b"
    
    # Load completed CSVs
    dfs = []
    for m in ['llama3.1_8b.csv', 'llama33_70b.csv', 'gpt_oss_120b.csv']:
        path = os.path.join('results', 'csv', m)
        if os.path.exists(path):
            df = pd.read_csv(path, on_bad_lines='skip')
            df['model_name'] = m.replace('.csv', '')
            dfs.append(df)
            
    if not dfs:
        print("No CSVs found")
        return
        
    df = pd.concat(dfs, ignore_index=True)
    df['attack_succeeded'] = pd.to_numeric(df['attack_succeeded'], errors='coerce') * 100
    baseline = df[df['defense_mode'] == 'none']
    
    # --- PREVIOUS CHARTS ---
    # 1. Overall Baseline
    overall = baseline.groupby('model_name')['attack_succeeded'].mean().reset_index()
    plt.figure(figsize=(8, 5))
    bars = plt.bar(overall['model_name'], overall['attack_succeeded'], color=['#67a9cf', '#ef8a62', '#b2182b'], edgecolor="black")
    plt.title('Baseline Attack Success Rate (No Defense)')
    plt.ylabel('Success Rate (%)')
    plt.ylim(0, 100)
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f"{bar.get_height():.1f}%", ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'baseline_asr.png'))
    plt.close()
    
    # 2. Defense Effectiveness
    defense_stats = df.groupby(['model_name', 'defense_mode'])['attack_succeeded'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=defense_stats, x='model_name', y='attack_succeeded', hue='defense_mode', palette='Set2', edgecolor="black")
    plt.title('Attack Success Rate by Defense Mode')
    plt.ylabel('Success Rate (%)')
    plt.ylim(0, 100)
    plt.legend(title='Defense Mode', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'defense_effectiveness.png'))
    plt.close()
    
    # 3. Evasion Style
    evasion = baseline.groupby('evasion_style')['attack_succeeded'].mean().reset_index().sort_values('attack_succeeded', ascending=False)
    plt.figure(figsize=(10, 6))
    bars = plt.barh(evasion['evasion_style'], evasion['attack_succeeded'], color=sns.color_palette("crest", len(evasion)), edgecolor="black")
    plt.title('Success Rate by Evasion Style (Baseline)')
    plt.xlabel('Success Rate (%)')
    plt.gca().invert_yaxis()
    for bar in bars:
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}%", va='center')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'evasion_styles.png'))
    plt.close()

    # --- NEW DETAILED CHARTS ---
    # 4. Heatmap of Defense vs Model
    heatmap_data = defense_stats.pivot(index='defense_mode', columns='model_name', values='attack_succeeded')
    mode_order = ['none', 'prompt_warning', 'spotlighting', 'input_filter']
    heatmap_data = heatmap_data.reindex(mode_order)
    
    plt.figure(figsize=(10, 5))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="RdYlGn_r", vmin=0, vmax=100,
                linewidths=0.5, linecolor='white', cbar_kws={'label': 'Attack Success Rate (%)'})
    plt.title("Detailed Defense Degradation Heatmap", pad=16)
    plt.ylabel("Defense Mechanism")
    plt.xlabel("Model")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'defense_heatmap.png'))
    plt.close()

    # 5. Attack Goal Breakdown (Baseline)
    goal = baseline.groupby('attack_goal')['attack_succeeded'].mean().reset_index().sort_values('attack_succeeded', ascending=False)
    plt.figure(figsize=(10, 6))
    bars = plt.barh(goal['attack_goal'], goal['attack_succeeded'], color=sns.color_palette("rocket", len(goal)), edgecolor="black")
    plt.title('Vulnerability by Attack Goal (Baseline)')
    plt.xlabel('Success Rate (%)')
    plt.gca().invert_yaxis()
    for bar in bars:
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}%", va='center')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'attack_goal.png'))
    plt.close()
    
    # 6. Benchmark Category Breakdown (Baseline)
    cat = baseline.groupby('category')['attack_succeeded'].mean().reset_index().sort_values('attack_succeeded', ascending=False)
    plt.figure(figsize=(9, 4))
    bars = plt.barh(cat['category'], cat['attack_succeeded'], color=sns.color_palette("viridis", len(cat)), edgecolor="black")
    plt.title('Vulnerability by Injection Category (Baseline)')
    plt.xlabel('Success Rate (%)')
    plt.gca().invert_yaxis()
    for bar in bars:
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}%", va='center')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'category_breakdown.png'))
    plt.close()

    print("All charts generated successfully!")

if __name__ == '__main__':
    main()
