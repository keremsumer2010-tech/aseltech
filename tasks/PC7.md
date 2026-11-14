# PC7 — Codex (ChatGPT) · Fens tarım ritmi, göl/baraj, site kalite kontrolü (14:35'te açıldı)

## Kimlik
Kerem'in bilgisayarı · OpenAI Codex · klon klasörü `aseltech-pc7` · commit öneki `[PC7]`

## Yazma alanı
`pipeline/pc7/` (kendi scriptlerin) · `data/fens/` · `data/water/` · `docs/qa/PC7.md` · `status/PC7.md` · QUEUE'da sadece Q10/Q17 satırları.
Başka hiçbir dosyaya yazma. `web/`, `game/`, `analysis/`, `pipeline/` kökü başkalarının.

## En kritik iş
Q10: İngiltere sahnesini GERÇEK ölçümle güçlendiren Fens ekin ritmi.

## Görevler (sırayla, bitince sormadan sıradakine)
1. **(14:40–16:30) Q10 Fens ekin ritmi** — `fens` bbox (-0.3, 52.4, 0.4, 52.9). ASF'den `platform=NISAR`, `processingLevel=GCOV`, tarihi ≥ 2026-06-17 (provisional) ürünleri listele.
   Her tarih için GCOV'dan bbox'ı kes (HV ve HH, gamma0 → dB). 3–5 tarla (düzgün dikdörtgen, ~0.5 km, birbirinden ayrı) seç; her tarlanın tarih başına ortalama HV dB'sini hesapla.
   Çıktı: `data/fens/crops.json` = `{dates, fields:[{id, name, lon, lat, hv_db:[...], hh_db:[...]}], quality:"provisional", quality_note, source, method}` + `data/fens/hv_timeseries.png` (grafik).
   Yorum (İngilizce, 3 cümle, `method` alanına): hasat/sürüm döneminde HV düşüşü görülüyor mu? Görülmüyorsa dürüstçe yaz.
   İndirme Earthdata ister: `~/.netrc` bu bilgisayarda kurulu ve çalışıyor (biçim RULES E-07). Şifre isteme, dosyayı okuma.
   Ham .h5 dosyalarını `raw/` altına indir (git dışı), işin bitince sil.
2. **(16:30–17:30) Site kalite kontrolü** → `docs/qa/PC7.md`: https://keremsumer2010-tech.github.io/aseltech/ ve science.html, data.html, faq.html: kırık link, konsol hatası, telefon (375 px) görünümü, İngilizce yazım. Sadece rapor; dosyalara dokunma.
3. **Q17 göl/baraj su alanı** (zaman kalırsa) → `data/water/`.

## Bitti sayılır eğer
crops.json geçerli JSON ve sözleşmeye uygun · grafik açılıyor · status/PC7.md'de kullanılan granüller ve yöntem yazılı · push edildi.

## Yapma listesi
Beta (2026-06-17 öncesi) veri kullanma · `.h5`/`.netrc` commit etme · başka PC'nin dosyasına yazma · sayı uydurma · `git add -A` / `git add .`.

## Rapor (`status/PC7.md`)
Ne bitti, nasıl doğrulandı, sınırlamalar, `AI: Codex → ...` satırı.

---
# 15:00 not
Görev 2 (site QA) için PC1 siteyi açık "makale" temasına geçiriyor; QA'yı 16:00 sonrası yeni temada yap. `docs/REVIEW_1500.md` yazım kurallarına göre metinlerde AI kokan ifadeleri de raporla.

---
# 15:05 BLOCKED çözümü (PC1)
Codex'in .netrc'yi okumaması doğru davranış; bu bilgisayarda Earthdata indirmesi YAPMA. Yeni sıra:
1. **Görev 2'ye (site QA) şimdi geç** → `docs/qa/PC7.md` (site açık temaya geçti; `docs/REVIEW_1500.md` yazım kurallarına göre de kontrol et).
2. Fens GCOV verisini **PC2 indirip kesecek** → `pipeline/subset/fens_gcov/<tarih>.npz` (`hh_db`, `hv_db`, `x`, `y`, `epsg`, `date`, `quality`). Dosyalar gelince Q10 analizini bunlardan yap (indirme yok) → `data/fens/crops.json` + grafik.
3. Q17 iptal (indirme gerektiriyor). Onun yerine: `game/` için bağımsız oynanış testi → `docs/qa/PC7.md` (10 farklı strateji: düşük/orta/yüksek pompalama, nadas; sonuçlar mantıklı mı, hata var mı). Oyun dosyalarına dokunma.
Status'taki BLOCKED satırını "yok" yap.

---
# 16:15 CHALLENGE UYUMU — A12 "Hangi polarizasyon değişimi gösteriyor?"
Q10 Fens analizinde (fens_gcov: `hh_db`, `hv_db`) **HH, HV ve HV/HH oranını** karşılaştır: hangi kanal ekim/hasat/sürüm değişimini en net gösteriyor? → `data/fens/crops.json` içinde üçü de + `docs/story/polarization.md` (4–5 cümle sade İngilizce: HV hacim saçılması → bitki; HH pürüzlülük/nem; radar pürüzlülük ve dielektrik sabitine duyarlıdır) + `docs/story/media/pc7_polarization.png`. Yazma alanına eklendi: `docs/story/polarization.md`, `docs/story/media/pc7_*.png`. İndirme yok.

> **16:25 PC1 — KAYNAKLAR ENTEGRASYONU:** `docs/KAYNAKLAR_ANALIZI.md`'yi oku; §4'te senin satırındaki işleri mevcut işine ek olarak yap (özellikle §1 NASA Land Subsidence StoryMap çerçevesi). Kendi cümlenle özetle, link ve atıf ver.

> **18:55 PC1:** Lincoln geçti. `docs/AKSAM_PLANI.md`'deki kendi satırına geç (akşam → Pazar). Durma.

> **19:45 PC1 — TEK SIRA ARTIK BURASI:** `docs/CALISMA_HARITASI.md` içindeki kendi bölümün. Yukarıdan aşağı yap, bitince "ASLA BOŞ KALMA" döngüsü. Teslime kadar durma.

---
# 20:00 PC1 — HATA AYIKLAMA GÖREVLERİ (Codex; indirme ve tarayıcı yok)
PC1 kontrolünde bulunanlar ve senin düzeltme iznin (bu maddeler için yazma alanı genişletildi; düzeltmeden önce `git log -3 -- <dosya>` ile son 15 dk'da başkası değiştirdiyse dokunma, `docs/qa/PC7.md`'ye yaz):
1. `web/index.html` ~117. satır: `pc9_fullyear_point.png` görseli boş `src` / kırık yol (PC8 bulgusu). `web/app.js`'de `data-src` yükleyicisi var mı kontrol et; yoksa doğrudan `src`'yi doğru göreli yola çevir (yayında site kökü web/, docs/story/ yanına kopyalanıyor → `docs/story/media/...`; yerelde `../docs/story/media/...` — mevcut ROOT mantığına uy).
2. `web/explorer.html`: kalibrasyon uyarısı yok → diğer sayfalardaki sabit metni ekle: "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."
3. Repo kökünde `requirements.txt` var mı? Yoksa oluştur, varsa güncelle: asf_search, h5py, numpy, scipy, matplotlib, pyproj, rasterio, shapely, requests, pytest, pillow. (`analysis/pc5/test_cross_sensor.py` `requests` olmadan toplanamıyor.)
4. `python -m pytest -q` tüm repo; geçmeyen/toplanamayan testleri `docs/qa/PC7.md`'ye yaz.
5. Tüm `data/**/*.json` için: geçerli JSON mu (NaN/Infinity tarayıcıda `response.json()`'u bozar), `quality` alanı var mı — script `pipeline/pc7/validate_json.py`; sonucu `docs/qa/PC7.md`.
6. Q10 Fens mevsim yorumu (çalışma haritası madde 2), sonra her 2 saatte doğrulamayı tekrar çalıştır.

---
# 20:10 PC1 — ÖZGÜN KATKI O2 (sahibi sensin; `docs/OZGUN_KATKILAR.md` §O2) — 20:00 hata ayıklama 1–3'ten hemen sonra
Mühendislik standardıyla, belirsizliği hesaba katan altyapı riski (indirme yok, repo verisiyle):
1. Girdiler: `analysis/out/central_valley_cum.npz` (kümülatif ızgara), `data/central_valley/uncertainty/` (σ; NaN düzeltmesi PC8'de), `risk/central_valley_infra.geojson` (OSM hatları), `data/central_valley/assets.json` (mevcut indeks).
2. Her segment: 100 m aralıkla örnekle; dikey tahmin (LOS/cos θ); **açısal distorsiyon β = Δçökme / mesafe** (pencereler: 100 m, 500 m, 1 km), segment boyunca **maks diferansiyel çökme**; kanallar için ayrıca boyuna profil.
3. Belirsizlik: piksel σ ile 1000 Monte Carlo → `p_beta_exceed` (eşikler 1/500 ve 1/1000; kaynaklı: Boscardin & Cording 1989, Skempton & MacDonald 1956 — kaynağı doğrula ve `engineering_risk.md`'ye yaz), `p_diff_gt_10cm`, %90 güven aralığı.
4. Çıktı: `risk/probabilistic_risk.py` (+ `risk/test_probabilistic_risk.py`: bilinen profil → bilinen β; σ=0 → olasılık 0/1), `data/central_valley/assets_prob.json` (segment başına `name, type, osm_id, beta_max, p_beta_exceed, p_diff_gt_10cm, ci90`), `docs/story/engineering_risk.md` (yöntem, eşik kaynakları, ilk 10 segment tablosu, California Aqueduct yorumu, sınırlamalar: tek yaz sezonu, LOS varsayımı), `docs/story/media/pc7_risk_prob.png`.
5. Mevcut deterministik indeksle karşılaştır: ilk 10 değişti mi? Bir paragraf.
Yazma alanına eklendi: `risk/probabilistic_risk.py`, `risk/test_probabilistic_risk.py`, `data/central_valley/assets_prob.json`, `docs/story/engineering_risk.md`.

---
# 20:50 PC1 — BÜYÜK GÖREV: `docs/ATLAS_PLANI.md`
Şu anki küçük işini bitir, sonra SORMADAN `docs/ATLAS_PLANI.md` içindeki kendi bölümüne geç ve yukarıdan aşağı yap. Teslime kadar durma; bitince ASLA BOŞ KALMA döngüsü (hata ayıklama dahil).

## 🔴 YENİ (Cmt 22:25, PC1) — Atlas sağlamlık testi + yeni şehirler
Neden: Sıralama tek bir referans ve tek bir koherens eşiğine dayanıyor. NASA mühendisi ilk bunu sorar: "Referansı değiştirirseniz sıra değişir mi?" Bunu sayıyla cevaplayan ekip yok.

**A. Sağlamlık testi (indirme yok, hemen başla)**
1. `pipeline/pc7/atlas_robustness.py`: her atlas şehri için (yerel `pipeline/subset/global_*` + Central Valley, Karapınar, Konya Ovası, Delta yığınları) başlık değerini şu varyasyonlarla yeniden hesapla:
   - 3 farklı havza dışı referans (kutunun farklı köşelerinde sabit zemin; koordinatları JSON'a yaz),
   - koherens eşiği 0.3 / 0.4 / 0.5,
   - kutu ±0.20° / ±0.25° / ±0.30°.
2. Çıktı `data/global/robustness.json`: her şehir için `{id, base_rate_cm_per_100d, min, max, spread_cm, rank_min, rank_max, n_variants}` + Kendall tau (temel sıralama ile varyantlar arası). Atlas.json'a YAZMA; PC10 `confidence` için okur.
3. `docs/story/media/pc7_atlas_robustness.png`: her şehir için hata çubuğu (min–max), sıralı. `docs/qa/PC7.md`'ye özet: "ilk 3 sıra tüm varyantlarda değişmiyor / değişiyor".
4. Testler `pipeline/pc7/tests/` (ağsız), `python -m pytest -q` geçmeli.

**B. Yeni şehirler (A bitince; Kerem'in bilgisayarında netrc var)**
NISAR Pulse ile kalite standardında (±0.25°, havza dışı referans, p2, cm/100d), önce ASF kapsaması, yoksa "no coverage":
- **Xi'an, Çin** 108.95, 34.27 (yer çatlakları, yayımlanmış çökme)
- **Taiyuan, Çin** 112.55, 37.85
- **Querétaro, Meksika** −100.39, 20.59
Çıktı `data/global/<şehir>/` (bu üç klasör senin), `docs/qa/PC7.md`'ye "hazır: <şehir>" (PC10 atlasa ekler). Aynı anda 1 indirme, ham dosyayı kestikten sonra sil.

**C.** Her yeni şehirde `tools/validate_atlas.py` + robustness yeniden çalıştır. Sonra ASLA BOŞ KALMA.
Yazma alanı ek: `pipeline/pc7/atlas_robustness.py`, `pipeline/pc7/tests/`, `data/global/robustness.json`, `data/global/{xian,taiyuan,queretaro}/`, `pipeline/subset/global_{xian,taiyuan,queretaro}/`, `docs/story/media/pc7_atlas_robustness.png`.

## 🔁 DEĞİŞİKLİK (Cmt 23:00, PC1) — A görevi PC11'e geçti, sen İNDİRME işlerine odaklan
PC11'in ortamı indirme yapamıyor; senin bilgisayarında netrc + paketler hazır. **Sağlamlık testini (A) YAPMA — PC11 yapıyor** (`data/global/robustness.json`). Senin sıran:
1. **Tahran, Pekin, Cakarta'yı kalite standardıyla yeniden hesapla** (PC11'den devir; atlas sıralamasındaki en büyük hata burada: PC5 §4 → Pekin −1.4 cm referans değişince −7.6 cm, Tahran −3.5 → −7.3). Tam ±0.25° kutu için TAZE subset indir (eski yığınlar kutuyu kapsamıyor, `docs/qa/PC11.md`). Referans havza dışında: Tahran güney Shahr-e Rey konisinin DIŞI, Pekin Tongzhou çanağının DIŞI. Merkezler: Tahran 51.30, 35.55 · Pekin 116.60, 39.95 · Cakarta 106.83, −6.15. Eski/yeni değeri `docs/qa/PC7.md`'ye yaz.
2. Xi'an, Taiyuan, Querétaro (önceki B).
3. Celaya −100.81, 20.52 · Kerman 57.07, 30.28 · Tianjin 117.20, 39.10 · Bulacan 120.90, 14.85 (PC11'den devir; kuru iklimliler önce).
Her şehirde `docs/qa/PC7.md`'ye "hazır: <şehir>" (PC10 atlasa ekler), commit + push. Aynı anda 1 indirme, ham dosyayı kestikten sonra sil, boş disk < 20 GB ise dur. `python` (3.12) kullan.
Yazma alanı ek: `data/global/{tehran,jakarta,beijing,xian,taiyuan,queretaro,celaya,kerman,tianjin,bulacan}/`, `pipeline/subset/global_<bu şehirler>/`.
