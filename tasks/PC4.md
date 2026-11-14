# PC4 — acikgozibrahim032-hub (Antigravity) — Görseller, obruklar, kaynaklar  ·  BUGÜN: docs/TODAY_PLAN.md
Klasörlerin: `data/uk/`, `data/karapinar/sinkholes.geojson`, `docs/story/`. Başka yere yazma.
Önce CLAUDE.md'deki "Veri kalitesi ve kalibrasyon" kuralını oku. Uydurma koordinat, sayı veya link YASAK.

## Görev 1 — UK "bulutun altı" görsel çifti (12:00–13:30 TR)
1. Fens/Lincolnshire (bbox CLAUDE.md'de `fens`) için NISAR GCOV tarihlerini ASF'den listele (`platform=NISAR`, `processingLevel=GCOV`).
2. Bu tarihlerden **optik görüntüde bulutlu olan** bir gün seç: NASA Worldview Snapshots / GIBS (girişsiz) ile
   o günün MODIS veya VIIRS true color görüntüsünü bbox için indir. Birkaç günü dene, en bulutlusunu seç.
3. Aynı günün NISAR GCOV **browse PNG**'sini indir (girişsiz iner).
4. Çıktılar:
   - `data/uk/optical_<YYYY-MM-DD>.jpg`, `data/uk/radar_<YYYY-MM-DD>.png` (aynı bbox'a kırp/hizala)
   - `data/uk/meta.json`: `{date, bbox, optical_source_url, optical_product, radar_granule, radar_browse_url, quality:"preview", note}`
   - radar görüntüsü kalite sınıfı `preview` (nicel değil).

## Görev 2 — Karapınar obruk noktaları (13:30–15:30 TR)
`data/karapinar/sinkholes.geojson` — sadece bir KAYNAKTA koordinatı verilen veya adı ve yeri net tanımlanmış obruklar.
Her nokta properties: `name`, `lon`, `lat`, `year_formed` (varsa), `source_title`, `source_url`, `coord_source` ("paper table" / "official" / "wikipedia" vb.).
Koordinatı tahmin etme. En az 5, ideal 10+ nokta. Hakemli makale veya resmi kurum (AFAD, MTA, üniversite) öncelikli.

## Görev 3 — Kaynak listesi + Holme Fen (15:30–17:00 TR)
`docs/story/sources.md` — her linki AÇ, doğrula. Başlık, link, 1 cümle bulgu, sayı varsa sayı:
- Holme Fen direği: ne zaman dikildi, zemin ne kadar alçaldı (kaynaklı)
- Central Valley çökmesi (NASA/JPL, USGS) · Sacramento Delta setleri · Karapınar/Konya çökme ve obruklar
- UK kil şişme-büzülme (BGS) · NISAR görevi (nasa.gov / jpl.nasa.gov) · NISAR veri sürümleri ve kalibrasyon durumu
`docs/story/calibration_note.md`: ASF/JPL ürün notlarına göre 2026-06-17 öncesi ürünlerin durumu (beta / pre-calibration mi?) — kaynaklı, kısa.

## Rapor
status/PC4.md: ne bitti, hangi kaynaklar, doğrulanamayanlar.
