# PC6 — Çelik (Antigravity) — Doğrulama + altyapı verisi  ·  Ana plan: docs/MASTER_PLAN.md
Klasörlerin: `validation/`, `risk/`. Başka yere yazma. Uydurma koordinat, sayı veya link YASAK.
Bu iş Pazar günkü özgün katkılar #3 (risk indeksi) ve #4 (GNSS doğrulama) için veriyi BUGÜNDEN hazırlar.

## Görev 1 — GNSS istasyonları (12:30–15:00 TR)
1. Central Valley bbox'ı (CLAUDE.md) içindeki sürekli GNSS istasyonlarını bul. Açık kaynak: Nevada Geodetic Laboratory (geodesy.unr.edu)
   veya EarthScope. Girişsiz indirilebilen kaynağı kullan; kaynağı status'a yaz.
2. `validation/gnss_stations.csv`: `station, lon, lat, source_url, series_url, first_date, last_date`.
3. NISAR verisinin kapsadığı dönemde (2025-11-24 → 2026-10-14) verisi olan istasyonlardan, çökme bölgesinde olan EN AZ 3 tanesinin
   dikey (Up) zaman serisini indir → `validation/gnss/<station>.csv` (`date, up_cm`). Birimi kontrol et.
4. `validation/README.md`: hangi istasyonlar, neden seçildi, kaynak, referans çerçevesi.

## Görev 2 — Altyapı hatları (15:00–17:30 TR)
OpenStreetMap Overpass API (girişsiz) ile Central Valley bbox'ı için:
- kanallar (`waterway=canal`, özellikle California Aqueduct / Delta-Mendota / Friant-Kern), ana yollar (`highway=motorway|trunk`), demiryolları (`railway=rail`)
→ `risk/central_valley_infra.geojson` (sadece gerekli etiketler: name, type, osm_id). Dosya < 20 MB olsun; gerekirse sadeleştir.
`risk/README.md`: sorgu metni, tarih, lisans notu ("© OpenStreetMap contributors, ODbL").

## Görev 3 (zaman kalırsa) — Karapınar için aynı altyapı hatları → `risk/karapinar_infra.geojson`

## Rapor
status/PC6.md: ne bitti, istasyon adları, dosya boyutları, doğrulanamayanlar.
