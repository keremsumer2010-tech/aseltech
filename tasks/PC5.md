# PC5 — Neden + doğrulama + hikâye (klasör: game/, docs/story/, analysis/drivers/)

## Görev 1a — Doğrulanmış kaynaklar (her linki AÇ)
`docs/story/sources.md`: Central Valley çökmesi (NASA/JPL, USGS), Sacramento Delta setleri, Konya çökme/obruk (hakemli),
UK kil şişme-büzülme (BGS), Holme Fen direği (kaç m alçaldı — kaynaklı), NISAR görevi. Başlık, link, 1 cümle bulgu + sayı.

## Görev 1b — GNSS istasyonları
Central Valley bbox'ındaki GNSS istasyonlarını ve açık zaman serisi kaynağını bul (ör. Nevada Geodetic Laboratory / EarthScope).
`analysis/drivers/gnss_stations.csv` (ad, lon, lat, URL) + 3 istasyonun Kas 2025–Eki 2026 dikey serisini indir → `analysis/drivers/gnss/*.csv`.

## Görev 2 — Toprak nemi zaman serisi
PC2'nin SME2 kesitlerinden bölge ortalaması/nokta serisi → `data/central_valley/drivers.json` (soil_moisture alanı).

## Görev 3 (bonus) — Aquifer Manager
`game/index.html`: pompalama %0–150 + yağışlı/kurak yıl → 10 yıllık çökme animasyonu. Hızlar CONFIG'de, sonra PC3'ün ölçtüğü değerle değişecek.

## Kabul
En az 6 doğrulanmış kaynak; 3 GNSS serisi; status'ta indirme yöntemi.
