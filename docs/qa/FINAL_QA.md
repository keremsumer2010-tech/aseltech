# Final QA Report (`docs/qa/FINAL_QA.md`)

**Date:** 2026-11-15 12:44 TR · **Owner:** PC4 (reassigned from PC7)

## 1. Link, Asset & Publishing Gate
- `python3 tools/check_site.py`: **43 pages checked, 0 broken links** (`web/*.html`, `docs/story/*.html`, `docs/bulletins/*.html`, `game/index.html`, `web3d/`).
- `python3 -m pytest tests/test_site_links.py -v`: **PASSED** (1/1).

## 2. JavaScript Syntax & Module Checks (`node --check`)
All 10 site and simulator JS files pass `node --check` with zero syntax errors:
- `web/app.js`, `web/nisar3d.js`, `web/js/atlas.js`, `web/js/atlas_sat.js`, `web/js/docs.js`, `web/js/explorer.js`, `web/js/home3.js`
- `game/game.js`, `game/model.js`, `game/tests.js`

## 3. Data & Headline Number Consistency
- `python3 -m pytest tests/test_numbers_consistency.py tests/test_site_numbers.py tests/test_atlas_schema.py -v`: **4/4 PASSED** (`vital_signs.json`, `home_summary.json`, `atlas.json`, `SCIENCE_SIGNOFF.md`, `slides.html`, `technical_note.md`, `press_summary.md`, `submission_form.md`).
- `python3 tools/vital_signs.py --check`: **OK** (`29 regions, fastest=konya_plain -11.0 cm/100d`).

## 4. Mobile (375 px) & Overflow CSS Guards
- `web/css/atlas.css`: `.atlas-page{overflow-x:hidden;overflow-y:auto}` and `.atlas-tscroll{overflow-x:auto}`
- `web/css/style.css`: `.site-nav{overflow-x:auto}`, `@media (max-width:860px)` table/code `overflow-x:auto;max-width:100%`
- `web/css/home3.css`: `.code{overflow-x:auto}`
- `game/style.css`: `body { overflow-x: hidden; overflow-y: auto; }` at mobile breakpoint.
- *Environment note:* Headless Chromium / Playwright is not installed in this Linux container (`ModuleNotFoundError: No module named 'playwright'`), so live browser DOM/console execution at `1920×1080` and `375×812` should be spot-checked on PC1/PC6 before 20:00 freeze.
