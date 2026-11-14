# PC6 QA Notları

Tarih: `2026-11-14` (`13:08 TR`) · Denetleyen: PC6

## 1. `data/*/meta.json` ve `web/mock/*/meta.json` Denetimi (Q14 — Faz 1)

Mevcut durumda `data/` altında henüz üretilmiş `meta.json` dosyası yok (`data/.gitkeep` mevcut; PC2/PC3/PC4 çıktıları bekleniyor). Mevcut örnek ve üretici kod denetimleri:

| Dosya | `quality` / `quality_note` | `vmin` / `vmax` | `bbox` (`[w,s,e,n]`) | Not |
|---|---|---|---|---|
| `web/mock/central_valley/meta.json` | `"placeholder"` / geliştirme notu var | `-6.1` / `6.1` (simetrik, `RdBu` ile uyumlu) | `[-120.2, 35.6, -119.0, 36.6]` (`VERI_SOZLESMESI.md` §1 ile birebir) | `dates` (3 tarih) `disp/*.png` ve `points.json` ile uyumlu. Mock dosyada `notes` yok ve `reference_point` string (`"scene median"`). |
| `analysis/cumulative.py` (üretici) | `"provisional"` + tam kalibrasyon dipnotu | Simetrik `-vlim` / `+vlim` | `BBOX[site]` ile birebir | `RdBu(0.0)` = `#67001f` (kırmızı, negatif/çökme) ve `RdBu(1.0)` = `#053061` (mavi, pozitif/yükselme) → `web/style.css` `.ramp` gradyanı ve `web/index.html` açıklaması ile tam uyumlu. |

## 2. İngilizce Metin, Etiket ve Sözleşme Denetimi (`web/`)

- **Dil ve anlatım (`web/index.html`, `web/app.js`):** `<html lang="en">`, tüm 6 sahne akıcı, sade ve bilimsel açıdan tutarlı İngilizce ile yazılmış; yazım hatası görülmedi.
- **Kalibrasyon dipnotu (`web/index.html:152`):** Zorunlu tam metin mevcut: *"NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."*
- **AI medya etiketleri (`web/index.html`, `web/assets/`):** 7 AI görselinin tamamı (`hero.jpg`, `fens_ai.jpg`, `holme_ai.jpg`, `canal_ai.jpg`, `sinkhole_aerial_ai.jpg`, `obruk_ai.jpg`, `game_valley_ai.jpg`) ve `hero.mp4` yuvası `"AI-generated illustration"` / `"AI-generated background illustration"` etiketi taşıyor. NASA logosu yok.
- **Analiz testleri (`python -m pytest analysis -q`):** `13 passed in 2.48s`.

## 3. Gözlenen Küçük İyileştirme Notları (Sahibine Bilgi — Dosyasına Dokunulmadı)

1. **`web/app.js:83-87` (`select(p)` null koruması):** `p.disp_cm.at(-1)` değeri `null` gelirse `Math.abs(null)` → `0` ve `0 < 0` → `false` olacağı için `"this spot rose 0.0 cm"` yazar. (`analysis/cumulative.py` geçerli piksellerden seçtiği için normalde `null` gelmez, ancak savunmacı `v == null` kontrolü faydalı olur.)
2. **`web/index.html:154` (kırık olabilecek link kontrolü):** `docs/story/sources.md` linki şu an henüz oluşmamış (PC4 üretince aktifleşecek). 17:00 yayını öncesi tekrar kontrol edilmeli.
3. **`web/index.html:47` (yer tutucu metin):** Holme Fen kartında `<span class="pending">Exact figure and source being verified.</span>` mevcut (PC4 kaynaklı rakamı verince güncellenmeli).
4. **Tekrar kontrol:** PC2/PC3/PC4 gerçek `data/*/meta.json` dosyalarını push ettiğinde Q14 tekrar çalıştırılıp `- [x PC6]` işaretlenecek.

---

## 4. `data/` Faz-2 Denetimi (`13:41 TR` — Central Valley Gerçek Verisi Geldi)

Gerçek `data/central_valley/` çıktıları (`meta.json`, `summary.json`, `points.json`, 8 `disp/*.png`) ve PC6 veri üretimleri (`validation.json`, `assets.json`) denetlendi (web sitesiyle ilgili `data/catalog.json`, `game/index.html`, `docs/game_v1.png`, `web/app.js` değişiklikleri kullanıcı isteğiyle geri alındı):

| Dosya | `quality` / `quality_note` | `vmin` / `vmax` | `bbox` (`[w,s,e,n]`) | Sonuç |
|---|---|---|---|---|
| `data/central_valley/meta.json` | `"provisional"` + tam NASA-JPL/ISRO kalibrasyon dipnotu | `-6.0` / `6.0` (simetrik, `RdBu`) | `[-120.2, 35.6, -119.0, 36.6]` (`VERI_SOZLESMESI.md` §1 ile birebir) | Geçti (8 PNG tümü mevcut, 7 granule CRID `P05023`, skip `beta-precal` notlu) |
| `data/central_valley/summary.json` | `"provisional"` + dipnot | `max_subsidence_cm: -7.8`, `rate_cm_per_yr_estimate: -26.4` | ref `(-119.14562, 36.45323)` | Geçti (`method_note` yaz mevsimi doğrusal ekstrapolasyon uyarısını dürüstçe içeriyor, `NaN` yok) |
| `data/central_valley/points.json` | n/a (site noktaları) | 12 nokta, `NaN` yok | Central Valley içi | Geçti (`2026-06-28 → 2026-10-14`, 8 tarih) |
| `data/central_valley/validation.json` | `"provisional"` + tam dipnot | `NaN` yok | 10 GNSS istasyonu footprint içi | Geçti (`CAHA` RMSE 0.752 cm `r=0.896`, `HANF` RMSE 0.834 cm `r=0.896`, `QCAP` RMSE 0.767 cm `r=0.820`, `TLBN` RMSE 1.173 cm `r=0.793`) |
| `data/central_valley/assets.json` | `"provisional"` + OSM ODbL + dipnot | 645 segment ≥ 1 km değerlendirildi (`high=81, medium=131, low=433`) | top 10 GeoJSON `NaN` yok | Geçti (Tulare Irrig. Canal 57.01 mm/km, California Aqueduct 49.12 mm/km, Friant-Kern Canal 46.06 mm/km) |

### Güncel Notlar
- `data/karapinar/meta.json` (`Q02`) henüz eklendi (`quality: provisional`, `vmin/vmax: -5.0/5.0`, `bbox: [33.3, 37.6, 33.8, 37.9]`, 9 PNG); tam Q14/UK kontrolü `data/uk/` tamamlandığında tekrarlanacak.
- `web/app.js`, `docs/URUN_TANIMI.md`, `game/`, `docs/game_v1.png`, `data/catalog.json` kullanıcı isteği üzerine PC6 öncesi duruma (`c7bac46` / `4cba32a`) geri alındı.
