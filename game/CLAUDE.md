# Valley Under Pressure — game design & rules (NISAR Vision simulator)

## What the game is
You run the water for a real farming valley for **24 months** (Oct 2026 → Sep 2028):
**Tulare Basin, California** or **Karapınar sub-basin, Konya, Türkiye**. Both were measured from
space by NASA-ISRO NISAR in summer 2026 (Tulare −7.8 cm LOS / ~−10.1 cm vertical in 108 days;
Karapınar −5.9 cm LOS). The model is calibrated so that the 2026 baseline settings reproduce
those measurements.

## The dilemma (core loop)
Each month the player sets three valley-wide levers and advances time:
| Lever | Effect |
|---|---|
| Groundwater pumping (0–150 %) | more income, deeper water table, more sinking |
| Canal (surface) water (0–max of the water year) | replaces pumping; capped by drought |
| Land left to rest / fallow (0–50 %) | less demand, less income |

Sinking has two parts (Terzaghi aquitard compaction):
- **elastic** — recovers when water levels come back in winter;
- **inelastic (permanent)** — happens once the head drops below its historical low
  (preconsolidation head); the clay is crushed and that underground storage is lost for good.

## Mission & score (game/mission.js)
The player is judged against **"doing nothing"**: a hidden run of the same valley, same two water
years, with the 2026 baseline settings. Three objectives, shown live and at the end:
1. **Keep the farms alive** — revenue ≥ 85 % of doing nothing (below 50 % counts as zero).
2. **Protect the aquifer** — permanent sinking ≤ half of doing nothing.
3. **Protect wells & canals** — fewer dry wells than doing nothing, canal capacity loss < 12 %.
Score = 40 % farms + 40 % aquifer + 20 % people → grade A (≥85) … F, shown from month 12 (permanent sinking only starts in the first summer, so earlier comparisons would flatter "doing nothing").
Balance (node game/test_mission.js): over-pumping and doing nothing → D/F; stopping all pumping
(farms collapse) → C; a balanced plan (≈75 % pumping, full canal water, 10 % fallow) → A/B.
There is no single magic setting: drought years (Dry/Critical) cap canal water, so the player must
adapt in year 2.

## Events the player sees (model.js stepMonth)
Water-year 2 declaration (Wet … Critical), domestic wells going dry, canal freeboard / conveyance
loss when differential subsidence passes 5 / 10 mm per km, Konya sinkhole-risk indicator near
mapped obruks (indicator only, not a prediction).

## Honesty rules
- Physical parameters carry their source; values marked `illustrative: true` are order-of-magnitude.
- Never claim the game predicts real sinkholes or real farm income; it is an educational model
  calibrated to one NISAR summer.
- Numbers shown about NISAR come only from `data/*/summary.json` / `data/global/atlas.json`.
- Calibration statement: NISAR data are provisional; calibration and validation are carried out by
  the NISAR project (NASA-JPL and ISRO), not by our team.

## Files
`index.html` (UI), `game.js` (map, charts, controls), `model.js` (physics, UMD),
`mission.js` (objectives + score, UMD), `tests.js` / `test_model.html` (browser checks),
`test_mission.js` (Node balance check). Before pushing: `node game/test_mission.js` and
`python tools/check_site.py && python -m pytest -q`.
