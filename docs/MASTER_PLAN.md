# MASTER PLAN — NISAR Pulse: Follow the Water
Team Taykut · NASA Space Apps 2026 · Challenge: Dancing with the SARs · Local event: Lincoln (UK)

## 1. Tek cümle
"NISAR radar sees through clouds and measures the ground moving by centimetres. We turn it into a story anyone can read:
farms are irrigated, groundwater is pumped, and the ground sinks — in California, in Konya, and beneath Britain's clouds."

## 2. Neden kazanır (jüri kriterleri → bizim karşılığımız)
| Kriter | Karşılık |
|---|---|
| Impact | Çökmenin altyapıya etkisi (kanal/yol/set), obruk riski, kalıcı akifer kaybı; NISAR Handbook §2.4'ün kendi uygulama soruları |
| Creativity | Kaydırmalı hikâye + "bulutun altını gör" kaydırıcısı + Aquifer Manager oyunu; üç ülke tek hikâye |
| Validity | Resmi NISAR ürünleri (GUNW), resmi ATBD yöntemine dayalı dönüşüm, kalite rozetleri, belirsizlik notu, Pazar: GNSS doğrulama |
| Relevance | NISAR verisi her sahnenin merkezinde; üç ürün (GUNW, GCOV, SME2) |
| Presentation | Tek link, telefonda da çalışan sayfa, 30 sn video, açık kaynak repo |

Hedef ödüller: Lincoln yerel birincilik → Global Nominee; global kategoriler: Best Use of Data, Best Storytelling, Local Impact.

## 3. Ürün — tek web sayfası (kaydırmalı hikâye)
0. **Açılış** — Higgsfield sinematik giriş videosu (AI etiketi) + başlık + "Scroll to follow the water".
1. **Britain under clouds (UK)** — aynı günün bulutlu optik görüntüsü ↔ NISAR radar önizlemesi, sürüklenebilir çizgi. Holme Fen kartı (kaynaklı). Mesaj: optik uydular göremez, radar görür.
2. **The dancing ground (USA, Central Valley)** — kümülatif çökme haritası, zaman kaydırıcısı + oynat, tıkla → grafik + sade cümle + insan ölçeği. Rozet: PROVISIONAL.
3. **Konya's sinkholes (TR, Karapınar)** — kaynaklı obruk noktaları + NISAR katmanı (cm haritası varsa, yoksa PREVIEW). Obruk kesiti illüstrasyonu (AI etiketi).
4. **Why it happens** — sulama → pompalama → çökme şeması; (Pazar) toprak nemi grafiği.
5. **Aquifer Manager** — oyun.
6. **How we know** — veri ürünleri, yöntem, kalite sınıfları, kalibrasyon dipnotu, kaynaklar, repo linki, ekip.

## 4. Kalite ve dürüstlük kuralları (her yerde)
- Kalibrasyon NISAR projesinin (NASA-JPL, ISRO) işidir; biz ürünleri yayınlandığı hâliyle kullanırız.
- Kalite sınıfları: PROVISIONAL / PRE-CALIBRATION BETA / PREVIEW; karıştırılmaz, rozetle gösterilir.
- Yapay zekâ ile üretilen görsel/video ASLA veri gibi gösterilmez; her birinde "AI-generated illustration" etiketi.
- Uydurma sayı yok; ölçülmeyen değer "illustrative" diye işaretlenir. NASA logosu kullanılmaz.

## 5. Ekip ve araçlar
| Kim | Araç | ID | Bugünkü iş |
|---|---|---|---|
| Kerem | Claude (yönetmen) | PC1 | Web sitesi, Higgsfield medya, birleştirme, Pages, sunum |
| Mehmet | Claude Code | PC3 | Çökme analizi (cm, kümülatif, Karapınar) |
| Mehmet | Antigravity | PC5 | Aquifer Manager oyunu + sunum metni |
| Memir | Antigravity | PC2 | NISAR GUNW indirme/kesme |
| İbrahim | Antigravity | PC4 | UK sahnesi görselleri, Karapınar obruk koordinatları, kaynak listesi |
| Mehmet | Antigravity (2.) | PC6 | GNSS istasyonları + OSM altyapı hatları (Pazar: doğrulama ve risk indeksi) |

## 6. BUGÜN — saat saat (TR)

PC6 bu tabloda yok; saatleri `tasks/PC6.md` içinde (12:30-15:00 GNSS, 15:00-17:30 altyapı). Kurallar `rules/RULES.md`, sahiplik `docs/GOREV_DAGILIMI.md`.

| Saat | PC1 | PC2 | PC3 | PC4 | PC5 |
|---|---|---|---|---|---|
| 12:00–13:30 | Site iskeleti + sahte veri; Higgsfield açılış videosu | Earthdata, liste, ilk GUNW, yapı dosyası | insar.py + testler | UK görsel çifti | Oyun |
| 13:30 kontrol | GUNW açıldı mı? Hayırsa B planı | | | | |
| 13:30–15:30 | Sahne 1–3 arayüz, rozetler | 6 provisional çift kes/push | Karapınar cm haritası | Obruk koordinatları (kaynaklı) | Oyun |
| 15:30 kontrol | İlk gerçek cm haritası? | | | | |
| 15:30–17:00 | Gerçek veriyi bağla, oyunu göm | (Pazar verisine başla) | Central Valley kümülatif + noktalar | Kaynak listesi + Holme Fen | Sunum metni |
| 17:00–17:30 | GitHub Pages yayında, telefonda test | | Karapınar data/ | | |
| 17:30+ | Prova: 3 dk konuşma + canlı demo | | | | |

**B planı (13:30'da GUNW açılmazsa):** Sahne 2–3 browse PNG'lerle (PREVIEW rozetli) yapılır; hikâye ve oyun aynen kalır.

## 7. Lincoln sunumu (bugün)
- 3 dakikalık akış: (1) Kanca: Holme Fen direği — "this ground fell metres" (sayı kaynaklı) (2) Sorun: veri var, okunmuyor (3) Canlı demo: bulut kaydırıcısı → Central Valley animasyonu → bir noktaya tıkla → Karapınar (4) Oyun 15 sn (5) How we know + Pazar planı.
- Herkesin rolü: Kerem anlatır, biri demoyu sürer, sorulara veri sorumlusu (Mehmet) cevap verir.
- Muhtemel sorular hazırlığı: "Bu kalibre mi?" → kalibrasyon dipnotu; "Eğik mi dikey mi?" → LOS notu; "Atmosfer?" → Handbook §7.

## 8. PAZAR — küresel teslime kadar (son an Pzt 02:59 TR)
1. Tam yıl zinciri (Kas 2025–Eki 2026) → AYRI katman, `beta-precal` uyarılı.
2. Kalıcı vs geri dönen ayrımı (özgün katkı #1).
3. GNSS doğrulama: 3 istasyon, RMSE (özgün katkı #4).
4. Altyapı risk indeksi: kanal/yol eğimi (özgün katkı #3) — zaman kalırsa.
5. Toprak nemi grafiği (SME2).
6. UK: kil bölgesi tek harita denemesi; sinyal yoksa dürüstçe "below detection" yaz.
7. Oyunda hız → ölçülen değer.
8. 30 sn video (İngilizce altyazı) veya ≤7 slayt; proje sayfası.

## 9. Teslim kontrol listesi (Space Apps)
- [ ] Proje sayfası İngilizce, tüm alanlar dolu (özet, nasıl çalışır, faydalar, hedefler, araçlar)
- [ ] Demo: ≤30 sn video (İngilizce altyazı) VEYA ≤7 slayt; link herkese açık
- [ ] Repo linki ve canlı site linki herkese açık
- [ ] Kullanılan NASA verisi ve diğer kaynaklar listelendi
- [ ] Yapay zekâ kullanımı açıklandı (Claude, Gemini, Higgsfield — neyi ürettikleri) — gereklilik metnini PC1 doğrulayacak
- [ ] NASA logosu yok; AI görselleri etiketli
- [ ] Teslim saati: Pazar 23:59 UK = Pazartesi 02:59 TR — hedef Pazar 22:00 TR

## 10. Riskler
| Risk | Önlem |
|---|---|
| Earthdata/indirme sorunu | 13:30 kontrol, B planı browse PNG |
| İnternet yavaş | Bugün sadece 6 dosya (~14 GB) |
| İşaret/referans hatası | Testler + resmi ATBD'den işaret doğrulama + makul aralık kontrolü (literatürle kıyas) |
| Ajanlar çakışır | Ayrı klasör, `git add <yol>`, PC1 birleştirir |
| Zaman | Öncelik: Sahne 2 > Sahne 1 > oyun > Sahne 3 > diğerleri |
