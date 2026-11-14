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
