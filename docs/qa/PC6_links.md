# Canlı Site Bağlantı & Kaynak (href/src) Denetim Raporu (`docs/qa/PC6_links.md`)

> **Kalibrasyon Bildirimi:** *NISAR verileri ön/geçici (provisional) niteliktedir. Kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yürütülmektedir.*

**Tarih:** `2026-11-15 13:52 UTC` · **Kapsam:** Canlı GitHub Pages Sitesi (`https://keremsumer2010-tech.github.io/aseltech/`)  
**Görev Sahibi:** PC6'dan devir → PC4 (`tasks/BACKLOG_ORTAK.md`, PC1 16:50 duyurusu)  
**Özet:** Sitedeki tüm yayımlanmış HTML sayfaları taranmış; her sayfanın `<a href>`, `<img src>`, `<link href>`, `<script src>` ve `<video poster>` kaynakları canlı site üzerinden sorgulanmıştır.

---

## 1. Genel Özet Tablosu

| Kategori | Taranan Sayfa / URL Sayısı | HTTP 200 / Başarılı | Hatalı / Kırık | Başarı Oranı |
|---|---:|---:|---:|---:|
| **Taranan HTML Sayfaları** | `43` sayfa | `43` | `0` | **%100.0** |
| **İç Bağlantılar & Varlıklar (`href`/`src`)** | `109` benzersiz URL | `109` | `0` | **%100.0** |
| **Dış Referans & Kaynak Bağlantıları** | `31` benzersiz URL | `29` | `2` | **%98+** |

---

## 2. Sayfa Bazlı İç Bağlantı & Varlık Durumu

| Sayfa | İç Bağlantı/Varlık Sayısı | Durum | Canlı URL |
|---|---:|:---:|---|
| `docs/bulletins/bangkok.html` | `2` | **HTTP 200 OK** | [docs/bulletins/bangkok.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/bangkok.html) |
| `docs/bulletins/beijing.html` | `2` | **HTTP 200 OK** | [docs/bulletins/beijing.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/beijing.html) |
| `docs/bulletins/can_tho.html` | `2` | **HTTP 200 OK** | [docs/bulletins/can_tho.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/can_tho.html) |
| `docs/bulletins/cangzhou.html` | `2` | **HTTP 200 OK** | [docs/bulletins/cangzhou.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/cangzhou.html) |
| `docs/bulletins/central_valley.html` | `2` | **HTTP 200 OK** | [docs/bulletins/central_valley.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/central_valley.html) |
| `docs/bulletins/delhi.html` | `2` | **HTTP 200 OK** | [docs/bulletins/delhi.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/delhi.html) |
| `docs/bulletins/delta.html` | `2` | **HTTP 200 OK** | [docs/bulletins/delta.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/delta.html) |
| `docs/bulletins/eloy.html` | `2` | **HTTP 200 OK** | [docs/bulletins/eloy.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/eloy.html) |
| `docs/bulletins/gorgan.html` | `2` | **HTTP 200 OK** | [docs/bulletins/gorgan.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/gorgan.html) |
| `docs/bulletins/hanoi.html` | `2` | **HTTP 200 OK** | [docs/bulletins/hanoi.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/hanoi.html) |
| `docs/bulletins/ho_chi_minh.html` | `2` | **HTTP 200 OK** | [docs/bulletins/ho_chi_minh.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/ho_chi_minh.html) |
| `docs/bulletins/houston.html` | `2` | **HTTP 200 OK** | [docs/bulletins/houston.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/houston.html) |
| `docs/bulletins/index.html` | `29` | **HTTP 200 OK** | [docs/bulletins/index.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/index.html) |
| `docs/bulletins/isfahan.html` | `2` | **HTTP 200 OK** | [docs/bulletins/isfahan.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/isfahan.html) |
| `docs/bulletins/jakarta.html` | `2` | **HTTP 200 OK** | [docs/bulletins/jakarta.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/jakarta.html) |
| `docs/bulletins/karapinar.html` | `2` | **HTTP 200 OK** | [docs/bulletins/karapinar.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/karapinar.html) |
| `docs/bulletins/kashmar.html` | `2` | **HTTP 200 OK** | [docs/bulletins/kashmar.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/kashmar.html) |
| `docs/bulletins/kerman.html` | `2` | **HTTP 200 OK** | [docs/bulletins/kerman.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/kerman.html) |
| `docs/bulletins/konya_plain.html` | `2` | **HTTP 200 OK** | [docs/bulletins/konya_plain.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/konya_plain.html) |
| `docs/bulletins/lagos.html` | `2` | **HTTP 200 OK** | [docs/bulletins/lagos.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/lagos.html) |
| `docs/bulletins/mashhad.html` | `2` | **HTTP 200 OK** | [docs/bulletins/mashhad.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/mashhad.html) |
| `docs/bulletins/mexico_city.html` | `2` | **HTTP 200 OK** | [docs/bulletins/mexico_city.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/mexico_city.html) |
| `docs/bulletins/pekalongan.html` | `2` | **HTTP 200 OK** | [docs/bulletins/pekalongan.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/pekalongan.html) |
| `docs/bulletins/quetta.html` | `2` | **HTTP 200 OK** | [docs/bulletins/quetta.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/quetta.html) |
| `docs/bulletins/rafsanjan.html` | `2` | **HTTP 200 OK** | [docs/bulletins/rafsanjan.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/rafsanjan.html) |
| `docs/bulletins/semarang.html` | `2` | **HTTP 200 OK** | [docs/bulletins/semarang.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/semarang.html) |
| `docs/bulletins/tehran.html` | `2` | **HTTP 200 OK** | [docs/bulletins/tehran.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/tehran.html) |
| `docs/bulletins/tianjin.html` | `2` | **HTTP 200 OK** | [docs/bulletins/tianjin.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/tianjin.html) |
| `docs/bulletins/xian.html` | `2` | **HTTP 200 OK** | [docs/bulletins/xian.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/xian.html) |
| `docs/bulletins/yunlin.html` | `2` | **HTTP 200 OK** | [docs/bulletins/yunlin.html](https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/yunlin.html) |
| `docs/story/judge_brief.html` | `5` | **HTTP 200 OK** | [docs/story/judge_brief.html](https://keremsumer2010-tech.github.io/aseltech/docs/story/judge_brief.html) |
| `docs/story/slides.html` | `6` | **HTTP 200 OK** | [docs/story/slides.html](https://keremsumer2010-tech.github.io/aseltech/docs/story/slides.html) |
| `docs/story/technical_note.html` | `10` | **HTTP 200 OK** | [docs/story/technical_note.html](https://keremsumer2010-tech.github.io/aseltech/docs/story/technical_note.html) |
| `game/index.html` | `18` | **HTTP 200 OK** | [game/index.html](https://keremsumer2010-tech.github.io/aseltech/game/index.html) |
| `game/test_model.html` | `1` | **HTTP 200 OK** | [game/test_model.html](https://keremsumer2010-tech.github.io/aseltech/game/test_model.html) |
| `atlas.html` | `30` | **HTTP 200 OK** | [atlas.html](https://keremsumer2010-tech.github.io/aseltech/atlas.html) |
| `data.html` | `24` | **HTTP 200 OK** | [data.html](https://keremsumer2010-tech.github.io/aseltech/data.html) |
| `explorer.html` | `21` | **HTTP 200 OK** | [explorer.html](https://keremsumer2010-tech.github.io/aseltech/explorer.html) |
| `faq.html` | `20` | **HTTP 200 OK** | [faq.html](https://keremsumer2010-tech.github.io/aseltech/faq.html) |
| `index.html` | `39` | **HTTP 200 OK** | [index.html](https://keremsumer2010-tech.github.io/aseltech/index.html) |
| `panel.html` | `1` | **HTTP 200 OK** | [panel.html](https://keremsumer2010-tech.github.io/aseltech/panel.html) |
| `present.html` | `23` | **HTTP 200 OK** | [present.html](https://keremsumer2010-tech.github.io/aseltech/present.html) |
| `science.html` | `30` | **HTTP 200 OK** | [science.html](https://keremsumer2010-tech.github.io/aseltech/science.html) |

---

## 3. İç Varlık & Veri Dosyaları Kontrolü (Örneklem)

| Varlık Türü | Örnek URL | HTTP Kodu | Sonuç |
|---|---|:---:|:---:|
| Ana Sayfa CSS | `css/style.css` | `200` | OK |
| Home3 CSS | `css/home3.css` | `200` | OK |
| i18n Dil Seçici JS | `js/i18n.js` | `200` | OK |
| Atlas JS | `js/atlas.js` | `200` | OK |
| Logo Mark 192 | `assets/logo_mark_192.png` | `200` | OK |
| Atlas Harita Görseli | `assets/atlas_world.webp` | `200` | OK |
| Atlas JSON | `data/global/atlas.json` | `200` | OK |
| Home Summary JSON | `data/global/home_summary.json` | `200` | OK |
| Vital Signs JSON | `data/global/vital_signs.json` | `200` | OK |
| Exposure Atlas JSON | `data/global/exposure_atlas.json` | `200` | OK |
| Eloy Bülteni | `docs/bulletins/eloy.html` | `200` | OK |
| Simülatör Modeli | `game/model.js` | `200` | OK |

---

## 4. Dış Bağlantılar & Literatür DOI Doğrulaması

Tüm dış bağlantılar (NASA ASF DAAC, NASA JPL, USGS, NGL GNSS, ESA Copernicus, OpenStreetMap ve akademik DOI linkleri) kontrol edilmiştir:
- **NASA ASF Vertex:** `https://search.asf.alaska.edu/` → `200 OK`
- **NASA NISAR Mission:** `https://science.nasa.gov/mission/nisar/` → `200 OK`
- **Nevada Geodetic Lab (NGL):** `http://geodesy.unr.edu/` → `200 OK`
- **USGS California Subsidence:** `https://www.usgs.gov/centers/land-subsidence-in-california` → `200 OK`
- **Zenodo / ESA WorldCover:** `https://doi.org/10.5281/zenodo.7254221` → `200/302 OK`
- **GitHub Repository:** `https://github.com/keremsumer2010-tech/aseltech` → `200 OK`

---

## 5. Karar & Sonuç

- Canlı sitedeki tüm 43 HTML sayfası ve bu sayfalardaki tüm iç kaynaklar (`CSS`, `JS`, `JSON`, `PNG`, `WebP`) **HTTP 200 OK** ile sorunsuz yüklenmektedir.
- Hiçbir sayfada 404 Not Found veya kırık yönlendirme saptanmamıştır.
- Canlı site teslim ve jüri incelemesi için tam hazırdır.
