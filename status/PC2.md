# PC2 durum

- Görev: 1 (Hesap, liste, ilk dosya, gunw_structure.md) — **TAMAMLANDI**
- Görev: 2 (6 provisional Central Valley çifti) — **DEVAM EDİYOR (1/6 tamam)**
- Çıktılar:
  - `pipeline/search.py`, `pipeline/download.py`, `pipeline/inspect_gunw.py`, `pipeline/subset.py`
  - `pipeline/central_valley_gunw.csv` (27 Path 34 Frame 20 ürünü; 7 provisional `P05023`, 20 beta-precal)
  - `docs/gunw_structure.md` (gerçek `2026-09-08 → 2026-09-20` P05023 HDF5'inden üretildi; λ = 0.24196324 m)
  - `pipeline/subset/central_valley/2026-09-08_2026-09-20.npz` (15.59 MB, shape=(1473, 1438), NaN=4.95%, ham `.h5` silindi)
- İndirme hızı: 10.32 MB/s (`2026-09-08 → 2026-09-20`, 2236.0 MB)
- Doğrulama:
  - `2026-09-08_2026-09-20.npz`: `np.load` ile açıldı; `unw` [-3.776, 6.936] rad, `coh` ort=0.626, `incidence` [37.73, 45.31] deg, `epsg=32611`.
- BLOCKED: yok
- AI: Antigravity (Gemini) → `pipeline/*.py` veri arama/indirme/inceleme/kesme scriptleri ve `docs/gunw_structure.md` üretimi
