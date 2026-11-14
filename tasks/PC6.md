---
type: gorev
id: PC6
owner: Mehmet (M3hmeT1888)
tool: Antigravity (Gemini)
folder: aseltech-gemini2
status: acik
date: 2026-11-14
depends_on: [PC3 (Pazar: _cum.npz, points.json)]
feeds: [PC1]
---

# PC6 · Doğrulama (GNSS) ve altyapı verisi

> **Saat saat sıra ve iş bitince sıradaki iş: `docs/ZAMAN_CIZELGESI.md`.** Atanmış QUEUE işlerin orada.

## Kimlik
Mehmet'in bilgisayarı, **`aseltech-gemini2`** klasörü, ikinci Antigravity. Aynı bilgisayarda PC3 ve PC5 var; onların klasörlerine dokunma.
Bugün Pazar'ın özgün katkıları (#3 risk indeksi, #4 GNSS doğrulama) için **veriyi hazırlıyorsun**.

## Yazma alanın
`validation/` · `risk/` · `data/<site>/validation.json` ve `data/<site>/assets.json` (Pazar) · `status/PC6.md`

## Başlamadan
- [ ] `rules/RULES.md` (K-2, §8 disk) ve `rules/VERI_SOZLESMESI.md` okundu
- [ ] PC3 aynı bilgisayarda GUNW indirirken büyük indirme yapma; senin dosyaların küçük (csv, geojson)

---

## Görev 1 · GNSS istasyonları (12:30-15:00)

1. Central Valley bbox içindeki sürekli GNSS istasyonları. Açık kaynak: Nevada Geodetic Laboratory (geodesy.unr.edu) veya EarthScope; girişsiz olanı kullan.
2. `validation/gnss_stations.csv`: `station, lon, lat, source_url, series_url, first_date, last_date`
3. NISAR dönemini (**en az 2026-06-28 → 2026-09-20**, ideal 2025-11-24 → 2026-10-14) kapsayan, çökme bölgesindeki **en az 3** istasyonun dikey (Up) serisi
   → `validation/gnss/<station>.csv` (`date, up_cm`). Birimi kontrol et (NGL `.tenv3` metre verir).
4. `validation/README.md`: hangi istasyonlar, neden, kaynak, referans çerçevesi (örn. IGS14 / NA12).

**Bitti sayılır eğer:** 3 istasyonun csv'si var, tarihleri provisional dönemi kapsıyor, birim cm, kaynak linkleri açılıyor.

## Görev 2 · Altyapı hatları (15:00-17:30)

OpenStreetMap Overpass API (girişsiz), Central Valley bbox:
- kanallar (`waterway=canal`; özellikle California Aqueduct, Delta-Mendota, Friant-Kern)
- ana yollar (`highway=motorway|trunk`), demiryolları (`railway=rail`)

→ `risk/central_valley_infra.geojson` (sadece `name, type, osm_id`), **< 20 MB** (gerekirse sadeleştir).
`risk/README.md`: sorgu metni, tarih, lisans: "© OpenStreetMap contributors, ODbL".

**Bitti sayılır eğer:** geojson açılıyor, üç kanalın en az biri isimle mevcut, boyut < 20 MB.

## Görev 3 · (zaman kalırsa) Karapınar altyapısı → `risk/karapinar_infra.geojson`

## Pazar
- `data/central_valley/validation.json`: her istasyon için InSAR değeri = `analysis/out/central_valley_cum.npz` içinde istasyon pikselinin (3×3 medyan) zaman serisi; GNSS ile aynı referansa getir; `rmse_cm`, `corr`. LOS/dikey farkını `notes`'a yaz.
- `data/central_valley/assets.json`: hatlar boyunca çökme eğimi (mm/km) → risk sınıfı; en riskli 10 segment.

---

## En kritik iş
İstasyonların NISAR dönemini kapsaması. Kapsamayan istasyon doğrulama yapamaz.

## Yapma
- PC3 dosyalarına yazma (sadece oku). Sayı uydurma.

## Rapor
`status/PC6.md`: istasyon adları ve dönemleri, dosya boyutları, doğrulanamayanlar, `AI:` satırı.

---
# 14:10 YENİ PAKET (öncelik sırası; bitince sormadan sıradakine)
1. **OYUN v2 — sıfırdan "Valley Under Pressure"** (14:10–17:00, en kritik iş). Tam şartname: `docs/OYUN_SPEC.md`. Eski `game/index.html`'i sil ve yeniden yaz (sadece `game/`). AI görseli YOK; gerçek uydu altlığı + NISAR katmanı + OSM kanallar + gerçek yer adları. Fizik modeli `game/model.js` (elastik/kalıcı çökme, preconsolidation head). Parametreleri PC5'in `docs/story/game_model.md` dosyasından al; o gelene kadar CONFIG'de "illustrative" yer tutucu. Her 30–45 dk çalışan bir ara sürüm push et.
   Kabul: OYUN_SPEC "Kabul" bölümündeki her madde + `docs/game_v2.png`.
2. **Q28 Karapınar risk** (oyun ara sürümü push edildikten sonra paralel değil, oyun bitince).
3. **Q13 README** — kurulum, veri hattının adım adım çalıştırılması (pipeline → analysis → data → site), lisans, kaynaklar, ekip.
4. **Q15 kod gözden geçirme** → `docs/code_review.md`.
5. **Q17 göl/baraj** (zaman kalırsa).

---
# 14:45 YENİ PAKET — "Jüriyi etkileyecek görseller ve kanıt dosyaları" (öncelik sırası; bitince sormadan sıradakine)
Yazma alanı bu paket için: `game/` · `analysis/pc6/` · `docs/story/media/` · `docs/story/risk_dossier.md` · `docs/story/validation_report.md` · `docs/qa/PC6.md` · `status/PC6.md`. İNDİRME YAPMA (aynı bilgisayarda PC3 indiriyor). AI görseli YOK, hepsi gerçek veriden.

1. **Gerçek veriden animasyon** (14:45–15:30) → `analysis/pc6/make_animation.py`
   - `data/central_valley/disp/*.png` + Esri olmayan basit koyu arka plan (veya `pipeline/subset` koordinatlarından çizilmiş sınır) ile tarih etiketi, renk çubuğu (cm), "NASA-ISRO NISAR · PROVISIONAL" etiketi olan 1080p **MP4** (ffmpeg varsa) ve **GIF**.
   - Aynısı Karapınar için. Çıktı: `docs/story/media/cv_subsidence.mp4|gif`, `docs/story/media/kp_subsidence.mp4|gif`. 30 sn video ve slaytlarda kullanılacak.
2. **Doğrulama raporu** (15:30–16:15) → `docs/story/validation_report.md` + `docs/story/media/validation_scatter.png` + istasyon başına küçük grafikler (`docs/story/media/gnss_<station>.png`)
   - Saçılım: tüm istasyonlarda NISAR son değer vs GPS son değer, 1:1 çizgisi, r ve RMSE yazılı. Hareketli (|GPS|>2 cm) ve sabit istasyonlar farklı renk.
   - 4–5 cümle İngilizce yorum: neden hareketli istasyonlarda uyum iyi, sabitlerde zayıf.
3. **Altyapı risk dosyası** (16:15–17:00) → `docs/story/risk_dossier.md` + `docs/story/media/risk_<n>.png`
   - En riskli 10 segment (assets.json): her biri için ad, tür, uzunluk, gradyan (mm/km), maks çökme, segment boyunca çökme profili grafiği (mesafe–cm) PNG.
   - California Aqueduct ve büyük kanallar varsa ayrıca vurgula. "Ne anlama geliyor" 2 cümle (kaynaklı: kanal kapasite kaybı örnekleri `docs/story/game_model.md`'de).
4. **Oyun v2 son kontrol** (17:00–17:30): canlı sitede (https://keremsumer2010-tech.github.io/aseltech/ → Simulator) iframe içinde ve tam ekran çalışıyor mu, `data/central_valley/summary.json` okunuyor mu, telefonda kontroller kullanılabilir mi. Sorun varsa sadece `game/` içinde düzelt.
5. **Pazar hazırlığı** (17:30 sonrası): PC2'nin Q07 tam yıl verisi gelince risk indeksini ve doğrulamayı tam yıl (mixed) için yeniden çalıştıracak komutları `docs/qa/PC6.md`'ye hazırla; mevcut scriptler `--data-dir` gibi parametrelerle ayrı klasöre yazabilsin (sadece kendi scriptlerin: `risk/`, `validation/`).

---
# 15:00 ÖNCELİK DEĞİŞİKLİĞİ — ÖNCE OYUN CİLASI (sonra 14:45 paketine dön)
`docs/REVIEW_1500.md` "Oyun" bölümündeki 7 maddeyi `game/` içinde uygula (sırayla, her madde ayrı commit). Ardından canlı sitede iframe ve tam ekran testi, `docs/game_v3.png`. Bitince 14:45 paketinin 1. maddesine (animasyon) geç.
Kural: sade, olgusal İngilizce; emoji/ünlem/abartı yok; "Zero AI" vb. rozetleri kaldır.
