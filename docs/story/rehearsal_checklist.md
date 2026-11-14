# NISAR Pulse — 17:30 Lincoln Rehearsal & Failsafe Checklist (`docs/story/rehearsal_checklist.md`)

> **Target Session:** `17:30 TR` Full Dry-Run (`3:00` live pitch + `2:00` Jury Q&A drill)  
> **Live Web App:** https://keremsumer2010-tech.github.io/aseltech/ · **Companion Cue Sheet:** [`docs/story/presentation_cues.md`](presentation_cues.md)  
> **Mandatory Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Team Roles & Responsibilities (`T − 15 min` through Q&A)

| Role | Member | Live `0:00 – 3:00` Responsibility | Jury Q&A & Failsafe Responsibility |
|---|---|---|---|
| **Lead Speaker** | **Kerem** | Delivers `Blocks 1–6` from [`presentation_cues.md`](presentation_cues.md) without reading verbatim off slides; pauses 1 s smoothly if Memir switches tabs | Routes deep math/science vs. data/risk questions to Mehmet & İbrahim; delivers closing summary |
| **Live Demo Pilot** | **Memir** | Owns screen sharing (`1920×1080`, `100%` zoom). Drives `Tabs 1–4` one click ahead of Kerem's cue (`#compareRange`, `#cvPlay`, `p01`, `#fyBox`, `CAHA`, `#riskList`, `#ringChart`, `#gamePlay`, `web3d`) | Executes **`< 2-second` offline tab switch** to local mirror / `Tab 5` (`slides.html`) or `demo_30s.mp4` without stopping Kerem |
| **Technical Q&A & Timekeeper** | **Mehmet** | Runs silent visible stopwatch from Kerem's first word; flashes **`0:30`**, **`1:00`**, **`1:30`**, **`2:00`**, **`2:30` (`SIMULATOR JUMP`)**, **`2:50 WRAP NOW`**, **`3:00 STOP`** cards | Answers technical Q&A on GUNW `−λ/4π` math, ionosphere/DEM deramp, `mixed` full-year chain (`fullyear.md`), L-vs-C coherence (`cross_sensor.md`), GNSS `r = 0.924`, and dual-orbit Track 34/114 (`vertical.json`); speaker backup if Kerem drops |
| **Data, Impact & Source Q&A Lead** | **İbrahim** | Verifies pre-flight local server, zero console errors, video mute states, and `Tab 1–6` readiness (`T − 15 min`) | Answers jury Q&A on UK Fens `HH`/`HV` (`crops.json`), London clay `below_detection` (`±3.6 cm`), Karapınar 29 sinkholes & permutation tests (`sinkhole_stats.md`), WorldPop/USDA exposure (`141,555` residents across CV + Konya Basin, incl. `11,572` in Karapınar), Mexico City (`-7.0 cm`), simulator (`Valley Under Pressure`), and HTTP-200 verified citations (`sources.md`) |

*(If presenting solo at any practice table: presenter drives pre-set Tabs `1–5` directly, skipping `Tab 2` optional detour if behind at `1:15`.)*

---

## 2. Exact Pre-Loaded Browser Tab Order (Single Fullscreen Window `F11`)

Open one clean incognito/distraction-free browser window at **`1920×1080`**, **`100%` browser zoom**, bookmarks bar hidden (`Ctrl+Shift+B`), DevTools closed:

| Tab # | URL / Local Target | Pre-Pitch Ready State Before `0:00` | Used In |
|---|---|---|---|
| **Tab 1** | `https://keremsumer2010-tech.github.io/aseltech/` *(or `http://localhost:8000/web/index.html` if venue Wi-Fi is unstable)* | Scrolled to very top Hero (`#heroMap`); `.stats` rendered; `#cvVideo` pre-buffered muted | `Blocks 1, 2, 3, 4, 6` |
| **Tab 2** | `https://keremsumer2010-tech.github.io/aseltech/explorer.html#central_valley_fullyear` | Pre-set to **Central Valley, California — full year (Nov 2025 – Oct 2026)** (`mixed` badge visible), `7 km W of Earlimart` point pre-clicked | `Block 3` (optional `3 s` full-year view) |
| **Tab 3** | `https://keremsumer2010-tech.github.io/aseltech/game/index.html` | Past intro overlay onto 7-district Tulare Basin map (`Month 0 of 24`), **Classroom Mode** drawer open (`2. Multi-Year Drought` visible) | `Block 5` (`0:15`, or instant fallback if `#gamePlay` iframe lags) |
| **Tab 4** | `https://keremsumer2010-tech.github.io/aseltech/web3d/index.html` | Three.js `0.160.0` basin mesh loaded (`quality: provisional · CRID P05023`, `2026-10-14` epoch) so orbiting responds immediately | `Block 5` (`5–8 s`) + Q&A |
| **Tab 5 (Offline Deck)** | `http://localhost:8000/docs/story/slides.html` *(zero-CDN local HTML deck)* | Loaded to **Slide 1 / 7**, keyboard arrows (`→` / `←`) verified working | `< 2 s` primary offline fallback |
| **Tab 6 (Data & FAQ Backup)** | `http://localhost:8000/web/faq.html` *(plus header link to `science.html` & `data.html`)* | Scrolled to top FAQ cards | Visual Q&A backup after `3:00` |

---

## 3. Offline Fallback Plan (Zero-Internet Resilience & `< 2-Second Switch Rule`)

Because basemaps (`Esri World Imagery`) and `maplibre-gl` / `Chart.js` CDN bundles require network access unless cached in open tabs, start the local mirror **15 minutes before pitching**:

1. **Local HTTP Server (Zero-Dependency Repository Mirror):**
   ```bash
   cd /home/ibrahim/İndirilenler/aseltech-gemini
   python3 -m http.server 8000
   ```
   *(If port `8000` is occupied, run `python3 -m http.server 8765` and update the localhost URLs accordingly.)*  
   Verify `http://localhost:8000/web/index.html`, `http://localhost:8000/docs/story/slides.html`, `http://localhost:8000/game/index.html`, and `http://localhost:8000/web3d/index.html` all return `HTTP 200`.
2. **Primary Zero-CDN Backup — `docs/story/slides.html` (`7`-Slide Self-Contained Deck):**
   - Zero external CSS/JS/CDN requests: all PNG maps (`data/central_valley/disp/2026-10-14.png`, `data/karapinar/disp/2026-10-12.png`, `data/uk/`) and verification charts (`docs/story/media/validation_scatter.png`, `gnss_CAHA.png`, `risk_1.png`, `game_sensitivity.png`) render straight from disk via `http://localhost:8000/docs/story/slides.html` or `file://...`.
   - Memir advances `Slides 1 → 7` using `→` / `←` (~25 s per slide) matching `Blocks 1–6`.
3. **Secondary Local Video Safety Net (Paused in VLC behind Browser, `Alt+Tab` ready):**
   - `docs/story/media/demo_30s.mp4` (`29.62 s`, `1080p`, `24 fps`, `~3.5 MB`, burned-in English subtitles matching [`docs/story/video_30s.srt`](video_shotlist.md) / [`video_subtitles.srt`](video_subtitles.srt) + mandatory provisional notice).
   - Optional local regional animations ready on disk: `docs/story/media/cv_subsidence.mp4`, `docs/story/media/cv_fullyear.mp4`, and `docs/story/media/kp_subsidence.mp4`.
4. **`< 2-Second Switch Rule` (Memir):**
   - If any live tile, iframe (`#gameBox`), or WebGL scene freezes for **`> 2 seconds`**, switch immediately (`Ctrl+Tab` to **Tab 5 `slides.html`** or **`Tab 3`**, or `Alt+Tab` to `demo_30s.mp4`) while **Kerem keeps talking smoothly without pausing or apologizing**.

---

## 4. Screen Sharing, Display & Audio Checks (`T − 15 min`)

- [ ] **Git Sync & Clean Worktree:** Run `git pull --rebase origin main` on the presentation laptop and start `python3 -m http.server 8000` in `/home/ibrahim/İndirilenler/aseltech-gemini`.
- [ ] **Share Full Browser Window / Entire Screen (never a single tab):** Guarantees `Ctrl+Tab` across `Tabs 1–6` and `Alt+Tab` to `demo_30s.mp4` stay visible without breaking screen share.
- [ ] **Display Resolution & Zero-Crop Layout:** `1920×1080` at `100%` OS scale and `100%` browser zoom; close bookmarks bar (`Ctrl+Shift+B`), terminal/chat overlays, and enable OS **Do Not Disturb**; confirm `PROVISIONAL` badges and `#how` disclaimer stay unclipped.
- [ ] **Zero Console Errors Check:** Quickly open & close `Ctrl+Shift+I` on `Tabs 1–4` to confirm clean rendering before pitching.
- [ ] **Video Mute & 4-Person Mic Check:** Confirm `#cvVideo` and `demo_30s.mp4` are **muted** during live narration; test **Kerem** active throughout `0:00–3:00`, **Mehmet** & **İbrahim** clean unmute for Q&A, **Memir** muted unless audio clip needed.

---

## 5. Timekeeping Protocol & Cut-Cord Checkpoints (Target `2:45` → Hard Stop `3:00`)

| Elapsed | Checkpoint | Required On-Screen State | Mehmet Cue to Kerem & Memir | Cut-Cord Shortcut if `> 8 s` Late |
|---|---|---|---|---|
| `0:30` | End Block 1 | Hero `.stats` + `#watch` (`#cvVideo`) complete; entering `#story` Chapter 2 | `1` finger / proceed | Cut `#cvVideo` dwell to `2 s` |
| `1:00` | End Block 2 | `#compareRange` dragged, `#polChart` & `#ukClay` shown; entering Chapter 3 | `2` fingers / move to CV | Skip verbal mention of Fens `4`-field `dB` spread; keep cloud + `±3.6 cm` |
| `1:30` | End Block 3 | `#cvPlay`, `p01`, `#fyBox`, `CAHA` & `Tulare Canal` (`57 mm/km`) shown | `3` fingers / move to Karapınar | Skip `Tab 2` (`explorer.html`) switch; stay on `#fyBox` card in `Tab 1` |
| `2:00` | End Block 4 | `#ringChart` (`4.2` vs `0.6 cm`), `sinkList` & `#why` diagram shown | **`1:00 LEFT`** card — switch to Simulator | Mention Mexico City in 1 clause; switch straight to `Tab 3` (`game/index.html`) |
| `2:30` | **HARD SIMULATOR / CLOSE TRIGGER** | Finish `2. Multi-Year Drought` + `web3d/` orbit; jump immediately to `#how` | **`0:30 LEFT · WRAP TO #how`** card | Cut `Tab 4` (`web3d/`) early regardless of sentence position; land on `#how` |
| `2:50` | Closing Attribution | `#how` (`.qlegend` + `.disclaimer`) on screen cleanly | **`WRAP NOW`** | Deliver mandatory NASA–JPL/ISRO provisional sentence & stop by `2:55` |

---

## 6. Pre-17:30 Lincoln Dry-Run Gate (3 Structured Runs)

1. **`17:05–17:15` · Tech & Asset Gate:** Start `python3 -m http.server 8000`, open `Tabs 1–6` + paused `demo_30s.mp4`, confirm zero missing images (`data/uk/`, `docs/story/media/pc9_fullyear_point.png`), zero JS console errors, and exact tab order.
2. **`17:15–17:25` · Synchronized Walkthrough + Full Timed Run (`3:00` + `2:00` Q&A):** Memir rehearses clicks one cue ahead of Kerem; target `2:40–2:50` finish; Mehmet & İbrahim drill all `5` flash FAQ answers (`presentation_cues.md §3`) at `<= 15 s` each.
3. **`17:25–17:30` · Disconnect & Wording Sign-Off Drill:** Toggle Wi-Fi off mid-`Block 2` and require `< 2 s` transition to `Tab 5` (`slides.html`) without breaking Kerem's speech. Verify team members strictly state NISAR calibration and validation are performed by NASA–JPL and ISRO rather than our team, label vertical and yearly rates as *estimates*, and never claim InSAR predicts sinkhole collapse dates. Note any UI findings in [`docs/qa/PC4.md`](../qa/PC4.md) or [`docs/qa/PC9.md`](../qa/PC9.md) before pushing.
