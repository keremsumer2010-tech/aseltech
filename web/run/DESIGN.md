# AQUIFER RUN — game design document (NISAR Vision)
Original side-scrolling platformer about groundwater and sinking ground. **Not** a copy of any
existing game: original hero, original pixel art drawn in code, original levels based on real
places NISAR measured. Lives in `web/run/` → published at `/run/`.

## 1. Pitch (one sentence)
> Run, jump and splash across four real sinking valleys, switch off the thirsty pumps, catch the
> rain, and keep the ground from collapsing under your feet — with the NISAR satellite as your guide.

## 2. Player fantasy & learning goal
- **Fantasy:** a young "water ranger" racing across farms, desert and city, saving a valley.
- **What the player learns (without reading a lecture):**
  1. Pumping groundwater faster than rain refills it lowers the water underground.
  2. When it drops below its old lowest level, clay squeezes **permanently** → the ground sinks.
  3. Sinking cracks canals, roads and houses; in Konya it is linked to sinkholes (obruk).
  4. A radar satellite (NISAR) can measure this sinking from space, to the centimetre.

## 3. Hero & guide
- **Nisa**, water ranger: wide-brim hat, blue backpack tank with a gauge, hose nozzle. 16×24 px.
- **NISAR** (the satellite) flies across the sky. Every ~25 s it does a **radar scan**: colour
  fringes sweep the level for 3 s and reveal **hidden sinking zones** (ground that will drop).

## 4. Core loop (per level, 2–4 minutes)
1. **Run & jump** right through the level (platforming).
2. **Collect raindrops** 💧 → fill your tank (max 10).
3. **Switch off pumps** (stand + press ACTION): each running pump drains the valley's
   **Aquifer meter**; switching it off stops the drain. Some pumps are guarded by puzzles/jumps.
4. **Water thirsty crops** (stand + ACTION, costs 2 tank) → they turn green → +score, and the
   farmer agrees to switch a pump off (story beat).
5. **Watch the Aquifer meter** (HUD, top): above the red line = safe. Below it, **sink tiles**
   (cracked soil) start dropping; they fall permanently while below the line.
6. Reach the **well-head flag** at the end → level report card.

## 5. Hazards (non-violent)
| Hazard | Behaviour |
|---|---|
| Sink tile | Cracked soil; drops 1 tile per 2 s while the meter is under the red line; permanent |
| Sinkhole (Konya) | Opens under a sink tile when the meter is very low; a pit |
| Earth fissure (Eloy) | Long crack, jump over; widens if meter low |
| Dust devil | Moves back and forth; touching it empties 3 tank; spray water (ACTION while moving) to calm it |
| Broken canal | Water leaks; repair spot (ACTION, costs 3 tank) restores a bridge |

No lives/death screen spam: falling into a pit → respawn at last checkpoint, −1 heart (3 hearts).

## 6. Levels (real places, real numbers from NISAR Vision)
| # | Level | Biome | Signature mechanic | Fact unlocked |
|---|---|---|---|---|
| 1 | Tulare Basin, California | farms, orchards, canals | tutorial: rain, pumps, crops; canal bridge repair | −7.8 cm in 108 days (NISAR, 2026) |
| 2 | Eloy, Arizona | desert, cotton, fissures | earth fissures widen; dust devils | #1 reliable basin, −8.6 cm per 100 days |
| 3 | Karapınar, Konya | steppe, wheat, obruk | sinkholes open under sink tiles | ground sank faster near sinkholes |
| 4 | Mexico City | dense city, old lake bed | buildings tilt, metro tunnel section | one of the fastest-sinking cities |
Data chips 🛰️ (3 per level, hidden) unlock a fact card each (`facts.json`).

## 7. Score & report card
Stars per level: ★ reach the end · ★ aquifer never below red line · ★ all 3 data chips.
Score = crops×100 + pumps off×150 + raindrops×10 + chips×300 − permanent sink tiles×50.
Report card shows: aquifer curve over the level, permanent sinking in cm (1 tile = 2 cm), the
real NISAR number for that place, and one sentence on what it means.

## 8. Controls
Keyboard: ←/→ or A/D move · Space/W/↑ jump (hold = higher) · E/Enter/X ACTION · P pause.
Touch (auto on touch devices): left/right pads bottom-left, JUMP + ACTION bottom-right.
Gamepad: optional.

## 9. Look & feel (PC1 owns)
- 16×16 px tiles, drawn in code from pixel maps, scaled ×3 (crisp, `imageSmoothingEnabled=false`).
- Palette: warm earth (soil, clay, sand), lush greens, water blues; red only for danger.
- Each biome: 3–4 parallax layers (sky gradient + sun/moon, far mountains/skyline, mid
  hills/fields, near details). Day-to-dusk tint as the level progresses.
- Effects: rain particles, splash, dust, crack spread, radar fringe sweep (rainbow bands like a
  real interferogram), screen shake on collapse.
- HUD: tank gauge, Aquifer meter with red line, hearts, chips, score. Title screen + level select
  map + report card, all in the same pixel style.

## 10. Architecture & module contract (all plain ES5/ES2017 scripts, no build step)
```
web/run/index.html   shell: canvas, touch buttons, loads scripts in this order
web/run/art.js       PC1  window.RunArt
web/run/engine.js    PC4  window.RunEngine
web/run/player.js    PC4  window.RunPlayer
web/run/systems.js   PC7  window.RunSystems
web/run/levels/*.json PC7 level data
web/run/facts.json   PC7 fact cards (with sources)
web/run/main.js      PC4  boot, scenes (title → map → level → report)
web/run/test_*.js    PC4/PC7 Node tests
```
### RunArt (PC1)
```js
RunArt.TILE = 16; RunArt.SCALE = 3;
RunArt.ready                       // Promise resolved when the sprite atlas is built
RunArt.drawTile(ctx, name, x, y)   // x,y in screen px (already scaled)
RunArt.drawSprite(ctx, name, frame, x, y, flipX)   // 'nisa_idle'(2) 'nisa_run'(4) 'nisa_jump'(1)
                                    // 'nisa_action'(2) 'dust_devil'(4) 'pump_on'(2) 'pump_off'(1)
                                    // 'crop_dry' 'crop_green' 'drop'(4) 'chip'(4) 'flag'(2) 'farmer'(2)
RunArt.drawBackground(ctx, biome, camX, w, h, t)   // biome: tulare|eloy|konya|mexico
RunArt.fx(ctx, type, x, y, t)      // 'splash' 'dust' 'crack' 'sparkle'
RunArt.radarSweep(ctx, w, h, p)    // p 0..1 interferogram fringe sweep overlay
RunArt.hud(ctx, state, w, h)       // state: {tank,tankMax,aquifer,redLine,hearts,chips,score,level}
RunArt.title(ctx, w, h, t); RunArt.card(ctx, x, y, w, h)  // panels in pixel style
```
Tile names: `grass dirt clay rock sand road brick canal water pipe_v pipe_h crate sign
sink1 sink2 sink3 fissure sinkhole_edge bridge bridge_broken house_wall house_roof tree bush
wheat cotton orchard fence lamp`.

### Level JSON (PC7) → read by engine (PC4)
```json
{ "id": "tulare", "name": "Tulare Basin, California", "biome": "tulare",
  "width": 220, "height": 15, "tiles": ["....string rows, one char per tile ...."],
  "legend": { "G": "grass", "D": "dirt", "C": "clay", "S": "sink1", "W": "water", "=": "bridge", "#": "rock" },
  "entities": [ {"type":"pump","x":30,"y":11}, {"type":"crop","x":42,"y":11},
                {"type":"drop","x":12,"y":8}, {"type":"chip","x":77,"y":4,"fact":"tulare-1"},
                {"type":"dust","x":120,"y":11,"range":6}, {"type":"checkpoint","x":100,"y":11},
                {"type":"flag","x":214,"y":11}, {"type":"farmer","x":44,"y":11,"line":"…"} ],
  "aquifer": { "start": 70, "redLine": 40, "drainPerPump": 0.9, "rainRefill": 4, "rainEverySec": 0 },
  "nisar": { "scanEverySec": 25, "realFactCm": -7.8, "realFactText": "…" } }
```
### RunSystems (PC7)
```js
RunSystems.createLevelState(levelJson) -> state
RunSystems.update(state, dt, events)   // events from engine: pickups, actions, falls
RunSystems.aquiferInfo(state) -> {value, redLine, belowRed, permanentTiles, cmSunk}
RunSystems.sinkTilesToDrop(state) -> [{x,y}]   // engine moves those tiles down
RunSystems.score(state) -> {score, stars:[bool,bool,bool], report:{...}}
```
### RunEngine / RunPlayer (PC4)
Fixed-timestep loop (60 Hz), camera follow with look-ahead, AABB tile collision, coyote time
(0.1 s) + jump buffer (0.1 s) + variable jump height, keyboard/touch/gamepad input, entity
update/draw dispatch, scene manager, pause, localStorage save of stars per level.

## 11. Quality bar
- 60 fps on a mid phone; no external assets except our own; no console errors.
- Every number shown about NISAR comes from `data/global/atlas.json` / `data/*/summary.json`
  (facts.json cites the file). Calibration sentence on the report card.
- Accessible: colour is never the only signal (icons + text), reduced-motion option disables
  shake and radar sweep animation.
- Tests: `node web/run/test_systems.js` (aquifer math, star rules, level JSON validity: every
  level is completable, flag reachable) and `node web/run/test_engine.js` (collision, jump).

## 12. Milestones (TR time)
| When | Milestone |
|---|---|
| +2 h | M1: engine + art placeholder: Nisa runs/jumps on level 1 tiles |
| +4 h | M2: systems: aquifer, pumps, drops, crops, sink tiles work in level 1 |
| +6 h | M3: all 4 levels, report card, title + map, touch controls |
| +8 h | M4: polish, tests green, link from site (replaces Water Hero button) |
