---
type: gorev
id: PC4
owner: İbrahim (acikgozibrahim032-hub)
tool: Antigravity (Gemini)
status: acik
date: 2026-11-14
depends_on: []
feeds: [PC1, PC5]
---

# PC4 · Hikâye: UK görselleri, obruklar, kaynaklar

> **Saat saat sıra ve iş bitince sıradaki iş: `docs/ZAMAN_CIZELGESI.md`.** Atanmış QUEUE işlerin orada.

## Kimlik
İbrahim'in bilgisayarı, Antigravity. Ana hattan bağımsız; bugün kimseyi beklemiyorsun.

## Yazma alanın
`data/uk/` · `data/karapinar/sinkholes.geojson` · `docs/story/sources.md` · `docs/story/calibration_note.md` · `status/PC4.md`

**Dikkat:** `data/karapinar/` içindeki diğer dosyalar PC3'ün. Sadece `sinkholes.geojson`'a yaz.

## Başlamadan
- [ ] `rules/RULES.md` (K-2 uydurma yok) ve `rules/VERI_SOZLESMESI.md` §3-§4 okundu
- [ ] Kural: **uydurma koordinat, sayı veya link yasak.** Her linki aç, içeriğin iddiayı desteklediğini gör.

---

## Görev 1 · UK "bulutun altı" görsel çifti (12:00-13:30)

1. Fens bbox için NISAR GCOV tarihlerini ASF'den listele (`platform=NISAR`, `processingLevel=GCOV`).
2. Bu tarihlerden **optik görüntüde bulutlu** bir gün seç: NASA Worldview Snapshots / GIBS (girişsiz),
   o günün MODIS veya VIIRS true color görüntüsü. Birkaç gün dene, en bulutlusunu seç.
3. Aynı günün NISAR GCOV **browse PNG**'sini indir (girişsiz).
4. Çıktılar (aynı bbox'a kırp/hizala):
   - `data/uk/optical_<YYYY-MM-DD>.jpg`, `data/uk/radar_<YYYY-MM-DD>.png`
   - `data/uk/meta.json` (sözleşme §4.2, `quality: "preview"`)

**Bitti sayılır eğer:** iki görüntü aynı alanı gösteriyor (kıyı çizgisi/The Wash hizalı), optikte bulut açıkça görünüyor, meta.json'daki iki URL açılıyor.

## Görev 2 · Karapınar obruk noktaları (13:30-15:30)

`data/karapinar/sinkholes.geojson`: sadece bir **kaynakta koordinatı verilen** veya adı ve yeri net tanımlanmış obruklar.
- properties: `name`, `year_formed` (varsa), `source_title`, `source_url`, `coord_source` (`paper table` / `official` / `wikipedia` / ...)
- Öncelik: hakemli makale, AFAD, MTA, üniversite.
- **Koordinatı tahmin etme.** En az 5, ideal 10+. Bulamadığın sayıyı status'a yaz, uydurma.

**Bitti sayılır eğer:** geojson geçerli (geojson.io'da açılıyor), her noktanın `source_url`'si açılıyor ve o obruğu anlatıyor.

## Görev 3 · Kaynak listesi ve kalibrasyon notu (15:30-17:00)

`docs/story/sources.md`: her kaynak için başlık, link, 1 cümle bulgu, varsa sayı (birimiyle).
- Holme Fen direği: ne zaman dikildi, zemin ne kadar alçaldı
- Central Valley çökmesi (NASA/JPL, USGS) · Sacramento Delta setleri
- Karapınar/Konya çökme ve obruklar
- UK kil şişme-büzülme (BGS)
- NISAR görevi (nasa.gov / jpl.nasa.gov) · NISAR veri sürümleri ve kalibrasyon durumu (ASF NISAR Data User Guide)

`docs/story/calibration_note.md`: ASF/JPL ürün notlarına göre 2026-06-17 öncesi ürünlerin durumu (beta / pre-calibration), kısa ve kaynaklı.

**Bitti sayılır eğer:** her satırın linki açıldı ve sayı sayfada geçiyor.

---

## En kritik iş
Doğrulanmış kaynak. Jüri tek bir uydurma sayı yakalarsa tüm projenin Validity puanı düşer.

## B planı
- Bulutlu gün + GCOV eşleşmesi bulunamazsa: en yakın iki gün (±1 gün), `note` alanına farkı yaz.
- 5 kaynaklı obruk bulunamazsa: bulunanları koy, eksik sayıyı status'a yaz. Uydurma yok.

## Yapma
- `data/karapinar/` klasörünü silme/temizleme. Başka dosyaya yazma.

## Rapor
`status/PC4.md`: ne bitti, hangi kaynaklar, doğrulanamayanlar, `AI:` satırı.

---
# 14:10 YENİ PAKET (öncelik sırası; harika iş çıkardın — devam)
1. **Q30** sayı eşleme (pitch.md, project_page.md ↔ data/*/summary.json).
2. **Q31** Holme Fen tek cümle + kaynak → `docs/story/holme_fen.md`.
3. **Jüri soru-cevap kartı** → `docs/story/judge_faq.md`: en olası 15 soru (kalibrasyon? LOS/dikey? atmosfer/iyonosfer? 108 günden yıllık hız? neden Central Valley? Karapınar'da obrukları NISAR öngörebilir mi? GNSS ile uyum? veri açık mı? AI kullanımı? …) — her biri 2–3 cümle İngilizce, kaynaklı, repodaki gerçek sayılarla.
4. **Slaytlar (≤7)** → `docs/story/slides.html` (tek dosya, gerçek ekran görüntüleri ve grafikler; AI görseli yok; tıklayınca ilerleyen). İçerik: pitch.md'den.
5. **30 sn video çekim listesi** → `docs/story/video_shotlist.md`: siteden hangi ekran kaydı, kaç saniye, altyazı metni (İngilizce), sıra. (Kaydı Kerem/PC1 yapacak.)
6. **Son İngilizce okuma**: `web/index.html` metinleri için düzeltme önerilerini `docs/qa/PC4.md`'ye yaz (web/ dosyasına dokunma, PC1 uygular).
