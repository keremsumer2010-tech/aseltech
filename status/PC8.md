# PC8 durum

- Görev: Q09 UK kil (Londra) kümülatif harita ve analiz (`tasks/PC8.md` Madde 1–4)
- Durum: Madde 1–3 **TAMAMLANDI** (`data/uk_clay/` üretildi ve doğrulandı; Madde 4 sürekli QA ve izleme adımında)
- Çıktılar:
  - `analysis/pc8/uk_clay_cumulative.py` (PC3 `analysis/cumulative.py` ve `analysis/insar.py` modüllerini değiştirmeden çalıştıran sarmalayıcı + Cramér–Rao ve atmosfer gürültü analizi)
  - `analysis/pc8/uk_clay_cum.npz` (1.03 MB, `(630, 679)` `EPSG:32630`) ve `analysis/pc8/uk_clay_pair_stats.json`
  - `data/uk_clay/meta.json` (`quality: "provisional"`, bbox `[-0.5, 51.3, 0.2, 51.7]`, 10 tarih `2026-06-21` → `2026-10-19`, `vmin=-4.0`, `vmax=4.0` cm)
  - `data/uk_clay/disp/2026-06-21.png` .. `2026-10-19.png` (10 adet şeffaf arka planlı RdBu PNG haritası)
  - `data/uk_clay/points.json` (12 nokta: 5 `most_subsiding`, 5 `median`, 2 `near_reference` Croydon)
  - `data/uk_clay/summary.json` (`detection_status: "below detection limit for one season"`, 3 cümle İngilizce `method_note`)
  - `docs/qa/PC8.md` (Q09 UK kil gürültü bütçesi, Cramér–Rao `0.31 cm` vs. atmosferik zincir gürültüsü `1.50 cm` tablosu ve `docs/story/media/` QA raporu)
- Doğrulama:
  - **Madde 1 (`uk_clay` kümülatif harita):** 9 ardışık provisional (`P05023`) çift (`2026-06-21` → `2026-10-19`, 120 gün, Track 101 A Frame 28, $\lambda=0.243932\text{ m}$) işlendi. Tam zincir geçerli piksel oranı **73.61%**, Croydon referans penceresi (`[-0.09804, 51.37603]`, ortalama koherens `0.923`). `2026-10-19.png` görsel olarak açılıp kontrol edildi (Thames Nehri ve rezervuarlar şeffaf maskeli), tüm JSON dosyaları parse edildi.
  - **Madde 2 (Dürüst bilimsel sonuç — `below detection limit for one season`):** Sahne geneli 1 km blok medyanı `-0.68 cm` LOS (`p2–p98`: `-2.95` ile `-0.07 cm`; güney kenar yerel uç değeri `-5.3 cm` LOS / `-7.1 cm` dikey *estimate*, 3 referans aralığı `[-5.5, -5.3] cm`). Teorik Cramér–Rao ($L=208$) piksel belirsizliği çift başına `0.10 cm`, 9 çiftlik zincirde `0.31 cm` (PC5'in `~0.3 cm` sınırı ile uyumlu) olsa da, düzlem çıkarımı sonrası çift başına `0.50 cm` RMS troposferik saçılım (tek çift `p2–p98` yayılımı `2.87 cm`'ye kadar) 9 çiftte **`1.50 cm` zincir gürültüsüne** (`1.22 cm` sahne std) yayılmaktadır. Beklenen `0.5–2.0 cm` mevsimsel Londra kili büzülme-şişme sinyali tek sezonda atmosferik gürültü altında kaldığından `summary.json` ve `docs/qa/PC8.md` içine açıkça **"below detection limit for one season"** yazıldı.
  - **Madde 3 (Fens kontrolü):** `pipeline/subset/` altında yalnızca `central_valley`, `karapinar` ve `uk_clay` mevcut; `fens` GUNW alt kümesi bulunmadığı için talimat uyarınca atlandı.
- AI: Antigravity (Gemini) → `analysis/pc8/uk_clay_cumulative.py` ve `docs/qa/PC8.md`
- BLOCKED: git pull --rebase origin main → CONFLICT (add/add): Merge conflict in data/uk_clay/disp/2026-07-03.png .. 2026-10-19.png, data/uk_clay/meta.json, data/uk_clay/points.json, data/uk_clay/summary.json / error: could not apply fdebcc6... [PC8] Q09 UK kil kumulatif harita ve below-detection analizi tamamlandi (`git rebase --abort` çalıştırıldı, hiçbir dosya silinmedi).
