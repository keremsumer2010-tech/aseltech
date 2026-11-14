# Lincoln Live Rehearsal & Failsafe Checklist (`17:30 TR`)

> **Target Site:** https://keremsumer2010-tech.github.io/aseltech/  
> **Total Presentation Budget:** `3:00` (`180 seconds` across `6 × 30 s` blocks) + Jury Q&A  
> **Mandatory Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Offline & Internet-Drop Backup Protocol (`< 2-Second Switch Rule`)

Prepare all four local fallbacks **15 minutes before the rehearsal** so a Wi-Fi drop, GitHub Pages stall, or MapLibre CDN timeout never breaks Kerem's speech:

1. **Start Local Static Web Server (zero internet dependency):**
   ```bash
   cd /home/ibrahim/İndirilenler/aseltech-gemini
   python3 -m http.server 8000
   ```
   Verify `http://localhost:8000/web/index.html`, `http://localhost:8000/game/index.html`, `http://localhost:8000/web3d/index.html`, and `http://localhost:8000/docs/story/slides.html` all load HTTP `200`.
2. **Pre-Buffer Local MP4 Video Backups (open in VLC / system media player or dedicated browser tab, muted):**
   - `docs/story/media/demo_30s.mp4` (`29.62 s`, `1080p`, `24 fps` full end-to-end site + simulator capture with burned English subtitles — instant 30-second fallback if live clicking stalls)
   - `docs/story/media/cv_subsidence.mp4` (Central Valley 8-epoch 1080p subsidence animation, matches `Figure 0`)
   - `docs/story/media/kp_subsidence.mp4` (Karapınar 9-epoch 1080p subsidence + 29-sinkhole animation)
3. **Self-Contained Offline 7-Slide Deck:**
   - Open `docs/story/slides.html` (works locally via `http://localhost:8000/docs/story/slides.html` or `file:///home/ibrahim/İndirilenler/aseltech-gemini/docs/story/slides.html` with zero external CDN requests, using embedded local PNG charts in `docs/story/media/`).
4. **The `< 2-Second Switch Rule` (Memir):**
   - If the live GitHub Pages site (`https://keremsumer2010-tech.github.io/aseltech/`) or any interactive canvas stalls for **more than 2 seconds**, Memir presses **`Ctrl+Tab`** immediately to **Tab 2** (`http://localhost:8000/web/index.html`) — or **Tab 5** (`docs/story/slides.html`) if WebGL/MapLibre stalls — while **Kerem keeps speaking without pausing or apologizing**.

---

## 2. Exact Browser Tab Order (Single Fullscreen Window `F11`)

Open these **6 tabs in exact left-to-right order** in a clean, distraction-free browser window (`1920×1080`, `100%` zoom, bookmarks bar hidden):

| Tab # | URL / Local Path | Pre-Set Scroll / State Before `0:00` | Purpose |
|---|---|---|---|
| **Tab 1** | `https://keremsumer2010-tech.github.io/aseltech/` | Scrolled to top Hero (`#heroMap`); `#cvVideo` pre-buffered | Primary live demo site (`Blocks 1–6`) |
| **Tab 2** | `http://localhost:8000/web/index.html` | Loaded locally & ready at Chapter 3 (`[data-step="cv"]`) | Instant `< 2 s` offline mirror if GitHub Pages drops |
| **Tab 3** | `http://localhost:8000/game/index.html` | **Terra Bella** district pre-selected | Instant fallback for Block 6 if `#gameBox` iframe takes `> 1 s` |
| **Tab 4** | `http://localhost:8000/web3d/index.html` | Central Valley 3D displacement mesh loaded | Visual backup for Q&A (3D exaggeration / Karapınar 3D sinkhole depth) |
| **Tab 5** | `http://localhost:8000/docs/story/slides.html` | Slide 1 active (advance with `→` key) | Zero-dependency offline slide deck backup |
| **Tab 6** | `http://localhost:8000/web/faq.html` (plus `web/science.html` link in header) | Top of FAQ cards visible | Rapid jury Q&A visual proof (`GNSS r = 0.924`, dual-orbit `85%`, `Q09 below_detection`) |

---

## 3. Screen Sharing, Display & Audio Checks (`T − 15 min`)

- [ ] **Share Full Browser Window (not a single tab):** Sharing the browser window guarantees `Ctrl+Tab` switches (Tabs 1–6) are visible to the jury without stopping screen share.
- [ ] **Display Resolution & Zoom:** Set screen to `1920×1080` (`100%` OS scale, `100%` browser zoom) so `.stats`, `#compare`, `#pointChart`, and `#ringChart` fit without awkward wrapping or cut-off axes.
- [ ] **Suppress Notifications & Popups:** Turn on OS Do Not Disturb; close terminal/editor windows or move them to another workspace; hide browser bookmarks bar (`Ctrl+Shift+B`) and press `F11`.
- [ ] **Video Mute Check:** Verify `#cvVideo` (`Figure 0`) and local `demo_30s.mp4` are **muted** during the live talk so audio tracks never talk over Kerem.
- [ ] **4-Person Microphone Check:** Test audio clarity and mute/unmute discipline for **Kerem** (active throughout `0:00–3:00`), **Mehmet** (unmuted for Q&A), and **İbrahim** (unmuted for Q&A); **Memir** stays muted unless sharing screen audio/tech note.
- [ ] **Offline File Size & Verification (`< 20 MB` check):** Confirm `demo_30s.mp4`, `cv_subsidence.mp4`, `kp_subsidence.mp4`, and `slides.html` load locally with zero broken `src` paths.

---

## 4. Timekeeping & Pacing Discipline (`3:00` Strict Limit)

- **Stopwatch Trigger:** **İbrahim** starts a silent visible stopwatch on Kerem's very first word (not on slide/screen load).
- **30-Second Checkpoint Targets (from `docs/story/presentation_cues.md`):**
  - **`0:30`:** Memir enters `#story` Chapter 2 (`[data-step="uk"]`, `#compare`).
  - **`1:00`:** Memir triggers `#cvPlay` in Chapter 3 (`[data-step="cv"]`, Central Valley).
  - **`1:30`:** Memir reaches Chapter 4 (`[data-step="gnss"]`, `CAHA`) and moves to Chapter 5 (`.riskbars`).
  - **`2:00`:** Memir reaches Chapter 6 (`[data-step="kp"]`, Karapınar `#ringChart`).
  - **`2:30` (`30s` Warning Signal):** **İbrahim holds up the `30s` cue / hand signal.** Regardless of exact sentence position, Kerem transitions immediately to **Block 6** and Memir jumps straight to **`#play` (`Valley Under Pressure`)**.
  - **`2:55`:** Kerem finishes the closing sentence (`"All provisional NISAR processing code, 3D surfaces, and verified sources are open on GitHub—thank you, and we welcome your questions."`) with a `5-second` buffer before the `3:00` bell.

---

## 5. Team Responsibility Matrix (`tasks/PC4.md`)

| Team Member | Before Start (`T − 15 min`) | Live 3-Minute Pitch (`0:00 – 3:00`) | Jury Q&A Session |
|---|---|---|---|
| **Kerem** *(Speaker)* | Warm up Blocks `1–6` aloud; check mic levels; mute desktop notifications | Speaks Blocks `1–6` cleanly in English following `presentation_cues.md` | Routes deep technical/source questions to Mehmet & İbrahim; delivers final summary |
| **Memir** *(Demo Driver)* | Start `python3 -m http.server 8000`; load Tabs `1–6` in fullscreen window; verify `Ctrl+Tab` speed | Executes synchronized clicks (`#watch`, `#compareRange`, `#cvPlay`, `p01`, `CAHA`, `#ringChart`, `#gamePlay`, `150%` Over-Pump) and `< 2 s` fallback | Pulls up Tab 4 (`web3d/`), Tab 5 (`slides.html`), or Tab 6 (`faq.html` / `science.html`) visually as Mehmet/İbrahim answer |
| **Mehmet** *(Tech Q&A)* | Keep `validation_report.md`, `uncertainty.md`, and `fullyear.md` key numbers open on secondary screen | Monitors technical chart transitions (`#gnssChart`, `#why`) | Answers Q2 (LOS/vertical & Dual-Orbit Track 34/114), Q3 (ionosphere/DEM/Cramér-Rao/`1.00 cm` GNSS RMSE), Q5 (108-day vs. 11-month Earlimart decomposition), and simulator Terzaghi physics |
| **İbrahim** *(Data Q&A & Timer)* | Verify Tab `1–6` HTTP 200 & local video buffers; set stopwatch ready | Calls visual `30 s` pacing splits and **`2:30` simulator jump signal** | Answers Q1 (Provisional `P05023` vs. beta/preview maturity policy), Q4 (Karapınar 29 sinkholes & `p = 0.0001` permutation limits), UK Fens / London clay `below_detection`, and literature sources (`sources.md`) |
