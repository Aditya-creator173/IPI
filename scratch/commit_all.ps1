# commit_all.ps1 — Stage and commit each file individually, then push once.

# 1. Scorer rewrite
git add benchmark_scripts/scoring_v2.py
git commit -m "tri-state scorer"

# 2. Key manager dotenv
git add benchmark_scripts/_keys.py
git commit -m "dotenv key loading"

# 3. NIM provider fixes
git add benchmark_scripts/_nim.py
git commit -m "fix NIM retries"

# 4. Runner: Cohere Command A
git add benchmark_scripts/run_cohere_command_a.py
git commit -m "cohere runner update"

# 5. Runner: DeepSeek V4 Pro
git add benchmark_scripts/run_deepseek_v4_pro.py
git commit -m "deepseek runner fix"

# 6. Runner: GPT-5
git add benchmark_scripts/run_gpt5.py
git commit -m "gpt5 runner fix"

# 7. Runner: Groq Compound
git add benchmark_scripts/run_groq_compound.py
git commit -m "groq runner fix"

# 8. Runner: Kimi K2
git add benchmark_scripts/run_kimi_k2.py
git commit -m "kimi runner fix"

# 9. Runner: Phi-4
git add benchmark_scripts/run_phi4.py
git commit -m "phi4 runner fix"

# 10. Runner: Auto pipeline
git add benchmark_scripts/run_auto_pipeline.py
git commit -m "add auto pipeline"

# 11. Runner: Seed OSS 36B (retired, but script kept for reproducibility)
git add benchmark_scripts/run_seed_oss_36b.py
git commit -m "add seed runner"

# 12. Model registry update
git add model_registry.json
git commit -m "update model registry"

# 13. Paper limitations update
git add paper/limitations.tex
git commit -m "add taxonomy disclosure"

# 14. MIT License
git add LICENSE
git commit -m "add MIT license"

# 15. Remove extract.py scratch file
git add extract.py
git commit -m "remove extract script"

# 16. Reliability study script + convergence plot script
git add scripts/
git commit -m "add stats scripts"

# 17. Reliability study JSON results
git add results/reliability_study.json
git commit -m "reliability study data"

# 18. Convergence study JSON + plot
git add results/convergence_study.json results/convergence_plot.png
git commit -m "convergence study data"

# 19. Correct behavior audit
git add results/correct_behavior_audit.json
git commit -m "behavior audit data"

# Push all commits at once
git push origin main
