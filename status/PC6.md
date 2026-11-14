# PC6 durum

- Görev: 1 (GNSS), 2 (Altyapı — Central Valley), 3 (Altyapı — Karapınar)
- Durum: Görev 1, 2 ve 3 tamamlandı; sıradaki iş `Q05` (`validation/compare.py`) ve `Q06` (`risk/compute_risk.py`)
- Çıktılar:
  - `validation/fetch_gnss.py` (7.1 KB)
  - `validation/gnss_stations.csv` (4.0 KB, 23 istasyon, Central Valley bbox `[-120.2, 35.6, -119.0, 36.6]`, en az `2026-06-28` → `2026-09-20`)
  - `validation/gnss/*.csv`: 10 istasyon (`TLBN`, `QCAP`, `CAHA`, `HANF`, `CAFP`, `P056`, `CAD1`, `P565`, `P564`, `P566`), 515–658 satır/dosya (`10.3–13.7 KB`), birim `cm` (`up_cm`, NGL IGS20/NA `.NA.tenv3` m→cm dönüşümü)
  - `validation/README.md` (kaynaklar, IGS20/NA referans çerçevesi, dönem ve değişim özeti)
  - `risk/fetch_osm_infra.py` (5.0 KB)
  - `risk/central_valley_infra.geojson` (1.066 MB < 20 MB; 3,238 hat: `canal`=1,662, `rail`=656, `motorway`=591, `trunk`=329; özellikler yalnızca `name, type, osm_id`)
  - `risk/karapinar_infra.geojson` (0.040 MB; 64 hat: `secondary`=45, `trunk`=19; özellikler yalnızca `name, type, osm_id`)
  - `risk/README.md` (Overpass QL sorguları, tarih `2026-11-14`, lisans `© OpenStreetMap contributors, ODbL`)
- Doğrulama:
  - `python validation/fetch_gnss.py` çalıştırıldı: 23 istasyon bulundu; seçilen 10 istasyonun `.sta` sayfaları HTTP 200 döndü; 10 istasyonun tümü `2026-06-28 → 2026-09-20` provisional döneminde tam günlük veriye (`jun_n=7, sep_n=7`) ve `TLBN` (-3.90 cm provisional / -10.77 cm tam yıl), `QCAP` (-3.59 cm / -7.79 cm), `CAHA` (-3.38 cm), `HANF` (-2.54 cm / -6.61 cm), `CAFP` (-2.40 cm), `P056` (-1.65 cm / -3.01 cm) gerçek çökme sinyallerine sahip; `P566` (-0.02 cm / -0.93 cm) referans kenar istasyonu.
  - Kaynak: NGL `https://geodesy.unr.edu/NGLStationPages/DataHoldings.txt` ve `https://geodesy.unr.edu/gps_timeseries/IGS20/tenv3/NA/<STA>.NA.tenv3` (`README_tenv3.txt`).
  - `python risk/fetch_osm_infra.py` çalıştırıldı: JSON geçerli, dosya boyutları < 20 MB, named kanallar arasında `California Aqueduct` (ve Coastal Branch Phase 1/2) ve `Friant-Kern Canal` mevcut (`Delta-Mendota Canal` bbox kuzey sınırının dışında).
- BLOCKED: yok
- AI: Antigravity (Gemini) -> GNSS/OSM veri indirme scriptleri, doğrulama kontrolü ve README dokümantasyonu
