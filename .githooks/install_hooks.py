#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPIBench Git Hooks Installer
==============================
Installs the pre-commit security hook from .githooks/ into .git/hooks/
so it runs automatically on every `git commit`.

Usage:
    python .githooks/install_hooks.py

One-time setup — run this after cloning or pulling this script for the first time.
"""

import os
import shutil
import stat
import sys
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parent.parent
    src_dir   = repo_root / ".githooks"
    dst_dir   = repo_root / ".git" / "hooks"

    if not dst_dir.exists():
        print("[ERROR] .git/hooks directory not found. Are you inside a git repo?")
        sys.exit(1)

    hooks_installed = 0

    for hook_src in src_dir.iterdir():
        # Skip non-hook files (e.g. this installer itself)
        if hook_src.name == "install_hooks.py":
            continue
        if hook_src.suffix in (".md", ".txt", ".py") and hook_src.name != "pre-commit":
            continue

        hook_dst = dst_dir / hook_src.name

        # Back up existing hook if present
        if hook_dst.exists():
            backup = hook_dst.with_suffix(".bak")
            shutil.copy2(hook_dst, backup)
            print(f"  [BACKUP] Backed up existing hook: {hook_dst.name} -> {backup.name}")

        shutil.copy2(hook_src, hook_dst)

        # Make executable (required on Unix; harmless on Windows)
        current_mode = hook_dst.stat().st_mode
        hook_dst.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        print(f"  [OK] Installed: {hook_src.name} -> .git/hooks/{hook_src.name}")
        hooks_installed += 1

    if hooks_installed == 0:
        print("[WARN] No hooks found in .githooks/ to install.")
    else:
        print(f"\n[OK] {hooks_installed} hook(s) installed successfully.")
        print("   The pre-commit security gate will now run on every `git commit`.")
        print("\n   To test it manually:")
        print("     python .git/hooks/pre-commit")
        print("\n   To bypass in an emergency (use with extreme caution):")
        print("     git commit --no-verify")


if __name__ == "__main__":
    main()
