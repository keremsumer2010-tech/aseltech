# PC2 durum

- Görev: 1 (Hesap, liste, ilk dosya, gunw_structure.md) — **TAMAMLANDI**
- Görev: 2 (6 provisional Central Valley çifti) — **SIRADA**
- Çıktılar:
  - `pipeline/search.py`, `pipeline/download.py`, `pipeline/inspect_gunw.py`, `pipeline/subset.py`
  - `pipeline/central_valley_gunw.csv` (27 Path 34 Frame 20 ürünü; 7 adet provisional `P05023`, 20 adet beta-precal)
  - `docs/gunw_structure.md` (gerçek `2026-09-08 → 2026-09-20` P05023 HDF5 dosyasından `h5py` ile üretildi; λ = 0.24196324 m)
- İndirme hızı: 10.32 MB/s (`2236.0 MB`)
- Doğrulama: `search.py` 27 satır üretti; `inspect_gunw.py` gerçek HDF5'ten 369 satır ağaç + attribute raporu yazdı, gözle okundu.
- BLOCKED: yok
- AI: Antigravity (Gemini) → `pipeline/*.py` veri arama/indirme/inceleme/kesme scriptleri ve `docs/gunw_structure.md` üretimi
