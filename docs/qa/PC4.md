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
| **`L134–137` (`#game` & `#gameNote`)** | `Aquifer Manager` / `ten years` / `The game is being built.` | PC6 oyunu **Valley Under Pressure (`game/index.html` v2, 24 ay, 7 Tulare Havzası bölgesi)** olarak güncelledi (`52d9796`). | Başlık `Valley Under Pressure`, açıklama `24 months across seven Tulare Basin districts calibrated to provisional NISAR rates (illustrative model).` olarak güncellenmeli. |
| **`L149` (`Method` kartı)** | `... and consecutive 12-day pairs are added up.` | Hem Central Valley (`7` çift içinde `24 günlük` `07-22→08-15` ve `09-20→10-14` var) hem Karapınar (`8` çift) yalnızca 12 günlük değil **12–24 günlük** çiftler içeriyor. Ayrıca iyono+plane+DEM düzeltmesi belirtilmemiş. | `"... after subtracting the ionosphere screen and fitting a topographic/plane ramp, consecutive pairs (12–24 days) are summed."` |
| **`L16` & `L154` (Üst menü & Alt bilgi)** | `#how` linki sonrası `3D` / `Slides` bağlantısı yok; alt bilgide yalnızca depo & `sources.md` var. | `Q16` (`web3d/`) ve 7-slayt (`docs/story/slides.html`) siteye bağlanmayı bekliyor; ayrıca `.github/workflows/pages.yml` `web/.` içeriğini `_site/` köküne kopyaladığı için statik `../web3d/` linki Pages kökünde kırılır (`web3d/` henüz `_site/web3d/` altına da kopyalanmıyor). | `.github/workflows/pages.yml` içine `cp -r web3d _site/web3d` (ve `game/` için `cp -r risk _site/risk`) eklenmesi; `web/index.html` menüsünde `web/app.js` içindeki `ROOT` (`../web3d/` lokal vs `./web3d/` Pages) mantığıyla çözülen `3D Explorer` bağlantısı ve `L154` alt bilgisinde depo üstünden `judge_faq.md` / `slides.html` linki verilmesi. |

*(Küçük üslup notu: `L29`'da `NASA-ISRO's NISAR` ifadesi geçiyor; gövde boyunca en-tireli `NASA–ISRO` veya tutarlı `NASA-ISRO` seçilebilir. Başka yazım/gramer hatası görülmedi.)*

---

## 7. PCQ Tur 1 & Q15 Kod İncelemesi Yanıtları (`docs/qa/PCQ.md`, `docs/code_review.md`)

1. **`docs/qa/PCQ.md:20` (`Sahip: PC4` — Terra Bella / Friant-Kern Kanalı kaynağı):** KVPR (2017) haberi ([link](https://www.kvpr.org/environment/2017-08-03/friant-kern-canal-slows-by-60-percent-subsidence-to-blame)) canlı **HTTP 200** doğrulandı ve metindeki kesin veriler (`152-mile`, `4,000 -> 1,600 cfs` / `~%60` kayıp, `25-mile` kesimde `2–3 ft` çökme, **Terra Bella** civarında en derin çökme, `~$400M` düzeltme maliyeti) `docs/story/sources.md` §2'ye eklendi (`22/22` benzersiz URL HTTP 200).
2. **`docs/qa/PCQ.md:22` (`docs/story/project_page.md` Karapınar 8-çift kümülatif güncellemesi):** `89ce49d` commit'inde zaten `data/karapinar/summary.json` (`−5.9 cm` LOS, `108` gün, `2 km W of Karapınar`, düşük-orta güven notu) ile güncellenmişti (`docs/qa/PCQ.md` incelemesi `6136c3f` sürümünde yapılmıştı).
3. **`docs/code_review.md:40` (`Owner: PC4` — `web3d/generate_3d_data.py:90` kullanılmayan `h5py` importu):** `try: import h5py` bloğu `importlib.util.find_spec("h5py") is None` kontrolüyle değiştirildi; böylece `h5py` kurulu olmadığında `gunw_io.py` uyumluluğu korunurken `pyflakes` kullanılmayan-import uyarısı giderildi.
4. **`docs/code_review.md` Pages dağıtım uyumluluğu (`web3d/`):** `web3d/index.html` (`#backLink`) + `web3d/app.js` başlangıcına `HEAD ../index.html` kontrolü eklendi; yerel `/web3d/` sunumunda `../web/`, GitHub Pages `_site/web3d/` dağıtımında `../` otomatik seçilir.

---

## 8. Video Altyazı & Sayı/Kaynak Kontrolü (`ZAMAN_CIZELGESI` Pazar 12:00–15:00)

`docs/story/video_shotlist.md` içindeki 6 SRT satırı (`00:00.0–00:30.0`) güncel `data/*/*.json`, `game/` ve `sources.md` ile satır satır denetlendi:
- **Güncelleme (Shot 5 & Cue 5):** `52d9796` ile gelen `game/index.html` (v2) başlığının **"Valley Under Pressure"** ve zaman ufkunun **24 ay (`Month 0 / 24`)** olduğu görüldü; çekim adımları (`Over-Pump`, `#pumpSlider`, `Terra Bella`) ve Cue 5 metni güncel v2 arayüze göre düzeltildi (`web/index.html:134–137` için de §6 önerisi güncellendi).
- **Sonuç:** `Cue 1–6` içindeki tüm sayılar (`1851`, `~4 m`, `2026-10-20`, `−7.8 cm` LOS, `−10.1 cm` dikey, `108` gün, `57.01 mm/km`, `1.00 cm` medyan RMSE, `−5.9 cm` LOS, `29` obruk) birebir doğrulandı (`docs/story/video_shotlist.md` § Line-by-Line Matrix).

---

## 9. Site v2 (`web/`) Sayı Kaynağı Denetimi & `data/*/meta.json` Sözleşme Kontrolü (`ZAMAN_CIZELGESI` Pazar 15:00–18:00)

`669b7e8` (Site v2) ve `d4bf097` (`drivers.json`) sonrası `web/index.html`, `web/science.html`, `web/data.html`, `web/faq.html`, `data/catalog.json` ve tüm `data/*/*.json` dosyaları otomatik betikle denetlendi (`2026-11-14`):

### 9a. `data/*/meta.json` ve JSON Bütünlüğü (`NaN` yok, tüm boyutlar `< 20 MB`)

| Klasör | `quality` | `bbox` Sözleşme Uyumu | `dates` vs `disp/*.png` | `NaN` / Boyut | Durum |
|---|---|---|---|---|---|
| `data/central_valley/` (`meta`, `summary`, `points`, `validation`, `assets`, `drivers`) | `provisional` | `[-120.2, 35.6, -119.0, 36.6]` ✔ | `8` tarih = `8` PNG ✔ | Yok · maks `47.2 KB` | **GEÇTİ** |
| `data/karapinar/` (`meta`, `summary`, `points`, `sinkholes.geojson`) | `provisional` | `[33.3, 37.6, 33.8, 37.9]` ✔ | `9` tarih = `9` PNG ✔ | Yok · maks `18.6 KB` | **GEÇTİ** |
| `data/uk/` (`meta.json`, `optical_2026-10-20.jpg`, `radar_2026-10-20.png`) | `preview` | `[-0.3, 52.4, 0.4, 52.9]` ✔ | GCOV hızlı bakış çifti (`700×500`) | Yok · maks `631.6 KB` | **GEÇTİ** |

### 9b. Site v2 (`web/index.html`, `web/science.html`, `web/data.html`) Sayı Kaynağı Matrisi

| Sayfa / Konum | Sayfa Üstündeki Sayı / İfade | Doğrulanan Kaynak Dosya | Sonuç |
|---|---|---|---|
| `web/index.html:30,38–39,84` | `7.8 cm` / `−7.8 cm` LOS, `108 days`, `28 Jun – 14 Oct 2026`, `7` pairs, `≈−10 cm` vertical | `data/central_valley/summary.json` (`-7.8`, `-10.1 @ 39.1°`, `n_pairs=7`) | **GEÇTİ** |
| `web/index.html:40,99–102` | `81` high, `131` medium, `433` low, `645` evaluated segments, `≥ 10 / 5 mm/km` | `data/central_valley/assets.json` `summary` | **GEÇTİ** |
| `web/index.html:41,90` & `science.html:70` | `10` GPS stations, **`6/10`** agree (`r ≥ 0.4`) | `data/central_valley/validation.json` (`CAHA 0.90`, `HANF 0.90`, `QCAP 0.82`, `TLBN 0.79`, `P056 0.66`, `P566 0.42` = tam **`6/10`**) | **GEÇTİ** |
| `web/index.html:42–43,108–110` | `−5.9 cm` LOS, `26 Jun – 12 Oct 2026`, `8` pairs, `29` sinkholes | `data/karapinar/summary.json` + `sinkholes.geojson` (`29` Feature) | **GEÇTİ** |
| `web/index.html:65,72–73` | `20 Oct 2026` UK VIIRS vs NISAR `preview`; `1851` post `nearly 4 m`, `2.75 m below sea level`, `1–2 cm/yr` | `data/uk/meta.json` + `docs/story/holme_fen.md` & `sources.md` §1 (`HTTP 200`) | **GEÇTİ** |
| `web/science.html:23,27,30,34` | `July 2025`, `17 Jun 2026`, `P05023`, `80 m`, `1239 MHz → 0.24196 m`, `[−6.2, −7.8] cm` | `docs/gunw_structure.md` (`0.24196324 m`), `sources.md` §5, `summary.json` | **GEÇTİ** |

### 9c. PC1 İçin Site v2 Güncel Düzeltme Notları *(Salt Okunur Denetim)*

1. **`data/catalog.json` (`web/data.html:38,42` tarafından canlı okunuyor):** `karapinar` ve `uk` girdileri hâlâ `quality: "pending"`, `layers: []` yazıyor; oysa tüm Karapınar (`provisional`), UK (`preview`) ve `data/central_valley/drivers.json` (`provisional`, `Q04`) dosyaları repoda hazır.
2. **`web/index.html:57, 164` & `web/science.html:34`:** `"consecutive 12-day pairs"` ifadesi Central Valley'de 2 adet (`07-22→08-15`, `09-20→10-14`), Karapınar'da 1 adet (`07-20→08-13`) **24 günlük** ardışık çift bulunduğu için `"consecutive pairs (12–24 days)"` olarak güncellenirse tam isabet olur.
3. **`web/science.html:25`:** `SME2 Soil moisture` satırı hâlâ `(in progress)` diyor; PC2 `data/central_valley/drivers.json` (`d4bf097`) çıktısını tamamladı.
4. **`docs/story/judge_faq.md` #13 (`web/faq.html` tarafından canlı okunuyor):** `Valley Under Pressure` (24 ay) adını yansıtması için sonraki adımda PC4 tarafından senkronize edilebilir (önceden eski `Aquifer Manager / 10 years` sürümünü anıyordu).

---

## 10. Tüm Depo Link Kontrolü & Günlük Özet (`ZAMAN_CIZELGESI` Cmt 22:00 · Pazar 18:00–22:00)

- **`docs/story/project_page.md` Son Okuma (`Pazar 18:00–20:00`):** Space Apps teslim taslağı Site v2 (`https://keremsumer2010-tech.github.io/aseltech/`), v2 simülasyon (`Valley Under Pressure`, 24 ay), `KVPR (2017)` Friant-Kern / Terra Bella kaynağı ve eşlikçi paketlerle (`sinkhole_timeline.md`, `judge_faq.md`, `slides.html`, `video_shotlist.md`) hizalandı.
- **Tüm Depo Canlı Dış Link Kontrolü (`Pazar 20:00–22:00` — `README.md`, `docs/`, `web/`, `web3d/`, `data/`, `game/`):** Toplam **50** benzersiz `https://` adayı tarandı (`task-728` + Pages/eğik-çizgi ek kontrolü):
  - **44 / 44** aktif doküman, veri API, CDN (`MapLibre 4.7.1`, `Chart.js 4.4.1`, `marked 12.0.2`, `Three.js 0.160.0`), GitHub Pages canlı URL'leri (`.../aseltech/`, `.../web3d/`, `.../docs/story/slides.html`), BGS/ASF/USGS/DergiPark/KVPR/GreatFen kaynakları **HTTP 200** verdi.
  - **`fonts.googleapis.com` & `fonts.gstatic.com` (`web/index.html:10`):** Yalnızca `preconnect` kök etiketi (`CSS` font URL'si `200`).
  - **PC3 `docs/story/game_model.md` QA Notu (Salt Okunur):**
    - `catalog-beta.data.gov/...` (`2` bağlantı) → **HTTP 404** (eski `catalog-beta` alt alan adı; `catalog.data.gov` veya birincil USGS bağlantısı önerilir).
    - `cdec.water.ca.gov/.../javareports?name=WSIHIST` → **`timed out`** (`game_model.md` içinde zaten erişilemedi notu var).
    - `lfweb.sjgov.org/EHD/0/doc/728929/Page133.aspx` → **HTTP 503** (sunucu geçici erişim hatası).
    - (`pubs.usgs.gov/of/2001/of01-35/pdf/ofr0135.pdf` bu makineden **HTTP 200** döndü.)
