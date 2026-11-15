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
4. **`docs/story/judge_faq.md` #13 (`web/faq.html` tarafından canlı okunuyor):** ~~Sonraki adımda senkronize edilebilir~~ → **BİTTİ (`Valley Under Pressure` 24 ay + `Q28` 1 km halka istatistikleri #7/#13'e işlendi).**

---

## 10. Tüm Depo Link Kontrolü & Günlük Özet (`ZAMAN_CIZELGESI` Cmt 22:00 · Pazar 18:00–22:00)

- **`docs/story/project_page.md` Son Okuma (`Pazar 18:00–20:00`):** Space Apps teslim taslağı Site v2 (`https://keremsumer2010-tech.github.io/aseltech/`), v2 simülasyon (`Valley Under Pressure`, 24 ay), `KVPR (2017)` Friant-Kern / Terra Bella kaynağı ve eşlikçi paketlerle (`sinkhole_timeline.md`, `judge_faq.md`, `slides.html`, `video_shotlist.md`) hizalandı.
- **`Q28` & `Q14` Sonrası Eşitleme (`docs/qa/PC6.md` yanıtı):**
  - `data/uk/meta.json` dosyasına yerel dosya adları (`"optical_image": "optical_2026-10-20.jpg"`, `"radar_image": "radar_2026-10-20.png"`) eklendi (`docs/qa/PC6.md:83` Q14 notu; `web/app.js` ve veri sözleşmesiyle tam uyumlu).
  - PC6 `Q28` obruk halkası analizi (`data/karapinar/assets.json`: `0–1 km` ortalama `−4.152 cm` LOS = `>5 km` arka planın `6.4×`'ı, `%100 <= -2 cm`, `Köken Obruğu-II`'ye `597.3 m` yolda `19.74 mm/km`) ve `Valley Under Pressure` (`24` ay) v2 oyunu `judge_faq.md`, `slides.html`, `pitch.md`, `sinkhole_timeline.md` ve `project_page.md` dosyalarının tamamında senkronize edildi (`0` adet eski `Aquifer Manager` kalıntısı).
- **Tüm Depo Canlı Dış Link Kontrolü (`Pazar 20:00–22:00` — `README.md`, `docs/`, `web/`, `web3d/`, `data/`, `game/`):** Toplam **50** benzersiz `https://` adayı tarandı (`task-728` + Pages/eğik-çizgi ek kontrolü):
  - **44 / 44** aktif doküman, veri API, CDN (`MapLibre 4.7.1`, `Chart.js 4.4.1`, `marked 12.0.2`, `Three.js 0.160.0`), GitHub Pages canlı URL'leri (`.../aseltech/`, `.../web3d/`, `.../docs/story/slides.html`), BGS/ASF/USGS/DergiPark/KVPR/GreatFen kaynakları **HTTP 200** verdi.
  - **`fonts.googleapis.com` & `fonts.gstatic.com` (`web/index.html:10`):** Yalnızca `preconnect` kök etiketi (`CSS` font URL'si `200`).
  - **PC3 `docs/story/game_model.md` QA Notu (Salt Okunur):**
    - `catalog-beta.data.gov/...` (`2` bağlantı) → **HTTP 404** (eski `catalog-beta` alt alan adı; `catalog.data.gov` veya birincil USGS bağlantısı önerilir).
    - `cdec.water.ca.gov/.../javareports?name=WSIHIST` → **`timed out`** (`game_model.md` içinde zaten erişilemedi notu var).
    - `lfweb.sjgov.org/EHD/0/doc/728929/Page133.aspx` → **HTTP 503** (sunucu geçici erişim hatası).
    - (`pubs.usgs.gov/of/2001/of01-35/pdf/ofr0135.pdf` bu makineden **HTTP 200** döndü.)

---

## 11. Son Senkronizasyon, `web3d/` Düzeltmeleri & `Q21` Çift-Yörünge Uyumu

- **`web3d/generate_3d_data.py` & `web3d/surfaces.json` (`13×13` NaN-farkındalıklı blok medyanı):** Eski `scipy.ndimage.median_filter(..., size=5)` çağrısı `NaN` pikselleri dikkate almadığı ve tek-piksel uç sıçramalar (`−10.78 cm` CV, `−6.59 cm` Karapınar) ürettiği için `cumulative.py` (`BLOCK_PX=13`, `BLOCK_MIN_VALID=0.5`, `BLOCK_MAX_STD=2.0`) ölçütüne birebir uyan `nan_tile_median` eklendi; yeniden üretilen `web3d/surfaces.json` (`508,115 B` / `496.2 KB`, sıfır `NaN`) artık `−7.79 cm` (CV) ve `−5.93 cm` (Karapınar) yüzey minimumlarıyla `summary.json` başlık değerleriyle (`−7.8 cm` / `−5.9 cm`) tam uyumlu.
- **`web3d/app.js` & `web3d/index.html`:** Referans/tepe pinleri ile 29 Karapınar obruk derinlik sütununun zaman kaydırıcısı veya dikey abartma değiştirildiğinde statik kalmayıp yerel yüzey yüksekliğini (`sampleSurfaceWorldY`) dinamik izlemesi sağlandı; ilk yükleme etiketleri (`-6 cm` / `+6 cm`) ve epok kaydırıcısı (`max="7" value="7"`) Central Valley verisiyle senkronize edilip alt bilgiye `7-Slide Deck` ve `Policy Game` bağlantıları eklendi.
- **`docs/story/pitch.md:30`:** Son kalan `"Aquifer Manager"` ifadesi `"Valley Under Pressure"` olarak düzeltildi; tüm `docs/story/` dokümanlarında eski oyun adı **0** adede indirildi.
- **`docs/story/judge_faq.md` (#2, #3, #4, #8), `pitch.md`, `slides.html`, `project_page.md`:** PC5 `uncertainty.md` (`0.66 cm` yerel çift RMS, `1.74–2.87 cm` zincir belirsizliği, SNR `2.7×–4.5×`, 5 aktif havza GNSS ortalama `0.86 cm` RMSE / `r = 0.81`) ve PC3 `Q21` (`bfc4f66`: Track 34 yükselen ↔ Track 114 alçalan, `6,719` 1 km blok, `r = 0.49` / yerel `0.60`, `|d| > 3 cm` alanlarda `%85` işaret uyumu, `< −6 cm` bölgelerde Track 114 medyanı `−5.7 cm`) bulgularıyla uyumlu hale getirildi.

---

## 12. Derinlemesine Hata Temizliği & PDF Satır-Satır Karşılaştırma

- **`docs/story/slides.html` (Ham Markdown & İşaret/Yön Düzeltmesi):** Slayt gövdesindeki `30` satırda yer alan ham Markdown backtick (`` `...` ``) ve bold (`**HTTP 200**`) sözdizimi düzgün HTML `<code>` / `<strong>` etiketlerine dönüştürüldü; Slide 3 ref boylamındaki eksi işaretli hatalı `°E` yön yazımı `119.1456°W` olarak düzeltildi.
- **`web3d/app.js` & `docs/story/video_shotlist.md`:** `web3d/app.js` içine `fmtLatLon(lat, lon)` eklenerek Central Valley gibi batı yarımküre koordinatlarının eksi işaretli `°E` yerine `36.4532°N, 119.1456°W` biçiminde gösterilmesi sağlandı (`video_shotlist.md:20` dahil `119.022°W` olarak düzeltildi).
- **`data/karapinar/sinkholes.geojson` ↔ Tapur & Bozyiğit (2015) PDF (`article-file/3454`, `pdftotext`):** İndirilen birincil PDF'teki tüm metin bölümleri ve Tablo 1 ile GeoJSON'daki **`29/29`** obruk (`lat`/`lon` DMS→ondalık, oluşum yılı, çap, derinlik, su durumu) programatik olarak birebir doğrulandı (`Büyükkarakuyu Şenyurt Obruğu` `2011` ve `Akviran Obruğu` `56 m` altı `24 m` su → `water-bearing` metin açıklamaları Tablo 1 yazım hatalarından ayırt edilerek teyit edildi; numarasız çiftçi bildirimli `37°46'10"N 33°31'35"E` Eşeli doğusu kaydı Tablo 1'deki 43 resmi obruk listesi dışında kaldığı doğrulandı).

---

## 13. `Q22` Dikey+Doğu-Batı Ayrıştırması, PC5 Piksel Belirsizlik Haritası, PC6 Doğrulama/Risk Raporları & PCQ Tur 2 `Q21` Satır-Satır Eşleme

- **`Q21` Satır-Satır JSON Doğrulaması (`analysis/out/cv_p34_vs_p114.json`):** `n_blocks_1km = 6719`, `pearson_r = 0.489`, `rmse_cm = 2.65`, `median_diff_cm = -1.29`, `slope_p114_vs_p34 = 0.514` değerleri [`docs/story/judge_faq.md`](../story/judge_faq.md), [`docs/story/pitch.md`](../story/pitch.md), [`docs/story/project_page.md`](../story/project_page.md) ve [`docs/story/slides.html`](../story/slides.html) içerisine birebir işlendi (`PCQ.md` Tur 2 §89 takibi tamamlandı).
- **`Q22` İki Geometri Dikey + Doğu-Batı Ayrıştırması (`data/central_valley/vertical.json`, `f9ce816`):** Track 34 Yükselen (`e = +0.64, u = 0.747`) + Track 114 Alçalan (`e = −0.60, u = 0.774`) birleşik çözümünden elde edilen **Alpaugh / Earlimart batı çanağı `−7.2 cm` dikey (`−0.1 cm` doğu-batı)** ve tepe blok `−9.8 cm` dikey (`+2.4 cm` doğu, `%49.6` ortak geçerli kapsama; `up_cm` `p2 = −5.98`, `p50 = −1.25`, `p98 = +2.35 cm`) bulguları tüm PC4 hikâye dokümanlarına eklendi.
- **PC5 Piksel Bazlı Cramér-Rao Faz Belirsizliği (`data/*/uncertainty/meta.json`, `acc6a10`) & PC6 Doğrulama/Risk Raporları (`823cb74`, `5248279`, `7369686`):** CV medyan **`0.294 cm`** / Karapınar medyan **`0.326 cm`** faz gürültüsü alt sınırı (`L = 208`), `10` GNSS istasyonu çapraz kesit uyumu (`r = 0.924`, final `RMSE = 1.37 cm`; `>2 cm` hareketli 4 istasyonda `0.76 cm` final RMSE / ort. zaman serisi `r = 0.851`), [`docs/story/validation_report.md`](../story/validation_report.md), [`docs/story/risk_dossier.md`](../story/risk_dossier.md) ve `docs/story/media/` 1080p MP4 animasyonları hikâye dokümanları ve bağlantılı paket listesiyle senkronize edildi.
- **Komşu Dosya QA Gözlemleri (yazma sınırı gereği PC4 dokunmadı):**
  - `data/central_valley/summary.json` (`0b49cab`) ile 3 referans penceresi aralığı `[−7.8, −4.7] cm` güncellendi (`project_page.md` ve `judge_faq.md` senkron); PC5 [`docs/story/uncertainty.md`](../story/uncertainty.md) ve PC6 [`docs/story/game_model.md`](../story/game_model.md) içindeki önceki `[−7.8, −6.2]` referans aralığı metinlerinin ilgili sahiplerince güncellenmesi önerilir.
  - PC6 [`docs/story/validation_report.md:21`](../story/validation_report.md#L21) içinde referans boylamı eksi işaretli sayı yanında yanlışlıkla `E` yarımküre eki taşıyor; `119.1456°W` olarak düzeltilmesi önerilir.

---

## 14. 15:00 Paketi #1 — NASA Earth Observatory Dil & Figür Kredisi Önerileri (`web/index.html`, `science.html`, `data.html`, `faq.html`)

*(Yalnızca öneri — `web/` dosyaları PC1 tarafından uygulanmak üzere değiştirilmedi.)*

| Dosya:Satır | Eski Metin | Yeni Öneri (NASA EO Stili) |
|---|---|---|
| `web/index.html:28–30` | `NASA Space Apps Challenge 2026 · Dancing with the SARs` / `<h1>The ground beneath our food is sinking.</h1>` / `up to 7.8 cm` | Künye satırı: `14 November 2026 · Team Taykut · Data: NASA-ISRO NISAR (provisional), ASF DAAC, NGL GPS, OpenStreetMap` · Başlık: `<h1>Satellite radar measures up to 7.8 cm of land subsidence in 108 days</h1>` · Alt metin: `up to 7.8 cm (line of sight, 28 Jun–14 Oct 2026)` |
| `web/index.html:38–43` | `Largest sinking measured... (line of sight, 108 days)` / `Same spot, estimated vertical motion` / `Largest sinking measured around Karapınar, Türkiye` | Birim+tarih netleştirme: `(line of sight, 28 Jun–14 Oct 2026)` · `Estimated vertical motion at peak (28 Jun–14 Oct 2026)` · `Peak line-of-sight subsidence near Karapınar, Türkiye (26 Jun–12 Oct 2026)` |
| `web/index.html:56–58` | `<h2>A radar that sees the ground move</h2>` | `<h2>Measuring centimetre-scale land motion from orbit</h2>`; ilk geçişte `line of sight (the slanted path between satellite and ground)` tanımını ekle |
| `web/index.html:64,72` | `<h2>Britain, under the clouds</h2>` / `Figure 1. Left: NASA VIIRS true colour (GIBS). Right: NISAR GCOV quick-look...` | `<h2>L-band radar images the UK Fens through cloud cover (20 Oct 2026)</h2>` · `Figure 1. Left: NASA VIIRS true-colour image over The Wash and the Fens, 20 Oct 2026 (NASA GIBS). Right: Same-day NISAR L2 GCOV radar quick-look (preview, not quantitative). Data: NASA GIBS and NASA-ISRO NISAR, ASF DAAC. Analysis: Team Taykut.` |
| `web/index.html:78,84` | `<h2>The dancing ground</h2>` / `Figure 2. Cumulative line-of-sight motion from 7 consecutive...` | `<h2>Central Valley subsided up to 7.8 cm in 108 days</h2>` · `Figure 2. Cumulative line-of-sight displacement across the Central Valley, 28 Jun–14 Oct 2026 (7 consecutive NISAR L2 GUNW pairs, Track 34; negative = motion away from satellite). Data: NASA-ISRO NISAR, ASF DAAC. Analysis: Team Taykut.` |
| `web/index.html:89,93` | `<h2>Does it match the ground?</h2>` / `Figure 3. Vertical estimate (LOS / cos incidence) vs GPS "up"...` | `<h2>Validation against 10 continuous GPS stations (median RMSE 1.0 cm)</h2>` · `Figure 3. NISAR vertical estimate (LOS / cos θ) compared with daily GPS vertical positions at 10 stations, 28 Jun–14 Oct 2026 (RMSE in cm). Data: NASA-ISRO NISAR (ASF DAAC) and Nevada Geodetic Laboratory. Analysis: Team Taykut.` |
| `web/index.html:98,102` | `<h2>When the ground tilts, canals fail</h2>` / `Figure 4. Risk = sinking gradient...` | `<h2>Differential subsidence tilts 81 of 645 infrastructure segments</h2>` · `Figure 4. Subsidence gradient (mm/km) and cumulative displacement along 645 canal, road and rail segments, 28 Jun–14 Oct 2026. Data: NASA-ISRO NISAR (ASF DAAC) and OpenStreetMap contributors (ODbL). Analysis: Team Taykut.` |
| `web/index.html:107,110` | `<h2>Konya's sinkholes</h2>` / `Figure 5. NISAR cumulative motion (track 7, 8 pairs)...` | `<h2>Karapınar subsided up to 5.9 cm near 29 documented sinkholes</h2>` · `Figure 5. Cumulative line-of-sight displacement around Karapınar, 26 Jun–12 Oct 2026 (8 NISAR L2 GUNW pairs, Track 7), overlaid with 29 documented sinkholes. Data: NASA-ISRO NISAR (ASF DAAC) and Tapur &amp; Bozyiğit (2015). Analysis: Team Taykut.` |
| `web/index.html:121,123,141` | `<h2>Why pumped ground does not come back</h2>` / `That is the "dance" NISAR records...` / `Figure 6. Schematic (not to scale).` | `<h2>Elastic seasonal rebound versus permanent clay compaction</h2>` · `"NISAR records this cycle as summer subsidence followed by partial winter recovery."` · `Figure 6. Cross-section of confined aquifer drainage and clay compaction (schematic, not to scale). Graphic: Team Taykut.` |
| `web/index.html:150` | `<h2>Valley Under Pressure</h2>` | `<h2>Two-year groundwater and subsidence simulator</h2>` |
| `web/index.html:161,164,165` | `<h2>How we know</h2>` / `(−λ/4π·φ)` | `<h2>Data, processing pipeline and measurement limits</h2>`; L164 formül yerine sade ifade: `scaled by the 24 cm radar wavelength; equations in Science`; L165: `dual-orbit Track 34 vs Track 114 (Q21/Q22) validation` ve 3-referans aralığı (`−4.7 to −7.8 cm`) bilgisini ekle |
| `web/science.html:25,31,34,38` | `SME2 ... (in progress)` / `coherence` / `connected component` / `between −6.2 and −7.8 cm` | `SME2`: `Regional soil-moisture context (data/central_valley/drivers.json, 28 Jun–14 Oct 2026)`; ilk geçişte `coherence (pixel-to-pixel phase stability, 0 to 1)` ve `connected component (contiguous unwrapped region)` tanımlarını ekle; L34 aralığını `between −4.7 and −7.8 cm (line of sight across 3 stable reference areas ≥ 30 km apart)` (`summary.json`) yap; `#valTable` altına kaynak/figür satırı + `Q21/Q22` çift-yörünge paragrafı (`Track 34 ascending vs Track 114 descending, 6,719 1 km blocks, 85% sign agreement on \|d\| > 3 cm; Alpaugh bowl −7.2 cm vertical in data/central_valley/vertical.json`) ekle |
| `web/data.html:17,27–38` | `<h1>Every number, downloadable</h1>` / `F` tablosu (11 satır) | `<h1>Processed datasets and metadata</h1>`; `const F` içine `data/central_valley/vertical.json`, `data/central_valley/uncertainty/meta.json`, `data/central_valley/drivers.json`, `data/central_valley/gcov/meta.json` ve `data/karapinar/assets.json` satırlarını ekle |
| `web/faq.html:16–17` | `<p class="kicker">Questions</p><h1>Frequently asked</h1>` | `<p class="kicker">Technical Q&amp;A</p><h1>Frequently asked questions</h1>` |

---

## 15. `15:00 Paketi (#2–4)` Uygulama Kaydı (`judge_faq`, `pitch`, `project_page`, `slides.html`, `video_shotlist`)

- **Yasaklı Kelime & İç Not Temizliği (`REVIEW_1500.md`):** `judge_faq.md` üstündeki `# Jury Q&A Card` ve `> Every statistic...` iç kullanım bloğu kaldırılarak `web/faq.html` içinde doğrudan `### 1.` ile temiz başlaması sağlandı (`12` Karapınar noktası güncellendi); `pitch.md`, `project_page.md`, `slides.html` içindeki `crystal-clear`, `Empowering`, `Hackathon Journey`, `vital`, `Zero AI` ifadeleri, yapay gradyanlar ve gereksiz rozetler NASA Earth Observatory olgusal stiliyle değiştirildi.
- **`slides.html` Gerçek Veri Görselleri & `Figure 1–8` Kredileri:** `docs/story/media/risk_1.png` (`Figure 4`, Tulare Kanalı profili), `docs/story/media/validation_scatter.png` (`Figure 5`, 10 istasyon `r = 0.924`) ve `docs/story/media/gnss_CAHA.png` (`Figure 6`, `CAHA RMSE 0.75 cm`) gömüldü; tüm 7 slaytta tarih, birim ve `Data: ... Analysis: Team Taykut.` kaynak satırları eklendi.
- **`video_shotlist.md` Site v2 Bölüm Uyumu:** Çekim listesi güncel `web/index.html` bölümlerine (`Story` Bölümleri 1–6 `[data-step="intro|uk|cv|gnss|risk|kp"]`, `Simulator` `#play/#gameFrame` ve `Science` `science.html` `#conv/#valid/#limits`) göre güncellendi.

---

## 16. PC5 Duyarlılık / Literatür Senkronizasyonu, `web/docs.js` İşleme Düzeltmesi ve `27/27` Bağlantı Doğrulaması (`4c098e8` Sonrası)

- **PC5 Raporları Entegrasyonu (`9eece9c`, `eefb665`, `3475cb1`, `519e428`):**
  - [`docs/story/key_findings.md`](../story/key_findings.md): Etkilenen ayak izi alanları (`258.7 km² <= −5 cm`, `1,673.9 km² <= −2 cm` CV; `3.1 km² <= −5 cm`, `49.1 km² <= −2 cm` Karapınar), hareketli (`n = 5`, medyan `RMSE 0.834 cm`, `r = 0.820`; iç havza `n = 4` medyan `0.800 cm`) vs. durağan (`n = 5`, `1.570 cm`) GNSS ayrımı ve `drivers.json` nem-çökme bağıntıları (`r = 0.654` `irrigation_index`, `r = 0.638` 12 günlük `lag-1` `SME2`) [`judge_faq.md`](../story/judge_faq.md) ve [`project_page.md`](../story/project_page.md) içine eklendi.
  - [`docs/story/risk_sensitivity.md`](../story/risk_sensitivity.md): `±25%` eşik duyarlılık analizinin (`72–115` yüksek riskli segment aralığı) ilk 10 öncelikli altyapı koridoru sırasını (`42.34–57.01 mm/km`) **%100 değişmez (`invariant`)** bıraktığı [`judge_faq.md`](../story/judge_faq.md), [`pitch.md`](../story/pitch.md), [`project_page.md`](../story/project_page.md) ve [`slides.html`](../story/slides.html) (`Figure 4`) dosyalarına işlendi.
  - [`docs/story/game_sensitivity.md`](../story/game_sensitivity.md) & [`game_sensitivity.png`](../story/game_sensitivity.png): Terra Bella kalibrasyon çarpanı (`k = 0.6232`, `b0 · S_skv ≈ 0.02356`) ve `N = 1,000` Monte Carlo simülasyon dağılımı (`108` gün `p10–p90` `−13.69` to `−4.12 cm`; `24` ay `−18.69 cm` nominal / stokastik `p10–p90` `−27.10` to `−6.23 cm`) [`judge_faq.md`](../story/judge_faq.md), [`pitch.md`](../story/pitch.md), [`project_page.md`](../story/project_page.md) içine eklendi ve [`slides.html`](../story/slides.html) Slayt 6'ya `Figure 9` olarak yerleştirildi.
  - [`docs/story/literature_comparison.md`](../story/literature_comparison.md): Hakemli 5 makale ([Neely et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8047915/), [Ojha et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6559157/), [Orhan et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7865528/), [Üstün et al. 2010](https://nhess.copernicus.org/articles/10/1151/2010/), [Canaslan Çomut et al. 2015](https://isprs-archives.copernicus.org/articles/XL-1-W5/115/2015/)) canlı `HTTP 200` doğrulamasıyla [`sources.md`](../story/sources.md), [`project_page.md`](../story/project_page.md) ve [`judge_faq.md`](../story/judge_faq.md) kaynakçasına eklendi (toplam **27** doğrulanmış harici kaynak URL'si).
- **`web/docs.js` Render Temizliği & Video Shotlist (`4c098e8`):**
  - `web/docs.js` (`strip = true`) üstteki `> ...` blok alıntılarını sildiği için [`calibration_note.md`](../story/calibration_note.md), [`sources.md`](../story/sources.md) ve [`sinkhole_timeline.md`](../story/sinkhole_timeline.md) içindeki `Calibration Notice` / `Mandatory Attribution` satırları düz bold paragrafa çevrilerek `web/science.html` ve `web/data.html` üzerinde görünürlükleri korundu; [`submission_rules.md`](../story/submission_rules.md) içindeki iç etiketler/yasaklı kelime temizlendi ve [`video_shotlist.md`](../story/video_shotlist.md) yeni `#watch` (`#cvVideo`, `Figure 0`) ile `web/science.html` (`#findings`, `#lit`, `#unc`, `#vreport`, `#dossier`) çapa bağlantılarına hizalandı.

---

## 17. PC7 Veri Sözleşmesi Bulgusu Çözümü (`data/karapinar/sinkholes.geojson` `quality` & `quality_note`)

- **PC7 Denetim Bulgusu (`4c4506d` / [`docs/qa/PC7.md`](PC7.md)):** `VERI_SOZLESMESI.md` §3 ("Her JSON çıktıda `quality` alanı ve kısa `quality_note` (İngilizce) bulunur") gereği `data/karapinar/sinkholes.geojson` kökünde eksik raporlanan iki alan, [`web/data.html`](../../web/data.html) mantığıyla birebir uyumlu olacak biçimde **`"quality": "reference"`** ve kaynaklı İngilizce **`"quality_note"`** (*Tapur & Bozyiğit 2015*) olarak eklendi; `29` Feature yapısı, MapLibre uyumu ve `offline_site_qa.quality_scope` kontrolü (`root` / `root`) doğrulandı.

---

## 18. `Q09` Birleşik Krallık Kil (`data/uk_clay/detection.json` `"below_detection"`) & `key_findings_public.md` Senkronizasyonu (`91dbd77`, `13f1991`)

- **Negatif Kontrol Entegrasyonu (`Q09` / [`docs/qa/PC3.md`](PC3.md)):** PC3 tarafından eklenen 9 çiftlik Londra kil bölgesi provisional GUNW analizi (`2026-06-21` → `2026-10-19`, `120` gün, Track 101 ascending frame 28, `data/uk_clay/detection.json`) doğrulanan kesin değerleriyle [`judge_faq.md`](../story/judge_faq.md) (Soru 6), [`project_page.md`](../story/project_page.md) (Nicel Sonuçlar tablosu) ve [`slides.html`](../story/slides.html) (Slayt 2 Birleşik Krallık kartı) içine işlendi:
  - `status: "below_detection"`, `chain_sigma = 1.21 cm`, `3σ` algılama eşiği `= 3.62 cm`; kuadratik atmosfer giderimi sonrası 1 km blokların **`%97.7`'si (`%98`) `±1.5 cm` içinde** (`p2/p50/p98 = −1.47 / +0.19 / +1.26 cm`), iç bölgede eşiği aşan blok sayısı **`0`** ve sahne kenarından `2.0 km` içerideki ham `−5.29 cm` değeri kenar atmosfer artefaktı olarak açıklandı.
- **`key_findings_public.md` Bağlantısı (`13f1991`):** PC5'in kamuya açık bulgu özeti [`docs/story/key_findings_public.md`](../story/key_findings_public.md), [`project_page.md`](../story/project_page.md) Eşlik Eden Teslim Paketi listesine eklendi.
- **Ek Stil Düzeltmesi:** `judge_faq.md` Soru 6 içinde kalan yasaklı `showcase` kelimesi `compare` ile değiştirilerek sıfır yasaklı kelime kuralı (`docs/REVIEW_1500.md`) tam korundu.

---

## 19. PC5 Etkilenen Alan Zaman Serisi (`area_stats.json`) & Obruk Permütasyon / Küme Kaydırma Testi (`sinkhole_stats.md`) Senkronizasyonu (`f215bc8`, `c4e8553`)

- **`area_stats.json` Ortak Geçerli Piksel Ayak İzleri (`f215bc8`):** Central Valley (`1,203,856` ortak geçerli `80 m` piksel = `7,704.68 km²`, `239.54 km² <= −5 cm` & `1,578.27 km² <= −2 cm`; zirve `1,661.49 km²` `2026-09-20`) ve Karapınar (`33,169` piksel = `212.28 km²`, `3.10 km² <= −5 cm` & `28.66 km² <= −2 cm`) zaman serisi değerleri [`project_page.md`](../story/project_page.md), [`pitch.md`](../story/pitch.md) ve [`slides.html`](../story/slides.html) içine işlendi; tek-epok kümülatif maskeyle (`summary.json`: `258.7 / 1,673.9 km²` CV ve `49.1 km²` Karapınar) farkı açıklandı. [`docs/story/media/pc5_area_cv.png`](../story/media/pc5_area_cv.png) eşlik eden medya paketine eklendi.
- **`sinkhole_stats.md` & `pc5_sinkhole_perm.png` Dört Katmanlı Anlamlılık Testleri (`c4e8553`):** `40,194` geçerli Karapınar pikselinde `0–2 km` obruk kuşağının (`n = 236` px, `16` koherent obruk, ort. `−4.06 cm`) `>5 km` arka plandan (`−0.65 cm`) `−3.41 cm` daha derine çöktüğünü kanıtlayan **ayrık `1.04 km` (`13×13 px`) blok permütasyon/Welch testleri (`−3.04 cm` fark, `p = 0.0001`, Welch `p = 9.7 × 10⁻⁸`)**, **`2.08 km` makro-blok testi (`−2.93 cm`, `p = 0.0001`)** ve **`3,423` katı `29`-obruk küme kaydırması (`p = 0.0207`)** [`sinkhole_timeline.md`](../story/sinkhole_timeline.md), [`judge_faq.md`](../story/judge_faq.md), [`project_page.md`](../story/project_page.md), [`pitch.md`](../story/pitch.md) ve [`slides.html`](../story/slides.html) Slayt 5'e entegre edildi.

---

## 20. Hata Düzeltme & Son Commit Senkronu (`38b774f` Sıfır AI Görseli, `drivers_analysis.md`, `#cvPlay` & `demo_30s.mp4`)

- **Eski `web/assets/` AI Görsel İddiaları Kaldırıldı (`38b774f`):** Commit `38b774f` kullanılmayan 7 Higgsfield AI görselini `web/assets/` altından tamamen sildiği (`web/faq.html` artık sitede AI görseli olmadığını beyan ettiği; `web/assets/simulator.jpg` yalnızca gerçek oyun ekran görüntüsü olduğu) doğrulandı; [`judge_faq.md`](../story/judge_faq.md) (Soru 15), [`project_page.md`](../story/project_page.md), [`pitch.md`](../story/pitch.md) (Slayt 7), [`slides.html`](../story/slides.html) (Slayt 7 — ayrıca `22/22` → `27/27` PC4 / `29/29` repo URL sayımı güncellendi) ve [`submission_rules.md`](../story/submission_rules.md) üzerindeki eski AI görsel ifadeleri ve `{...}` yer tutucu notları temizlendi.
- **`drivers_analysis.md` İstatistiksel Güç Şerhi (`2a22266`):** `r = 0.654` (`irrigation_index`) ve `r = 0.638` (`lag-1 SME2` nem) değerlerinin `N = 8` epokta (`|r_krit| = 0.707–0.754`, `%80` güç `>= 0.849`) kesin permütasyonda **`p_perm = 0.088`** ve **`0.130`** ile `α = 0.05` altında anlamlı olmadığı ve trendden arındırılmış hızlarda (`Δd/Δt`, `n = 7`) `r = 0.037–0.130` (`p >= 0.81`) kaldığı şerhi [`judge_faq.md`](../story/judge_faq.md) (Soru 5) ve [`project_page.md`](../story/project_page.md) içine eklendi.
- **Canlı Video (`demo_30s.mp4`, `365f767`) & `#cvPlay` Seçicisi (`47ed18a`):** `web/index.html` üzerinde `#cvPlay` olarak değişen zaman kaydırıcısı düğmesi ve yeni `#ukClay` / `#ringBox` / `#ringChart` bölümleri [`video_shotlist.md`](../story/video_shotlist.md) ve [`pitch.md`](../story/pitch.md) içinde güncellendi; PC6 tarafından derlenen `29.62 s` (`1080p`, `3,482,862 B` son güncelleme `ef20069`) [`docs/story/media/demo_30s.mp4`](../story/media/demo_30s.mp4) dosyası [`video_shotlist.md`](../story/video_shotlist.md), [`project_page.md`](../story/project_page.md) ve [`pitch.md`](../story/pitch.md) ile ilişkilendirildi.

---

## 21. `16:05 ACİL`, `16:15 CHALLENGE UYUMU` & `16:25 KAYNAKLAR ENTEGRASYONU` Doğrulama Kaydı

- **`16:05 ACİL` Lincoln Sunum Paketi:** `docs/story/presentation_cues.md` (`6 × 30 sn` konuşma/tıklama blokları, Kerem / Memir / Mehmet & İbrahim rol paylaşımı, ilk 5 jüri sorusuna tek cümlelik yanıt) ve `docs/story/rehearsal_checklist.md` (çevrimdışı `demo_30s.mp4` / `cv_subsidence.mp4` / `slides.html` / yerel HTTP yedekleri, 1–6 sekme sırası, ekran/ses ve `2:30` zamanlama disiplini) hazırlandı.
- **`16:15 CHALLENGE UYUMU` (#1–#6, `docs/CHALLENGE_UYUM.md`):**
  - `A5` Kitleler: [`docs/story/audiences.md`](../story/audiences.md) (5 hedef kitle — bilim insanı, su/kanal yöneticisi, eğitimci, karar verici, halk — için ne bulur & ne yapabilir somut kaynaklı 2'şer cümle).
  - `A13` Gelecek Uygulamalar: [`docs/story/future_applications.md`](../story/future_applications.md) (NISAR Applications White Papers & Handbook kaynaklı 7 somut uygulama maddesi).
  - `A7 / B6` Ekip Bölgesel Hikâyesi: [`docs/story/team_story.md`](../story/team_story.md) (en üstte `TASLAK — ekip kendi cümleleriyle düzeltecek` uyarısı ile Ankara merkezli ekibin Konya–Karapınar obrukları, [Tapur & Bozyiğit 2015](https://dergipark.org.tr/tr/download/article-file/3454) ve [Orhan et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7865528/) kaynaklı bağlamı — sıfır uydurma kişisel anı).
  - `A5` Eğitimci Materyali: [`docs/story/lesson_plan.md`](../story/lesson_plan.md) (40 dakikalık lise ders planı, *Valley Under Pressure* simülatör laboratuvarı, 5 sayısal değerlendirme sorusu + tam cevap anahtarı + NASA ARSET / Intro to SAR öğrenme bağlantıları).
  - `C` & `#6` Challenge Anahtar İfadeleri: [`docs/story/sources.md`](../story/sources.md) §7 ve [`docs/story/project_page.md`](../story/project_page.md) / [`docs/story/pitch.md`](../story/pitch.md) dosyaları `interactive application`, `track and visualize surface change`, `actionable insights`, `patterns and rhythms`, `physical drivers`, `future applications` anahtar ifadeleri ve 11 aylık Earlimart ayrıştırmasıyla (`fullyear.md`) hizalandı.
- **`16:25 KAYNAKLAR ENTEGRASYONU` (`docs/KAYNAKLAR_ANALIZI.md` §1–4):**
  - [NASA NISAR Land Subsidence StoryMap](https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828) (Peacock et al. 2024; 2013–2017 UAVSAR Central Valley & California Aqueduct → 2026 spaceborne NISAR çerçevesi), 6 NISAR Societal Benefits White Paper PDF'i (`Subsidence`, `Drought_and_Groundwater_Withdrawal1`, `Levees_and_Dams1`, `Sinkholes1`, `Food_Security1`, `NISARApplications_SoilMoisture1`), ASF NISAR Data User Guide, ASF Vertex, Earthdata Search, Intro to SAR, Intro to Remote Sensing, NASA ARSET Trainings, UAVSAR Postcards ve CSA SAR Tutorial bağlantıları canlı **`HTTP 200`** ile doğrulanarak [`docs/story/sources.md`](../story/sources.md), [`docs/story/project_page.md`](../story/project_page.md), [`docs/story/pitch.md`](../story/pitch.md), [`docs/story/audiences.md`](../story/audiences.md), [`docs/story/future_applications.md`](../story/future_applications.md) ve [`docs/story/lesson_plan.md`](../story/lesson_plan.md) içine işlendi.

---

## 22. Lincoln Sunum Birleştirmesi & `A2 / A12 / B1 / B3` Eşgüdümlü Çıktı Senkronu (`a438ea3` + Step B)

- **`presentation_cues.md` & `rehearsal_checklist.md` Canlı Site DOM Birleştirmesi (`a438ea3`):** `web/index.html` üzerindeki gerçek etkileşim öğeleri (`#heroMap`, `.stats`, `#watch` / `#cvVideo`, `#compareRange`, `#polBox` / `#polChart` `data/fens/crops.json`, `#ukClay` `±3.6 cm`, `#cvPlay`, `#fyBox` + `explorer.html#central_valley_fullyear`, `.storymap`, `#gnssTable`, `#riskList`, `#ringChart`, `#sinkList`, `#why`, `#who`, `#play` / `#gamePlay`, `#next`, `#how`, `game/index.html` `2. Multi-Year Drought`, `web3d/index.html` + `demo_30s.mp4`, `slides.html`, `python3 -m http.server 8000/8765`, `2:30` / `2:50` sert kesme eşikleri) doğrudan `data/*/summary.json` ölçümleriyle tek pakette birleştirildi ve push edildi.
- **Yeni Challenge Çıktılarının (`A2`, `A12`, `B1`, `B3`, `uk_findings.md`) PC4 Dokümanlarına İşlenmesi:**
  - **`B1` (`docs/story/cross_sensor.md`, `data/central_valley_s1/cross_sensor.json`):** NISAR L-band (`24.20 cm`, `12.10 cm` saçak, Tulare tarım çekirdeğinde yaz aylarında `%80.4` geçerli piksel koheransı, `5` çekirdek GPS `RMSE = 0.823 cm`) vs. Sentinel-1/RCM C-band (`5.55 cm`, `2.77 cm` saçak; `OPERA_L3_DISP-S1_V1` arşivi `2026-04-26`'da bitiyor) [`judge_faq.md`](../story/judge_faq.md) Soru 10, [`slides.html`](../story/slides.html) Slayt 2, [`project_page.md`](../story/project_page.md) ve [`pitch.md`](../story/pitch.md) içine işlendi.
  - **`A12` (`docs/story/polarization.md`, `data/fens/crops.json`) & `B3` (`docs/story/exposure.md`):** Birleşik Krallık Fens'te `4` tarlada `HH`'nin `HV`'den `~7 dB` parlak oluşu (`4.27` vs `3.49 dB` zaman aralığı) ile WorldPop/USDA CDL/ESA WorldCover kesişimi (`> 2 cm` LOS alanda **`83,273` sakin** — `71,701` CV + `11,572` Karapınar — ve CV `> 2 cm` alanının **`%79.2`'si / `1,251.37 km²`'si tarım arazisi**) [`judge_faq.md`](../story/judge_faq.md) Soru 11, [`slides.html`](../story/slides.html) Slayt 2, [`project_page.md`](../story/project_page.md) ve [`pitch.md`](../story/pitch.md) içine eklendi.
  - **`A2` Meksiko (`data/global/mexico_city/summary.json`):** `8` provisional çift (`2026-06-22 → 2026-10-20`), `−4.4 cm` LOS zirve / `−6.2 cm` dikey kestirim verisi 4. bölge ölçeklenebilirlik örneği olarak [`judge_faq.md`](../story/judge_faq.md) Soru 6, [`project_page.md`](../story/project_page.md) ve [`pitch.md`](../story/pitch.md) dosyalarına eklendi.
  - **Kaynak & Hijyen Doğrulaması:** [`docs/story/sources.md`](../story/sources.md) sonuna NASA SERVIR `SAR Handbook Ch. 2` (`https://earthdata.nasa.gov/s3fs-public/2025-04/SARHB_CH2_Content.pdf`) ve USDA NASS CDL (`https://www.nass.usda.gov/Research_and_Science/Cropland/SARS1a.php`) eklendi; `sources.md` içindeki **`43/43` benzersiz HTTPS bağlantısının tamamı canlı `HTTP 200`** verdi ve yasaklı kelime/doğruluk şerhi taramaları temiz geçti (`judge_faq.md` Soru 15 ve `slides.html` Slayt 7 güncellendi).

---

## 23. `20:00` + `20:10` (`OZGUN_KATKILAR.md` §T) + `REVIEW_1500` Hijyen Taraması & `O1` Entegrasyonu

- **`20:00` Çıktıları (`project_page.md`, `slides.html`, `judge_faq.md`):**
  - [`docs/story/project_page.md`](../story/project_page.md) `−20.3 cm` / `mixed` tam yıl (`2025-10-20 → 2026-10-21`), Sacramento–San Joaquin Delta (`−1.8 cm`), Konya Kapalı Havzası (`−4.5 cm`), `4` küresel şehir (`Tokyo −2.2`, `Jakarta −2.9`, `Venice −1.0`, `Mexico City −4.4 cm`), `B1` C-band vs L-band (`%80.4`), `B3` nüfus/tarım maruziyeti (`141,555` sakin, `%79.2` tarım), `Q09` Londra kil `below_detection` ve `6` Challenge anahtar ifadesiyle son haline getirildi.
  - [`docs/story/slides.html`](../story/slides.html) tam `7` slayt + `@media print` A4 PDF CSS + canlı site & GitHub depo bağlantıları + `O1` (`0.317 km³/yr`) dahil özgün katkı özetiyle güncellendi.
  - [`docs/story/judge_faq.md`](../story/judge_faq.md) Soru 11 `141,555` sakin olarak güncellendi; **Soru 16–20** (`mixed` beta tam yıl şerhi, Delta, 4 küresel şehir, C-band vs L-band, maruziyet sınırları) eklendi.
  - [`docs/story/team_story.md`](../story/team_story.md) en üstündeki `TASLAK — ekip kendi cümleleriyle düzeltecek` uyarısı korundu.
- **`20:10` (`OZGUN_KATKILAR.md` §T) Teknik Not:** [`docs/story/technical_note.md`](../story/technical_note.md) ve yazdırılabilir A4 [`docs/story/technical_note.html`](../story/technical_note.html) oluşturuldu (`Abstract`, `1 Data`, `2 Methods`, `3 Validation`, `4 Uncertainty`, `5 Results`, `6 Original Contributions O1–O3`, `7 Limitations`, `Verified References`).
- **`O1` Entegrasyonu (PC8):** `data/central_valley_fullyear/storage_loss.json` ve `docs/story/storage_loss.md` yayına alındıktan hemen sonra **`0.3174 km³/yr`** (`317.41 million m³/yr`, duyarlılık `0.0664–0.3198 km³/yr`, `4,508.29 km²`, ortalama `7.04 cm/yr`, `~0.49×` Millerton Gölü `0.642 km³`, `quality: mixed`) gerçek değerleri `technical_note.md`, `technical_note.html`, `project_page.md` ve `slides.html` içine işlendi (`O2` ve `O3` üst akışları bekleniyor).
- **`REVIEW_1500` Hijyen Taraması (PC4 vs. Diğer PC Dosyaları):**
  - **PC4 dosyaları düzeltildi:** `team_story.md` (L24–25 `validated` → `compared` / kaldırıldı), `future_applications.md` (L6, L18 `validated` → `operational`), `pitch.md` (L61/L152 `calibrated` → `matched`, L142 `Ground Truth` → `GPS Comparison`), `sources.md` (L118 `confirming` → `showing`), `project_page.md` (L50 `calibrated` → `matched`, L102 `ground-truth` → `GPS-reference`).
  - **Kardeş PC dosyalarında tespit edilen ifadeler (kapsam gereği dokunulmadı; sahiplerinin düzeltmesi için not edildi):**
    - `docs/story/cross_sensor.md` L21: `ground truth`
    - `docs/story/fullyear.md` L63: `calibrated`
    - `docs/story/key_findings.md` L15: `calibrated`
    - `docs/story/game_sensitivity.md` L10, L35: `calibrated`, `proves`
    - `docs/story/narration_script.md` L28, L41: `confirming`, `validated`
    - `docs/story/slides_notes.md` L25, L33, L48, L54: `proven`, `confirming`, `calibrated`
    - `docs/story/submission_form.md` L33: `validated`

---

## 24. Atlas İkinci Tur (PC4 #5–9) & C05 Erken Uyarı Bültenleri Senkronu (`2026-11-14 23:00 TR`)

- **12 Atlas Şehir Kartı ([`docs/story/atlas_cities/`](../story/atlas_cities)):**
  - Tamamlanan şehir kartları: `central_valley.md`, `konya_plain.md`, `karapinar.md`, `jakarta.md`, `mexico_city.md`, `delta.md`, `isfahan.md`, `rafsanjan.md`, `bangkok.md`, `ho_chi_minh.md`, `tehran.md`, `beijing.md`.
  - Her kart $\le 150$ kelime; jeolojik çökme etmeni (kil, akifer boşalımı, turba oksidasyonu), etkilenen nüfus ve altyapı koridorları, hakemli literatür hızları (DOI linkleriyle), NISAR L-band ölçümü (`cm/100d`, dönem, geçerli piksel, güven sınıfı) ve NISAR'ın katkısı içerir.
  - PC5 onayı olmayan sayılara açıkça `preliminary` şerhi düşülmüştür.
- **Atlas Yöntem Belgesi ([`docs/story/atlas_methods.md`](../story/atlas_methods.md)):**
  - Standart $\pm 0.25^\circ$ kutu, $1\text{ km}$ blok medyan ve $p_2$ filtreleme, sıralamada dönemden bağımsız `rate_cm_per_100d` seçilme gerekçesi, havza dışı kayaç referans seçimi ve duyarlılık oranı, güven sınıflandırması (§4), LOS-dikey geometrisi, provisional kalibrasyon şerhi ve `pipeline.nisarpulse` CLI komutları tek sayfada belgelendi.
- **Atlas Veri Sözlüğü ([`docs/story/atlas_data_dictionary.md`](../story/atlas_data_dictionary.md)):**
  - `data/global/atlas.json` dosyasındaki üst düzey şema ve 22 bölgesel anahtarın tamamı (alan adı, tipi, birimi, anlamı, formülü ve örnek değerleri) belgelendi.
- **Jüri Atlas Zor Soruları ([`docs/story/judge_faq.md`](../story/judge_faq.md) #22–26):**
  - 5 zor atlas sorusu (#22 sıralama literatür farkı, #23 108 gün yıllık hızı temsil eder mi, #24 tropik koherens ve muson gecikmesi, #25 referans seçimi ve hassasiyeti, #26 ilk ölçüm iddiaları) bilimsel temelleriyle eklendi.
- **C05 — Erken Uyarı Bültenleri Üretimi ([`docs/bulletins/`](../bulletins/)):**
  - `tools/bulletin.py` çalıştırılarak atlas.json'daki 11 bölgenin tamamı için güncel HTML bültenleri (`konya_plain.html`, `central_valley.html`, `jakarta.html`, `bangkok.html`, `mexico_city.html`, `karapinar.html`, `ho_chi_minh.html`, `tehran.html`, `isfahan.html`, `beijing.html`, `delta.html`) ve `index.html` (11 bültenlik liste) üretildi.
- **Kalite Standartları ve Hata Ayıklama:**
  - `data/numbers_registry.json` içine eksik `"quality": "provisional"` alanı eklenerek `pipeline/pc7/validate_json.py` testinin 106 dosyanın tamamında 0 hata ile geçmesi sağlandı.

### 27. Bilimsel Tutarlılık & Sayı Senkronu Bulguları (Paz 03:05 Ataması — Başkalarının Dosyaları)
- `docs/story/global_atlas.md:32` (Sahip: **PC10**): `analysis/pc5/numbers_registry.py` çıktısı hâlâ eski Mexico City havza-içi referans değerini (`-4.4 cm`) raporluyor; güncel `data/global/mexico_city/summary.json` (volkanik kayaç ref.) **`-7.0 cm` LOS (`-5.8 cm/100d`)** ile güncellenmeli.
- `docs/story/atlas_validation.md` (Sahip: **PC5**): Önceki 9–13 şehirlik tabloyu içeriyor; `docs/story/atlas_top5_check.md` (PC1) ve `data/global/atlas.json` (21 bölge) ile senkronize edilmeli.

### 28. ATLAS v2 (`12dcc5c`) Gözlemleri & ENTEGRASYON (`2026-11-15 01:37 TR`)
- `data/global/atlas.json` (`12dcc5c`, PC10): `central_valley` (`rank: 11`, `rate_cm_per_100d_common: -7.3`, `rate_ci_cm_per_100d: [-7.2, -2.3]`, `robustness_spread: 5.3362`, `valid_fraction: 0.629`) beklenmedik biçimde `confidence: "low"` / `indicative_only: true` olarak işaretlenmiş; oysa `data/global/central_valley/validation_note.json` içinde `"recommended_confidence": "medium"` yer alıyor (`build_atlas.py` yalnızca `validation_note.json`'daki `"confidence"` alanını okuyor ve `data/central_valley/` altında `validation_note.json` yok). **PC10/PC1** bu düşüşün kasıtlı olup olmadığını doğrulamalı.
- `data/results_registry.json`: PC4'e ait `atlas_feature`, `calibration`, `technical_note` satırları `summary` ve `key_number` alanlarıyla dolduruldu (`status: ready`).
- `docs/story/{atlas_feature,press_summary,technical_note,judge_faq}.md`, `technical_note.html`, `slides.html` ve `docs/qa/SCIENCE_SIGNOFF.md` **ATLAS v2** (`21` bölge, `9` reliable / `12` indicative, ortak `93` günlük pencere, `Semarang` `10-11` faz sıçraması temizlenip `-6.2 cm` #5 reliable, `Cangzhou` #7 `-2.4 cm`) ile senkronize edildi.

### 29. 29-Bölge Atlas Tamamlama & `pytest` Hata Analizi (`2026-11-15 09:13 TR`)
- **PC7 kırılan test (`pipeline/pc7/tests/test_atlas_robustness.py:43`):** `test_subset_override_parses_city_path_without_network` Linux POSIX ortamında başarısız oluyor (`Path(r"C:\scratch\global_beijing").as_posix()` Linux'ta ters eğik çizgileri `/` yapmadığı için `'C:\\scratch\\global_beijing' != 'C:/scratch/global_beijing'`). `94 passed, 1 failed`. **PC7** `PureWindowsPath` veya `os.name == "nt"` kontrolü ile düzeltmeli.
- **8 yeni şehir kartı (`docs/story/atlas_cities/`):** `kashmar.md`, `kerman.md`, `houston.md`, `can_tho.md`, `tianjin.md`, `lagos.md`, `gorgan.md`, `pekalongan.md` (`<= 150` kelime, hakemli DOI kaynaklı, `provisional` şerhli) yazıldı; `tools/atlas_completeness.py` üzerinde **PC4: 0 missing** (`29/29` şehir tamam).
- **8 yeni `validation_note.json` (`data/global/<id>/`):** Aynı 8 şehir için DOI + literatür kıyası + `gorgan`/`pekalongan` `phase_cycle_jump` QC gerekçeleriyle yazıldı (`"reviewed_by": "pending PC5"`), `PC5` eksiği `11`'den `3`'e düştü (yalnızca `sigma_cm.png` eksikleri kaldı).

### 30. Kırık Bağlantı Taraması & `validate_atlas.py` Denetimi (`2026-11-15 09:15 TR`)
- **`docs/story/*.md` + `docs/story/atlas_cities/*.md` yerel bağlantı taraması:** `0` kırık yerel bağlantı (`broken local links: 0`).
- **`tools/validate_atlas.py` (`29` bölge):** `274` bulgu (`248` error, `26` warning): (a) yeni ATLAS v2 sıralama anahtarı `rate_cm_per_100d_common` olduğu halde `validate_atlas.py` hâlâ `rate_cm_per_100d` sıralaması arıyor (**PC10**); (b) `kashmar`, `kerman`, `houston`, `tianjin`, `lagos` için `atlas.json` içinde `country: ""`; (c) bazı `summary.json` dosyalarında `p2_cm`, `valid_fraction`, `confidence`, `ref_range_cm` alanları eksik (`konya_plain`, `semarang`, `can_tho`, `delta`, `bangkok`, `pekalongan`, `jakarta`, `yunlin`, `hanoi`, `ho_chi_minh`). **PC10/PC2** incelemeli.

### 31. Teslim Paketi & Canlı URL Denetimi (`2026-11-15 09:17 TR`)
- `docs/story/submission_package.md` oluşturuldu (`BACKLOG_ORTAK.md` §E `[x PC4]`).
- Canlı URL kontrolünde `https://keremsumer2010-tech.github.io/aseltech/web/index.html` adresinin `HTTP 404` döndürdüğü tespit edildi (Pages `web/.` içeriğini kökte yayınlıyor); `docs/story/submission_form.md:43` doğrulanmış **`https://keremsumer2010-tech.github.io/aseltech/`** (`HTTP 200`) ile düzeltildi.

### 32. Ortak 93 Günlük Pencere vs. Tam Pencere Sıralama Kıyası (`2026-11-15 09:24 TR`)
`data/global/atlas.json` içindeki `rate_cm_per_100d_common` (`2026-06-28 → 2026-09-29`, `93` gün) sıralaması ile tam dönem (`96–120` gün, `rate_cm_per_100d`) sıralaması karşılaştırıldı (`BACKLOG_ORTAK.md` §B `[x PC4]`):
- **Güvenilir (`reliable`, 16 bölge) öne çıkan yer değiştirmeler:**
  - `konya_plain`: `#1 → #1` (`0` fark; `−8.9 → −11.0 cm/100d`, pik yaz sulaması ortak pencerede yoğunlaşıyor).
  - `eloy`: `#4 → #2` (`+2`; `−6.7 → −8.6 cm/100d`) ve `kashmar`: `#7 → #4` (`+3`; `−5.2 → −7.0 cm/100d`) — Ekim başındaki yavaşlama kesilince yaz ortası çökme hızı yükseliyor.
  - `central_valley`: `#2 → #3` (`−1`; `−7.2 → −7.3 cm/100d`), `mashhad`: `#3 → #5` (`−2`; `−7.2 → −6.9 cm/100d`), `semarang`: `#5 → #7` (`−2`; `−6.5 → −5.5 cm/100d`).
  - `quetta`: `#11 → #16` (`−5`; `−3.2 → −0.7 cm/100d` — çekimin büyük bölümü ortak pencere dışındaki Haziran/Ekim uçlarında gerçekleşmiş).
  - `cangzhou` (`+2`, `#15 → #13`), `can_tho` (`+1`), `tianjin` (`+1`), `delta` (`+1`).
- **Indicative (`13` bölge) öne çıkan yer değiştirmeler:**
  - `ho_chi_minh`: `#9 → #13` (`−4`; `−3.5 → +4.6 cm/100d`, muson dönemi kabarma/salınım etkisi).
  - `bangkok`: `#6 → #3` (`+3`; `−6.2 → −12.5 cm/100d`, muson gürültü salınımı).
  - `gorgan` (`#1 → #1`), `delhi` (`#2 → #2`) sabit; `jakarta` (`−2`), `isfahan` (`+2`), `xian` (`+2`).

### 33. `atlas_top5_check.md` Yönteminin 6–15. Sıralara Uygulanması (`2026-11-15 09:29 TR`)
`docs/story/atlas_top5_check.md` yöntemi (`p01` adım-adım zaman serisi `|Δ|` kontrolü + hakemli literatür kıyası) `data/global/atlas.json` **6–15. sıralarına** uygulandı (`BACKLOG_ORTAK.md` §B `[x PC4]`):
- **Sonuç:** 10 bölgenin tamamında tek adımda `12.1 cm` faz döngüsü sıçraması veya birbirini götüren `> 5 cm` tek tarih aykırısı **yok** (`0` QC bayrağı; tüm adımlar `< 6.05 cm` yarı-döngü sınırının altında).

| Sıra | Bölge (`id`) | Ortak Hız (`cm/100d`) | Tepe LOS (`cm`) | Maks `|Δ|` Adım (`cm`) | Güven | Literatür Hızı & Uyum |
|---:|---|---:|---:|---:|---|---|
| 6 | `mexico_city` | `−6.3` | `−7.0` | `3.55` | `medium` | `30–40 cm/yr` (doğu/kuzey göl yatağı; kenar/kayaç ref. ile uyumlu) |
| 7 | `semarang` | `−5.5` | `−6.2` | `5.14` | `medium` | `6–19 cm/yr` (kıyı; `10-11` faz sıçraması temizlendi, uyumlu) |
| 8 | `kerman` | `−5.3` | `−6.1` | `1.60` | `high` | `>35 cm/yr` il geneli (`10.1126/sciadv.adp0896`; uyumlu) |
| 9 | `rafsanjan` | `−4.2` | `−5.8` | `1.19` | `medium` | `15–30+ cm/yr` (Rafsanjan Ovası; uyumlu) |
| 10 | `houston` | `−4.0` | `−5.2` | `1.70` | `medium` | `1.0–4.9 cm/yr` (`10.3390/rs14236184`; yaz pik/ref duyarlılığı notlu) |
| 11 | `can_tho` | `−3.4` | `−3.4` | `1.76` | `medium` | `1.0–4.0+ cm/yr` (`10.3390/rs13020189`; uyumlu) |
| 12 | `tianjin` | `−2.8` | `−2.9` | `1.37` | `medium` | `5–17 cm/yr` (`10.3390/s26041203`; uyumlu) |
| 13 | `cangzhou` | `−2.4` | `−2.4` | `1.07` | `medium` | `~2–4 cm/yr` (`10.1007/s12665-013-2532-7`; uyumlu) |
| 14 | `lagos` | `−2.1` | `−2.4` | `1.49` | `medium` | `0.2–8.7 cm/yr` (`10.1016/j.geog.2019.12.006`; uyumlu) |
| 15 | `delta` | `−1.4` | `−1.3` | `1.58` | `medium` | `1.2–2.2 cm/yr` (turba oksidasyonu; uyumlu) |

### 34. Blok 3 — `web/atlas.html` Okuma Rehberi & Sayfa Meta Başlıkları (`2026-11-15 09:34 TR`)
- `web/atlas.html`: `atlasStats` altına 4 adımlı **How to read this map** kutusu (LOS vs vertical, renk ölçeği, `high`/`medium` güven rozeti, `indicative only` ayrımı) + `og:image` eklendi (`BACKLOG_ORTAK.md` §C `[x PC4]`).
- `web/{index,atlas,science,data,explorer,faq}.html`: `<title>` ve `<meta name="description">` etiketleri 29 bölgeli ATLAS v2 ve 30 soruluk SSS ile güncellendi (`[x PC4]`). NISAR 3D dosyalarına dokunulmadı.
