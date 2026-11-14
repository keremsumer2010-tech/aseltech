---
type: mimari
status: acik
date: 2026-11-14
owner: PC1
---

# Depo haritası

Hangi klasör ne için var, kimin. Sahiplik tablosunun kesin hâli: `docs/GOREV_DAGILIMI.md` §2.

## 1. Kök

```
CLAUDE.md            giriş noktası: okuma sırası                       PC1
AGENTS.md GEMINI.md  Antigravity/Gemini için CLAUDE.md'ye yönlendirme  PC1
README.md LICENSE    dışarıya görünen yüz, MIT                         PC1
.gitignore           ham veri, kimlik, build çıktısı dışarıda           PC1
.gitattributes       satır sonu sabitleme (LF)                         PC1
.github/workflows/   pages.yml: web + data + game → GitHub Pages        PC1

rules/               değişmez kurallar ve veri sözleşmesi              PC1
docs/                planlar, ürün tanımı, sözlük                      PC1
docs/story/          kaynaklar, kalibrasyon notu (PC4), pitch (PC5)
tasks/               PC başına görev dosyası + QUEUE + BACKLOG         PC1
                     (QUEUE.md: herkes sadece sahiplendiği satırı değiştirir)
docs/qa/             PC başına QA notu (docs/qa/PCx.md)                her PC kendi dosyası
status/              PC başına durum dosyası                           her PC kendi dosyası

pipeline/            indirme, kesme, alt kümeler (.npz)                PC2
analysis/            faz→cm, kümülatif, testler, out/*.npz             PC3
data/                web'in okuduğu her şey (sözleşme: rules/VERI_SOZLESMESI.md)
validation/          GNSS istasyonları ve zaman serileri               PC6
risk/                OSM altyapı hatları                               PC6
game/                Aquifer Manager (tek HTML)                        PC5
web/                 site                                              PC1
raw/                 ham .h5 indirmeleri (GIT DIŞI)
```

## 2. `data/` içi

```
data/catalog.json                                  PC1
data/central_valley/{meta,points,summary,decomp}.json, disp/*.png   PC3
data/central_valley/drivers.json                   PC2 (Pazar)
data/central_valley/{validation,assets}.json       PC6 (Pazar)
data/central_valley_fullyear/                      PC3 (Pazar, quality: mixed)
data/karapinar/{meta,points,summary}.json, disp/   PC3
data/karapinar/sinkholes.geojson                   PC4
data/uk/                                           PC4
```

## 3. Git dışı tutulanlar

| Yol / kalıp | Neden |
|---|---|
| `raw/`, `*.h5`, `*.nc`, `*.tif` (büyük) | GB'larca ham veri; GitHub 100 MB'ı reddeder |
| `.netrc`, `_netrc`, `.env` | Kimlik bilgisi |
| `node_modules/`, `dist/`, `.venv/`, `__pycache__/` | Yeniden üretilebilir |
| `cache/`, `*.zip` | Geçici |

## 4. Dallar ve uzak depo

| | |
|---|---|
| Dal | Sadece `main` |
| Uzak depo | Tek: `origin` = `github.com/keremsumer2010-tech/aseltech` (public) |
| Yayın | `main`'e her push → GitHub Actions → Pages |

## 5. Yayın nasıl çalışır

`.github/workflows/pages.yml`: `web/` (varsa `npm run build` → `web/dist`) site köküne,
`data/` → `/data`, `game/` → `/game` kopyalanır. Bu yüzden web kodu veriyi **göreli** yolla okur
(`data/central_valley/meta.json`, başında `/` yok). Vite kullanılıyorsa `vite.config.js` içinde `base: './'`.
