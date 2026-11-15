# Dosya haritası (codebase map)

Yapay zekâ ajanları ve insanlar için: **bir dosyayı aramadan önce buraya bak.** Tüm depoyu taramak yerine
aradığın şeyin hangi klasörde olduğunu buradan bul, sadece o dosyayı aç.
Son güncelleme: 2026-11-15 (web/ CSS ve JS dosyaları `web/css/` ve `web/js/` altına taşındı).
Sahiplik ve kurallar: `docs/DEPO_HARITASI.md`, `docs/GOREV_DAGILIMI.md`, `rules/RULES.md`.

## 1. Yayın: neyin canlı siteye gittiği

`.github/workflows/pages.yml`, `main`'e her push'ta siteyi şöyle kurar:

| Depodaki yol | Canlı sitedeki yol |
|---|---|
| `web/*` | `/` (site kökü) |
| `data/` | `/data/` |
| `game/` | `/game/` |
| `web3d/` | `/web3d/` |
| `docs/story/` | `/docs/story/` |
| `docs/bulletins/` | `/docs/bulletins/` ve `/bulletins/` |
| `risk/*.geojson` | `/risk/` |
| `validation/gnss_stations.csv` | `/validation/` |

Yayın öncesi kalite kapısı: `tools/check_site.py` (kırık link) + `tests/test_numbers_consistency.py`, `tests/test_site_links.py`.
Yerelde çalıştırma: `.claude/launch.json` → `python -m http.server 8791 --directory aseltech`, sonra `http://localhost:8791/web/index.html`.
JS dosyaları `location.pathname.includes('/web/')` ile yerelde mi canlıda mı olduğunu anlar, veriyi `ROOT + 'data/...'` ile okur.

## 2. `web/`: ana site

HTML sayfaları kökte kalır (canlı URL'ler, QR kodlar ve sunum linkleri bunlara bağlı, taşıma).

| Sayfa | Ne | Yüklediği CSS | Yüklediği JS |
|---|---|---|---|
| `index.html` | Ana sayfa | `css/style.css`, `css/home3.css`, `css/theme.css` | `js/home3.js` |
| `atlas.html` | Küresel çökme atlası (harita + NISAR uydu katmanı) | `css/style.css`, `css/atlas.css`, `css/atlas_sat.css`, `css/theme.css`, `vendor/maplibre-gl.css` | `vendor/maplibre-gl.js`, `vendor/satellite.min.js`, `js/atlas.js`, `js/atlas_sat.js`, `js/tour.js`, `js/tour_atlas.js` |
| `science.html` | Bilim / yöntem sayfası | `css/style.css`, `css/theme.css` | `js/docs.js` + sayfa içi script |
| `data.html` | Veri indirme / katalog | `css/style.css`, `css/theme.css` | `js/docs.js` + sayfa içi script |
| `faq.html` | SSS | `css/style.css`, `css/theme.css` | `js/docs.js` |
| `explorer.html` | Veri gezgini (sadece `present.html`'den linkli) | `css/style.css`, `css/theme.css` | `js/explorer.js` |
| `present.html` | Sunum modu (slaytlar) | `css/style.css`, `css/theme.css` | sayfa içi script |
| `panel.html` | İç ekip paneli (Türkçe, sitede linki yok) | sayfa içi | sayfa içi |

```
web/
  *.html              sayfalar (yukarıdaki tablo)
  css/                style.css (ortak), theme.css (ortak tema, en son yüklenir),
                      home3.css (ana sayfa), atlas.css, atlas_sat.css (atlas)
  js/                 home3.js (ana sayfa), atlas.js (atlas haritası; data/global/atlas.json okur),
                      atlas_sat.js (NISAR uydu yörüngesi; data/nisar_tle.json + satellite.js),
                      docs.js (science/data/faq ortak yardımcılar), explorer.js (data/catalog.json okur),
                      tour.js (rehberli tur motoru: ekran kararır, tek bölüm aydınlanır, yanında açıklama kutusu;
                      atlas ve simülatör ortak kullanır), tour_atlas.js (atlas turunun adımları, "? How to use" düğmesi),
                      i18n.js (TR/EN dil düğmesi ve çeviri motoru; 7 sayfanın <head>'inde), i18n_tr.js (Türkçe sözlük, bkz. §2.1)
  assets/             logo_mark_*.png, atlas_world.{jpg,webp}, simulator.jpg, bluemarble_2k.jpg (atlas.js)
  vendor/             maplibre-gl (atlas haritası), satellite.min.js (atlas uydu yörüngesi)
```

### 2.1 Türkçe / İngilizce çeviri

- Varsayılan dil İngilizce; İngilizcede sayfaya dokunulmaz, Türkçe sözlük hiç yüklenmez.
- Başlıktaki `TR`/`EN` düğmesi seçimi `localStorage` `nv-lang` içinde saklar ve sayfayı yeniler. `?lang=tr` / `?lang=en` de çalışır.
- `web/js/i18n.js` Türkçede `i18n_tr.js`'i yükler, sayfadaki metni çevirir, sonradan eklenen metni de (atlas listesi,
  simülatör olayları, tur kutuları) MutationObserver ile çevirir. Simülatör motoru `game/i18n_load.js` üzerinden yükler.
- Sözlük anahtarı = İngilizce metin (boşluklar tek); `{0}` `{1}` = metnin içindeki `<b>`/`<a>`/`<span>`; `#` = herhangi bir sayı
  (sırayla yerleşir), `#3` = İngilizcedeki 3. sayı (Türkçe cümle sırası sayıları yer değiştirdiğinde kullanılır).
- Eksik çeviriyi bulmak: sayfayı `?i18n=collect` ile aç, konsolda `I18N.missing()`. Eksik metin İngilizce kalır, hata vermez.
- Çevrilmeyenler: bilim sayfasındaki 7 katlanmış teknik rapor (`translate="no"`, başlıkta "İngilizce rapor" notu),
  harita/görsel içindeki yazılar ve grafik (canvas) etiketleri, yer adları, dosya yolları ve komutlar, `docs/bulletins/`, `web3d/`.

## 3. `game/`: yeraltı suyu simülatörü (canlıda `/game/`)

| Dosya | Ne |
|---|---|
| `index.html` | Oyun sayfası; `style.css`, `model.js`, `game.js`, `tests.js`, `tour_steps.js` yükler |
| `model.js` | Fizik/akifer modeli (oyunun hesap çekirdeği) |
| `game.js` | Arayüz, harita, etkileşim |
| `tests.js` | Model için tarayıcı içi testler |
| `test_model.html` | Sadece `model.js` testlerini çalıştıran geliştirici sayfası |
| `tour_steps.js` | Rehberli turun adımları; motoru `../js/tour.js` (canlı) ya da `../web/js/tour.js` (yerel) yükler. İlk "Start simulation"da kendiliğinden açılır, "? Guide" düğmesi tekrar oynatır |
| `i18n_load.js` | Sitenin çeviri motorunu yükler (`../js/i18n.js` canlı, `../web/js/i18n.js` yerel); dil düğmesi üst çubukta |
| `assets/` | Oyun logosu |

Rehberli tur (atlas + simülatör): ilk ziyarette bir kez açılır (localStorage `gt-done-atlas-v1` / `gt-done-sim-v1`).
Adım eklemek için `web/js/tour_atlas.js` ya da `game/tour_steps.js` içindeki `steps` listesine `{el: '#id', title, text}` ekle;
görünmeyen öğenin adımı kendiliğinden atlanır.

## 4. `web3d/`: 3B çökme yüzeyi (canlıda `/web3d/`)

`index.html` + `app.js` (three.js CDN'den) + `style.css`; veri `surfaces.json` (500 KB),
`generate_3d_data.py` ile üretilir. Sitedeki hiçbir sayfa buna link vermiyor; sadece doğrudan URL ve belgelerden erişiliyor.

## 5. Veri ve üretim hattı

| Klasör | Ne | Ana dosyalar |
|---|---|---|
| `data/` | Sitenin okuduğu her şey (format: `rules/VERI_SOZLESMESI.md`) | `catalog.json` (explorer/data), `numbers_registry.json`, `results_registry.json` (data/science), `nisar_tle.json` (atlas uydusu), `global/` (atlas: `atlas.json`, `home_summary.json`, şehir başına klasör) |
| `data/<bölge>/` | Bölge çıktıları: `meta.json`, `points.json`, `summary.json`, `disp/*.png` | central_valley, karapinar, konya_plain, delta, uk, uk_clay, fens, *_fullyear, *_p114/_p172 |
| `pipeline/` | NISAR verisini arama, indirme, kesme | `nisarvision/` (ana paket: `python -m nisarvision`), `search.py`, `download.py`, `subset.py`, `subset/` (.npz alt kümeler), `pc2/`, `pc7/`, `pc10/` (PC'lere özel betikler; `pc10/build_atlas.py` atlası kurar) |
| `analysis/` | Faz → cm, kümülatif seri, ayrıştırma | `insar.py`, `cumulative.py`, `gunw_io.py`, `web_grid.py`, `decomp/`, `pc5/ pc6/ pc8/ pc9/`, `out/` (ara çıktılar) |
| `validation/` | GNSS/GPS doğrulaması | `fetch_gnss.py`, `compare.py`, `gnss/*.csv`, `gnss_stations.csv` |
| `risk/` | Altyapı riski (OSM) | `compute_risk.py`, `probabilistic_risk.py`, `*_infra.geojson` |
| `tools/` | Site/atlas yardımcıları ve kontroller | `check_site.py` (link kontrolü), `bulletin.py` (docs/bulletins üretir), `build_home_summary.py`, `validate_atlas.py`, `atlas_qc.py`, `atlas_exports.py`, `vital_signs.py`, `sync_*.py` |
| `tests/` | pytest: site sayıları ve atlas şeması tutarlılığı | `test_site_numbers.py`, `test_site_links.py`, `test_numbers_consistency.py`, `test_atlas_schema.py`, `test_home_summary.py` |

## 6. Belgeler ve ekip koordinasyonu

| Yol | Ne |
|---|---|
| `CLAUDE.md` (= `AGENTS.md`, `GEMINI.md`) | Giriş noktası, okuma sırası |
| `rules/` | `RULES.md` (değişmez kurallar), `VERI_SOZLESMESI.md` (veri formatı) |
| `tasks/` | `PCx.md` görev dosyaları, `QUEUE.md`, `BACKLOG*.md`, `SUREKLI.md` |
| `status/` | Her PC'nin durum dosyası |
| `docs/` | Planlar (`MASTER_PLAN`, `ZAMAN_CIZELGESI`, `TODAY_PLAN`), `URUN_TANIMI`, `SOZLUK`, `DEPO_HARITASI` (sahiplik) |
| `docs/story/` | Sunum, pitch, kaynaklar, yöntem notları, `media/` (sitede kullanılan figürler) |
| `docs/bulletins/` | Bölge bültenleri (HTML, `tools/bulletin.py` üretir) |
| `docs/qa/` | PC başına QA notları |

## 7. Silinen fosil dosyalar (2026-11-15)

Hiçbir sayfa, script, test veya yayın adımı kullanmadığı için silindi; gerekirse git geçmişinden geri alınabilir:
`web/app.js` (eski ana hikâye scripti), `web/nisar3d.js` (linksiz 3B yörünge görünümü) ve yalnız onun kullandığı
`web/vendor/three/`, `web/assets/earth_day_3600.jpg`, `web/assets/earth_lights_4096.jpg`; ayrıca `web/assets/logo_mark_32.png`,
`web/mock/` (erken sahte veri), `data/central_valley_p114_fullyear/` (hiçbir yerde referansı yoktu).
`data/numbers_registry.json` içinde bu dosyalara işaret eden eski satırlar, `analysis/pc5/numbers_registry.py` yeniden çalışınca temizlenir.

Yarı-kullanılan (silme, ama bil): `web/panel.html` (iç ekip paneli, sitede linksiz), `web3d/` (yayında ama linksiz),
`game/test_model.html` (geliştirici test sayfası). `pages.yml` içindeki `nisar3d.js` cache-bust satırı artık boşa çalışıyor (zararsız).
