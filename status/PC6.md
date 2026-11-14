# PC6 durum

- Görev: Görev 1–3 (`[x]`), Q05 (`[x]`), Q06 (`[x]`), Q20 (`[x]`), Q14 (`[~PC6]` Central Valley denetlendi, Karapınar/UK bekleniyor)
- Geri Alınanlar (kullanıcı isteği — web sitesiyle ilgili değişiklikler):
  - `web/app.js` → PC1'in `c7bac46` durumuna geri döndürüldü (0 satır fark).
  - `docs/URUN_TANIMI.md` §4 tablosu → önceki durumuna (`4cba32a`) geri döndürüldü.
  - `game/index.html`, `docs/game_v1.png`, `data/catalog.json` → kaldırıldı (`game/.gitkeep` korundu).
  - `tasks/QUEUE.md` → `Q18` ve `Q19` tekrar `- [ ]` yapıldı.
- Kalan PC6 Çıktıları (veri, doğrulama, risk, sunum metni):
  - **Görev 1–3 & Q05 (`validation/compare.py`, `data/central_valley/validation.json`):** 10 NGL istasyonu; güncel `central_valley_cum.npz` ile çalıştırıldı (`CAHA` RMSE `0.752 cm` `r=0.8957`, `HANF` RMSE `0.834 cm` `r=0.8955`, `QCAP` RMSE `0.767 cm` `r=0.8198`, `TLBN` RMSE `1.173 cm` `r=0.7926`).
  - **Q06 (`risk/compute_risk.py`, `data/central_valley/assets.json`):** 645 segment ≥ 1 km değerlendirildi (`high=81, medium=131, low=433`); `Tulare Irrigation District Canal` (`57.01 mm/km`), `California Aqueduct` (`49.12 mm/km`), `Friant-Kern Canal` (`46.06 mm/km`).
  - **Q20 (`docs/story/pitch.md`):** 3 dk sunum + 30 sn video `.srt` + 7 slayt (`{PLACEHOLDER}` yer tutuculu).
  - **Q14 (`docs/qa/PC6.md`):** `data/central_valley/meta.json` ve `data/karapinar/meta.json` denetlendi (`data/uk/` bekleniyor).
- Doğrulama:
  - `python validation/compare.py --self-test` ve `python validation/compare.py`: geçti.
  - `python risk/compute_risk.py --self-test` ve `python risk/compute_risk.py`: geçti.
  - `python -m pytest analysis -q`: geri alma sonrası yeniden çalıştırıldı.
- BLOCKED: yok (`data/uk/` ve Holme Fen kaynağı PC4'te).
- AI: Antigravity (Gemini) -> GNSS/OSM scriptleri, `docs/story/pitch.md`, QA ve geri alma işlemi.
