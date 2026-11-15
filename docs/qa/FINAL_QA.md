# Final QA Report (`docs/qa/FINAL_QA.md`)

**Date:** 2026-11-15 15:40 TR · **Owner:** PC4 (reassigned from PC7) · **Status:** All gates green

## 1. Link, Asset & Publishing Gate
- `python3 tools/check_site.py`: **43 pages checked, 0 broken links** (`web/*.html`, `docs/story/*.html`, `docs/bulletins/*.html`, `game/index.html`, `web3d/`).
- `python3 -m pytest tests/test_site_links.py -v`: **PASSED** (1/1).

## 2. JavaScript Syntax & Module Checks (`node --check`)
All 14 site, i18n, and simulator JS files pass `node --check` with zero syntax errors:
- `web/js/atlas.js`, `web/js/atlas_sat.js`, `web/js/docs.js`, `web/js/explorer.js`, `web/js/home3.js`, `web/js/i18n.js`, `web/js/i18n_tr.js`, `web/js/tour.js`, `web/js/tour_atlas.js`
- `game/game.js`, `game/i18n_load.js`, `game/model.js`, `game/tests.js`, `game/tour_steps.js`

## 3. Data & Headline Number Consistency
- `python3 -m pytest tests/ -v`: **11/11 PASSED** (`test_atlas_schema.py`, `test_home_summary.py` [6 tests], `test_numbers_consistency.py`, `test_site_links.py`, `test_site_numbers.py` [2 tests]).
- `python3 tools/vital_signs.py --check`: **OK** (`29 regions, fastest=eloy -8.6 cm/100d`, `15 reliable / 14 indicative`, `1,167,429 residents on 477.72 km²`).
- `python3 analysis/pc5/numbers_registry.py`: **OK** (`total=45 approved=30 preliminary=15 rejected=0 discrepancies=0`).

## 4. Mobile (375 px) & Overflow CSS Guards
- `web/css/atlas.css`: `.atlas-page{overflow-x:hidden;overflow-y:auto}` and `.atlas-tscroll{overflow-x:auto}`
- `web/css/style.css`: `.site-nav{overflow-x:auto}`, `@media (max-width:860px)` table/code `overflow-x:auto;max-width:100%`
- `web/css/home3.css`: `.code{overflow-x:auto}`
- `game/style.css`: `body { overflow-x: hidden; overflow-y: auto; }` at mobile breakpoint.
- `tools/bulletin.py`: `@media (max-width:600px)` table horizontal scroll, padding reduction, 2-column pkg-bar across all 29 A4 bulletins (`docs/bulletins/*.html`).
- *Environment note:* Headless Chromium / Playwright is not installed in this Linux container (`ModuleNotFoundError: No module named 'playwright'`), so live browser DOM/console execution at `1920×1080` and `375×812` should be spot-checked on PC1/PC6 before 20:00 freeze.
