# IPIBench — Exhaustive Master Repository Tree & Cleanup Audit

> **Generated:** 2026-08-07 | **Total Files Audited:** 213 files across 12 directories

This document provides an exhaustive, file-by-file inventory of the entire codebase to assist reviewers and instructors in performing a clean, zero-risk repository audit.

|-- **.agents/**
|-- **.vscode/**
|   -- settings.json — *[ACTIVE FILE] Repository resource file.*
|-- **analysis/**
|   -- analysis.ipynb — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|-- **benchmark_scripts/**
|   |-- **legacy_models/**
|   |   |-- README.md — *[RESEARCH UTILITY] Plotting/analysis script (README.md).*
|   |   |-- run_liquidai_lfm.py — *[LEGACY RUNNER] Model runner in legacy_models directory (run_liquidai_lfm.py).*
|   |   |-- run_llama4_maverick.py — *[LEGACY RUNNER] Model runner in legacy_models directory (run_llama4_maverick.py).*
|   |   -- run_nous_hermes_405b.py — *[LEGACY RUNNER] Model runner in legacy_models directory (run_nous_hermes_405b.py).*
|   |-- _bedrock.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _cloudflare.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _cohere.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _core.py — *[ESSENTIAL] Core benchmark execution engine, compliance evaluator, and defense handlers.*
|   |-- _github.py — *[LEGACY HELPER] GitHub Models client wrapper for preserved Phi-4 dataset.*
|   |-- _google.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _groq.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _keys.py — *[ESSENTIAL] Shared API key manager with key rotation, unnumbered fallbacks, and provider aliases.*
|   |-- _mistral.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _nim.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _openrouter.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _qwencloud.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- _sambanova.py — *[ACTIVE HELPER] Client wrapper for provider API (key rotation, retries, usage logging).*
|   |-- do_refactor.py — *[UTILITY] Automated code generator script for model runners and provider helpers.*
|   |-- run_auto_pipeline.py — *[ESSENTIAL] Multi-provider automated pipeline orchestrator for sequential 35-model execution.*
|   |-- run_batch_2.py — *[CANDIDATE FOR CLEANUP] Legacy batch execution runner (run_batch_2.py).*
|   |-- run_batch_github.py — *[CANDIDATE FOR CLEANUP] Legacy batch execution runner (run_batch_github.py).*
|   |-- run_batch_nim.py — *[CANDIDATE FOR CLEANUP] Legacy batch execution runner (run_batch_nim.py).*
|   |-- run_batch_openrouter.py — *[CANDIDATE FOR CLEANUP] Legacy batch execution runner (run_batch_openrouter.py).*
|   |-- run_claude_haiku.py — *[ACTIVE RUNNER] Execution script for model run_claude_haiku.py.*
|   |-- run_claude_opus.py — *[ACTIVE RUNNER] Execution script for model run_claude_opus.py.*
|   |-- run_claude_sonnet.py — *[ACTIVE RUNNER] Execution script for model run_claude_sonnet.py.*
|   |-- run_codestral.py — *[ACTIVE RUNNER] Execution script for model run_codestral.py.*
|   |-- run_cohere_command_a.py — *[CANDIDATE FOR CLEANUP] Legacy model runner superseded by newer API/tier (run_cohere_command_a.py).*
|   |-- run_cohere_command_a_plus.py — *[ACTIVE RUNNER] Execution script for model run_cohere_command_a_plus.py.*
|   |-- run_cohere_command_a_reasoning.py — *[ACTIVE RUNNER] Execution script for model run_cohere_command_a_reasoning.py.*
|   |-- run_deepseek_r1.py — *[ACTIVE RUNNER] Execution script for model run_deepseek_r1.py.*
|   |-- run_deepseek_v32.py — *[ACTIVE RUNNER] Execution script for model run_deepseek_v32.py.*
|   |-- run_deepseek_v4_flash.py — *[ACTIVE RUNNER] Execution script for model run_deepseek_v4_flash.py.*
|   |-- run_deepseek_v4_pro.py — *[ACTIVE RUNNER] Execution script for model run_deepseek_v4_pro.py.*
|   |-- run_diffusiongemma.py — *[ACTIVE RUNNER] Execution script for model run_diffusiongemma.py.*
|   |-- run_gemini35_flash.py — *[ACTIVE RUNNER] Execution script for model run_gemini35_flash.py.*
|   |-- run_gemini36_flash.py — *[ACTIVE RUNNER] Execution script for model run_gemini36_flash.py.*
|   |-- run_gemma4_26b_moe.py — *[ACTIVE RUNNER] Execution script for model run_gemma4_26b_moe.py.*
|   |-- run_gemma4_31b.py — *[ACTIVE RUNNER] Execution script for model run_gemma4_31b.py.*
|   |-- run_glm51.py — *[CANDIDATE FOR CLEANUP] Legacy model runner superseded by newer API/tier (run_glm51.py).*
|   |-- run_glm52.py — *[ACTIVE RUNNER] Execution script for model run_glm52.py.*
|   |-- run_gpt5.py — *[ACTIVE RUNNER] Execution script for model run_gpt5.py.*
|   |-- run_gpt_oss_120b.py — *[ACTIVE RUNNER] Execution script for model run_gpt_oss_120b.py.*
|   |-- run_gpt_oss_20b.py — *[ACTIVE RUNNER] Execution script for model run_gpt_oss_20b.py.*
|   |-- run_grok4.py — *[ACTIVE RUNNER] Execution script for model run_grok4.py.*
|   |-- run_groq_compound.py — *[ACTIVE RUNNER] Execution script for model run_groq_compound.py.*
|   |-- run_ibm_granite.py — *[ACTIVE RUNNER] Execution script for model run_ibm_granite.py.*
|   |-- run_kimi_k2.py — *[ACTIVE RUNNER] Execution script for model run_kimi_k2.py.*
|   |-- run_ling_30_flash.py — *[ACTIVE RUNNER] Execution script for model run_ling_30_flash.py.*
|   |-- run_llama31_405b.py — *[ACTIVE RUNNER] Execution script for model run_llama31_405b.py.*
|   |-- run_llama31_8b.py — *[ACTIVE RUNNER] Execution script for model run_llama31_8b.py.*
|   |-- run_llama33_70b.py — *[ACTIVE RUNNER] Execution script for model run_llama33_70b.py.*
|   |-- run_llama4_scout.py — *[ACTIVE RUNNER] Execution script for model run_llama4_scout.py.*
|   |-- run_minimax_m2.py — *[ACTIVE RUNNER] Execution script for model run_minimax_m2.py.*
|   |-- run_mistral_large3.py — *[ACTIVE RUNNER] Execution script for model run_mistral_large3.py.*
|   |-- run_nemotron_ultra.py — *[ACTIVE RUNNER] Execution script for model run_nemotron_ultra.py.*
|   |-- run_phi4.py — *[ACTIVE RUNNER] Execution script for model run_phi4.py.*
|   |-- run_poolside_laguna.py — *[ACTIVE RUNNER] Execution script for model run_poolside_laguna.py.*
|   |-- run_qwen35_27b.py — *[ACTIVE RUNNER] Execution script for model run_qwen35_27b.py.*
|   |-- run_qwen35_397b.py — *[ACTIVE RUNNER] Execution script for model run_qwen35_397b.py.*
|   |-- run_qwen36_27b.py — *[ACTIVE RUNNER] Execution script for model run_qwen36_27b.py.*
|   |-- run_qwen37_max.py — *[ACTIVE RUNNER] Execution script for model run_qwen37_max.py.*
|   |-- run_qwen38_max.py — *[ACTIVE RUNNER] Execution script for model run_qwen38_max.py.*
|   |-- run_qwen3_30b_moe.py — *[ACTIVE RUNNER] Execution script for model run_qwen3_30b_moe.py.*
|   |-- run_qwen3_coder_480b.py — *[ACTIVE RUNNER] Execution script for model run_qwen3_coder_480b.py.*
|   |-- run_qwq32b.py — *[ACTIVE RUNNER] Execution script for model run_qwq32b.py.*
|   |-- run_qwq_plus.py — *[ACTIVE RUNNER] Execution script for model run_qwq_plus.py.*
|   |-- run_sarvam8b.py — *[ACTIVE RUNNER] Execution script for model run_sarvam8b.py.*
|   |-- run_sea_lion_v4.py — *[ACTIVE RUNNER] Execution script for model run_sea_lion_v4.py.*
|   |-- run_seed_oss_36b.py — *[CANDIDATE FOR CLEANUP] Legacy model runner superseded by newer API/tier (run_seed_oss_36b.py).*
|   -- scoring_v2.py — *[RESEARCH UTILITY] Plotting/analysis script (scoring_v2.py).*
|-- **LOCAL ONLY/**
|   |-- 4_defence_prompts.md — *[ESSENTIAL] Definitions for the 4 defense system prompt modes (none, systemic, sandwich, xml).*
|   |-- agent_context.md — *[DOCUMENTATION] Architecture state tracker and agent context handover log.*
|   |-- deepseek_chat_transcript.md — *[DOCUMENTATION] Qualitative transcript from exploratory model sessions.*
|   |-- full_project_audit.md — *[DOCUMENTATION] Full repository audit notes and historical matrix changes.*
|   |-- gemini_chat_transcript.md — *[DOCUMENTATION] Qualitative transcript from exploratory model sessions.*
|   |-- manual_testing_log.md — *[DOCUMENTATION] Qualitative probing logs and manual case study records (NRF-022 to NRF-028).*
|   |-- model_evaluation_matrix.md — *[ESSENTIAL] Single source of truth model evaluation matrix & active execution tracking log. DO NOT DELETE.*
|   |-- novel_research_findings.md — *[DOCUMENTATION] Empirical findings documentation (NRF-001 through NRF-028).*
|   |-- script_changes.md — *[DOCUMENTATION] Historical log of script edits and refactor changes.*
|   |-- selected_prompts.md — *[ESSENTIAL] Curated 100 indirect prompt injection scenario prompt definitions.*
|   |-- system_prompt_archive.md — *[DOCUMENTATION] Archive of attack payloads and system prompt templates.*
|   -- temp.md — *[CANDIDATE FOR CLEANUP] Temporary research draft scratchpad.*
|-- **paper/**
|   |-- draft.pdf — *[PUBLICATION] LaTeX source files and paper draft PDF.*
|   -- limitations.tex — *[PUBLICATION] LaTeX source files and paper draft PDF.*
|-- **results/**
|   |-- **csv/**
|   |   |-- codestral.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- cohere_command_a.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- cohere_command_a_plus.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- cohere_command_a_reasoning.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- deepseek_r1.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- deepseek_v32.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- deepseek_v4_flash.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- deepseek_v4_pro.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- diffusiongemma.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemini35_flash.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemini36_flash.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemini3_flash.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemma4_26b_moe.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemma4_31b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- glm52.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gpt_oss_120b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gpt_oss_20b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- groq_compound.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- ibm_granite.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- kimi_k2.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- ling_30_flash.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- llama3.1_8b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- llama33_70b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- llama4_scout.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- minimax_m2.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- mistral_large3.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- nemotron_ultra.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- phi4.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- poolside_laguna_m1.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen35_27b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen35_397b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen36_27b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen37_max.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen38_max.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen3_30b_moe.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen3_coder_480b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwq32b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwq_plus.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- sarvam8b.csv — *[ACTIVE FILE] Repository resource file.*
|   |   |-- sea_lion_v4.csv — *[ACTIVE FILE] Repository resource file.*
|   |   -- tencent_hunyuan.csv — *[ACTIVE FILE] Repository resource file.*
|   |-- **jsonl/**
|   |   |-- codestral.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- cohere_command_a.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- cohere_command_a_plus.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- cohere_command_a_reasoning.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- deepseek_r1.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- deepseek_v32.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- deepseek_v4_flash.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- deepseek_v4_pro.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- diffusiongemma.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemini35_flash.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemini36_flash.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemini3_flash.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemma4_26b_moe.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gemma4_31b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- glm52.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gpt_oss_120b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- gpt_oss_20b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- groq_compound.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- ibm_granite.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- kimi_k2.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- ling_30_flash.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- liquidai_lfm.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- llama3.1_8b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- llama33_70b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- llama4_scout.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- minimax_m2.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- mistral_large3.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- nemotron_ultra.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- nous_hermes_405b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- phi4.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- poolside_laguna_m1.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen35_27b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen35_397b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen36_27b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen37_max.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen38_max.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen3_30b_moe.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwen3_coder_480b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwq32b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- qwq_plus.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- sarvam8b.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   |-- sea_lion_v4.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |   -- tencent_hunyuan.jsonl — *[ACTIVE FILE] Repository resource file.*
|   |-- **reports/**
|   |   |-- deepseek_v4_pro_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   |-- gemma4_26b_moe_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   |-- gemma4_31b_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   |-- gpt_oss_120b_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   |-- groq_compound_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   |-- llama3.1_8b_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   |-- llama33_70b_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   |-- nemotron_ultra_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   |-- poolside_laguna_m1_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |   -- qwen36_27b_analysis.md — *[RESEARCH UTILITY] Jupyter Notebook for exploratory statistical analysis.*
|   |-- convergence_plot.png — *[RESEARCH OUTPUT] Visual chart plotting sample size statistical convergence.*
|   |-- convergence_study.json — *[RESEARCH OUTPUT] Statistical analysis data file (convergence_study.json).*
|   |-- correct_behavior_audit.json — *[RESEARCH OUTPUT] Statistical analysis data file (correct_behavior_audit.json).*
|   |-- reliability_study.json — *[RESEARCH OUTPUT] Statistical analysis data file (reliability_study.json).*
|   -- results.csv — *[ESSENTIAL DATASET] Master consolidated evaluation dataset across all benchmarked models.*
|-- **scratch/**
|   -- commit_all.ps1 — *[UTILITY] Local PowerShell helper script for git operations.*
|-- **scripts/**
|   |-- convergence_plot.py — *[RESEARCH UTILITY] Plotting/analysis script (convergence_plot.py).*
|   -- reliability_study.py — *[RESEARCH UTILITY] Plotting/analysis script (reliability_study.py).*
|-- .env — *[ESSENTIAL / SECRET] Provider API keys & account credentials. DO NOT DELETE.*
|-- .env.example — *[REFERENCE] Example environment schema template for team setup.*
|-- all_files_inventory.txt — *[ACTIVE FILE] Repository resource file.*
|-- benchmark.json — *[CANDIDATE FOR CLEANUP] Legacy v1 benchmark scenario definitions (superseded by benchmark_v2.json).*
|-- benchmark_v2.json — *[ESSENTIAL DATASET] Core v2 benchmark dataset (100 IPI scenarios x 4 defense modes = 400 test cases).*
|-- benchmark_v2_review_flags.json — *[DATASET] Human review flags for ambiguous model outputs.*
|-- check_safety.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (check_safety.py).*
|-- confidence_intervals.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (confidence_intervals.py).*
|-- exhaustive_ascii_tree.txt — *[ACTIVE FILE] Repository resource file.*
|-- generate_analysis.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (generate_analysis.py).*
|-- generate_charts.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (generate_charts.py).*
|-- generate_report.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (generate_report.py).*
|-- launch_all.py — *[CANDIDATE FOR CLEANUP] Legacy root multi-script launcher (superseded by benchmark_scripts/run_auto_pipeline.py).*
|-- LICENSE — *[CONFIG] Open source MIT license.*
|-- manual_rescore.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (manual_rescore.py).*
|-- merge_results.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (merge_results.py).*
|-- migrate_benchmark.py — *[CANDIDATE FOR CLEANUP] One-off v1 to v2 schema migration script.*
|-- model_registry.json — *[ESSENTIAL DATASET] Master JSON catalog mapping all 80 model parameters, providers, and axes.*
|-- progress_check.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (progress_check.py).*
|-- README.md — *[ESSENTIAL] Primary project documentation, abstract, positioning table, and execution guide. DO NOT DELETE.*
|-- requirements.txt — *[CONFIG] Python package manifest (openai, anthropic, boto3, etc.).*
|-- run_benchmark.py — *[CANDIDATE FOR CLEANUP] Legacy root benchmark runner script (superseded by benchmark_scripts/_core.py).*
|-- run_groq_sequential.py — *[CANDIDATE FOR CLEANUP] Legacy root Groq runner script (superseded by benchmark_scripts/_groq.py).*
|-- taxonomy_mapping.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (taxonomy_mapping.py).*
-- verify_fixes.py — *[ACTIVE UTILITY] Core data analysis, chart generation, or evaluation tool (verify_fixes.py).*
