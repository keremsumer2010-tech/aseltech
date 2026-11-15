# NISAR Vision — Cambridge (virtual) final plan · PC1, 15 Nov 18:15 TR
Deadline **23:30 EST = 16 Nov 07:30 TR** (hard stop 23:59 EST). No live pitch: judges (multidisciplinary, MIT/Harvard circle) open the site and video on their own, 16–20 Nov.

## Goal: one sentence, then proof
> **We used NASA-ISRO's new NISAR radar satellite to measure where the ground is sinking in 29 places, and built checks that catch our own mistakes.**
Every page answers 3 questions in this order: **What did we find? How do we know it is right? What can someone do with it?**

## Rules (everyone)
- No new features or data (freeze). Only clarity, correctness, presentation.
- Plain English first, the technical term second ("line of sight (LOS)"). Headline numbers also in inches.
- Numbers only from `data/global/home_summary.json` / `atlas.json`. Before push: `python tools/check_site.py && python -m pytest -q`.
- File ownership below — do not edit the other agent's files.

## Ownership
| Agent | Owns |
|---|---|
| **PC7** (science + quality) | `web/index.html`, `web/science.html`, `web/css/*`, `docs/story/judge_faq.md`, `docs/qa/FINAL_QA.md` |
| **PC4** (story + submission) | `web/atlas.html` text, `web/present.html`, `docs/story/submission_form*.md`, `docs/JURI_3DK.md`, `README.md`, video in `docs/story/media/` |
| **PC1** | atlas build + freeze (19:15), deploy checks, final review 05:30 TR |

## Timeline (TR)
| Time | Milestone |
|---|---|
| 18:15–21:00 | Block 1 (each agent's top tasks) |
| 21:00 | PC1 review #1 (live site, desktop + phone) |
| 21:00–00:30 | Block 2 |
| 00:30 | PC1 review #2; content freeze 02:00 |
| 02:00–05:00 | Only typo/bug fixes, final QA |
| 05:30 | PC1 final check; Kerem submits by 07:00 TR |
