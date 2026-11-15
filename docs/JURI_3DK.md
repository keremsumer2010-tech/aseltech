# JÜRİ 3 DAKİKA — final kurgu (PC1, Paz 11:15 TR · Cambridge, MA Virtual güncelleme 18:00 TR)
Yerel etkinlik **NASA Space Apps Cambridge (virtual)**. Canlı 3 dk sunum YOK; çok disiplinli yargıçlar (MIT/Harvard çevresi, tasarımcı, eğitimci, mühendis) 16–20 Kasım'da proje sayfasını, videoyu ve siteyi **kendi başlarına** 3 dakikada inceleyecek. Bu süre içinde şunu net görmeli: **sorun ne, ne yaptık, neden özgün, neden güvenilir, kime yarar.** Sitede yazan her cümlenin bir işi olacak; her sayının kaynağı olacak; gerisi "Deep dive" altına.
Yeni veri/özellik yok: **toplama, birleştirme, sadeleştirme.** Veri dondurma 20:00, teslim 22:00.

## Sanal Yargıç Yolu (Cambridge, MA Virtual — 3 Dakikada Kendi Başına İnceleme Rotası)
| Sıra | Süre | Durak | Yargıcın Gördüğü |
|---|---|---|---|
| 1 | `0:00–0:35` | **Ana Sayfa (`web/index.html`)** | Tek cümlelik öz ("We used NASA-ISRO's new NISAR radar satellite to measure where the ground is sinking in 29 places, and built checks that catch our own mistakes"), 5 büyük sayı ve `#1 Eloy, Arizona (−8.6 cm / −3.4 in)`. |
| 2 | `0:35–1:05` | **How We Know (`web/index.html#w2` / `web/science.html`)** | Kendi hatamızı yakalayan QC (Semarang 12.1 cm faz sıçraması düzeltmesi), 10 GPS istasyonu (`r = 0.924`) ve ikincil OPERA kontrolü (`r = 0.912`). |
| 3 | `1:05–1:45` | **Küresel Atlas (`web/atlas.html`)** | 3B küre üzerinde 29 havza (`15` güvenilir / `14` gösterge), renk skalası, 4 ABD havzası (`Eloy`, `Central Valley`, `Houston`, `Delta`) ve Konya Ovası dürüstlük/öz-denetim örneği. |
| 4 | `1:45–2:10` | **Tek Sayfa Bülten (`docs/bulletins/eloy.html` / `konya_plain.html`)** | Su yöneticisinin doğrudan kullanacağı A4 bülten: hız, etkilenen nüfus (GHSL), kritik altyapı eğim ön taraması (`81/645`) ve zorunlu kalibrasyon dipnotu. |
| 5 | `2:10–2:35` | **Yeraltı Suyu Simülatörü (`game/`)** | Terra Bella hızına kalibre edilmiş 24 aylık etkileşimli Terzaghi sıkışma modeli — pompalamayı artırıp kalıcı kil çökmesini 30 saniyede deneyimleme. |
| 6 | `2:35–3:00` | **Tanıtım Videosu (`docs/story/media/nisar_vision_overview.mp4`)** | 3 soru akışını (*What we found → How we know → What it's for*) İngilizce altyazılı, gerçek uydu/site görüntüleriyle özetleyen ≤3 dk (1080p) başvuru videosu. |

## Tek cümlelik özümüz (her yerde aynı)
> **We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: 29 basins measured with one open pipeline on the same 93 days, every number traceable to its file, and every headline checked against GPS, NASA's OPERA product and the literature.**

## Özgün yanlarımız (jüriye söylenecek 4 şey)
1. **Aynı pencere, aynı yöntem, 29 havza** — NISAR'ın ilk provisional verisiyle karşılaştırılabilir küresel sıralama (93 günlük ortak pencere, ±0.25° kutu, havza dışı referans).
2. **Kendi hatasını yakalayan atlas** — zaman serisi kalite kontrolü (L-band tam faz döngüsü 12.1 cm, tek tarih aykırısı) Semarang'ın 1. sıra değerini hata olarak yakaladı; düzeltilince −12.1 → −6.2 cm. Tahran ve Pekin referans hatası düzeltildi.
3. **Bağımsız kanıt** — Central Valley 10 GPS istasyonu r = 0.92; Mexico City NASA JPL OPERA r = 0.91.
4. **Ölçümden karara** — çöken zeminde yaşayan 1.17 milyon kişi (1,167,429 kişi); Central Valley'de yılda 0.32 km³ kalıcı akifer kaybı; kanal/yol segmentleri için hasar olasılığı; her bölge için tek sayfa bülten; herkesin oynayabileceği simülatör; tek komutla yeniden üretilebilir açık motor.

## 3 dakikalık akış (ana sayfa sırası = sunum modu sırası)
| Süre | Bölüm | Jürinin göreceği | Kaynak |
|---|---|---|---|
| 0:00–0:20 | **Hero** | tek cümle + 3 büyük sayı (29 havza · 1.17 M kişi · r = 0.92 GPS) + "Explore the atlas" | `vital_signs.json`, `validation_report.md` |
| 0:20–1:00 | **Atlas** | küre küçük önizleme + ilk 5 tablo (ortak pencere: #1 Eloy −8.6) + Konya dürüstlük örneği (denetim sonucu gösterge) | `atlas.json` |
| 1:00–1:30 | **Kendi hatamızı yakaladık** | Semarang önce/sonra (tek grafik/iki sayı) + "5 bölge indicative" | `qc_flags.json`, `atlas_top5_check.md` |
| 1:30–2:05 | **Neden güvenilir** | GPS r = 0.92, OPERA r = 0.91, belirsizlik σ ≈ 0.3 cm, provisional/kalibrasyon cümlesi | `validation_report.md`, `opera_check.json` |
| 2:05–2:40 | **Ne işe yarar** | 1.17 M kişi · 0.32 km³/yıl kalıcı kayıp · kanal riski · bülten · "Try the simulator (30 s)" | `exposure_atlas.json`, `storage_loss.json`, `assets_prob.json` |
| 2:40–3:00 | **Özgün + açık** | 4 özgün katkı kartı + "reproduce in one command" + ekip | README, engine.md |
| sonra | **Deep dive** | eski uzun hikâye bölümleri, Science, Data, bültenler | mevcut |

## Kurallar
- Her bölüm: 1 başlık (≤8 kelime), 1 cümle (≤25 kelime), 1 büyük sayı (birim + kalite etiketi), 1 görsel, 1 bağlantı.
- Sayılar yalnız `data/global/home_summary.json` (PC10 üretir) ve SIGNOFF'tan. Elle sayı yok.
- Kalibrasyon cümlesi görünür: "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."
- Jargon yok ya da tek kelimeyle açıklanmış (LOS = "toward/away from the satellite").
- Ana sayfa ilk ekranda (1920×1080 ve 375 px) mesajı versin; tüm sayfa < 2 sn açılış.

## Sahipler
PC1: ana sayfa (`web/index.html` üst kısmı, `web/app.js` ilgili kısım) ve son kurgu. PC4: metin. PC6: site mühendisliği/simülatör. PC10: `home_summary.json` + atlas dondurma. PC7: sayı tutarlılık bekçisi + yarım veri işleri. PC2: tek komut yeniden üretim. PC8: teslim formu + jüri tek sayfası. PC11: Cakarta, sonra dondurma desteği.
