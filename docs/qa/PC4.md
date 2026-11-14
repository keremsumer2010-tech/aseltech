# PC4 QA Raporu

Tarih: `2026-11-14` (`14:21 TR`) · Kapsam: PC4 çıktıları (`data/uk/`, `data/karapinar/sinkholes.geojson`, `docs/story/`, `web3d/`) + 14:10 Paketi (`Q30`, `Q31`, `judge_faq.md`, `slides.html`, `video_shotlist.md`, `web/index.html` İngilizce okuma)

---

## 1. Görev 1 — `data/uk/` ("Bulutun Altı" Görsel Çifti)

| Kontrol | Dosya / Alan | Sonuç |
|---|---|---|
| Dosya boyutu & RGB format | `data/uk/optical_2026-10-20.jpg` (`19,490 B`), `data/uk/radar_2026-10-20.png` (`631,556 B`) | **GEÇTİ** — ikisi de `(700, 500)` RGB, `< 20 MB`, `transparency` chunk yok (su alanlarında beyaz piksel hatası giderildi) |
| Bulut vs. Radar içeriği | `VIIRS_SNPP_CorrectedReflectance_TrueColor` vs. `NISAR_L2_PR_GCOV_..._20261020T192237_..._P05023_..._LATLON.png` | **GEÇTİ** — optik `~%98.2` bulutlu (MODIS `%100`), radar `%100` geçerli piksel; The Wash kıyı çizgisi bulutsuz GIBS referansıyla (`2026-09-26`, `2026-10-08`) görsel olarak piksel bazında hizalı doğrulandı |
| Meta & Kalite | `data/uk/meta.json` (`1,421 B`) | **GEÇTİ** — geçerli UTF-8 JSON, `quality: "preview"`, `bbox: [-0.3, 52.4, 0.4, 52.9]`, her iki URL HTTP 200 |

---

## 2. Görev 2 — `data/karapinar/sinkholes.geojson`

| Kontrol | Detay | Sonuç |
|---|---|---|
| Geçerli GeoJSON & Şema | `FeatureCollection`, `29` `Point` feature, `18,638 B` UTF-8, `NaN` yok | **GEÇTİ** — `name`, `lon`, `lat`, `year_formed`, `diameter_m`, `depth_m`, `status`, `source_title`, `source_url`, `coord_source` tam |
| Konum ve Kapsam | `lon ∈ [33.35750, 33.58111]`, `lat ∈ [37.72556, 37.89444]` | **GEÇTİ** — tüm `29` nokta sıkı şekilde Karapınar radar `bbox = [33.3, 37.6, 33.8, 37.9]` içinde |
| Veri Bütünlüğü (K-2) | Tapur & Bozyiğit (2015), *Marmara Coğrafya Dergisi* 31:415-446 Tablo 1 + metin | **GEÇTİ** — PDF URL (`.../article-file/3454`) HTTP 200; PDF'te dakika/saniye hatası (`37° 43' 99"`) içeren `Küpbasan Yeni Obruk-I` dışarıda bırakıldı, tahmin yapılmadı |

---

## 3. Görev 3 & Queue `Q11`, `Q12` (`docs/story/`)

| Kontrol | Dosya | Sonuç |
|---|---|---|
| Kaynak doğrulama | `docs/story/sources.md`, `docs/story/calibration_note.md` | **GEÇTİ** — canlı **HTTP 200** doğrulandı; alıntılanan her sayı kaynak dokümanda birebir doğrulandı |
| Zorunlu dipnot | `calibration_note.md`, `sources.md`, `project_page.md` | **GEÇTİ** — *"NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."* tam metni yer alıyor; `BETA (<2026-06-17)` / `PROVISIONAL (P05023)` / `VALIDATED (>=2026-10-21)` ASF dokümanlarıyla doğrulandı |
| Taslak & Kurallar (Q11, Q12) | `docs/story/project_page.md`, `docs/story/submission_rules.md` | **GEÇTİ** — doğrulanmış depo URL'si (`https://github.com/keremsumer2010-tech/aseltech`) ve `data/central_valley/summary.json` kaynaklı 7-çift bulguları (`2026-06-28` → `2026-10-14`, `108` gün, 1 km blok medyan tepe `−7.8 cm` LOS / `−10.1 cm` dikey tahmini `39.1°`, `6 km N of Terra Bella`, doğrusal yaz mevsimi tahmini `−26.4 cm/yıl`) işlendi; yalnızca `{PUBLIC_GITHUB_PAGES_URL}` ve `{PUBLIC_DEMO_LINK_30S_VIDEO_OR_7_SLIDES}` yayın yer tutucuları bırakıldı; `Space_Apps_2022_Project_Submission_Guide.pdf` HTTP 200 doğrulandı ve `www.spaceappschallenge.org/resources/participant-faq/` için TLS hatası dürüstçe raporlandı (`E-06`) |

---

## 4. Queue `Q16` — `web3d/` (3D "Yerin Nefesi" Görünümü)

| Kontrol | Detay | Sonuç |
|---|---|---|
| Veri üretimi (`web3d/generate_3d_data.py` -> `web3d/surfaces.json`) | `508,881 B` (`497.0 KB`), valid UTF-8 JSON, `NaN` yok; Central Valley (`80×96` × `8` epok, `2026-06-28` → `2026-10-14`, `7` çift, `vmin=-6.0`, `vmax=+6.0`, `p2=-5.83`, `p50=-0.51`, `p98=+3.26`, tepe `−7.8 cm` LOS `6 km N of Terra Bella`, `%62.9` geçerli) & Karapınar (`48×80` × `9` epok, `2026-06-26` → `2026-10-12`, `8` çift, `vmin=-5.0`, `vmax=+5.0`, `p2=-4.18`, `p50=-0.65`, `p98=+2.45`, tepe `−5.9 cm` LOS `2 km W of Karapınar`, `%14.2` geçerli + `29` obruk) | **GEÇTİ** — `analysis/out/central_valley_cum_stack.npz` & `karapinar_cum_stack.npz` + `data/*/summary.json` yeniden kullanıldı; `analysis/` / `data/central_valley/` değiştirilmedi |
| Ön yüz & JS söz dizimi (`web3d/index.html`, `style.css`, `app.js`) | `node --check web3d/app.js` + lokal HTTP sunucu (`/web3d/`, `style.css`, `app.js`, `surfaces.json`) **HTTP 200** + Three.js `@0.160.0` & `OrbitControls.js` CDN **HTTP 200** | **GEÇTİ** — dikey abartma `10,000×–150,000×` (varsayılan `50,000×`), `RdBu` renk skalası, `Peak LOS Subsidence` etiketi ve zorunlu `provisional` dipnotu mevcut |

---

## 5. PC6 QA Bulgularıyla Çapraz Kontrol (`docs/qa/PC6.md`)

`docs/qa/PC6.md` §3 maddelerine istinaden PC4 tarafı notu:
1. **`web/index.html:154` (`docs/story/sources.md` linki):** Dosya oluşturuldu; push sonrası canlı link çalışacaktır.
2. **`web/index.html:47` (Holme Fen yer tutucusu):** PC4 tarafından birincil kaynaklardan doğrulanan kesin rakamlar (`Great Fen Heritage`: `1848` ahşap kazık, `1851` dökme demir direk, ilk dönemde yılda `9 inç`, `1852`'den bu yana günümüzde yüzey üstünde **yaklaşık 4 m**; `Wikipedia`: deniz seviyesinin **2.75 m / 9.0 ft altı**) `docs/story/sources.md` §1 ve `docs/story/holme_fen.md` içine işlenmiştir (PC1 aşağıdaki §6'daki hazır HTML'i yapıştırabilir).

---

## 6. `web/index.html` Son İngilizce Okuma & Düzeltme Önerileri *(Salt Okunur Denetim — `web/` Değiştirilmedi, PC1 Uygular)*

Kapsam: `web/index.html` (`1–163`). Genel İngilizce tonu akıcı ve tutarlı biçimde İngiliz imlası (`centimetres`, `labelled`) kullanıyor; tespit edilen 6 somut iyileştirme aşağıdadır:

| Satır / Öğe | Mevcut Metin (`web/index.html`) | Sorun / Tutarsızlık | Önerilen İngilizce Metin (`PC1`) |
|---|---|---|---|
| **`L47` (`#holmeText`)** | `In the Fens, an iron post driven into the peat in the 1850s now stands far above the ground: ... <span class="pending">Exact figure and source being verified.</span>` | Hâlâ `.pending` yer tutucusu duruyor; doğrulanmış rakam ve kaynak eksik. | `docs/story/holme_fen.md` hazır metni: `"Driven flush with the peat in 1851, the Holme Fen cast-iron post now stands nearly <b>4 metres</b> above the sunken fields—leaving the fenland <b>2.75 metres below sea level</b> (Britain's lowest land point) while drained farmland still loses 1–2 cm/yr (<a href=\"https://www.greatfen.org.uk/about-great-fen/heritage/holme-fen-posts\" target=\"_blank\" rel=\"noopener\">The Great Fen</a>)."` *(İngiliz imlası `metres` sayfadaki `centimetres` ile uyumlu)* |
| **`L52` (`#compareEmpty`)** | `Cloud / radar image pair for the Fens is being prepared.` | `data/uk/` tamamlandı; JS yüklenemeden görülürse veya fallback açık kalırsa eskimiş bilgi verir. | `"Loading same-day VIIRS cloud image and NISAR GCOV radar preview (2026-10-20)..."` (`data/catalog.json` güncellenince `PLACEHOLDER` rozeti kalkar) |
| **`L92` (`#kpEmpty`)** | `Verified sinkhole locations (each with a source) are being compiled.` | `data/karapinar/sinkholes.geojson` (`29` obruk) hazır olmasına rağmen "derleniyor" ifadesi duruyor. | `"Loading 29 peer-reviewed Karapınar sinkhole records..."` (JS veri gelince bu `.pending` satırını gizlemeli) |
| **`L137` (`#gameNote`)** | `The game is being built.` | `game/index.html` (v2) repoda hazır; eskimiş `.pending` metni. | `"Interactive 10-year aquifer simulation calibrated to provisional Central Valley drawdown rates (illustrative model)."` |
| **`L149` (`Method` kartı)** | `... and consecutive 12-day pairs are added up.` | Hem Central Valley (`7` çift içinde `24 günlük` `07-22→08-15` ve `09-20→10-14` var) hem Karapınar (`8` çift) yalnızca 12 günlük değil **12–24 günlük** çiftler içeriyor. Ayrıca iyono+plane+DEM düzeltmesi belirtilmemiş. | `"... after subtracting the ionosphere screen and fitting a topographic/plane ramp, consecutive pairs (12–24 days) are summed."` |
| **`L16` & `L154` (Üst menü & Alt bilgi)** | `#how` linki sonrası `3D` / `Slides` bağlantısı yok; alt bilgide yalnızca depo & `sources.md` var. | `Q16` (`web3d/`) ve 7-slayt (`docs/story/slides.html`) siteye bağlanmayı bekliyor. | Üst menüye `<a href="../web3d/">3D Explorer</a>` eklenmesi; `L154` alt bilgisinde `· <a href="../docs/story/judge_faq.md">Judge FAQ</a>` veya `slides.html` bağlantısının eklenmesi. |

*(Küçük üslup notu: `L29`'da `NASA-ISRO's NISAR` ifadesi geçiyor; gövde boyunca en-tireli `NASA–ISRO` veya tutarlı `NASA-ISRO` seçilebilir. Başka yazım/gramer hatası görülmedi.)*
