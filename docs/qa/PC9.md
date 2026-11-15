# PC9 QA Notları — Central Valley Tam Yıl Analizi (Q08)

**Sorumlu:** PC9 (`aseltech-pc9`) · **Tarih:** 2026-11-14 · **Kalite Sınıfı:** `mixed` (`18 beta-precal` + `7 provisional`, `CRID P05023`)  
**Kalibrasyon Bildirimi:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Veri Sözleşmesi ve Çıktı Doğrulaması (`data/central_valley_fullyear/`)

- **Zincir bütünlüğü (`analysis/pc9/run_fullyear.py --step cumulative`):**
  - `pipeline/subset/central_valley_beta/` (18 çift, `2025-11-24` → `2026-06-28`, `quality=beta-precal`) ve `pipeline/subset/central_valley/` (7 çift, `2026-06-28` → `2026-10-14`, `quality=provisional`) toplam **25 ardışık çiftte** kesintisiz (`0` boşluk, `0` dışlanan aykırı piksel) birleştirildi (`26` tarih, `324` gün).
  - Bütün katmanların boyutu `1200×1000` RGBA, `bbox = [-120.2, 35.6, -119.0, 36.6]`, `vmin/vmax` her tarihPNG'sinde sabit (`-16.0 / +16.0 cm`), dosya boyutları `<= 1.6 MB` (`rules/RULES.md` K-12 `<= 20 MB` sınırının çok altında).
- **Kalite sınıfı ayrımı (`rules/VERI_SOZLESMESI.md` §3):**
  - Çıktılar ayrı `data/central_valley_fullyear/` klasöründe üretildi; yaz dönemi `provisional` baseline (`data/central_valley/`) değiştirilmedi.
  - `meta.json`, `summary.json` ve `decomp.json` dosyalarının tamamında `"quality": "mixed"`, kapsamlı `"quality_note"` uyarısı ve hangi 18 çiftin `beta-precal`, hangi 7 çiftin `provisional` olduğunun açık listesi yer alıyor.
- **Ayrıştırma kapısı (`docs/qa/PC5.md` §3.2 kontrol listesiyle karşılaştırma):**
  - `status == "ok"`, `valid_fraction = 0.4604` (`975,173 / 2,118,174` piksel, `> 0.30` kapısını geçiyor), `min_points = 8`, `min_span_years = 0.75` (`324 gün = 0.887 yıl`).
  - Tepe çökme noktası `p01` (`7 km W of Earlimart`, `-119.35254E, 35.88329N`):
    - 324 günlük kümülatif LOS: `-20.32 cm` (`-26.9 cm` dikey `estimate`, insidans `40.9°`), referans duyarlılığı aralığı `[-20.3, -11.7] cm` (3 referans penceresi).
    - Kalıcı doğrusal hız: **`-16.77 ± 2.24 cm/yr` LOS** (`-22.2 cm/yr` dikey `estimate`, $R^2 = 0.972$), `Neely et al. (2021)` Central Valley literatür aralığı (`-17.7` ile `-34.5 cm/yr`) içinde.
    - Mevsimsel genlik: **`5.83 ± 0.75 cm` LOS** (`11.67 cm` tepeden tepeye), yıllık en derin nokta **Ağustos (`low_month = 8`)**.
    - Havza geneli medyan (`p50`): kalıcı `-3.74 cm/yr` (`324` günde `-3.32 cm`), mevsimsel genlik `1.66 cm` (`3.32 cm` tepeden tepeye) → kalıcı / geri dönen oranı **`1.00 : 1`**.

---

## 2. Gözlenen Görsel ve Metin Kontrolleri

- `data/central_valley_fullyear/disp/2026-10-14.png`, `decomp_permanent.png` ve `decomp_seasonal.png` görsel olarak açılıp incelendi: Tulare Gölü yatağı koherens maskesiyle saydam, Corcoran/Earlimart/Tulare/Huron çanakları tutarlı kırmızı çökme ve belirgin mevsimsel genlik (`magma`), Woodlake referans bölgesi sıfır civarında.
- `docs/story/media/pc9_fullyear_point.png` görsel olarak açılıp incelendi: `beta-precal` dönemi kesikli turuncu çizgi ve sarı arka plan etiketiyle, `provisional` dönemi düz koyu kırmızı çizgiyle net ayrıldı; etiketlerde çakışma veya kesilme yok; birim/tarih/kredi ve kalibrasyon bildirimi mevcut.
- `docs/story/media/pc9_fullyear_12day_steps.png` (`370.1 KB`) ve `docs/story/media/pc9_fullyear_monthly_steps.png` (`343.1 KB`) görsel olarak açılıp incelendi: eksen üst boşluğu ayarlandıktan (`ax1.set_ylim(-6.1, 6.6)` ve `(-11.4, 7.3)`) sonra Mart `+4.09 cm` çubuğu ve başlık bandı çakışmasız, 12 günlük ve aylık adımlarda `beta-precal` / `provisional` ayrımı ve birim/tarih/kredi açık.
- `docs/story/fullyear.md` (`15,373` karakter), `docs/story/presentation_cues.md` ve `docs/story/rehearsal_checklist.md`: `docs/REVIEW_1500.md` kurallarına göre kontrol edildi (düz yazı bölümünde sıfır `!`, yasaklı AI kelimesi `0`, her sayı birimli ve tarihli, tam yıl için `includes pre-calibration data` / `beta-precal` + `provisional` etiketli, A6 zaman adımı tabloları ve Karapınar hazırlık notu eklendi).

---

## 3. Otomatik Test Sonuçları

Komut: `python -m pytest analysis/pc9 analysis/decomp analysis/test_insar.py analysis/test_cumulative.py -v`

- Sonuç: **`41 passed, 1 warning in 23.31s`** (`analysis/pc9` 4/4, `analysis/decomp` 18/18, `analysis/test_insar.py` 15/15, `analysis/test_cumulative.py` 4/4).
- Üretilen ve yerel bırakılan ara çıktı (`analysis/out/central_valley_fullyear_cum_stack.npz` `50.8 MB`): `rules/RULES.md` K-12 gereği repoya eklenmedi.

---

## 4. Üst Akış Dosyalarına Dair QA Notları (`rules/RULES.md` §3 — Düzenlenmedi)

- **DEM önbellek hatası (`analysis/cumulative.py` satır 220–228 / `analysis/dem.py`):** Yerel `raw/dem` yokken `dem_on_grid(x, y, epsg)` tümü NaN (`finite: 0`) bir `analysis/out/<site>_dem.npy` dosyası yazıyor; `cumulative.py` var olan `.npy` dosyasını yükleyip `deramp_elevation(cm, dem)` çağırınca `ValueError: too few valid pixels to fit` veriyor. PC3/PC2 dosyalarına dokunulmadı; PC9 şehirleri `analysis/pc9/run_atlas_region.py` sarmalayıcısı üzerinden `plane-only deramp` fallback'i ile çalıştırıldı.

---

## 5. ATLAS_PLANI FAZ 1 — Küresel Şehir Doğrulamaları (`PC10` & `PC5` İçin)

- **`hazır: eloy` (`-111.55, 32.75`, `±0.25°`, `data/global/eloy/`):**
  - **Ölçüm (`2026-06-19` → `2026-10-17`, `120` gün, `9` `provisional` çift, track `77` asc frame `18`):** `max_subsidence_cm = -8.0 cm` LOS (`-10.3 cm` dikey `estimate`, `38.9°`), `p2_cm = -4.3 cm`, `rate_cm_per_100d = -6.67`, `rate_cm_per_yr_estimate = -24.5 cm/yr` (yaz penceresi *estimate*), `valid_fraction = 0.696`, `range_cm = [-8.4, -7.2]` (3 referans, oran `0.15 < 0.30`), `confidence = "high"`. Birincil referans `(-111.4221, 32.5240)` güney Silver Bell / Picacho kaya eteğinde (`mean_coh = 0.93`).
  - **Görsel kontrol:** `data/global/eloy/disp/2026-10-17.png` açılıp incelendi; Eloy/Picacho tarım havzasında net kırmızı çökme çekirdeği, kenar kayalıklarda sıfır civarı değerler, yapay eğim yok.
  - **Literatür:** Arizona Department of Water Resources (ADWR InSAR & GNSS programı, Pinal County / Eloy–Picacho alt havzaları, `azwater.gov` / AZGS) aktif çökme çekirdeklerinde **`> 7 cm/yr`** (`2.8 in/yr`) güncel hız ve tarihsel olarak **`> 5.7 m`** kümülatif çökme bildirmektedir (ör. Conway 2016, *Hydrogeology Journal*, `doi:10.1007/s10040-015-1329-z`). Yaz dönemi (`120` gün) NISAR ölçümü beklenen büyüklük mertebesiyle uyumludur.

- **NOT (`analysis/cumulative.py` satır 220–230 & `analysis/dem.py`):** Repoda `raw/dem/*.tif` bulunmayan temiz klonlarda `dem_on_grid(x, y, epsg)` tüm değerleri `NaN` olan bir `(1473, 1438)` dizi döndürüp `analysis/out/<site>_dem.npy` içine kaydediyor; ardından `deramp_elevation(cm, dem)` `ValueError: too few valid pixels to fit` hatasıyla duruyor. PC9 sarmalayıcısı (`analysis/pc9/run_fullyear.py`) PC3 koduna dokunmadan `cumulative.py`'nin dahili `dem = None` (`plane-only deramp`) geri dönüşünü tetikleyerek bu durumu çözdü; sarp kuzeydoğu Sierra eteklerinde topografik troposfer artığı düzlem düzeltmeyle kalabileceğinden bu nokta `docs/story/fullyear.md` yöntem notunda açıkça belirtildi.
- **NOT (`analysis/cumulative.py` satır 340 & 419):** `--mixed` bayrağıyla `analysis/out/central_valley_fullyear_cum_stack.npz` içine `quality="provisional"` yazılıyor (ancak 160 m kopyaya doğru biçimde `quality="mixed"` yazılıyor ve `run_decomp.py --quality mixed` ile eziliyor), ayrıca `summary["method_note"]` içinde `"summer season"` metni kalıyor (`analysis/pc9/run_fullyear.py` sonrası `data/central_valley_fullyear/summary.json` içinde düzeltildi).

- **`hazır: cangzhou` (`116.85, 38.30`, `±0.25°`, `data/global/cangzhou/`):**
  - **Ölçüm (`2026-06-21` → `2026-10-19`, `120` gün, `8` `provisional` çift, track `111` asc frame `21`):** `max_subsidence_cm = -2.4 cm` LOS (`-3.2 cm` dikey `estimate`, `42.3°`), `p2_cm = -3.3 cm`, `rate_cm_per_100d = -2.0`, `rate_cm_per_yr_estimate = -7.2 cm/yr` (yaz penceresi *estimate*), `valid_fraction = 0.432`, `range_cm = [-2.4, -1.6]` (3 referans; birincil `(116.8723, 38.3365)` Cangzhou kent merkezi ve GD alt referans `(117.0944, 38.0618)` `-2.4 cm` üzerinde uyuşurken, GB alt referans `(116.6210, 38.0829)` GB alüvyal tarım çökme kuşağı içinde kaldığı için `-1.6 cm` veriyor — yayılım oranı `0.333 >= 0.30`), `confidence = "medium"`.
  - **Görsel kontrol:** `data/global/cangzhou/disp/2026-10-19.png` açılıp incelendi; kent merkezi sıfır civarında stabil (mavi/beyaz), güneybatıda (Nanpi/Botou yönü, tepe `116.6654, 38.1414`) net kırmızı çökme kuşağı.
  - **Literatür:** Kuzey Çin Ovası / Cangzhou genelinde son dönem InSAR çalışmaları `> 3 cm/yr` yaygın çökme ve güneybatı Nanpi–Dongguang tarım kuşağında `11.5 cm/yr`'a varan çekirdek hızları bildirirken (`Land` 2023, `doi:10.3390/land12122114`), Güney–Kuzey Su Transferi ve yeraltı suyu kısıtları sayesinde kent merkezinin görece stabilize olduğu gösterilmiştir (`Journal of Hydrology` 2022, `doi:10.1016/j.jhydrol.2021.127368`). Yaz dönemi (`120` gün) `-2.4 cm` LOS (`-7.2 cm/yr` doğrusal *estimate*) ve kent-dışı desen literatürle uyumludur.

- **`hazır: gorgan` (`54.43, 36.84`, `±0.25°`, `data/global/gorgan/` — `confidence: "low"` UYARISI):**
  - **Ölçüm (`2026-06-21` → `2026-10-19`, `120` gün, `9` `provisional` çift, track `107` desc frame `70`, `1` çift QC'de elendi `%30.1` etkilenmiş):** `max_subsidence_cm = -34.6 cm` LOS (`-41.8 cm` dikey `estimate`, `34.2°`), `p2_cm = -33.1 cm`, `rate_cm_per_100d = -28.83`, `rate_cm_per_yr_estimate = -105.2 cm/yr`, `valid_fraction = 0.267` (`< 0.40`), `range_cm = [-34.6, -13.8]` (3 referans, yayılım oranı `0.601 >> 0.30`).
  - **Görsel & fiziksel kontrol (`data/global/gorgan/disp/2026-10-19.png`):** `P107 F070` swath kenarı kutunun batı yarısını (`lon < 54.40`) dışarıda bırakıyor (`valid_fraction = 0.267`). Tepe değer `(54.3954, 36.5926)` Gorgan ovasında değil, güneydeki sarp/ormanlık Elburz (Alborz) eteklerinde; DEM olmadan `plane-only deramp` ve faz açma/koherens bozulması nedeniyle yapay/topografik artık veriyor. Bu nedenle `confidence = "low"` işaretlendi — **basın özetinde başlık hızı olarak kullanılmamalıdır**.
  - **Literatür:** Gorgan Ovası'nda yayımlanmış InSAR hızları yerel maksimum `~14 mm/ay` (`16.9 cm/yr`, Monesdayen vd. 2023, *Hydrogeomorphology*, `doi:10.22034/HYD.2023.55996.1688`) ve ova genelinde `~5 cm/yr` düzeyindedir (ayrıca Tourani vd. 2021, `doi:10.5281/zenodo.4322617`). Mevcut `-105.2 cm/yr` değerinin artefakt olduğu literatürle de doğrulanmaktadır.

- **`hazır: houston` (`-95.80, 29.80`, `±0.25°`, `data/global/houston/`):**
  - **Ölçüm (`2026-06-18` → `2026-10-16`, `120` gün, `9` `provisional` çift, track `62` asc frame `16`, `0` elenen çift):** `max_subsidence_cm = -5.2 cm` LOS (`-6.7 cm` dikey `estimate`, `39.1°`), `p2_cm = -4.6 cm`, `rate_cm_per_100d = -4.33`, `rate_cm_per_yr_estimate = -15.9 cm/yr` (yaz penceresi *estimate*), `valid_fraction = 0.461` (`>= 0.40`), `range_cm = [-5.2, -3.3]` (2 referans; yayılım oranı `0.365 >= 0.30`), `confidence = "medium"`.
  - **Görsel kontrol (`data/global/houston/disp/2026-10-16.png`):** `P062 F016` frame'i kutunun güney ~%70'ini kapsıyor (kuzey şeridi frame sınırı dışı); Addicks/Barker rezervuarı çevresinde (Katy/West Houston) ve güneybatıda (`-95.9579, 29.5589`) net kırmızı çökme desenleri görülüyor.
  - **Literatür:** Katy / Batı Houston bölgesinde Sentinel-1 + GNSS (Houston20) çalışmaları çok yıllık net hızı `1.4–2.0 cm/yr` bildirir (*Remote Sensing* 2023, `doi:10.3390/rs15184424`). `120` günlük yaz penceresindeki `-5.2 cm` LOS (`range_cm = [-5.2, -3.3]`) yaz mevsimsel çekimi ve Körfez Kıyısı kil sıkışması/referans duyarlılığını yansıtır (`confidence = "medium"`).

- **`hazır: lagos` (`3.39, 6.45`, `±0.25°`, `data/global/lagos/`):**
  - **Ölçüm (`2026-06-24` → `2026-10-10`, `108` gün, `8` `provisional` çift, track `152` desc frame `85`, `0` elenen çift):** `max_subsidence_cm = -2.4 cm` LOS (`-3.3 cm` dikey `estimate`, `42.4°`), `p2_cm = -2.9 cm`, `rate_cm_per_100d = -2.22`, `rate_cm_per_yr_estimate = -8.2 cm/yr` (yaz penceresi *estimate*), `valid_fraction = 0.328` (Atlantik Okyanusu ve Lagos Lagünü maskesi nedeniyle `< 0.40`), `range_cm = [-2.4, -2.4]` (2 iç kara referansı `>= 30 km` ayrı ve birebir `-2.4 cm` üzerinde uyuşuyor), `confidence = "medium"`.
  - **Görsel kontrol (`data/global/lagos/disp/2026-10-10.png`):** Güneydeki okyanus ve lagün temiz biçimde maskelenmiş; Victoria Island – Lekki kıyı kuşağında (`3.5495, 6.4502`) tutarlı kırmızı çökme bandı görülüyor.
  - **Literatür:** Ikuemonisan vd. (2020/2021, *Geodesy and Geodynamics*, `doi:10.1016/j.geog.2019.12.006`) Sentinel-1 SBAS ile Lagos kıyı/dolgu zonlarında `-8.7 cm/yr` (`-87 mm/yr`, yerel tepe `-94 mm/yr`) hız bildirmiştir; ayrıca Ohenhen & Shirzaei (2022, *Earth's Future*, `doi:10.1029/2022EF003219`) kıyı çökme riskini doğrulamaktadır. `-8.2 cm/yr` doğrusal *estimate* literatürdeki kıyı zonu hızlarıyla uyumludur.

---

## 6. ATLAS_PLANI FAZ 2 — Tam Yıl Yıllıklaştırma (`konya_plain_fullyear`, `mexico_city_fullyear`, `central_valley_fullyear`)

- **`konya_plain_fullyear` → `insufficient_data` (`data/konya_plain_fullyear/summary.json`):**
  - ASF CMR sorgusu (`NISAR_L2_GUNW_BETA_V1`, `bbox=[32.4, 37.4, 33.9, 38.1]`): 54 granülün tamamı (`P007, P079, P100, P108, P172`) en geç `2026-01-16` (`cycle 009`) tarihinde bitiyor; `provisional` ise `2026-06-21` (`P108`) / `2026-06-26` (`P007`) tarihinde başlıyor (`156–168` günlük Şubat–Haziran boşluğu). Kesintisiz tam yıl zinciri kurulamadığı için `tasks/PC9.md` kuralı gereği `"status": "insufficient_data"` yazıldı ve Mexico City tam yıl zincirine (`26` çift, `gaps=0`) geçildi.

---

## 7. ATLAS_PLANI FAZ 3 — Central Valley Tam Yıl (`2025-11-24` → `2026-10-14`) ↔ 11 Aylık GNSS & Kalıcı Çökme Alanı

- **GNSS karşılaştırması (`validation/compare.py` → `data/central_valley_fullyear/validation.json`, `10` istasyondan `8`'i geçerli InSAR ayak izi içinde):**
  | İstasyon | `r` (Korelasyon) | `RMSE` (cm) | InSAR Son (cm) | GNSS Son (cm) |
  |---|---:|---:|---:|---:|
  | `CAHA` | `0.9206` | `1.840` | `-8.486` | `-7.447` |
  | `CAFP` | `0.9072` | `2.113` | `-9.485` | `-7.453` |
  | `P564` | `0.9017` | `5.781` | `-9.089` | `-1.674` |
  | `QCAP` | `0.8784` | `1.669` | `-7.435` | `-7.730` |
  | `HANF` | `0.7929` | `2.333` | `-6.851` | `-6.712` |
  | `CAD1` | `0.6335` | `2.724` | `-3.989` | `-1.147` |
  | `P565` | `0.6138` | `1.916` | `-2.358` | `-1.011` |
  | `P566` | `-0.2771` | `2.963` | `+1.446` | `-0.908` |
- **Kalıcı çökme alanı (`analysis/decomp/decompose.py`, `160 m × 160 m` = `0.0256 km²/px`, toplam geçerli alan `6,242.5 km²` = `%46.0`):**
  - Kalıcı çökme **`> 5 cm/yr`** (`v_cm_per_yr < -5.0`): **`2,274.7 km²`** (geçerli alanın `%36.4`'ü)
  - Kalıcı çökme **`> 10 cm/yr`** (`v_cm_per_yr < -10.0`): **`397.6 km²`** (geçerli alanın `%6.4`'ü)
