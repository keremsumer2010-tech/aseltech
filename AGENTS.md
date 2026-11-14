# Agent rules (Antigravity / Gemini / other agents)

This repo's single source of truth for rules is **CLAUDE.md**. Read it fully before doing anything; every rule there applies to you.

- Gemini / Antigravity workers use the ID **PCG** (see `tasks/PCG.md`) and write status to `status/PCG.md`.
- Start: `git pull` → read `CLAUDE.md`, `docs/TODAY_PLAN.md`, `tasks/PCG.md` → do the task → update `status/PCG.md` → `git pull --rebase` → commit `[PCG] ...` → push.
- Only write inside the folders listed in your task file.
- Never invent numbers or sources. Follow the "data quality and calibration" rule in CLAUDE.md.
