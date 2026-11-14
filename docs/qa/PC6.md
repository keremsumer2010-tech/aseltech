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
