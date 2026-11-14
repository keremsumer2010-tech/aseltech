# NASA Space Apps Project Submission Rules and Checklist

## 1. Source Provenance & Verification Boundary

- **Primary Verified Official Guide (HTTP 200):**  
  [Space Apps 2022 Project Submission Guide (PDF)](https://spaceapps-prod.s3.amazonaws.com/media/documents/Space_Apps_2022_Project_Submission_Guide.pdf) — downloaded and verified directly from official Space Apps AWS S3 hosting (`4,478,948` bytes).
- **Direct Portal FAQ Access Limitation (Honest Verification Note):**  
  Automated HTTPS retrieval of the live Participant FAQ page (`spaceappschallenge.org/resources/participant-faq/`) failed SSL certificate validation in this Linux environment (`CERTIFICATE_VERIFY_FAILED`). Rather than guessing current-season portal edits or AI-policy wording, **a team member must open the live Resources / Participant FAQ / Terms & Conditions pages in a standard browser on `spaceappschallenge.org` before final submission** to confirm whether any event-year deadlines, team-size caps, or AI disclosure checkboxes have changed.

---

## 2. Verified Submission Requirements (from Official Submission Guide)

### A. Required Form Structure on Project Page
- **Project Title**
- **High-Level Project Summary** *(what was developed, how it addresses the challenge, why it matters)*
- **Link to Final Project** *(external public repo or hosted app—must require NO login, permission request, or registration)*
- **Link to Project "Demo"** *(strictly ONE link to either a slide presentation OR a video)*
- **Detailed Project Description** *(functionality, benefits, goals, tools, languages, hardware/software)*
- **Space Agency Data** *(exact open-source datasets used from NASA and/or Space Agency Partners such as ISRO)*
- **Project Development and Technical Challenges** *(portal field: learning, motivation, development approach, obstacles resolved)*
- **References** *(all code, data, text, and images used—even if open-source or freely available—plus permission verification for any copyrighted material)*

### B. Project Demo Format Limits ("Do Not Exceed")
- **Option 1 — Video Presentation:** Maximum **30 seconds**; may be spoken in any language **provided English subtitles are included**.
- **Option 2 — Slide Presentation:** Maximum **7 slides**; **must be written in English**.
- Judges stop reviewing demos once the **30-second** mark or **7th slide** is reached.
- Because the portal does not host videos or document uploads directly, host the demo externally (YouTube, Google Drive, GitHub, Dropbox, OneDrive) and verify public unauthenticated access in a private/incognito window.
- Official 30-second pitch arc ("30 Seconds of Glory"): `0:00` Introduce yourself/team -> `0:02` Challenge addressed -> `0:05` Name solution & problem solved -> `0:10–0:20` How it works + Space Agency Data impact -> `0:30` Future impact.

### C. Global Judging Eligibility Baseline
- Must address an **official challenge** (submissions to *"Invent Your Own Challenge"* are **not eligible for Global Judging** in the verified guide).
- All team members (**1–6 members per website limit in the verified 2022 guide**) must be registered and added to the team Project Page before submission closes.
- Project page fields and linked materials must be in **English** (except spoken video audio with English subtitles), free of profanity/inappropriate language, and submitted before the registered local event deadline (`11:59 PM` local time, or team creator's local time for Universal Event).
- Must use open-source data from NASA and/or Space Agency Partners (here: NASA–ISRO NISAR & NASA GIBS) and affirm both confirmation checkboxes (Submission Guide / Participant Terms compliance + original work & full References citation).
- Evaluation dimensions: **Impact, Creativity, Validity, Relevance, Presentation**.

---

## 3. Team Pre-Submit Compliance Checklist

- [ ] **No Fake Metrics (`K-2`):** Every `{...}` placeholder in `docs/story/project_page.md` replaced only with actual measured values from `data/central_valley/summary.json`, `data/karapinar/`, and `data/uk/`; zero invented statistics or unverified URLs.
- [ ] **Mandatory NISAR Calibration Attribution (`K-3`):** *"NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."* appears visibly in the project page, web footer, and slides/video.
- [ ] **Preview vs. Quantitative Separation:** UK Fens radar PNG explicitly labeled `preview`; Central Valley / Karapınar GUNW maps explicitly labeled `provisional` (no pre-`2026-06-17` `beta-precal` data mixed into quantitative results).
- [ ] **AI Disclosure (`K-13 / K-14`):** All Higgsfield AI assets (`hero.jpg`, `hero.mp4`, scene illustrations) clearly labeled `"AI-generated illustration"` in UI, demo slides, and Project Page **References / AI Disclosure**, alongside AI development tool attribution.
- [ ] **Brand & Privacy Hygiene (`K-9 / K-11`):** Zero NASA/ISRO official logos embedded in the app UI; zero API keys, `.netrc` credentials, passwords, or private emails in GitHub repo or public links.
- [ ] **Incognito Access Check:** Open final live GitHub Pages URL, GitHub repository link, and Demo link in an incognito browser to confirm zero 404s or login walls before pressing **Submit**.
- [ ] **Live Portal Final Check:** Confirm 2026 event challenge selection, closing timestamp (`local time`), team roster lock, and current-year AI addendum directly on `spaceappschallenge.org` in browser.
