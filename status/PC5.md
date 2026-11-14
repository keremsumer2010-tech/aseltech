# PC5 durum

- Görev: 14:10 Paketi — **Oyun Modeli (`docs/story/game_model.md` · `game_model hazır` → PC6)**, **Görev 1 (`decompose.py`)**, **Görev 2 + Q27 (`error_budget.py` + `docs/story/uncertainty.md`)**, **Görev 3 + Q26 (`point_quality.py` + `docs/qa/PC5.md`) TAMAMLANDI**
- Durum: tamamlandı (yerel commitler hazır; push bekleniyor)
- Güncelleme: 2026-11-14 14:26 TR
- Çıktılar:
  - **`docs/story/game_model.md` (game_model hazır → PC6):** San Joaquin Valley ($S_y=0.15$, $S_{ke}=0.00222$, $S_{kv}=0.07875$, $b_0=150\text{ m}$), CDEC/DWR D-1641 su yılı olasılıkları (`Wet 0.30, Normal 0.40, Dry 0.15, Critical 0.15`), Friant–Kern (>%60) / California Aqueduct (~%20) kanal kayıpları ve `summary.json` (`-10.1 cm` dikey / `-7.8 cm` LOS, 108g) için $k_{\text{cal}}=1.067$ kalibrasyonu + `GAME_MODEL_CONFIG`.
  - **`analysis/decomp/decompose.py` + `test_decompose.py` (Görev 1):** Vektörleştirilmiş `d(t) = a + v·t + A·sin(2πt) + B·cos(2πt)`, delta-yöntemi SE, `<8` nokta / `<9` ay koruması.
  - **`analysis/decomp/error_budget.py` + `test_error_budget.py` + `docs/story/uncertainty.md` (Görev 2 + Q27):**
    - 7 `provisional` çift (`beta-precal` hariç): ham yerel yüksek koherens $\sigma_{\text{çift}} = 0.504\text{ cm}$ ($\sigma_{\text{toplam}} = 1.33\text{ cm}$), deramp sonrası yerel $\sigma_{\text{çift}} = 0.657\text{ cm}$ ($\sigma_{\text{toplam}} = 1.74\text{ cm}$ LOS / $2.24\text{ cm}$ dikey *estimate*), sahne geneli kararlı bölge $\sigma_{\text{çift}} = 1.085\text{ cm}$ ($\sigma_{\text{toplam}} = 2.87\text{ cm}$ LOS). İyonosfer `p1–p99` aralığı **2.93 – 17.26 cm LOS** (medyan **7.40 cm**).
    - **Q27 GNSS Özeti:** Tüm 10 istasyonda medyan RMSE **1.00 cm**; havza içi aktif 5 istasyonda (`CAHA`, `HANF`, `P056`, `QCAP`, `TLBN`) ortalama RMSE **0.86 cm**, $r = 0.81$, ortalama eğilim farkı **-0.51 cm/yıl**.
  - **`analysis/decomp/point_quality.py` + `test_point_quality.py` + `docs/qa/PC5.md` (Görev 3 + Q26):**
    - `data/central_valley/summary.json` (`-7.8015 → -7.8 cm` LOS, `-10.056 → -10.1 cm` dikey *estimate*, `-26.384 → -26.4 cm/yr` *estimate*, `39.125° → 39.1°`) ve `data/karapinar/summary.json` (`-5.9270 → -5.9 cm` LOS, `42.0°`) bağımsız olarak sıfırdan doğrulandı.
    - **Q26 Nokta Kalitesi:** 12 CV noktasının hiçbiri $\lambda/4 = 6.05\text{ cm}$ faz açma sınırını aşmadı; `p08` (Richgrove, `+4.44 cm` geçici sıçrama) ve `p03` (Huron, `-3.25 cm` adım) `ELEVATED_JUMP` (> $\lambda/8 = 3.02\text{ cm}$) olarak işaretlendi.
- Doğrulama:
  - `python -m pytest analysis/decomp -q` → **15 passed in 5.49s**
  - `python -m analysis.decomp.error_budget` ve `python -m analysis.decomp.point_quality` gerçek veride doğrulandı.
- AI: Antigravity (Gemini) → `analysis/decomp/` modülleri/testleri, `docs/story/game_model.md`, `docs/story/uncertainty.md`, `docs/qa/PC5.md`
- BLOCKED: git pull --rebase origin main / git push origin main → (1) fatal: Cannot prompt because user interactivity has been disabled / could not read Username for 'https://github.com': terminal prompts disabled; (2) CONFLICT (add/add): Merge conflict in analysis/decomp/decompose.py, analysis/decomp/test_decompose.py ve docs/story/game_model.md (push engeli sırasında PC3 tarafından 69bc5db ve 66b315f ile push edildi; error_budget.py, point_quality.py, docs/story/uncertainty.md ve docs/qa/PC5.md çakışmasız olarak yerel 1984b3a ve cd0d136 commitlerinde hazır).
