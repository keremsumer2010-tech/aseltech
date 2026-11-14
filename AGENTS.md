# Agent rules (Antigravity / Gemini / other agents)

This repo's single source of truth for rules is **CLAUDE.md**. Read it fully before doing anything; every rule there applies to you.

Which worker are you? Ask the human if unsure.
- Antigravity on **memir-erdogmus**'s computer = **PC2** → task `tasks/PC2.md`, status `status/PC2.md`.
- Antigravity on **M3hmeT1888**'s computer = **PC5** → task `tasks/PC5.md`, status `status/PC5.md`.
  (M3hmeT1888's Claude Code is PC3 and works in a DIFFERENT clone folder; never touch `analysis/`.)
- Antigravity on **acikgozibrahim032-hub**'s computer = **PC4** → task `tasks/PC4.md`, status `status/PC4.md`.
- SECOND Antigravity on **M3hmeT1888**'s computer (clone folder `aseltech-gemini2`) = **PC6** → task `tasks/PC6.md`, status `status/PC6.md`.
  On M3hmeT1888's computer: folder `aseltech-claude` = PC3 (Claude Code), `aseltech-gemini` = PC5, `aseltech-gemini2` = PC6. Your folder name tells you who you are.

- Start: `git pull` → read `CLAUDE.md`, `docs/TODAY_PLAN.md`, your task file → do the task → update your status file → `git pull --rebase` → commit `[PCx] ...` → push.
- NEVER IDLE: when a task is done, do not stop or ask — follow the "HİÇ BOŞ KALMA PROTOKOLÜ" in CLAUDE.md
  (next task in your file → `tasks/QUEUE.md` → QA/docs). `git pull` every 30–45 min.
- Only write inside the folders listed in your task file (or in the queue item you claimed). Commit only your own files (`git add <paths>`, never `git add -A`).
- Never ask for, store or print passwords. The human enters Earthdata credentials into `~/.netrc` themselves.
- Never invent numbers or sources. Follow the "data quality and calibration" rule in CLAUDE.md.
