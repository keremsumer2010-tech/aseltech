# PC5 — Oyun + hikâye (klasör: game/ ve docs/story/)

## Görev 1a — Kaynak listesi (Gemini veya Claude ile, ama HER linki aç ve doğrula)
`docs/story/sources.md`: Central Valley çökmesi (NASA/JPL, USGS), Konya çökmesi/obruk (hakemli makale),
NISAR görevi (nasa.gov / jpl.nasa.gov), yeraltı suyu ve sulama ilişkisi. Her kaynak: başlık, link, 1 cümlelik bulgu, sayı varsa sayı.
Doğrulamadığın link YAZMA.

## Görev 1b — "Aquifer Manager" prototipi
`game/index.html` (saf HTML/JS, tek dosya olabilir):
- Oyuncu pompalama seviyesini (%0–150) ve yağışlı/kurak yıl senaryosunu seçer.
- Basit model: yıllık çökme = ölçülen_hız × pompalama_oranı × senaryo_katsayısı (şimdilik ölçülen_hız = 10 cm/yıl, "placeholder" yaz).
- 10 yıllık animasyon: kesit görünümde toprak katmanı iner, kanal/yol ikonları hasar görür.
- Sonuç ekranı: toplam çökme + "what this means" cümlesi. Katsayılar tek bir CONFIG nesnesinde.

## Kabul
- sources.md'de en az 6 doğrulanmış kaynak; oyun tarayıcıda hatasız açılıyor; status'ta ekran görüntüsü `docs/game_v1.png`.
