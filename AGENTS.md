# Agent rules (Antigravity / Gemini / other agents)

This repo's single source of truth for rules is **CLAUDE.md**. Read it fully before doing anything; every rule there applies to you.

- Antigravity worker on memir-erdogmus's computer = **PC2**. Task file: `tasks/PC2.md`, status: `status/PC2.md`.
- Start: `git pull` → read `CLAUDE.md`, `docs/TODAY_PLAN.md`, your task file → do the task → update your status file → `git pull --rebase` → commit `[PC2] ...` → push.
- Only write inside the folders listed in your task file.
- Never ask for, store or print passwords. The human enters Earthdata credentials into `~/.netrc` themselves.
- Never invent numbers or sources. Follow the "data quality and calibration" rule in CLAUDE.md.
