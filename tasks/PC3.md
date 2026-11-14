# PC3 — Çökme analizi

## Kimlik
M3hmeT1888 · Claude Code · klasör `aseltech-claude`

## Yazma alanı
`analysis/`, `data/central_valley/` (meta, disp, points), `data/karapinar/` (sinkholes.geojson HARİÇ), `docs/*_checkpoint_*.png`, `status/PC3.md`

## En kritik iş
16:30 TR'ye kadar `data/central_valley/` (meta.json + disp/*.png + points.json) push edilmiş olmalı. Demonun kalbi bu.

## Görevler
1. **(12:00–14:00) Modül + Karapınar kontrol haritası**
   - İnsan Earthdata/`.netrc`'yi kendisi kurar. `pip install asf_search h5py numpy matplotlib pytest`
   - `analysis/insar.py`: `phase_to_cm(unw, wavelength_m)`, `mask_coherence(arr, coh, thr=0.3)`, `reference(arr, (row,col))`, `los_to_vertical(cm, incidence_deg)`.
     İşaret yönünü ATBD/ürün dokümanından doğrula; kaynağı yoruma yaz. `analysis/test_insar.py` → pytest geçmeli.
   - Karapınar GUNW path 7, 2026-09-18→09-30 → `docs/karapinar_checkpoint_cm.png` (renk çubuğu cm).
2. **(14:00–16:30) Central Valley kümülatif** — `analysis/cumulative.py central_valley`:
   npz'leri tarih sırasıyla topla, coherence maskesi, sabit referans bölgesi (az hareketli + yüksek koherens), LOS→dikey →
   `data/central_valley/meta.json` (`quality:"provisional"`, `quality_note`, `method`, `reference_point`), `disp/<date>.png` (sabit vmin/vmax), `points.json` (10–15 nokta: çökme merkezleri + 2–3 sabit kontrol noktası).
3. **(16:30 sonrası)** Karapınar için aynısı → `data/karapinar/`; sonra QUEUE Q02/Q08.

## Bitti sayılır eğer
pytest geçti · PNG'ler bbox'a oturuyor ve şeffaf · değerler makul (Central Valley birkaç cm–onlarca cm çökme beklenir; literatürle kıyasla, aşırıysa işaret/referansı kontrol et) · meta.json sözleşmeye uygun · status'ta maks çökme, referans, çift sayısı.

## B planı
- PC2'den npz gelmezse: kendin 1–2 çift indirip tek interferogram haritası üret (tarih aralığını açıkça yaz).
- Zincirde boşluk varsa: sadece ardışık kısmı kullan, `notes`'a yaz.

## Yapma listesi
"Kalibre ettik" deme · beta veriyi provisional ile toplama · `pipeline/` veya `web/`'e yazma · sayıyı yuvarlayıp abartma.

## Rapor (`status/PC3.md`)
Maks çökme (cm, nerede), referans noktası, kullanılan çiftler, test sonucu, sınırlamalar.
