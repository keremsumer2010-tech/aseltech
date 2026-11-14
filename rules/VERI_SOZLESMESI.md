---
type: kural
status: kapali
date: 2026-11-14
owner: PC1
---

# Veri sözleşmesi

Web sitesi, oyun ve doğrulama bu formatları okur. Bir formatı değiştirmek için **önce PC1'e sor**;
PC1 bu dosyayı günceller, sonra kod değişir. Format sessizce değişirse site kırılır.

---

## 1. Bölgeler

Sıra her yerde **`[lon_min, lat_min, lon_max, lat_max]`** = `[w, s, e, n]`.

| site | bbox | Ürün / dönem | Not |
|---|---|---|---|
| `central_valley` | -120.2, 35.6, -119.0, 36.6 | GUNW path 34 ve 114, Kas 2025–Eki 2026 | Ana bölge |
| `konya` | 32.4, 37.4, 33.9, 38.1 | GUNW path 7/100/108/172, Eki 2025–Eki 2026 | |
| `karapinar` | 33.3, 37.6, 33.8, 37.9 | GUNW path 7 ve 172, Haz–Eki 2026 | Obruk bölgesi |
| `fens` (UK) | -0.3, 52.4, 0.4, 52.9 | GCOV/SME2, Haz–Kas 2026 | Bulut sahnesi |

## 2. Veri kaynağı ve fizik sabitleri

- Arama/indirme: ASF SearchAPI / `asf_search`, parametre **`platform=NISAR`** (`dataset=NISAR` çalışmıyor).
- `.h5` indirmek Earthdata girişi ister (giriş yoksa "Access denied"). Browse PNG'ler girişsiz iner.
- Her PC kendi Earthdata hesabını kullanır; kimlik bilgisi `~/.netrc` (Windows: `~/_netrc`) dosyasında, repoda asla.
- Dalga boyu λ SABİT YAZILMAZ: her dosyadan `λ = 299792458 / grids/frequencyA/centerFrequency` (Central Valley GUNW: 1239 MHz → **0.24196 m**). Yollar: `docs/qa/PC1.md`.
- LOS yer değiştirme = −λ/(4π) × unwrapped phase. **İşaret konvansiyonu ürün dokümanından doğrulanır**, kaynak koda yazılır.
- GUNW: 80 m UTM grid. GCOV: gamma0 (terrain corrected). Metadata cube'larda LOS birim vektörü ve incidence var.

## 3. Kalite sınıfları

| `quality` | Tanım | Nerede kullanılır |
|---|---|---|
| `provisional` | Her iki tarihi **2026-06-17 ve sonrası** olan PROVISIONAL (CRID P05023) ürünler | Bugünkü demo **sadece bunlar** |
| `beta-precal` | 2026-06-17 öncesi tarih içeren ürün (kalibrasyon öncesi beta) | Pazar, ayrı klasör |
| `mixed` | provisional + beta-precal birlikte işlenmiş seri | Sadece `*_fullyear` / `*_beta` klasörleri |
| `preview` | Browse PNG; nicel değil, sadece görsel | B planı ve UK sahnesi |
| `placeholder` | PC1'in site geliştirirken koyduğu sahte veri; gerçek dosya aynı adla üzerine yazılır | Sadece geliştirme; yayında kalırsa rozetle "PLACEHOLDER" |

Kurallar:
- Farklı sınıflar aynı hesapta/katmanda birleşmez. `mixed` çıktı **ayrı klasörde** durur.
- Her JSON çıktıda `quality` alanı ve kısa `quality_note` (İngilizce) bulunur.
- Zincirde boşluk varsa (iki ardışık tarih arasında çift yoksa) seri bağlanmaz; boşluk `notes` alanına yazılır.

## 4. Dosya formatları

### 4.1 Ara ürünler (pipeline / analysis)

| Dosya | Sahip | İçerik |
|---|---|---|
| `pipeline/central_valley_gunw.csv` | PC2 | `granule, date1, date2, crid, url, size_mb, quality` |
| `pipeline/subset/<site>/<t1>_<t2>.npz` | PC2 | `unw` (float32, rad), `coh` (uint8, 0-255 = 0-1), `x`, `y`, `epsg`, `wavelength`, `incidence` (varsa), `quality`. **`np.savez_compressed`**, dosya ≤ 20 MB |
| `analysis/out/<site>_cum.npz` | PC3 | Son tarihe kadar kümülatif çökme ızgarası: `cum_cm` (float32, NaN = maskeli), `x`, `y`, `epsg`, `dates`, `quality`. PC6 risk indeksi bunu okur |

### 4.2 Web'in okuduğu dosyalar (`data/`)

```
data/catalog.json                 PC1   [{site, title, quality, layers:[...]}]
data/<site>/meta.json             PC3   {site, bbox:[w,s,e,n], dates:[YYYY-MM-DD...], units:"cm",
                                         vmin, vmax, source, notes, quality, quality_note}
data/<site>/disp/<date>.png       PC3   o tarihe kadar kümülatif LOS çökme; renkli, şeffaf arka plan,
                                         bbox'a oturur; renk aralığı (vmin/vmax) TÜM tarihlerde sabit
data/<site>/points.json           PC3   [{id, name, lon, lat, dates:[...], disp_cm:[...]}]  (10-15 nokta)
data/<site>/summary.json          PC3   {max_subsidence_cm, period:[t_start,t_end], rate_cm_per_yr_estimate,
                                         reference_point:{lon,lat}, quality}   ← oyun ve sunum bu sayıyı okur
data/<site>/decomp.json           PC3   {permanent_cm_per_yr, seasonal_amp_cm} PNG yolları + istatistik (Pazar)
data/<site>/drivers.json          PC2   {dates, subsidence_cm, soil_moisture, irrigation_index, lag_corr} (Pazar)
data/<site>/assets.json           PC6   GeoJSON; her segmentte {name, type, risk, gradient_mm_per_km, max_cm} (Pazar)
data/<site>/validation.json       PC6   [{station, lon, lat, rmse_cm, corr, dates, insar:[...], gnss:[...]}] (Pazar)
data/karapinar/sinkholes.geojson  PC4   Point; properties {name, year_formed, source_title, source_url, coord_source}
data/uk/meta.json                 PC4   {date, bbox, optical_source_url, optical_product, radar_granule,
                                         radar_browse_url, quality:"preview", note}
data/uk/optical_<date>.jpg        PC4
data/uk/radar_<date>.png          PC4
```

Genel:
- Tarihler ISO `YYYY-MM-DD`. Birimler alan adında veya `units` alanında açık.
- JSON UTF-8, girintili (okunabilir diff için). NaN JSON'a yazılmaz → `null`.
- Web yolları **göreli** okur (`data/...`, başında `/` yok). GitHub Pages proje alt yolunda yayınlanır.

## 5. Değişiklik geçmişi

| Tarih | Değişiklik | Kim |
|---|---|---|
| 2026-11-14 | CLAUDE.md'den taşındı. Eklenen: `summary.json` (oyun/sunum için tek sayı kaynağı), `analysis/out/<site>_cum.npz` (PC6 için sayısal ızgara), npz sıkıştırma ve `coh` uint8 kuralı | PC1 onayladı (2026-11-14) |
| 2026-11-14 | Eklenen: `placeholder` kalite sınıfı (PC1 site geliştirme verisi) | PC1 |
| 2026-11-14 | λ sabiti kaldırıldı → dosyadaki `centerFrequency`; GUNW yolları `docs/qa/PC1.md` | PC1 |
