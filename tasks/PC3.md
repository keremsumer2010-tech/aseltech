# PC3 — Analiz (klasör: analysis/)

## Görev 1 — Konya kontrol noktası + dönüşüm modülü
1. `pip install asf_search h5py numpy matplotlib rasterio`; Earthdata hesabı aç.
2. konya bbox'ı için GUNW path 108 listesini `analysis/konya_gunw.csv` olarak çıkar; en kısa aralıklı TEK GUNW'yi `raw/` altına indir.
3. `analysis/insar.py` yaz:
   - `phase_to_cm(phase, wavelength_m)` → LOS cm (işaret konvansiyonunu ürün dokümanından doğrula, kaynağı yorum satırına yaz)
   - `mask_coherence(arr, coh, thr=0.3)`
   - `reference(arr, ref_rowcol)` → stabil bir noktaya göre sıfırla
   - `cumulative(stack)` → ardışık interferogramları topla
4. `analysis/test_insar.py`: sentetik veriyle (bilinen faz → bilinen cm) test; `python -m pytest` geçmeli.
5. İndirdiğin Konya GUNW'den tek santim haritası: `docs/konya_checkpoint_cm.png` (renk çubuğu, cm).

## Kabul
- Testler geçiyor, Konya PNG push edildi, status'ta kullandığın dataset yolları ve işaret konvansiyonunun kaynağı var.
