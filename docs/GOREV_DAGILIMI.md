---
type: karar
status: acik
date: 2026-11-14
owner: PC1
evidence: "docs/MASTER_PLAN.md · docs/TODAY_PLAN.md · tasks/PC1-PC6.md"
---

# Görev dağılımı: 14-15 Kasım

4 kişi, 3 bilgisayar, 6 ajan. Bugün Lincoln yerel sunumu (demo **17:30 TR**), yarın global teslim
(**Pzt 02:59 TR**, iç hedef Paz 22:00 TR).

## Karar

İş, veri akışının katmanlarına göre bölünüyor: **veri indirme (PC2) → çökme analizi (PC3) → web (PC1)**
ana hat; yanında bağımsız üç hat: **hikâye ve kaynaklar (PC4)**, **oyun ve sunum metni (PC5)**,
**doğrulama ve altyapı verisi (PC6)**. PC1 yönetmen: görev yazar, birleştirir, siteyi yayınlar.

## Neden bu bölünme

Projenin darboğazı tek: **ilk gerçek santim haritası**. Her şey (site, oyun sayısı, sunum, risk,
doğrulama) ona bağlı. Ana hat (PC2 → PC3 → PC1) bu yüzden en kısa tutuldu ve kimseye başka iş
verilmedi. Geri kalan üç hat ana hatta hiç dokunmadan ilerleyebilecek işlerden seçildi; ana hat
gecikirse onlar boşta kalmaz.

---

## 1. Kim kim

| ID | Kişi (GitHub) | Bilgisayar · klon klasörü | Araç | Rol |
|---|---|---|---|---|
| **PC1** | Kerem (keremsumer2010-tech) | Kerem'in PC | Claude | Yönetmen + web + yayın + sunum |
| **PC2** | Memir (memir-erdogmus) | Memir'in PC | Antigravity | Veri indirme ve kesme |
| **PC3** | Mehmet (M3hmeT1888) | Mehmet'in PC · `aseltech-claude` | Claude Code | Çökme analizi (cm) |
| **PC4** | İbrahim (acikgozibrahim032-hub) | İbrahim'in PC | Antigravity | UK görselleri, obruklar, kaynaklar |
| **PC5** | Mehmet (M3hmeT1888) | Mehmet'in PC · `aseltech-gemini` | Antigravity | Matematik/analiz: ayrıştırma modülü + belirsizlik bütçesi (13:30) |
| **PC6** | Mehmet (M3hmeT1888) | Mehmet'in PC · `aseltech-gemini2` | Antigravity | GNSS doğrulama + altyapı verisi |

Mehmet'in bilgisayarında 3 ajan var: **klasör adın kim olduğunu söyler.** İnsan sorumluluğu:
Mehmet üçünü de izler; PC5 ve PC6 ajan işidir, kararları Mehmet verir.

---

## 2. Sahiplik: kim nereye yazar

Her yolun tek sahibi var (`rules/RULES.md` K-7). Burada olmayan bir yere yazman gerekiyorsa: BLOCKED, PC1'e sor.

| Sahip | Yazma izni olan yollar |
|---|---|
| **PC1** | `web/` · `data/catalog.json` · `CLAUDE.md` `AGENTS.md` `GEMINI.md` `README.md` `LICENSE` `.gitignore` `.gitattributes` · `.github/` · `rules/` · `tasks/` · `docs/*.md` (kök seviye) · `status/PC1.md` |
| **PC2** | `pipeline/` (script, csv, `subset/`) · `docs/gunw_structure.md` · `data/<site>/drivers.json` (Pazar) · `status/PC2.md` |
| **PC3** | `analysis/` (kod, test, `out/`) · `data/<site>/meta.json` · `data/<site>/disp/` · `data/<site>/points.json` · `data/<site>/summary.json` · `data/<site>/decomp.json` · `data/*_fullyear/` · `docs/karapinar_checkpoint_cm.png` · `status/PC3.md` |
| **PC4** | `data/uk/` · `data/karapinar/sinkholes.geojson` · `docs/story/sources.md` · `docs/story/calibration_note.md` · `status/PC4.md` |
| **PC5** | (14:40) `analysis/pc5/` · `data/*/uncertainty/` · `docs/story/literature_comparison.md` · `key_findings.md` · `game_sensitivity.md` · `risk_sensitivity.md` · `docs/qa/PC5.md` · `status/PC5.md` |
| **PC6** | (14:00: web/ PC1'e geri döndü) + Q23–Q25 yolları · `validation/` · `risk/` · `data/<site>/validation.json` · `data/<site>/assets.json` (Pazar) · `status/PC6.md` |
| **PCQ** (14:20, bağımsız kontrol ajanı, ASF erişimi yok; 15:10 PC8 işleri) | `docs/story/submission_form.md` · `video_subtitles.srt` · `narration_script.md` · `presentation_cues.md` · `rehearsal_checklist.md` · `docs/qa/PCQ.md` · `README.md` (Q13) · `docs/code_review.md` (Q15) · `status/PCQ.md` |
| **PC7** (14:35, Codex) | `pipeline/pc7/` · `data/fens/` · `data/water/` · `docs/qa/PC7.md` · `status/PC7.md` |
| **PC8** (15:20, Mehmet Antigravity #3, `aseltech-gemini3`) | `docs/qa/PC8.md` · `status/PC8.md` (test) |
| **Herkes** | `tasks/QUEUE.md` içinde **sadece sahiplendiği satır** · sahiplendiği QUEUE işinin "Klasör" sütunundaki yollar · `docs/qa/PCx.md` (kendi QA notları) |

Dikkat: `data/karapinar/` klasörüne hem PC3 hem PC4 yazar; `docs/story/`'ye PC4 ve PC5 yazar.
**Klasörü temizleyen script yasak** (K-7).

---

## 3. Roller

### PC1 · Yönetmen, web, yayın
Sahip olduğu alan: `web/`, katalog, kural ve görev dosyaları, yayın.

Bugünkü çıktı: kaydırmalı hikâye sitesi GitHub Pages'te canlı (17:30 TR), PC2-PC5 çıktıları bağlı,
sunum provası yapılmış.

En kritik iki iş: **(1)** Pages yayınının `data/` ve `game/` klasörlerini de içermesi (workflow hazır:
`.github/workflows/pages.yml`, ayarlardan "Source: GitHub Actions" seçilmeli), **(2)** saat 13:30 ve
15:30 kontrol noktalarında B planı kararını zamanında vermek.

### PC2 · Veri
Sahip olduğu alan: `pipeline/`.

Bugünkü çıktı: Central Valley için 6 provisional GUNW çiftinin kesilmiş alt kümeleri ve GUNW dosya yapısı belgesi.

En kritik iş: **ilk dosyanın yapısını (`docs/gunw_structure.md`) 13:30'dan önce push etmek.** PC3 buna bağlı.

### PC3 · Çökme analizi
Sahip olduğu alan: `analysis/`, `data/<site>/` içindeki çökme dosyaları.

Bugünkü çıktı: test edilmiş faz→cm dönüşümü, Karapınar kontrol haritası, Central Valley kümülatif
çökme haritaları + noktalar + `summary.json`.

En kritik iş: **işaret konvansiyonu ve referans noktası.** Yanlış işaret = "yer yükseliyor" diyen bir
harita. Her çift aynı referansa göre sıfırlanmadan toplanmaz.

### PC4 · Hikâye, obruklar, kaynaklar
Sahip olduğu alan: `data/uk/`, obruk noktaları, `docs/story/` içindeki kaynak dosyaları.

Bugünkü çıktı: UK "bulutun altı" görsel çifti, kaynaklı Karapınar obruk noktaları, doğrulanmış kaynak listesi.

En kritik iş: **uydurma koordinat ve link olmaması.** Her nokta ve her sayı açılıp doğrulanmış bir kaynaktan.

### PC5 · Oyun ve sunum metni
Sahip olduğu alan: `game/`, `docs/story/pitch.md`.

Bugünkü çıktı: çalışan Aquifer Manager oyunu (tek HTML), 3 dk sunum + 30 sn video senaryosu + 7 slayt metni.

En kritik iş: **oyundaki hızın "illustrative" etiketli olması**; PC3'ün `summary.json` değeri gelince ona bağlanması.

### PC6 · Doğrulama ve altyapı
Sahip olduğu alan: `validation/`, `risk/`.

Bugünkü çıktı: Central Valley GNSS istasyon listesi + en az 3 istasyonun dikey zaman serisi;
OSM kanal/yol/demiryolu hatları.

En kritik iş: **istasyonların NISAR dönemini kapsaması.** Kapsamayan istasyon doğrulamada işe yaramaz.

---

## 4. Bağımlılıklar

```
PC2 gunw_structure.md ──► PC3 insar.py
PC2 subset/*.npz ────────► PC3 cumulative.py ──► data/central_valley/* ──► PC1 site
                                              ├─► summary.json ──► PC5 oyun hızı, PC5 pitch sayıları
                                              └─► analysis/out/*_cum.npz ──► PC6 risk indeksi (Pazar)
PC4 data/uk, sinkholes ──► PC1 site
PC5 game/ ───────────────► PC1 site (iframe/link)
PC6 validation/, risk/ ──► (Pazar) validation.json, assets.json ──► PC1 site
```

Zincir: PC2 13:30'u kaçırırsa PC3 kayar, PC3 15:30'u kaçırırsa PC1 B planına geçer
(browse PNG'ler, `preview` rozetli). Diğer hatlar ana hattı beklemez.

**Yedek kritik yol:** PC1, Kerem'in bilgisayarında aynı ilk GUNW'yi (09-08→09-20) arka planda indirip açar
(Kerem Earthdata `.netrc`'yi kendisi kurar). PC2 takılırsa zincir PC1'den sürer.

## 4b. Faz planı (TR) — "veri yokken ne yapılır?"

İlke: **sözleşme önce.** Formatlar `rules/VERI_SOZLESMESI.md`'de sabit; herkes sahte/örnek veriyle hemen başlar,
gerçek veri gelince sadece dosya değişir. Kimse veri bekleyerek durmaz.

| Faz | Saat | PC1 | PC2 | PC3 | PC4 | PC5 | PC6 |
|---|---|---|---|---|---|---|---|
| 0 Hazırlık | 12:00-12:20 | Pages ayarı; Kerem Earthdata | Earthdata, `.netrc`, paketler | Earthdata, `.netrc`, paketler | Kurulum | Kurulum | Kurulum |
| 1 Bağımsız | 12:20-13:30 | Site iskeleti `placeholder` veriyle; Higgsfield açılış; yedek GUNW | İlk GUNW + `gunw_structure.md` | `insar.py` + sentetik testler; Karapınar indirmesi | UK bulut/radar çifti | Oyun | GNSS istasyonları |
| ✔ 13:30 | | **GUNW açıldı mı?** Hayır → B planı | | | | | |
| 2 Gerçek veri | 13:30-16:00 | UK çiftini bağla | 6 çift, her biri gelince push | İlk 2 npz gelince kümülatif hattı çalıştır, her yenisinde yeniden üret | Obruklar | Oyun cilası | OSM hatları |
| ✔ 15:30 | | **İlk gerçek cm haritası sitede mi?** | | | | | |
| 3 Birleştirme | 16:00-17:00 | Tüm veri + oyun | QUEUE | Karapınar | Kaynaklar | Sunum metni | QUEUE |
| 🔒 16:30 | | **Özellik dondurma:** yeni özellik yok, sadece düzeltme ve QA | | | | | |
| 4 Yayın + QA | 17:00-17:30 | Yayın | Siteyi telefonda test | Sitedeki sayıları kendi çıktısıyla karşılaştır | Kaynak linklerini test et | Oyunu sitede test et | İngilizce metin kontrolü |
| 5 Prova | 17:30+ | Sunum | Demo sürücüsü | Soru-cevap: veri/yöntem | Soru-cevap: kaynaklar | | |
QA notları: `docs/qa/PCx.md`.

## 5. İki tarafı olan işler

Ana sahip kararı verir ve dosyayı yazar; ikinci taraf kendi ucunu ona göre bağlar.

| İş | Ana sahip | İkinci taraf |
|---|---|---|
| Oyun ve sunumdaki ölçülmüş çökme sayısı | **PC3** (`summary.json`) | **PC5** (CONFIG ve pitch'teki yer tutucular) |
| GUNW alanlarının adı ve birimi | **PC2** (`gunw_structure.md`) | **PC3** (okuma kodu) |
| `catalog.json` yeni bölge/katman | **PC1** | PC3, PC4 status'ta "yeni katman hazır" yazar |
| GNSS doğrulaması | **PC6** (`validation.json`) | **PC3** (`points.json` + `_cum.npz`'den istasyon pikseli) |
| Altyapı risk indeksi | **PC6** (`assets.json`) | **PC3** (`_cum.npz`) |
| Toprak nemi / sebep grafiği | **PC2** (`drivers.json`) | **PC3** (çökme zaman serisi) |

## 6. Ortak kurallar

- Bir iş kod yazılınca değil, `rules/RULES.md` §7 "bitti" tanımı sağlanınca biter.
- Blokaj varsa saat beklenmez: hemen `BLOCKED:` + push.
- Saatlik kontrol: PC1 her saat başı `status/*.md` dosyalarını okur.
- Görevi biten **sormadan** `tasks/QUEUE.md`'den iş alır (`rules/RULES.md` §7.1). `tasks/BACKLOG.md` (bonus) için PC1'e sorar.

## 7. Takvim

| Saat (TR) | Kontrol |
|---|---|
| Cmt 12:00 | Başla |
| Cmt 13:30 | İlk GUNW açıldı mı? (Hayır → B planı: browse PNG) |
| Cmt 15:30 | İlk gerçek cm haritası var mı? |
| Cmt 17:30 | Demo canlı, sonra prova |
| Cmt akşam | Lincoln sunumu |
| Paz | Tam yıl, kalıcı/geri dönen, GNSS, risk, toprak nemi; video, proje sayfası |
| Paz 22:00 | **İç teslim hedefi** |
| Pzt 02:59 | Resmi kapanış (Paz 23:59 UK) |

Ayrıntı: `docs/TODAY_PLAN.md` ve `docs/MASTER_PLAN.md` §6, §8.

## Elenen alternatifler

- **Herkes her şeye yardım etsin:** elendi. 6 ajan aynı dosyalara dokunursa çakışma ve kayıp kaçınılmaz.
- **Analizi (PC3) iki ajana bölmek:** elendi. Referans noktası ve işaret tek elden seçilmeli; iki ajan iki farklı referans seçerse haritalar birbirini tutmaz.
- **Oyunu Pazar'a bırakmak:** elendi. Ana hatta hiç bağımlılığı olmayan, bugün paralel yürüyebilen tek yaratıcı iş; Lincoln jürisi için güçlü bir an.

## Geri alınabilir mi

Evet. PC1 rolleri saat başı kontrolde değiştirebilir; değişiklik önce bu dosyaya, sonra görev dosyasına yazılır.
