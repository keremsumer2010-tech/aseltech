# PC6 — GNSS doğrulama verisi + altyapı hatları

## Kimlik
M3hmeT1888 · Antigravity (Gemini) · klasör `aseltech-gemini2`

## Yazma alanı
`validation/`, `risk/`, `status/PC6.md`

## En kritik iş
En az 3 GNSS istasyonunun dikey serisi (jürinin "nasıl biliyorsunuz?" sorusunun cevabı).

## Görevler  (faz planı ve saatler: docs/GOREV_DAGILIMI.md §3b — 16:30 özellik dondurma, 17:00–17:30 QA görevin orada)
1. **(12:30–15:00) GNSS istasyonları**
   - Central Valley bbox'ı (`rules/VERI_SOZLESMESI.md` §1) içindeki sürekli GNSS istasyonları; girişsiz açık kaynak (Nevada Geodetic Laboratory geodesy.unr.edu veya EarthScope).
   - `validation/gnss_stations.csv` (format §5).
   - 2025-11-24 → 2026-10-14 döneminde verisi olan, çökme bölgesindeki EN AZ 3 istasyonun Up serisi → `validation/gnss/<station>.csv` (`date, up_cm`; birimi kontrol et).
   - `validation/README.md`: istasyonlar, seçim nedeni, kaynak, referans çerçevesi.
2. **(15:00–17:30) Altyapı hatları** — Overpass API (girişsiz), Central Valley bbox'ı:
   kanallar (`waterway=canal`; California Aqueduct, Delta-Mendota, Friant-Kern), `highway=motorway|trunk`, `railway=rail`
   → `risk/central_valley_infra.geojson` (`name, type, osm_id`), < 20 MB. `risk/README.md`: sorgu, tarih, "© OpenStreetMap contributors, ODbL".
3. **(17:30 sonrası)** Karapınar hatları → `risk/karapinar_infra.geojson`; sonra QUEUE Q05/Q06.

## Bitti sayılır eğer
csv'de her istasyonun kaynağı var · ≥3 seri, tarih aralığı NISAR dönemini kapsıyor, birim cm · geojson geçerli ve < 20 MB · README'ler var.

## B planı
- Bir kaynak giriş isterse diğerini dene; ikisi de olmazsa `BLOCKED` ve istasyon listesini (seri olmadan) push et.
- Overpass zaman aşımı: bbox'ı 4 parçaya bölüp birleştir.

## Yapma listesi
İstasyon/koordinat uydurma · giriş gerektiren kaynağa şifre girme · `data/`'ya yazma (Q05/Q06'yı sahiplenmeden).

## Rapor (`status/PC6.md`)
İstasyon adları ve konumları, seri aralıkları, dosya boyutları, doğrulanamayanlar.
