# NISAR Pulse — 17:30 Lincoln Rehearsal Checklist (`docs/story/rehearsal_checklist.md`)

**Target Session:** `17:30 TR` Full Rehearsal (`3:00` pitch + `2:00` Q&A drill) · **Owner:** PC9 (emergency backup for PC4)  
**Companion Cue Sheet:** [`docs/story/presentation_cues.md`](presentation_cues.md) · **Full Q&A Bank:** [`docs/story/judge_faq.md`](judge_faq.md)

---

## 1. Team Roles ("Kim Ne Yapar")

| Role | Member | Responsibilities Before & During the Pitch | Fallback Role |
|---|---|---|---|
| **Lead Speaker** | **Kerem** | Delivers the 6 spoken 30-second blocks from [`presentation_cues.md`](presentation_cues.md) without reading off the screen; pauses cleanly if Memir needs 1 extra second to switch tabs. | Reads over [`docs/story/slides.html`](slides.html) Slide 1–7 headlines if live browser fails. |
| **Live Demo Pilot** | **Memir** | Owns screen sharing (`1920x1080`, `100%` zoom). Drives Tabs 1–4 smoothly one click ahead of Kerem's cue without scrolling rapidly or spinning maps unnecessarily. | Switches immediately to local [`docs/story/slides.html`](slides.html) or [`docs/story/media/demo_30s.mp4`](media/demo_30s.mp4) if internet stalls. |
| **Technical Q&A + Timekeeper** | **Mehmet** | Runs silent stopwatch during the `3:00` pitch (flashes fingers / card at `0:30`, `1:00`, `1:30`, `2:00`, `2:30`, `2:45 WRAP`, `3:00 STOP`). Answers jury questions on NISAR GUNW math, `mixed` pre-calibration caution, ionosphere/deramp, dual-orbit inversion, and GPS validation. | Steps in as speaker backup if Kerem loses microphone or pauses mid-block. |
| **Risk, Basin & Impact Q&A Lead** | **İbrahim** | Answers jury questions on canal differential tilt (`81 / 645` segments, `±25%` ranking stability), Karapınar's 29 sinkholes vs. prediction limits, London clay `below_detection`, Terzaghi `Valley Under Pressure` simulator priors (`illustrative`), and open MIT data reproducibility. | Confirms audience audio/screen clarity from the back of the room during soundcheck. |

---

## 2. Browser Tab Order (Pre-Loaded 10 Minutes Before Pitch)

Open one clean incognito or distraction-free browser profile at **`1920x1080`** (`100%` zoom, bookmarks bar hidden, DevTools closed, system notifications set to Do Not Disturb):

| Tab # | URL (Live GitHub Pages) | Pre-Pitch Ready State | Used In |
|---|---|---|---|
| **Tab 1** | `https://keremsumer2010-tech.github.io/aseltech/` | Scrolled to the very top (`Hero` map loaded, `#findings` and MapLibre map verified rendered). | Blocks 1, 2, 3, 4, 6 |
| **Tab 2** | `https://keremsumer2010-tech.github.io/aseltech/explorer.html#central_valley_fullyear` | Pre-selected to **Central Valley, California — full year (Nov 2025 – Oct 2026)** (`mixed` badge visible), one point near Earlimart (`~-119.35°E, 35.88°N`) pre-clicked so the 11-month chart shows right away. | Block 3 (optional 3 s switch) |
| **Tab 3** | `https://keremsumer2010-tech.github.io/aseltech/game/index.html` | Loaded past any opening dialog onto the Tulare Basin map (`Month 0 of 24`), `Classroom Mode` panel open on the right so **2. Multi-Year Drought** is one click away. | Block 5 (`0:15`) |
| **Tab 4** | `https://keremsumer2010-tech.github.io/aseltech/web3d/index.html` | Three.js basin mesh loaded (`quality: provisional · CRID P05023`, `2026-10-14` epoch active) so dragging rotates immediately with zero load stall. | Block 5 (`0:10`) |
| **Tab 5 (Offline Deck)** | Local `docs/story/slides.html` (via `http://localhost:8765/docs/story/slides.html` or file path) | Loaded to **Slide 1 / 7**, keyboard arrow keys (`→` / `←`) tested. | Instant fallback if Wi-Fi fails |

---

## 3. Offline Fallback Plan (If Internet Drops During Demo)

Because the MapLibre basemap (`Esri World Imagery`) and `maplibre-gl` / `Chart.js` CDN scripts on `index.html` require internet unless already cached in open tabs, keep a **two-layer local safety net** open and tested before entering the room:

1. **Primary Offline Backup — `docs/story/slides.html` (7-Slide Self-Contained HTML Deck):**
   - Zero external CSS/JS dependencies: works 100% offline directly from disk (`file:///.../docs/story/slides.html`) or via a local server (`python -m http.server 8765` from the repo root, opening `http://localhost:8765/docs/story/slides.html`).
   - All maps (`data/central_valley/disp/2026-10-14.png`, `data/karapinar/disp/2026-10-12.png`, `data/uk/` optical vs radar) and validation plots (`docs/story/media/validation_scatter.png`, `gnss_CAHA.png`, `risk_1.png`, `game_sensitivity.png`) render locally from repository assets.
   - Kerem walks through **Slides 1 → 7** (~25 seconds per slide) using `→` / `←` or mouse clicks on **Tab 5**.
2. **Secondary Offline Backup — `docs/story/media/demo_30s.mp4` (`3.49 MB`, `1920x1080`, `h264`, `< 30 s`):**
   - Keep `docs/story/media/demo_30s.mp4` open and paused at `00:00` in VLC / native OS video player on the same monitor behind the browser window (`Alt+Tab` ready).
   - Contains burned-in English subtitles matching [`docs/story/video_subtitles.srt`](video_subtitles.srt) and the required provisional notice. If both the live site and slide projector freeze, play `demo_30s.mp4` (`29.6 s`) and resume live narration for the remaining time.
   - Optional local regional loops also on disk: `docs/story/media/cv_subsidence.mp4` (`3.22 MB`), `docs/story/media/cv_fullyear.mp4` (`4.43 MB`), and `docs/story/media/kp_subsidence.mp4` (`0.92 MB`).

---

## 4. Screen Sharing & Environment Setup

- [ ] Close Slack/Discord/WhatsApp desktop apps and mute OS notifications (`Do Not Disturb` on).
- [ ] Run `git pull --rebase origin main` on the presentation laptop and launch `python -m http.server 8765` in the repo root as a background local mirror **15 minutes before the pitch**.
- [ ] Verify Tab 1 (`index.html`), Tab 2 (`explorer.html#central_valley_fullyear`), Tab 3 (`game/index.html`), and Tab 4 (`web3d/index.html`) load with **zero console errors** (`Ctrl+Shift+I` check, then close DevTools).
- [ ] If presenting on Zoom/Meet/projector, share **Entire Screen** (not a single browser tab) so `Alt+Tab` between the browser and local `demo_30s.mp4` works cleanly without stopping screen share; enable *"Share system audio"* only if playing `demo_30s.mp4` with audio.
- [ ] Confirm browser zoom is **`100%`** and no text overlays (system volume, presenter bar) hide the `PROVISIONAL` badge or bottom attribution footer.

---

## 5. Timekeeping Protocol (Target `2:45` in Practice -> Hard Stop `3:00`)

| Elapsed Time | Block Finishing | Expected On-Screen State | Mehmet Signal to Kerem & Memir |
|---|---|---|---|
| `0:30` | Block 1 (UK Fens swipe) | Finished `#compareRange` swipe; scrolling to Chapter 3 | Subtle `1` nod / proceed |
| `1:00` | Block 2 (Central Valley `-7.8 cm`) | Point `p01` clicked on Chapter 3 map; showing `#fyBox` | Subtle `2` nod / move to full-year & GPS |
| `1:30` | Block 3 (Full-year + GPS + Tulare Canal) | `Tulare Irrigation District Canal` highlighted; scrolling to Chapter 6 | Subtle `3` nod / move to Karapınar |
| `2:00` | Block 4 (Karapınar `-5.9 cm` & London control) | Sinkhole ring chart visible; switching to Tab 3 (`Simulator`) | **`1:00 LEFT`** card — switch to Tab 3 right away |
| `2:30` | Block 5 (Simulator + 3D `web3d/`) | Drought simulation run + `web3d/` orbited; switching to Tab 1 `#how` | **`0:30 LEFT`** card — move to closing lines |
| `2:50` | Block 6 (`#who`, `#next`, `#how` disclaimer) | Provisional attribution visible cleanly on `#how` | **`WRAP NOW`** — finish final attribution sentence cleanly before `3:00` |

---

## 6. Pre-17:30 Lincoln Dry-Run Gate (Sign-Off Order)

1. **`17:10` Tech Check:** Open Tabs 1–5 + local `http.server 8765` + VLC with `demo_30s.mp4`; confirm zero broken images on Tab 1 and Tab 5 (`slides.html`).
2. **`17:20` Click Sync Check:** Walk once silently through Blocks 1–6 so Memir learns exact scroll pauses and Kerem spots every number (`-7.8 cm`, `240 km²`, `-20.3 cm` / `-16.8 cm/yr` mixed pre-cal note, `1.0 cm` GPS RMSE, `57 mm/km`, `-5.9 cm` near `29` sinkholes, `±3.6 cm` London).
3. **`17:30` Timed Rehearsal #1 (Full 3:00 + 2:00 Q&A):** Start stopwatch; target `2:40–2:50` finish. Drill the 5 FAQ answers (`presentation_cues.md §3`) with Mehmet and İbrahim answering in **1 sentence each** (`<= 15 s` per question).
4. **`17:45` Disconnect Drill:** Turn Wi-Fi off mid-Block 2 in a 60-second drill and verify Memir switches to **Tab 5 (`docs/story/slides.html`)** within `3 seconds` without interrupting Kerem.
5. **Post-Rehearsal Rule:** Note any timing bottlenecks or site glitches in [`docs/qa/PC9.md`](../qa/PC9.md); do not change numbers on the fly unless read directly from `data/*/summary.json`.
