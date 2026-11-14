# ATLAS FİNAL PLANI — "NISAR Global Subsidence Atlas 2026" (PC1, Paz 00:20)
Bu dosya `docs/ATLAS_PLANI.md`'nin (KALİTE STANDARDI hâlâ zorunlu) ÜSTÜNE eklenen son plandır. Hedef: jüri siteyi açtığı anda "bunu NASA mı yaptı?" desin; mühendis "bu sayıların arkasında durabilirim" desin.
**PC6 ve PC8 artık PC1 koordinasyonunda (Kerem kararı, Paz 00:20).** PC3'e Mehmet görev verir.

## 1. Durum tespiti (Paz 00:15, repo ve canlı sayfa incelendi)
| Konu | Durum | Sorun |
|---|---|---|
| Atlas verisi | 11 bölge (6 güvenilir, 5 indicative), `atlas.json` kalite alanlarıyla | Hedef 20+. **Tahran (−3.5) ve Pekin (−1.4) yanlış referansla:** havza dışı referansla −7.3 ve −7.6 (PC11 kısmi kontrol). Sıralamadaki en büyük hata bu. |
| Atlas sayfası | `web/atlas.html` çalışıyor: küre, liste, güven rozeti, bülten bağlantısı | Zaman kaydırıcı/animasyon yok, katman yok, çevrimdışı yedek yok (Lincoln'de internet kesilirse küre siyah kalır), sunum turu yok. |
| Bültenler | 11 şehir HTML bülteni | Operasyonel ürün görünümü (başlık bloğu, ürün kimliği, sürüm) eksik; nüfus etkisi yok. |
| Bilim | Sayı sicili, detectability, robustness (yerel veriyle "inconclusive") | Tam kutulu yeni şehirlerle robustness kesinleşmeli; 108 gün → yıllık sorusu açık (PC9 FAZ 2). |
| Anlatım | Basın özeti, teknik not, şehir kartları, yöntem, veri sözlüğü | NASA Earth Observatory tarzı tek "öne çıkan hikâye" yok; veri atıfları (DOI) eksik. |
| Takım adı | Sitede "Team Aseltech" (PC6 B32) | Kerem onayı gerekir (Taykut mu Aseltech mi). |

## 2. NASA'dan alınan ilhamlar → bizdeki karşılığı
| NASA örneği | Neyi iyi yapıyor | Bizde |
|---|---|---|
| NASA Eyes on the Earth / Worldview | Küre + zaman kaydırıcı + katman seçimi | Atlas v2: tarih kaydırıcı, katmanlar (çökme / belirsizlik σ / koherens), otomatik "tur" (PC6) |
| NASA Climate "Vital Signs" | 4 büyük gösterge kartı, tek bakışta | Atlas üstünde 4 kart: ölçülen şehir, en hızlı çöken yer, >5 cm çöken alan km², çöken zeminde yaşayan insan (PC8 veri, PC6 sayfa) |
| NASA Earth Observatory "Image of the Day" | Tek güçlü görsel + 3 paragraf, sade dil, kaynak satırı | `docs/story/atlas_feature.md` "Where the ground is sinking fastest in 2026" + 3 açıklamalı görsel (PC4) |
| NASA Disasters Program harita paketleri | Ürün kimliği, tarih, veri kaynağı, sorumluluk reddi, sürüm | Bülten v2 başlık bloğu: Product ID, issue time, data window, quality class, disclaimer (PC8) |
| JPL OPERA DISP-S1 (NASA'nın kendi çökme ürünü) | Bağımsız NASA ürünü | "NISAR vs OPERA" çapraz kontrol: Kuzey Amerika şehirleri (PC2) |
| NASA SVS görselleştirmeleri | Gerçek veriden sinematik animasyon | Video v2 hazır; Paz 16:00'da final atlasla yeniden üret (PC6, opsiyonel) |
| NASA açık veri ilkesi | İndirilebilir veri + atıf | `atlas.geojson` + `atlas.csv` + DOI'li veri atıfları (PC10, PC4) |

## 3. İş paketleri (herkes aynı anda; ayrıntılar `tasks/PCx.md` sonunda "ATLAS FİNAL" bölümü)
- **PC10 — atlas çekirdeği:** 20+ şehir, yeni alanlar (`detectable`, `robustness_spread`, `people_exposed`, `opera_check`), `atlas.geojson` + `atlas.csv`. **Tahran/Pekin kuralı:** PC11 Paz 06:00'a kadar tam kutu indirmeye başlamazsa Tahran ve Pekin'i PC10 yeniden hesaplar.
- **PC6 — atlas sayfası v2 (sahibi):** zaman kaydırıcı animasyon, katmanlar, Vital Signs kartları, sunum turu, çevrimdışı yedek, paylaşılabilir şehir linki.
- **PC8 — operasyonel ürünler:** bülten v2 (NASA Disasters tarzı) + çöken zeminde yaşayan nüfus (GHSL açık veri) + `data/global/vital_signs.json` + teslim formu atlas metni.
- **PC2 — kendi şehirleri, sonra NISAR vs OPERA** (Houston, Eloy, Mexico City, Central Valley).
- **PC4 — Earth Observatory tarzı öne çıkan hikâye** + veri atıfları + slayt/teknik not finali.
- **PC5 — baş bilimci:** her yeni şehre karar, Tahran/Pekin düzeltmesinin onayı, Paz 19:00 SCIENCE_SIGNOFF.
- **PC7, PC9, PC11:** mevcut uzun planları (şehirler, robustness, yıllıklaştırma, küresel altyapı riski).

## 4. Zaman çizelgesi
| Saat (TR) | Kilometre taşı |
|---|---|
| Paz 06:00 | ≥16 şehir atlasa girdi; Tahran/Pekin tam kutu hesapta |
| Paz 10:00 | Atlas v2 sayfası (kaydırıcı, katman, kartlar, tur) yayında |
| Paz 14:00 | 20+ şehir; robustness kesin; yıllıklaştırma sonucu; OPERA kıyası |
| Paz 16:00 | Öne çıkan hikâye, bülten v2, nüfus etkisi; (ops.) video final |
| Paz 19:00 | PC5 SCIENCE_SIGNOFF |
| Paz 20:00 | Veri dondurma — sadece hata düzeltme |
| Paz 22:00 | Teslim |

## 5. Değişmeyen kurallar
KALİTE STANDARDI (`docs/ATLAS_PLANI.md`), REVIEW_1500 dili, uydurma yok, `atlas.json`'u yalnız PC10 yazar, `git add <kendi yolların>`, önce commit → `pull --rebase` → push. Kalibrasyon cümlesi her üründe: "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."
