# ZAMAN ÇİZELGESİ — kim, saat kaçta, ne yapar (TR saati)
Bu dosya `tasks/PCx.md` ile birlikte okunur. Çakışırsa bu dosyadaki SIRA geçerlidir; görevin ayrıntısı `tasks/PCx.md` ve `tasks/QUEUE.md`'de.
Bir işi erken bitiren, SIRADAKİ satırına hemen geçer (bekleme yok). Kendi satırların bittiyse QUEUE'da atanmamış işi al (RULES §7.1).
Kontrol noktaları: **13:30** ilk GUNW açıldı mı · **15:30** ilk gerçek cm haritası sitede mi · **16:30** özellik dondurma · **17:00** yayın · **17:30** prova.
Pazar: **20:00** son veri dondurma · **22:00** teslim (resmi son Pzt 02:59).

## CUMARTESİ 14 KASIM
| Saat | PC1 Kerem (Claude) | PC2 Memir (Antigravity) | PC3 Mehmet (Claude Code) | PC4 İbrahim (Antigravity) | PC5 Mehmet (Antigravity-1) | PC6 Mehmet (Antigravity-2) |
|---|---|---|---|---|---|---|
| 12:40–13:30 | Görev denetimi; yedek GUNW (iniyor) | Earthdata `.netrc` → ilk GUNW (09-08→09-20) → `docs/gunw_structure.md` PUSH | `insar.py` + sentetik testler | UK bulut/radar çifti → `data/uk/` | Oyun iskeleti | GNSS istasyon listesi |
| 13:30–14:00 | ✔ Kontrol 1; site iskeleti (placeholder) | 6 çiftin indirme/kesmesine başla | Karapınar kontrol haritası | Obruk araştırması | Oyun mekaniği | GNSS dikey seriler (≥3) |
| 14:00–15:30 | Site: Sahne 1–3, rozetler; UK çiftini bağla | Çift kes → her biri PUSH | İlk 2 npz gelince kümülatif hat; her yeni npz'de yeniden üret | Obruk noktaları → `sinkholes.geojson` | Kesit animasyonu | GNSS `README` → OSM sorgusu |
| 15:30–16:30 | ✔ Kontrol 2; gerçek cm haritasını bağla | Son çiftler | `data/central_valley/*` + `summary.json` PUSH | Kaynaklar + Holme Fen | Oyun bitir → PUSH | OSM Central Valley hatları |
| 16:30–17:00 | 🔒 Dondurma; oyunu ve obrukları bağla | Q01 Karapınar GUNW indirme | Karapınar kümülatif başla | Kalibrasyon notu | Sunum metni (3 dk + 30 sn + 7 slayt) | `risk/central_valley_infra.geojson` PUSH |
| 17:00–17:30 | GitHub Pages yayın, telefon testi | QA: siteyi telefonda test → `docs/qa/PC2.md` | QA: sitedeki sayılar = kendi çıktın mı | QA: kaynak linkleri | QA: oyun sitede | QA: İngilizce metinler |
| 17:30–18:30 | Prova (3 dk), Lincoln sunumu hazırlığı | Prova: demo sürücüsü | Prova: veri/yöntem soruları | Prova: kaynak soruları | Sunum metni son hâl | OSM Karapınar hatları |
| Lincoln sunumu | Kerem anlatır | Demo | Soru-cevap | Soru-cevap | — | — |
| 18:30–20:00 | Sunum sonrası düzeltmeler | Q01 devam → Karapınar alt kümeleri | Q02 Karapınar cm haritası | Q11 proje sayfası taslağı | Oyun hızını `summary.json`'a bağla | Q06 risk scripti (sahte ızgarayla) |
| 20:00–22:00 | Yeni verileri siteye bağla | Q03 CV GCOV (6 tarih) | `analysis/out/central_valley_cum.npz` (PC6 için) + literatür kıyası | Q12 Space Apps kuralları doğrulama | Q13 README | Q06 devam |
| 22:00–23:00 | Gün sonu durum, Pazar görevlerini yaz | Q07 tam yıl indirmesini BAŞLAT (gece sürsün, PC açık kalsın) | Günlük rapor, testler | Günlük rapor | Q15 kod gözden geçirme | Günlük rapor |
| Gece | — | Q07 indirme (sadece indir/kes, insan uyuyabilir) | — | — | — | — |

## PAZAR 15 KASIM
| Saat | PC1 | PC2 | PC3 | PC4 | PC5 | PC6 |
|---|---|---|---|---|---|---|
| 09:00–12:00 | Durum kontrolü, gece işlerini doğrula | Q07 kesmeyi bitir → `subset/central_valley_beta/` | Q08 kalıcı vs geri dönen (`*_fullyear`, mixed) | Obruk zaman çizelgesi + yeraltı suyu kaynakları | 30 sn video senaryosu + `.srt` altyazı | Q05 GNSS karşılaştırma (PC3'ün `_cum.npz`) |
| 12:00–15:00 | Tam yıl + doğrulama katmanlarını bağla | Q04 SME2 toprak nemi → `drivers.json` | Q05'e istasyon pikseli desteği; sonuç kontrolü | Video altyazılarının kaynak/sayı kontrolü | ≤7 slayt son hâl | Q06 risk indeksi → `assets.json` |
| 15:00–18:00 | Risk + nem grafiği bağla; Higgsfield video kesimi | Q09 UK kil (Londra) GUNW indir/kes | Q09 UK kil analizi ("below detection" olabilir) | Sitedeki her sayının kaynağı var mı denetimi | Oyun cilası, erişilebilirlik | Q14 tüm `meta.json` QA |
| 18:00–20:00 | Proje sayfası doldurma | Q10 Fens ekin ritmi (zaman kalırsa) | Son sayılar → `summary.json` final | Proje sayfası metni son okuma | Video son kurgu desteği | Q17 göl/baraj (zaman kalırsa) |
| 🔒 20:00 | **Son veri dondurma** | | | | | |
| 20:00–22:00 | Video + proje sayfası + AI kullanım açıklaması | Telefon/tarayıcı testi | Sayı kontrolü | Link kontrolü | Video/slayt kontrolü | Metin kontrolü |
| **22:00** | **"Submit for Judging"** | | | | | |
| 22:00–02:59 | Sadece acil düzeltme | — | — | — | — | — |

## İnsanlar için
- Ajan durursa: `Durma. git pull yap, docs/ZAMAN_CIZELGESI.md'de saatine bak, sıradaki işe devam et.`
- Mehmet: üç ajanın aynı anda büyük indirme yapmaz; PC3 önceliklidir.
- Gece indirmesi için bilgisayar açık ve uykuya geçmeyecek şekilde kalmalı (Memir).
