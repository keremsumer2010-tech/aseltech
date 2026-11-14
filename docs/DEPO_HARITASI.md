# DEPO HARİTASI

## Klasörler
| Klasör | İçerik |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` | Ajan girişleri (okuma sırası) |
| `rules/` | Bağlayıcı kurallar ve veri sözleşmesi |
| `docs/` | Planlar, ürün tanımı, sözlük, kaynaklar (`docs/story/`), QA raporu |
| `tasks/` | Her PC'nin görev dosyası + `QUEUE.md` ortak kuyruk |
| `status/` | Her PC'nin durum raporu |
| `pipeline/` | İndirme/kesme kodu ve küçük alt kümeler (`pipeline/subset/`) |
| `analysis/` | cm dönüşümü, kümülatif, ayrıştırma kodu + testler |
| `validation/` | GNSS istasyonları ve seriler |
| `risk/` | OSM altyapı hatları |
| `data/` | Siteye giden son çıktılar (veri sözleşmesi) |
| `web/` | Web sitesi (PC1) |
| `game/` | Aquifer Manager (PC5) |

## Git dışı (asla commit edilmez)
`raw/` (ham .h5), `*.h5`, `*.nc`, `cache/`, `.netrc`, `.env`, `.venv/`, `node_modules/`, `__pycache__/`. Bkz. `.gitignore`.

## Yayın
- GitHub Pages, `main` dalı, kök klasörden yayın. Kökteki `index.html` → `web/` sayfasına yönlendirir.
- Site adresi: `https://keremsumer2010-tech.github.io/aseltech/`
- Site `../data/` yolundan veri okur; bu yüzden `data/` dosyaları push edilince site otomatik güncellenir (1–2 dk).
- Yayını sadece PC1 açar/değiştirir.
