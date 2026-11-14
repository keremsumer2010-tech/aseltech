# VERİ SÖZLEŞMESİ — bölgeler, kalite sınıfları, dosya formatları ve sahipleri
Değişiklik sadece PC1 tarafından yapılır. Web (PC1) bu formatları okur; uymayan dosya siteye bağlanamaz.

## 1. Bölgeler (lon_min, lat_min, lon_max, lat_max)
| site | bbox | NISAR verisi | not |
|---|---|---|---|
| central_valley | -120.2, 35.6, -119.0, 36.6 | GUNW path 34 (ana), 114; GCOV; SME2 — Kas 2025–Eki 2026 | Ana bölge |
| karapinar | 33.3, 37.6, 33.8, 37.9 | GUNW path 7 (ana), 172 — Haz–Eki 2026 | Obruk bölgesi |
| konya | 32.4, 37.4, 33.9, 38.1 | GUNW path 7/100/108/172 — Eki 2025–Eki 2026 | Geniş Konya |
| fens | -0.3, 52.4, 0.4, 52.9 | GCOV, SME2, GUNW — Haz–Kas 2026 | UK bulut sahnesi, ekin |
| uk_clay | (Londra; Q09'u alan belirler, status'a yazar) | GUNW — Haz–Eki 2026 | Sinyal küçük olabilir |

Bugünkü Central Valley zinciri (provisional, P05023): 2026-06-28→07-10, 07-10→07-22, 07-22→08-15, 08-15→08-27, 08-27→09-08, 09-08→09-20.
Tam yıl zinciri: 2025-11-24 → 2026-10-14, 25 ürün, sadece "P05023" (X05010 atlanır).

## 2. Kalite sınıfları (her dosyada `quality` alanı zorunlu)
| quality | Tanım | Gösterim |
|---|---|---|
| `provisional` | Her iki tarihi ≥ 2026-06-17 olan PROVISIONAL ürünler | Sarı rozet "PROVISIONAL" |
| `beta-precal` | 2026-06-17 öncesi tarih içeren ürünler (kalibrasyon öncesi beta; aksi doğrulanana kadar) | Turuncu rozet, ayrı katman, grafikte kesikli çizgi |
| `preview` | Browse PNG — nicel değil | Gri rozet "PREVIEW — not quantitative" |
| `mixed` | provisional + beta birlikte kullanılan analiz (sadece `*_fullyear` klasörlerinde) | Turuncu rozet + açıklama |
- Sınıflar aynı hesapta birleştirilmez (mixed hariç, o da ayrı klasörde).
- Sabit dipnot (web): "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team. We use the products as released."

## 3. Ara dosyalar
| Yol | İçerik | Sahip |
|---|---|---|
| `pipeline/<site>_<ürün>.csv` | granule, t1, t2, sürüm kodu, url, boyut, quality | PC2 |
| `pipeline/subset/<site>/<t1>_<t2>.npz` | `unw` (rad), `coh`, `x`, `y`, `epsg`, `wavelength` (m), `incidence` (derece, varsa), `quality` | PC2 |
| `pipeline/subset/<site>_beta/…` | aynı format, beta-precal | PC2 / QUEUE |
| `docs/gunw_structure.md` | GUNW HDF5 ağacı ve kullanılan yollar | PC2 |

## 4. Siteye giden dosyalar (`data/`)
| Yol | Format | Sahip |
|---|---|---|
| `data/<site>/meta.json` | `{site, bbox:[w,s,e,n], dates:[YYYY-MM-DD], units:"cm", vmin, vmax, source, method, reference_point, quality, quality_note}` | PC3 |
| `data/<site>/disp/<YYYY-MM-DD>.png` | O tarihe kadar kümülatif çökme; renkli, şeffaf arka plan, tam bbox'a oturur; renk aralığı tüm tarihlerde sabit (vmin/vmax) | PC3 |
| `data/<site>/points.json` | `[{id, name, lon, lat, dates:[...], disp_cm:[...], note}]` (negatif = çökme) | PC3 |
| `data/<site>/drivers.json` | `{dates, soil_moisture, soil_moisture_units, irrigation_index, quality, source}` | QUEUE Q04 |
| `data/<site>/assets.json` | GeoJSON FeatureCollection; her özellikte `name, type, gradient_mm_per_km, max_cm, risk_rank` | QUEUE Q06 |
| `data/<site>/validation.json` | `[{station, lon, lat, rmse_cm, corr, dates, insar_cm, gnss_cm}]` | QUEUE Q05 |
| `data/<site>_fullyear/decomp.json` | `{permanent_cm_per_yr_png, seasonal_amp_cm_png, stats, quality:"mixed"}` | QUEUE Q08 |
| `data/uk/meta.json` | `{date, bbox, optical_source_url, optical_product, radar_granule, radar_browse_url, quality:"preview", note}` | PC4 |
| `data/uk/optical_<date>.jpg`, `data/uk/radar_<date>.png` | Aynı bbox'a hizalı görsel çifti | PC4 |
| `data/karapinar/sinkholes.geojson` | Nokta; `name, year_formed, source_title, source_url, coord_source` | PC4 |
| `data/catalog.json` | `[{site, title, layers:[...]}]` | PC1 |

## 5. Doğrulama ve altyapı ham verisi
| Yol | Format | Sahip |
|---|---|---|
| `validation/gnss_stations.csv` | `station, lon, lat, source_url, series_url, first_date, last_date` | PC6 |
| `validation/gnss/<station>.csv` | `date, up_cm` | PC6 |
| `risk/<site>_infra.geojson` | OSM hatları: `name, type, osm_id` (+ ODbL notu README'de) | PC6 |

## 6. Fizik notları
- NISAR L-band λ ≈ 0.2384 m. LOS yer değiştirme = −λ/(4π) × unwrapped phase — işaret konvansiyonu ürün dokümanından/ATBD'den DOĞRULANMALI.
- Dikey ≈ LOS / cos(incidence) (yatay hareket ihmal varsayımı; sitede belirtilir).
- GUNW 80 m UTM grid; GCOV = gamma0, terrain corrected.
