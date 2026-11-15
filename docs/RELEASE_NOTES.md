# NISAR Vision — Release Notes & 20:00 Freeze Checklist (`docs/RELEASE_NOTES.md`)

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

**Release:** `v2026.11.15-pre-freeze` · **Target Data Freeze:** `2026-11-15 20:00 TR` (`17:00 UTC`) · **Delivery:** `22:00 TR`

---

## 1. What Is Included

1. **Global Subsidence Atlas (`data/global/atlas.json`, `web/atlas.html`):**
   - **29 regions** (`16` reliable, `13` indicative) processed with one open-source pipeline (`pipeline/nisarpulse/`) and ranked on the common 93-day summer window (`2026-06-28 → 2026-09-29`).
   - `#1` reliable: **Konya Plain** (`−11.0 cm/100d` common, `−9.6 cm` over `108 d`, `11.6%` valid-coverage caution).
   - Interactive 4-step reading guide, `"What changed"` (`atlas_changelog.json`, latest 10), `rate_ci_cm_per_100d` confidence intervals, `sigma_cm.png` toggle, and bidirectional `?basin=` links with the simulator.
   - Schema contract (`data/global/atlas.schema.json`) and automated tests (`tests/test_atlas_schema.py`, `tests/test_site_numbers.py`, `tools/vital_signs.py --check`).
2. **California Central Valley Deep Dive (`web/index.html`, `web/science.html`, `web/data.html`, `web/explorer.html`):**
   - `−7.8 cm` LOS peak (`108 d`, `−10.1 cm` vert. est.), `239.54 km² < −5 cm`, `10`-station GNSS `r = 0.924` (`1.00 cm` median RMSE), `81 / 645` infrastructure segments `> 20 mm/km` (`57.01 mm/km` Tulare Canal, `±25%` rank-invariant).
   - Full-year `Earlimart p01` decomposition (`−16.8 ± 2.2 cm/yr` permanent vs. `11.7 cm` seasonal, `R² = 0.97`, `mixed`) and `0.3174 km³/yr` permanent aquifer storage loss.
3. **Konya / Karapınar Sinkholes & London Clay Negative Control:**
   - Karapınar (`−5.9 cm` LOS) shows `6.4×` faster sinking `< 1 km` vs. `> 5 km` of 29 mapped sinkholes (`p = 0.0001` block perm, `p = 0.0207` constellation shifts).
   - London Clay negative control (`below_detection`, `97.7%` within `±1.5 cm`, `3σ = 3.62 cm` floor).
4. **Offline Presentation Mode & Simulator (`web/present.html`, `game/index.html`, `docs/story/`):**
   - 6-stop offline Lincoln presentation deck (`web/present.html`), 3-minute cue sheet (`presentation_cues.md`), 12 printable Q&A cards (`qa_cards.md`), 60-second backup demo script (`demo_script_v3.md`), `technical_note.md/.html`, `29/29` city cards, and `Valley Under Pressure` simulator (`6/6` model tests).

---

## 2. Known Limitations

- **Provisional & Mixed Products:** Core NISAR `GUNW`/`GCOV` products (`CRID P05023`, `>= 2026-06-17`) are provisional; full-year chains (`central_valley_fullyear`, `karapinar_fullyear`) mix pre-calibration `beta` granules (`< 2026-06-17`).
- **LOS Geometry:** Single-orbit vertical conversions (`LOS / cos θ`) are estimates assuming negligible horizontal motion.
- **Summer Window & Archive Gaps:** 93–120 day June–October windows capture peak pumping and overstate net annual compaction where winter rebound occurs; `konya_plain_fullyear` has a `156–168` day Feb–Jun 2026 archive gap.
- **Automated QC & Exposure:** `tools/atlas_qc.py` flags `12.1 cm` half-cycle jumps and `> 5 cm` cancelling single-date spikes (isolating `5` QC-flagged basins as indicative), while `exposure_atlas.json` covers all `29` regions (`1,200,716` residents on `511.65 km²` `< −5 cm`, excluding nested `karapinar`).

---

## 3. Changelog Summary (`atlas_changelog.json`)

- **Tehran:** Recomputed with off-basin reference (`−3.5 cm` → `−7.4 cm` LOS).
- **Semarang:** `2026-09-29 → 2026-10-11` `12.1 cm` half-cycle unwrapping jump removed; coastal peak recovered (`−6.2 cm` LOS, `#7` reliable).
- **Beijing:** Re-run with full box (`−11.1 cm` peak; `11 Jul` single-date spike remains flagged as `indicative only`).
- **Central Valley:** Retained `medium` confidence under `data/global/independent_validation.json` (`r >= 0.80` GNSS rule, `r = 0.924`).
- **Atlas Expansion:** Grown from `11` → `21` → `29` regions (`16` reliable / `13` indicative), ranked on the common 93-day window.

---

## 4. 20:00 Data Freeze Checklist

- [ ] Run `python3 pipeline/pc10/build_atlas.py` & `python3 tools/atlas_qc.py` after final PC11 ingestion (e.g. Jakarta `P010 F174`).
- [ ] Run `python3 tools/vital_signs.py` (and `--check`) + `python3 tools/sync_atlas_text.py`.
- [ ] Run `python3 -m pytest tests/test_site_numbers.py tests/test_atlas_schema.py -v` (must be `100%` pass).
- [ ] Re-verify `docs/qa/SCIENCE_SIGNOFF.md` 10 headline rows against `atlas.json` and `vital_signs.json`.
- [ ] Confirm `0` broken links and `200 OK` on `https://keremsumer2010-tech.github.io/aseltech/` after final push; after `20:00 TR`, bug fixes only.
