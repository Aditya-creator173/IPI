# shadow/ — Pre-Adjudication Shadow Rescore Archive

## Purpose

This directory contains **shadow-rescored CSVs** for the GPT-5 series models
(6 files, ~2,400 rows) generated during the pre-adjudication audit phase
(Session 2, 2026-08-26).

## Contents

| File | Model | Purpose |
|------|-------|---------|
| `gpt5.csv` | GPT-5 | Shadow copy for encoding-fix delta audit |
| `gpt54.csv` | GPT-5.4 | Shadow copy for encoding-fix delta audit |
| `gpt55.csv` | GPT-5.5 | Shadow copy for encoding-fix delta audit |
| `gpt56_sol.csv` | GPT-5.6 Sol | Shadow copy for encoding-fix delta audit |
| `gpt56_terra.csv` | GPT-5.6 Terra | Shadow copy for encoding-fix delta audit |
| `gpt56_luna.csv` | GPT-5.6 Luna | Shadow copy for encoding-fix delta audit |

## Why These Exist

During the Windows cp1252 `\ufffd` encoding bug fix (Scorer v3.0 → v3.1,
commit `567ae02`), the GPT-5 series was the primary affected cohort.
These shadow copies preserve the **pre-fix scores** as a comparison baseline,
establishing that the encoding correction caused exactly 0 unintended score flips
in the GPT-5 series (both models in the 62-CSV rescore that showed +0.3% delta
were non-GPT models).

## Status

**READ-ONLY / AUDIT TRAIL ONLY.** Do not use these files for analysis.
The canonical, post-encoding-fix CSVs live in `results/csv/`.

These shadow files are retained for reproducibility audit purposes only
and are NOT included in any paper figures or leaderboard rankings.

## Removal Policy

These files may be safely deleted after the camera-ready revision is accepted
and the audit trail is no longer required. They are excluded from paper artifact
packaging via `.gitignore` patterns if needed.
