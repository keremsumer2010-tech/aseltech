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

- **NOT (`analysis/cumulative.py` satır 220–230 & `analysis/dem.py`):** Repoda `raw/dem/*.tif` bulunmayan temiz klonlarda `dem_on_grid(x, y, epsg)` tüm değerleri `NaN` olan bir `(1473, 1438)` dizi döndürüp `analysis/out/<site>_dem.npy` içine kaydediyor; ardından `deramp_elevation(cm, dem)` `ValueError: too few valid pixels to fit` hatasıyla duruyor. PC9 sarmalayıcısı (`analysis/pc9/run_fullyear.py`) PC3 koduna dokunmadan `cumulative.py`'nin dahili `dem = None` (`plane-only deramp`) geri dönüşünü tetikleyerek bu durumu çözdü; sarp kuzeydoğu Sierra eteklerinde topografik troposfer artığı düzlem düzeltmeyle kalabileceğinden bu nokta `docs/story/fullyear.md` yöntem notunda açıkça belirtildi.
- **NOT (`analysis/cumulative.py` satır 340 & 419):** `--mixed` bayrağıyla `analysis/out/central_valley_fullyear_cum_stack.npz` içine `quality="provisional"` yazılıyor (ancak 160 m kopyaya doğru biçimde `quality="mixed"` yazılıyor ve `run_decomp.py --quality mixed` ile eziliyor), ayrıca `summary["method_note"]` içinde `"summer season"` metni kalıyor (`analysis/pc9/run_fullyear.py` sonrası `data/central_valley_fullyear/summary.json` içinde düzeltildi).
