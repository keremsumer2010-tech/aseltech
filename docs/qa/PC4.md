# PC4 QA Raporu

Tarih: `2026-11-14` (`13:30 TR`) · Kapsam: PC4 çıktıları (`data/uk/`, `data/karapinar/sinkholes.geojson`, `docs/story/`, `web3d/`)

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
| Taslak & Kurallar (Q11, Q12) | `docs/story/project_page.md`, `docs/story/submission_rules.md` | **GEÇTİ** — doğrulanmış depo URL'si (`https://github.com/keremsumer2010-tech/aseltech`) ve `web3d/` 4-çift sonuçları işlendi; `data/central_valley/summary.json` gelene kadar tam zincir için `{CV_MAX_CM}` / `{CV_RATE_CM_YR}` yer tutucu korundu (`K-2`); `Space_Apps_2022_Project_Submission_Guide.pdf` HTTP 200 doğrulandı ve `www.spaceappschallenge.org/resources/participant-faq/` için TLS hatası dürüstçe raporlandı (`E-06`) |

---

## 4. Queue `Q16` — `web3d/` (3D "Yerin Nefesi" Görünümü)

| Kontrol | Detay | Sonuç |
|---|---|---|
| Veri üretimi (`web3d/generate_3d_data.py` -> `web3d/surfaces.json`) | `252,132 B` (`~246.2 KB`), valid UTF-8 JSON, `NaN` yok; Central Valley (`80×96`, `2026-06-28` → `2026-08-27`, `4` kesintisiz çift, `vmin=-6.0`, `vmax=+6.0`, `p2=-4.14`, `p50=-0.26`, `p98=+3.56`, 400 m medyan tepe `−15.4 cm` LOS) & Karapınar (`48×80`, `2026-09-18` → `2026-09-30`, `vmin=-3.0`, `vmax=+3.0`, `p2=-2.12`, `p50=-0.78`, `p98=+0.79` + `29` obruk) | **GEÇTİ** — `analysis/insar.py` ve `cumulative.py` fonksiyonları yeniden kullanıldı, `analysis/` / `data/central_valley/` değiştirilmedi |
| Ön yüz & JS söz dizimi (`web3d/index.html`, `style.css`, `app.js`) | `node --check web3d/app.js` + lokal HTTP sunucu (`/web3d/`, `style.css`, `app.js`, `surfaces.json`) **HTTP 200** + Three.js `@0.160.0` & `OrbitControls.js` CDN **HTTP 200** | **GEÇTİ** — dikey abartma `10,000×–150,000×` (varsayılan `50,000×`), `RdBu` renk skalası ve zorunlu `provisional` dipnotu mevcut |

---

## 5. PC6 QA Bulgularıyla Çapraz Kontrol (`docs/qa/PC6.md`)

`docs/qa/PC6.md` §3 maddelerine istinaden PC4 tarafı notu:
1. **`web/index.html:154` (`docs/story/sources.md` linki):** Dosya oluşturuldu; push sonrası canlı link çalışacaktır.
2. **`web/index.html:47` (Holme Fen yer tutucusu):** PC4 tarafından birincil kaynaklardan doğrulanan kesin rakamlar (`Great Fen Heritage`: `1848` ahşap kazık, `1851` dökme demir direk, ilk dönemde yılda `9 inç`, `1852`'den bu yana günümüzde yüzey üstünde **yaklaşık 4 m**; `Wikipedia`: deniz seviyesinin **2.75 m / 9.0 ft altı**) `docs/story/sources.md` §1 içine işlenmiştir (`Q18` kapsamında PC6 veya PC1 güvenle güncelleyebilir).
