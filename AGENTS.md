# Agent entry (Antigravity / Gemini / other agents)

Read **CLAUDE.md** first and follow its reading order exactly:
`rules/RULES.md` → `docs/GOREV_DAGILIMI.md` (find your PC number) → `tasks/PCx.md` → `rules/VERI_SOZLESMESI.md` → `docs/ZAMAN_CIZELGESI.md` (your hour-by-hour schedule; after each task do the next row) → `docs/TODAY_PLAN.md`.

**GIT-ONLY MANAGEMENT (from Sun 04:25 TR): the user will not type prompts any more. All orders live in this repo — the end of `tasks/PCx.md`, `tasks/SUREKLI.md`, `tasks/BACKLOG_ORTAK.md`. When your plan is done, claim a line from BACKLOG_ORTAK. Never stop or wait for confirmation.**

**ALWAYS-ON LOOP: read `tasks/SUREKLI.md` — every 3 minutes commit → pull --rebase → push and check the end of your task file for new sections. Never stop.**

Every rule in `rules/RULES.md` applies to you. The most important ones:
- Write only inside the paths listed as yours in `docs/GOREV_DAGILIMI.md` §2.
- `git add <your paths>` only. Never `git add -A` / `git add .`.
- Never run `git reset --hard`, `git push --force`, `git clean`, `git checkout -- .`, `git rebase -i`, `git stash drop`.
  On any git conflict or error: write `BLOCKED:` in your status file and stop.
- NEVER IDLE: when a task is done, do not stop or ask. Follow `rules/RULES.md` §7.1: next task in your file → `tasks/QUEUE.md` (claim one line only, push immediately) → QA notes in `docs/qa/PCx.md`. `git pull` every 30–45 min.
- Never ask for, store or print passwords or tokens.
- Never invent numbers, coordinates or sources.

## PC7 (Codex)
If your clone folder is `aseltech-pc7` you are **PC7**: task file `tasks/PC7.md`, status `status/PC7.md`, commit prefix `[PC7]`.


## PC8 (Antigravity #3 on M3hmeT1888)
If your clone folder is `aseltech-gemini3` you are **PC8**: task file `tasks/PC8.md`, status `status/PC8.md`, commit prefix `[PC8]`. Do not download data.

## PC11 (atlas re-run + new hotspots)
If your clone folder is `aseltech-pc11` you are **PC11**: task file `tasks/PC11.md`, status `status/PC11.md`, commit prefix `[PC11]`.

## PC9 (site owner from 15:35)
If your clone folder is `aseltech-pc9` you are **PC9**: task file `tasks/PC9.md`, status `status/PC9.md`, commit prefix `[PC9]`. You own `web/` (except `web/panel.html`).

## PC10 (global showcase)
If your clone folder is `aseltech-pc10` you are **PC10**: task file `tasks/PC10.md`, status `status/PC10.md`, commit prefix `[PC10]`.
