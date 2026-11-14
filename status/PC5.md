# PC5 Durum Raporu

- **Durum:** çalışıyor — Görev 1 tamamlandı, Görev 2'ye geçiliyor
- **Kimlik:** M3hmeT1888 · Antigravity (Gemini) · PC5
- **Güncelleme:** 2026-11-14 14:52 TR

## Görev 1 — Piksel Bazında Belirsizlik Haritası (`analysis/pc5/uncertainty_map.py`)
- **Yöntem:** Cramér–Rao / Rodriguez & Martin (1992) faz standart sapması $\sigma_\phi = \frac{\sqrt{1-\gamma^2}}{\gamma\sqrt{2L}}$, $\sigma_d = \frac{\lambda}{4\pi}\sigma_\phi \cdot 100$ ve $N$ ardışık `provisional` çift üzerinden kare-toplam ($\sigma_{\text{toplam}} = \sqrt{\sum \sigma_{d,i}^2}$).
- **Bakış Sayısı ($L$) Kaynağı:** `docs/gunw_structure.md` §2 içinde gerçek HDF5 üstverisinden (`numberOfAzimuthLooks=16`, `numberOfRangeLooks=13` → nominal $L = 208$). RSLC aşırı örnekleme / `2000_SH` (Karapınar) nedeniyle etkin bakış $L_{\text{eff}} = 100$'e düşerse ölçek çarpanı $1.442\times$ olarak `meta.json`'da ayrıca raporlandı (`--looks` parametresi açık).
- **Varsayımlar:** (1) Çiftler arası istatistiksel bağımsızlık, (2) yalnızca kısa ölçekli koherens/beneklenme faz gürültüsünü kapsar; **atmosferik su buharı türbülansı, rampa kalıntısı ve faz açma hatalarını KAPSAMAZ**.
- **Sayılar:**
  - **Central Valley** (`data/central_valley/uncertainty/`, 7 çift, PNG `1200x1000` RGBA, `vmin=0.0`, `vmax=1.0 cm`, geçerli `%64.69`): medyan **`0.294 cm`**, p90 **`0.471 cm`**, min–max `0.027–0.763 cm` ($L=100$ duyarlılığı: medyan `0.424 cm`, p90 `0.679 cm`).
  - **Karapınar** (`data/karapinar/uncertainty/`, 8 çift, PNG `500x300` RGBA, `vmin=0.0`, `vmax=1.0 cm`, geçerli `%15.44`): medyan **`0.326 cm`**, p90 **`0.548 cm`**, min–max `0.068–0.765 cm` ($L=100$ duyarlılığı: medyan `0.470 cm`, p90 `0.790 cm`).
- **Doğrulama:** `pytest analysis/pc5/test_uncertainty_map.py -q` → **5 passed**, her iki `sigma_cm.png` dosyası açılıp saydamlık ve bbox hizalaması kontrol edildi.
- **AI:** Gemini → `analysis/pc5/uncertainty_map.py`, `test_uncertainty_map.py`
