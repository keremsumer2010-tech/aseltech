---
type: gorev
id: PC5
owner: Mehmet (M3hmeT1888)
tool: Antigravity (Gemini)
folder: aseltech-gemini
status: acik
date: 2026-11-14
depends_on: [PC3 (summary.json, sonradan)]
feeds: [PC1]
---

# PC5 · Aquifer Manager oyunu ve sunum metni

## Kimlik
Mehmet'in bilgisayarı, **`aseltech-gemini`** klasörü, Antigravity. Aynı bilgisayarda PC3 (`aseltech-claude`) ve PC6 (`aseltech-gemini2`) var; onların klasörlerine dokunma.

## Yazma alanın
`game/` · `docs/story/pitch.md` · `docs/game_v1.png` · `status/PC5.md`

## Başlamadan
- [ ] `rules/RULES.md` (K-2, K-11, K-14) okundu
- [ ] Oyun bağımsız: ana hattı beklemeden başla.

---

## Görev 1 · Aquifer Manager (12:00-16:00)

`game/index.html`: saf HTML/CSS/JS, tek dosya olabilir; CDN kullanırsan **sabit sürüm**. Metinler İngilizce.

- Oyuncu her yıl pompalama seviyesini seçer (%0-150); yıl tipi rastgele: wet / normal / drought.
- Model ve katsayılar tek `CONFIG` nesnesinde:
  ```js
  const CONFIG = {
    base_rate_cm_per_yr: 10,      // PLACEHOLDER: will be replaced by our NISAR measurement
    rate_source: "illustrative",  // "nisar" olunca data/central_valley/summary.json'dan
    year_factor: { wet: 0.5, normal: 1.0, drought: 1.6 },  // illustrative
  };
  subsidence_cm = base_rate_cm_per_yr * (pumping / 100) * year_factor[yearType];
  ```
- Görsel: yan kesit (yüzey, tarlalar, kanal, yol; altında akifer). Çökme arttıkça yüzey iner, kanal eğilir, çatlak ikonları çıkar.
- 10 yıl sonunda sonuç ekranı: toplam çökme, basit çiftçi geliri, "what this means" cümlesi, tekrar oyna.
- Alt bilgi: *"Rates are illustrative until replaced with NISAR-derived values. NISAR data are provisional; calibration is done by the NISAR project (NASA-JPL/ISRO), not by our team."*
- Mobil uyumlu, konsol temiz.

**Bitti sayılır eğer:** telefonda ve masaüstünde 10 yıl oynanıyor, konsolda hata yok, `docs/game_v1.png` ekran görüntüsü push edildi.

## Görev 1b · Ölçülmüş hıza bağla (PC3 `summary.json` gelince)
`data/central_valley/summary.json` → `rate_cm_per_yr_estimate` → `CONFIG.base_rate_cm_per_yr`, `rate_source: "nisar"`.
Alt bilgi metnini "Rate based on NISAR provisional data, {period}" olarak güncelle. Sayıyı elle yazma, dosyadan oku.

## Görev 2 · Sunum metni (16:00-17:30)

`docs/story/pitch.md`, `docs/TODAY_PLAN.md` sahnelerine göre:
1. **Lincoln 3 dk konuşma** (`docs/MASTER_PLAN.md` §7 akışı): kanca → sorun → canlı demo adımları → oyun 15 sn → how we know.
2. **30 sn video senaryosu:** sahne sahne, saniye aralığı, İngilizce altyazı.
3. **≤ 7 slayt:** başlık ve madde metni.

Sayı yazma; yer tutucu bırak: `{CV_MAX_CM}`, `{CV_PERIOD}`, `{N_SINKHOLES}` (PC1 doldurur, kaynak `summary.json` / `sinkholes.geojson`).

**Bitti sayılır eğer:** üç bölüm var, video senaryosu 30 sn'yi aşmıyor, slayt ≤ 7, metinde tek bir uydurma sayı yok.

---

## En kritik iş
Oyundaki hızın etiketli olması. Etiketsiz bir 10 cm/yıl, jüriye "ölçtük" gibi görünür.

## Yapma
- PC3'ün dosyalarına yazma (sadece oku).
- AI görselini veri gibi gösterme.

## Rapor
`status/PC5.md`: ne bitti, nasıl test edildi (hangi tarayıcı/cihaz), ekran görüntüsü yolu, `AI:` satırı.
