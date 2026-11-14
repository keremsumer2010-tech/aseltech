---
type: gorev
id: PC1
owner: Kerem (keremsumer2010-tech)
tool: Claude
status: acik
date: 2026-11-14
depends_on: [PC2, PC3, PC4, PC5, PC6]
feeds: [herkes]
---

# PC1 · Yönetmen, web, yayın, sunum

## Kimlik
Kerem'in bilgisayarı, Claude. Görev yazar, denetler, birleştirir, siteyi yayınlar, Lincoln'de anlatır.

## Yazma alanın
`web/` · `data/catalog.json` · kök dosyalar (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `README.md`, `LICENSE`, `.gitignore`, `.gitattributes`) ·
`.github/` · `rules/` · `tasks/` · `docs/*.md` · `status/PC1.md`

## Başlamadan
- [x] `rules/RULES.md`, `docs/GOREV_DAGILIMI.md`, `rules/VERI_SOZLESMESI.md` okundu
- [x] GitHub → Settings → Pages → **Source: GitHub Actions** seçildi (workflow: `.github/workflows/pages.yml`)
- [x] `rules/VERI_SOZLESMESI.md` §5 yeni dosyalar (`summary.json`, `_cum.npz`) onaylandı

---

## Görev 1 · Site iskeleti ve yayın (12:00-13:30)

1. `web/` altında tek sayfa, kaydırmalı hikâye: açılış + 6 sahne (`docs/URUN_TANIMI.md` §2).
2. Sahte veriyle başla: `data/central_valley/` için sözleşmeye uyan 3 tarihlik sahte `meta.json`, `disp/*.png`, `points.json`. **Sahte dosyalar `quality: "placeholder"` taşır** ve PC3'ün gerçek dosyaları gelince silinmez, üzerine yazılır (aynı ad).
3. Veri yolları göreli (`data/...`). Vite kullanılıyorsa `base: './'`.
4. İlk push → Actions sekmesinde yayın yeşil → canlı linki telefonda aç.

**Bitti sayılır eğer:** canlı link telefonda açılıyor, sahte haritada kaydırıcı çalışıyor, konsol hatasız.

## Görev 2 · Kalite rozetleri ve sabit metinler (13:30-15:30)

- Her veri katmanında `quality` rozetinden üretilen etiket: PROVISIONAL / PREVIEW / PLACEHOLDER.
- Sabit dipnot: *"NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."*
- Tıkla-grafik cümlesi kuralla üretilir: `"This spot sank {abs(disp_cm[-1]):.1f} cm between {dates[0]} and {dates[-1]}."` + insan ölçeği eşlemesi (sabit tablo, kaynaklı).
- Higgsfield medya: açılış videosu, obruk kesiti, Holme Fen illüstrasyonu. **Hepsinde "AI-generated illustration".**

**Bitti sayılır eğer:** her katmanda rozet görünüyor; AI medyasının hepsinde etiket var.

## Görev 3 · Gerçek veriyi bağla (15:30-17:00)

- PC3: `data/central_valley/*`, `data/karapinar/*` → `data/catalog.json`'a ekle.
- PC4: `data/uk/*`, `data/karapinar/sinkholes.geojson` → Sahne 1 ve 3.
- PC5: `game/index.html` → Sahne 5 (iframe veya link).

**Bitti sayılır eğer:** sitede hiç `placeholder` rozeti kalmadı (veya kalanlar bilinçli ve listelendi).

## Görev 4 · Demo ve prova (17:00-17:30+)

- Canlı link telefonda ve dizüstünde test. `docs/URUN_TANIMI.md` §4 tablosunu güncelle.
- 3 dk konuşma akışı: `docs/MASTER_PLAN.md` §7. Muhtemel sorular: kalibrasyon, LOS/dikey, atmosfer.

## Saatlik iş (her saat başı)
`git pull` → `status/*.md` oku → BLOCKED olan varsa çöz veya görevi değiştir (önce `docs/GOREV_DAGILIMI.md`, sonra `tasks/PCx.md`).

## Pazar
- [ ] Tam yıl katmanı (`mixed` uyarılı), kalıcı/geri dönen, GNSS, risk indeksi, toprak nemi bağlama
- [ ] Space Apps proje sayfası (İngilizce), 30 sn video veya ≤7 slayt, teslim kontrol listesi (`docs/MASTER_PLAN.md` §9)
- [ ] AI kullanım açıklaması: her `status/PCx.md` içindeki `AI:` satırları toplanır
- [ ] **Paz 22:00 TR'de "Submit for Judging"**

---

## En kritik iş
Yayının `data/` ve `game/`'i içermesi. Sadece `web/` yayınlanırsa site boş harita gösterir.

## B planı
- 13:30'da GUNW açılmadıysa: Sahne 2-3 browse PNG ile (`preview` rozetli). Hikâye ve oyun aynen kalır.
- Actions yayını çalışmazsa: `web/`, `data/`, `game/`'i tek klasöre koyup Netlify Drop'a sürükle (geçici link).

## Yapma
- Başka PC'nin klasörüne yazma; düzeltme gerekiyorsa görev dosyasını güncelle.
- Sahte veriyi gerçek gibi gösterme.

## Rapor
`status/PC1.md`: canlı link, hangi sahneler gerçek veriyle bağlı, açık BLOCKED'lar, AI satırları.
