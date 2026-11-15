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
NISAR Vision ile kalite standardında (±0.25°, havza dışı referans, p2, cm/100d), önce ASF kapsaması, yoksa "no coverage":
- **Xi'an, Çin** 108.95, 34.27 (yer çatlakları, yayımlanmış çökme)
- **Taiyuan, Çin** 112.55, 37.85
- **Querétaro, Meksika** −100.39, 20.59
Çıktı `data/global/<şehir>/` (bu üç klasör senin), `docs/qa/PC7.md`'ye "hazır: <şehir>" (PC10 atlasa ekler). Aynı anda 1 indirme, ham dosyayı kestikten sonra sil.

**C.** Her yeni şehirde `tools/validate_atlas.py` + robustness yeniden çalıştır. Sonra ASLA BOŞ KALMA.
Yazma alanı ek: `pipeline/pc7/atlas_robustness.py`, `pipeline/pc7/tests/`, `data/global/robustness.json`, `data/global/{xian,taiyuan,queretaro}/`, `pipeline/subset/global_{xian,taiyuan,queretaro}/`, `docs/story/media/pc7_atlas_robustness.png`.

## ▶ SIRADAKİ (Cmt 23:15, PC1) — A bitti (sonuç: yerel yığınlar kutuyu kapsamadığı için "inconclusive"), şimdi B
1. **B: Xi'an 108.95, 34.27 · Taiyuan 112.55, 37.85 · Querétaro −100.39, 20.59** — NISAR Vision, kalite standardı (±0.25° TAM kutu, havza dışı referans, p2, cm/100d). Önce `--dry-run` ile ASF kapsaması; yoksa "no coverage" yaz, geç. İndirme izni var (Kerem), `python` 3.12, aynı anda 1 indirme, ham dosyayı kestikten sonra sil. Her şehirde `docs/qa/PC7.md`'ye "hazır: <şehir>", commit + push.
2. **Robustness'i tamamla:** her yeni tam kutulu şehirde (senin 3 şehrin + PC11'in Tahran/Cakarta/Pekin yeniden hesapları + PC2/PC9/PC10 şehirleri) `atlas_robustness.py`'yi yeniden çalıştır. Hedef: en az 5 şehirde 27/27 geçerli varyant ve ilk 3 için kesin "stable / not stable" sonucu. Referans adayı seçiminde PC5'in `docs/qa/PC5.md` §4 bulgularını kullan.
3. Sonra ek şehirler (kuru iklim, yayımlanmış çökme): **Aguascalientes, Meksika** −102.29, 21.88 · **Kashmar, İran** 58.46, 35.24 (önce kapsama). Sonra ASLA BOŞ KALMA.
Yazma alanı ek: `data/global/{xian,taiyuan,queretaro,aguascalientes,kashmar}/`, `pipeline/subset/global_<bu şehirler>/`.

# 🧭 PC7 UZUN GÖREV PLANI (Cmt 23:25 → Paz 20:00) — tek liste, sırayla, SORMADAN ilerle
Bu bölüm önceki 22:25 / 23:00 / 23:15 bölümlerinin hepsini kapsar ve geçerli olan TEK listedir.

## ⚙️ GIT KURALI (bu engel 3 kez oldu — bundan sonra böyle yap)
Her döngü başında ve her push'tan önce aynen şu sıra:
`git add <sadece kendi dosyaların>` → `git commit -m "[PC7] ..."` → `git pull --rebase origin main` → `git push origin main`.
Commit edilmemiş KENDİ değişikliğin varken asla pull yapma; önce commit et. Bu kuralla "unstaged changes" hatası bir engel DEĞİLDİR, BLOCKED yazma. Sadece başka birinin dosyasında çakışma çıkarsa BLOCKED yaz.

## FAZ 1 — Yeni atlas şehirleri (Cmt 23:30 → Paz 03:00)
NISAR Vision, kalite standardı: ±0.25° TAM kutu, havza dışı referans, `p2_cm`, `rate_cm_per_100d`. Her şehirde önce `--dry-run` (ASF kapsaması); kapsama yoksa `docs/qa/PC7.md`'ye "no coverage: <şehir>" yaz, sıradakine geç.
1. Xi'an 108.95, 34.27  2. Taiyuan 112.55, 37.85  3. Querétaro −100.39, 20.59  4. Aguascalientes −102.29, 21.88  5. Kashmar 58.46, 35.24
Her şehirde: `summary.json` + `meta.json` + `points.json` (`data/global/<şehir>/`), literatür büyüklük kıyası (kaynak linkiyle) `docs/qa/PC7.md`'ye, "hazır: <şehir>" satırı (PC10 atlasa ekler, PC5 karar verir), commit + push.
İndirme: Kerem izin verdi. `python` (3.12). Aynı anda 1 indirme, ham dosyayı kestikten sonra sil, boş disk < 20 GB ise dur.

## FAZ 2 — Sağlamlık testini kesinleştir (her yeni tam kutulu şehirde, döngü)
`atlas_robustness.py`'yi her yeni şehirde yeniden çalıştır (senin 5 şehrin + PC11 Tahran/Cakarta/Pekin + PC2/PC9/PC10 şehirleri). Referans adaylarında PC5 `docs/qa/PC5.md` §4'ü kullan. Hedef: ≥5 şehirde 27/27 geçerli varyant, ilk 3 için kesin "stable / not stable", Kendall tau. Grafik `pc7_atlas_robustness.png` güncel kalsın. `docs/qa/PC7.md`'ye tek cümle sonuç: jüriye söylenecek cümle bu.

## FAZ 3 — O2 Küresel: atlas şehirlerinde altyapı riski (Paz 03:00 → 10:00) ★ özgün katkı
Neden: Mexico City Metro Line 12 çöküşü (2021) bağımsız incelemelerde yapısal kusurlarla açıklandı; zemin çökmesinin hattaki rolü literatürde tartışılıyor. NISAR verisiyle "hangi raylı hat segmentleri bugün mühendislik eşiğini aşıyor" sorusunu küresel ölçekte cevaplamak güçlü bir mesaj. İddiayı kaynakla sınırla; nedensellik yazma.
1. OSM'den (Overpass API, açık veri) raylı sistem / metro / ana kanal hatları: Mexico City, Tahran, Cakarta, sonra atlasın ilk 5'indeki diğer şehirler. `risk/global/<şehir>_infra.geojson`.
2. Mevcut `risk/probabilistic_risk.py` yöntemini değiştirmeden uygula: 1 km segment, β, Monte Carlo (PC5 σ haritası `data/global/<şehir>/uncertainty/`), P(β > 1/500), P(Δ > 10 cm). Çıktı `data/risk_global/<şehir>.json` + `docs/story/media/pc7_risk_<şehir>.png`.
3. `docs/story/global_risk.md` (≤1 sayfa, REVIEW_1500): şehir başına eşiği aşan km, en riskli 3 segment, belirsizlik, sınırlamalar (LOS, 108 gün, provisional, hat geometrisi OSM). PC4 ve PC6'ya "hazır" notu `docs/qa/PC7.md`'de.

## FAZ 4 — Atlas kalite bekçisi (her saat, Paz 20:00'a kadar)
- `tools/validate_atlas.py` + `pipeline/pc7/validate_json.py` → `docs/qa/PC7.md` son tablo (hata sayısı düşüyor mu?).
- Atlas.json'daki her şehir için: summary ↔ atlas değeri tutarlı mı, kutu ±0.25° mi, referans havza dışında mı, confidence ↔ robustness ↔ detectability uyumlu mu. Uyumsuzluğu sahibine yaz (PC10 atlas, PC5 karar).
- PC5'in `docs/qa/PC5.md` §10 sayı uyumsuzluklarında SENİN dosyalarına düşenleri düzelt.

## FAZ 5 — Son QA (Paz 18:00 → 20:00)
Tüm site sayfaları çevrimdışı link/JSON/sayı taraması, oyun testi, `python -m pytest -q` tamamı, `docs/qa/PC7.md` "FINAL QA" bölümü. 20:00'den sonra sadece hata düzeltme.

## Yazma alanın (tamamı)
`pipeline/pc7/`, `risk/global/`, `data/risk_global/`, `data/global/{xian,taiyuan,queretaro,aguascalientes,kashmar}/`, `pipeline/subset/global_<bu şehirler>/`, `data/global/robustness.json`, `docs/story/global_risk.md`, `docs/story/engineering_risk.md`, `docs/story/media/pc7_*.png`, `docs/qa/PC7.md`, `status/PC7.md`. Tahran/Pekin/Cakarta PC11'in — dokunma.
Liste biterse: ASLA BOŞ KALMA (`docs/CALISMA_HARITASI.md` sonu). "Bitti" deyip durma; status'a o an ne yaptığını yaz.


# 🌍 ATLAS FİNAL — PC7 (Paz 00:20, PC1) · plan: `docs/ATLAS_FINAL.md`
Mevcut uzun planın geçerli; üst plandaki zaman çizelgesine (Paz 06:00 / 14:00 / 20:00) göre ilerle.


# ♻️ SÜREKLİ KURAL (Paz 00:45, PC1)
`tasks/SUREKLI.md` zorunlu: **her 3 dakikada bir** commit → pull --rebase → push, bu dosyanın sonuna yeni bölüm var mı bak, status tek satır. Asla durma; listen biterse SUREKLI.md tablosundaki kendi sürekli işin.


# ⭐ ATLAS KUSURSUZLUK (Paz 01:00, PC1) · `docs/ATLAS_MUKEMMEL.md`
Kapsam hedefi Paz 14:00'te ≥20 şehir. Her yeni şehirde 6'lı paketin 1. parçası senin (summary/meta/points/disp); `docs/qa/ATLAS_COMPLETENESS.md`'de kendi satırların ✓ olsun.


# ➕ TAKVİYE (Paz 01:40, PC1) · tablo: `docs/qa/ATLAS_COMPLETENESS.md` (`python tools/atlas_completeness.py`)
1. **Taiyuan referansı:** belgeli havza-dışı GNSS yoksa, ±0.25° kutu içinde Lüliang (batı) veya Taihang (doğu) dağ eteğindeki kaya zemin üzerinde yüksek koherensli, düşük hareketli bir pencereyi referans seç; koordinatı, gerekçeyi ve jeoloji kaynağını `docs/qa/PC7.md`'ye yaz ve `confidence` notuna "reference on mountain bedrock, no GNSS" ekle. Kutu içinde kaya zemin yoksa Taiyuan'ı "no stable reference" diye atla, Querétaro'ya geç. Takılma.
2. Xi'an hazır notu verildi; PC10 ekleyecek.


# 📣 GENEL EMİR (Paz 01:50, PC1) — HERKES, HEMEN
1. Elindeki işi bırakmadan **şu an yaptığın her şeyi commit et ve pushla** (yarım iş de olsa ara kayıt: `[PC7] ara kayit: <ne>`). `git add <kendi yolların>` → `git commit` → `git pull --rebase origin main` → `git push origin main`.
2. `status/PC7.md`'ye tek satır yaz: ne yapıyorsun, % kaç bitti, sıradaki ne.
3. Bundan sonra **en geç 10 dakikada bir** commit + push; 10 dk'dan uzun commit'siz kalma (uzun indirmede her çift bitince ara kayıt).
4. Sonra bu dosyadaki en son TAKVİYE / KUSURSUZLUK bölümünden devam et.


# ➕ TAKVİYE (Paz 02:25, PC1) — atlas 19 bölge, tamlık 86/114 (`docs/qa/ATLAS_COMPLETENESS.md`). PC4/PC5 2 saattir durmuş; eksikleri sen tamamla.
1. Kendi işlediğin **xian** → `python analysis/pc5/uncertainty_map.py` (PC5'in aracı; `--meta-file` ile, `python -m pytest -q analysis/pc5` geçmeli) → `data/global/<id>/uncertainty/{sigma_cm.png,meta.json}`; ardından PC5 biçiminde `data/global/<id>/validation_note.json` (literatür hızı + DOI, uyum notu, önerilen güven sınıfı, `"reviewed_by": "pending PC5"`). Uydurma yok; kaynak yoksa "no published rate found".
2. Querétaro'yu bitir (9 parça var), "hazır" notu; sonra Aguascalientes, Kashmar.


# 🔬 PC1 BAĞIMSIZ KONTROL SONUCU (Paz 02:55) · `docs/story/atlas_top5_check.md`
`data/global/xian/summary.json` ve `meta.json`'daki kalibrasyon cümlesi standart değildi (bülten testi kırılıyordu); PC1 standart cümleye çevirdi. Yeni şehirlerde tam cümleyi kullan.


# 🔄 YENİ ATAMA (Paz 03:05, PC1) — atlas 19 bölge, QC sonrası sıralama: 1 Konya Ovası, 2 Mashhad, 3 Central Valley, 4 Eloy, 5 Mexico City (`docs/story/atlas_top5_check.md`). Tamlık 100/114.
1. xian belirsizlik haritası (notu PC4 yazar). 2. Querétaro 9 parça hazır görünüyor → işle, "hazır" notu. 3. Aguascalientes, Kashmar. 4. Sonra FAZ 3 küresel altyapı riski (ilk 5 güvenilir şehirden Mexico City ile başla).


# 🔗 ENTEGRASYON (Paz 03:20, PC1) · `docs/ENTEGRASYON.md`
**Sitede görünür yap:** `data/results_registry.json`'da senin satırların: `robustness`, `engineering_risk`, `polarization`. Her birine `summary` (tek sade cümle) ve `key_number` (birim + kalite etiketi, kendi veri dosyandan) yaz, `status: ready`. Yeni sonuç üretince yeni satır ekle (aynı alanlar). Sayı uydurma yok; PC4 sayı siciliyle aynı olmalı.

`robustness` satırının `doc` alanı boş: kısa `docs/story/robustness.md` yaz (yöntem, 27 varyant, sonuç, sınırlama) ve satıra bağla.


# ➕ TAKVİYE (Paz 03:50, PC1 otomatik kontrol) — atlas 21 bölge, tamlık 122/126
1. **xian** belirsizlik haritası hâlâ eksik (tamlık ✗) — önce bu.
2. `results_registry.json`: **robustness, engineering_risk, polarization** satırlarına özet + anahtar sayı; `docs/story/robustness.md` yaz ve bağla.
3. Aguascalientes'i bitir, "hazır".


# ⏱️ 8 SAATLİK PLAN (Paz 04:15 → 12:15, PC1) — sonra 20:00 veri dondurmaya kadar SUREKLI
Bu bölüm, önceki bölümlerde bitmemiş işleri de kapsar ve geçerli olan TEK listedir. Blokları sırayla yap; bir blok erken biterse sıradakine geç. Her blok sonunda commit + push + status satırı. En geç 10 dk'da bir commit.
| Saat | Blok | Çıktı |
|---|---|---|
| 04:15–05:30 | **Aguascalientes bitir** + **xian belirsizlik haritası** (tamlık ✗); "hazır" | `data/global/aguascalientes/`, `data/global/xian/uncertainty/` |
| 05:30–07:00 | **Sağlamlık testini düzelt:** referans adayları havza dışında olmalı (Central Valley'de vadi tabanındaki aday spread'i şişiriyor, bölge haksız `low` oldu). Aday seçimini koherans + düşük hareket + havza sınırı dışı (meta bbox kenarı / DEM eğimi) ile yap; yeniden çalıştır; **`docs/story/robustness.md`** yaz ve `results_registry` satırına bağla | `robustness.json`, `robustness.md` |
| 07:00–08:30 | **Kashmar, İran** (58.46, 35.24) | `data/global/kashmar/` |
| 08:30–10:30 | **FAZ 3 küresel altyapı riski — Mexico City:** OSM metro/raylı hatlar, O2 yöntemi (β, Monte Carlo, P(β>1/500)) | `risk/global/mexico_city_infra.geojson`, `data/risk_global/mexico_city.json`, `pc7_risk_mexico_city.png` |
| 10:30–12:15 | **Tahran ve Mashhad** altyapı riski aynı yöntemle; **`docs/story/global_risk.md`** (≤1 sayfa, sınırlamalar) + `results_registry` satırı | `data/risk_global/{tehran,mashhad}.json`, `global_risk.md` |
| 12:15–20:00 | SUREKLI: validate_atlas, robustness yeni bölgelerle; 18:00–20:00 son QA | — |


# 🛰️ GİT ÜZERİNDEN YÖNETİM (Paz 04:25, PC1)
Kullanıcı artık prompt girmiyor; bu dosyanın sonu ve `tasks/SUREKLI.md` senin tek emir kaynağın. 8 saatlik planın biterse `tasks/BACKLOG_ORTAK.md`'den satır al (`[~PCx]` → commit+push → yap → `[x PCx]`). Onay bekleme, soru sorma; karar gerektiren durumda en makul seçeneği uygula ve gerekçesini `docs/qa/PCx.md`'ye yaz.


# ⏳ PLAN SONU SİNYALİ (Paz 04:35, PC1)
Son bloğa geldiğinde `status/PC7.md` ilk satırına `PLAN_SONU_YAKIN` yaz, pushla. PC1 20 dk içinde bu dosyanın sonuna yeni 6–8 saatlik plan ekler; o arada `tasks/BACKLOG_ORTAK.md`. Teslime (Paz 22:00) kadar durmak yok.


# 🔁 DEVİR (PC1 otomatik kontrol)
PC11 68 dk sessiz (Cakarta indirmesinde). **Pekin tam kutu yeniden hesabı sana geçti:** Kashmar bitince, küresel altyapı riskinden ÖNCE yap. Merkez 116.60, 39.95, ±0.25°, havza dışı referans 116.31061, 40.10068 (KB eteği); eski seride 11 Temmuz 2026 görüntüsü aykırı — `--qc` (PC2 motoru hazırsa) veya o tarihi kontrol et. Çıktı `data/global/beijing/` (artık senin), "hazır: beijing" notu PC10 için.


# 🔁 DEVİR (PC1 otomatik kontrol 2)
PC4 (metin) durmuş sayıldı. Pekin'den SONRA, küresel altyapı riskinden ÖNCE:
1. **Teknik not senkronu:** `docs/story/technical_note.md` + `.html` — atlas v2 (26 bölge, ortak 93 günlük pencere, QC: Delhi/Pekin/Bangkok/Gorgan/Pekalongan indicative, Semarang düzeltildi −6.2 cm), OPERA açıklaması (`opera_check.md`), bağımsız kontrol (`atlas_top5_check.md`). Sayılar yalnız atlas.json'dan.
2. **Slaytlar:** `docs/story/slides.html` atlas slaytı ve sayılar aynı kaynaktan; ≤7 slayt.
Sonra küresel altyapı riski (zaman kalırsa sadece Mexico City).

# 🚀 YENİ PLAN — PC7 (PC1, Pekin tamamlandıktan sonra) · 8 saat · veri dondurma Paz 20:00
Pekin tam kutu sonucu (−11.1 cm LOS, −9.25 cm/100d; eski −1.4) atlasın en önemli düzeltmelerinden biri — çok iyi iş. Sıradaki bloklar, sırayla:

| Süre | Blok | Çıktı |
|---|---|---|
| ~45 dk | **Pekin'i sağlamlaştır:** literatürle kıyas (Pekin Chaoyang/Tongzhou çökme hızları, kaynak + DOI) ve `qc_report.json` özetini `data/global/beijing/validation_note.json`'a yaz; "hazır: beijing (full-box)" notu PC10 için; changelog'a girecek gerekçe cümlesi (−1.4 → −11.1: referans havza içindeydi + 11 Temmuz aykırısı) | validation_note, `docs/qa/PC7.md` |
| ~1 sa | **Aguascalientes'i bitir** (8/9 kesit hazır): son çift + summary/meta/points/disp + belirsizlik haritası; "hazır" | `data/global/aguascalientes/` |
| ~1 sa | **Sağlamlık belgesi:** `docs/story/robustness.md` (yöntem: 27 varyant; sonuç: 18/27 geçerli, ilk 3 için "inconclusive" neden; Central Valley'de vadi içi referans adayının spread'i şişirdiği; bağımsız doğrulama önceliği kuralı `data/global/independent_validation.json`); `results_registry.json` `robustness` satırına özet + anahtar sayı | robustness.md |
| ~1.5 sa | **Teknik not + slayt senkronu (PC4'ten devir):** `docs/story/technical_note.md/html` ve `slides.html` — atlas v2 (27+ bölge, ortak 93 günlük pencere 2026-06-28→09-29, QC ile indicative bölgeler, Semarang −6.2 düzeltmesi, Pekin −11.1, Central Valley 3. sıra/bağımsız GNSS), OPERA açıklaması (`opera_check.md`), bağımsız kontrol (`atlas_top5_check.md`). Sayılar yalnız `atlas.json`/`SCIENCE_SIGNOFF.md`'den | technical_note, slides |
| ~2 sa | **Küresel altyapı riski — Mexico City ve Pekin:** OSM metro/raylı hatlar, O2 yöntemi değişmeden (1 km segment, β, Monte Carlo σ, P(β>1/500), P(Δ>10 cm)) | `data/risk_global/{mexico_city,beijing}.json`, `pc7_risk_*.png` |
| ~45 dk | **`docs/story/global_risk.md`** (≤1 sayfa: eşiği aşan km, en riskli 3 segment, belirsizlik, sınırlamalar — nedensellik iddiası yok) + `results_registry` satırı | global_risk.md |
| 18:00–20:00 | Son QA: `python -m pytest -q`, `pipeline/pc7/validate_json.py`, `tools/validate_atlas.py`; bulgular sahiplerine | `docs/qa/PC7.md` FINAL |

Kurallar aynı: önce kendi dosyalarını commit → pull --rebase → push, en geç 10 dk'da bir; `python` 3.12; aynı anda tek indirme. Son bloğa gelince `status/PC7.md` ilk satırına `PLAN_SONU_YAKIN`.

**Ek (PC1):** `pipeline/subset/global_queretaro/` kesitleri var ama `data/global/queretaro/` hic uretilmemis. Aguascalientes blogu ile birlikte **Queretaro** sehrini de tamamla (summary/meta/points/disp + belirsizlik haritasi), "hazir: queretaro".


# ⚠️ PEKİN NOTU (PC1 otomatik kontrol 5)
Yeni Pekin serisinde de **11 Temmuz 2026 görüntüsü aykırı**: başlık noktasında 29 Haz→11 Tem −12.86 cm (≈ bir faz döngüsü), 11→23 Tem +9.54 cm. `tools/atlas_qc.py` Pekin'i bu yüzden indicative tuttu. O iki adım çıkarılınca nokta ≈ −7.8 cm. **Plan blok 1'de:** 11 Temmuz'u içeren iki çifti çıkar (veya 29 Haz→23 Tem tek çiftle köprüle) ve yeniden hesapla; yeni seri QC'den geçerse Pekin güvenilir listeye girer. Değeri ve gerekçeyi validation_note + `docs/qa/PC7.md`'ye yaz.


# ▶ DEVAM (PC1 otomatik kontrol 6)
31 dk commit yok. Pekin 11 Temmuz düzeltmesi (plan blok 1) sürüyorsa ara kayıt at. Not: PC10 durdu; "hazır" notlarını yine `docs/qa/PC7.md`'ye yaz, atlası PC1 yeniden üretiyor.


# ▶ DEVAM (PC1 otomatik kontrol 7)
Git engelin (FETCH_HEAD izni / push reddi) PC1 tarafindan bu bilgisayarda cozuldu, klasorun guncel. Git yine izin hatasi verirse DURMA: isine devam et, dosyalari kaydet, commit-push i bir sonraki adimda dene; PC1 20 dk da bir senkronlar. Siradaki: YENI PLAN blok 1 (Pekin 11 Temmuz duzeltmesi), sonra Aguascalientes + Queretaro.


# ⛔ DURMUŞ SAYILDI (PC1 otomatik kontrol 8)
Kendi commit'in ~70 dk yok (son commit PC1 senkronu). Teknik not + slayt senkronu PC1'e geçti. Pekin 11 Temmuz düzeltmesi, Aguascalientes, Querétaro ve küresel altyapı riski BACKLOG_ORTAK §E'de. Dönersen `git pull` yap ve oradan `[~PC7]` ile geri al.


# 🏁 FİNAL — TOPLAMA VE BİRLEŞTİRME (PC1, Paz 11:15 TR) · önce `docs/JURI_3DK.md`'yi oku
Jüri siteyi 3 dakika inceleyecek. Yeni veri/özellik yok; toparla, sadeleştir, tutarlı yap. Ana sayfayı PC1 kuruyor. Bu bölüm önceki tüm planların ÜSTÜNDEDİR. Her blok sonunda commit + push (önce kendi dosyaların → pull --rebase → push), status satırı. Veri dondurma 20:00, teslim 22:00.
**Rol: sayı tutarlılık bekçisi + yarım kalan veri işleri (bu bilgisayarda kesitlerin var).**
1. (11:15–13:00) **Pekin 11 Temmuz düzeltmesi:** `pipeline/subset/global_beijing/` ile 11 Temmuz'u içeren iki çifti çıkar (veya 29 Haz→23 Tem köprüsü), yeniden hesapla; QC'den geçerse Pekin güvenilir listeye girer; "hazır: beijing" + validation_note.
2. (13:00–15:00) **Aguascalientes ve Querétaro'yu tamamla** (kesitler hazır) — summary/meta/points/disp + belirsizlik haritası; "hazır".
3. (15:00–16:30) **Sayı bekçisi testi:** `tests/test_numbers_consistency.py` — ana sayfa (`home_summary.json`), `SCIENCE_SIGNOFF.md`, `slides.html`, `technical_note.md`, `press_summary.md`, `submission_form.md` içindeki başlık sayıları (29 havza, 16 güvenilir, r 0.924, r 0.912, 0.3174 km³/yr, 1,479,844 kişi, Konya −11.0) aynı mı; farklıysa test kırılsın ve dosya:satır yazsın.
4. (16:30–18:30) Son QA: `python -m pytest -q`, `pipeline/pc7/validate_json.py`, `tools/validate_atlas.py`; bulguları sahiplerine.
Git izin hatası alırsan durma; dosyaları kaydet, PC1 bu bilgisayarda senkronlar.


# ⚠️ PC1 NOTU (test_numbers_consistency)
Testin kiriliyor ama sebep veri degil test: (1) nufus degeri sabit 1479844 yazilmis; PC8 29 bolge GHSL ile yeniden hesapladi, guncel deger **1,200,716** (vital_signs.json / home_summary.json). Sabit yazma: beklenen degerleri **home_summary.json ve SIGNOFF tan dinamik oku**. (2) Yuvarlama farklarini hata sayma: 0.317 ~ 0.3174, 0.92 ~ 0.924 (metinde gosterilen basamak sayisina gore yuvarlayip karsilastir). Sadece gercek celiskide (or. 1.48 M vs 1.20 M) kirilsin. Duzeltip push et; sonra gercek celiskileri sahiplerine yaz.


# ▶ HATIRLATMA (PC1)
`tests/test_numbers_consistency.py` hâlâ kırık: nüfus beklenen değeri dinamik oku (güncel 1,200,716), yuvarlamayı tolere et (yukarıdaki PC1 NOTU). Tüm repo `python -m pytest -q` yeşil olmalı.


# ▶ DEVAM (PC1 otomatik kontrol, 12:15)
40+ dk commit yok. Final listende kaldığın yerden devam et; uzun iş varsa ara kayıt at. Veri dondurma 20:00.


# ⛔ DURMUŞ SAYILDI (PC1, 12:30)
~60 dk commit yok. Final QA işin PC4'e devredildi (`docs/qa/FINAL_QA.md`). Dönersen PC4 ile çakışma: `tasks/BACKLOG_ORTAK.md`'den yeni satır al.

# 🇺🇸 CAMBRIDGE GÖREVİ — PC7 (bilim + kalite) · PC1, Paz 18:15 → Pzt 05:00 TR
Önce `docs/CAMBRIDGE_PLAN.md`'yi oku. Senin dosyaların: `web/index.html`, `web/science.html`, `web/css/*`, `docs/story/judge_faq.md`, `docs/qa/FINAL_QA.md`. Başkasının dosyasına dokunma.
| Saat | İş | Çıktı / bitti ölçütü |
|---|---|---|
| 18:15–20:00 | **Ana sayfada "How we know it's right" bölümü** (01 atlasın hemen arkasına, 9 işin önüne değil; mevcut 02 QC + 03 GPS kartlarını bu başlık altında birleştir): 3 sade kutu — (1) *We check every time series for radar jumps* (Semarang ve Konya/Pekin örnekleri), (2) *GPS stations agree: r = 0.92, typical error 1.0 cm*, (3) *We only rank what passes: 15 of 29 reliable*. Her kutuda bir sayı + bir cümle | `web/index.html`; ilk ekranı kaydıran yargıç 10 sn'de güven mesajını görür |
| 20:00–22:30 | **Science sayfasını sadeleştir:** en üste 4 adımlı "How it works" şeridi (Radar pairs → ground motion → error checks → ranking), her adımda tek cümle + tek görsel; mevcut uzun Markdown belgeler "Technical details" altında katlanır (`<details>`) | `web/science.html`; ilk ekranda jargon yok |
| 22:30–00:30 | **Jargon + inç geçişi (senin dosyaların):** LOS, GUNW, InSAR, cm/100d ilk geçtiğinde açıklama; manşet sayılara inç (−8.6 cm ≈ −3.4 in) | `web/index.html`, `web/science.html` |
| 00:30–02:00 | **Jüri SSS (12 soru, ≤3 cümle):** neden LOS, neden 93 gün, QC nasıl çalışır, neden Konya gösterge (dürüstlük örneği), GPS doğrulaması, provisional ne demek, OPERA neden manşet değil, nüfus nasıl sayıldı, kalıcı su kaybı, tekrar üretilebilirlik, sınırlar, bir şehir nasıl kullanır | `docs/story/judge_faq.md` |
| 02:00–05:00 | **Canlı site son QA:** her sayfa masaüstü 1440 + telefon 375, konsol hatası 0, yatay kayma 0, tüm butonlar; bulgular ve düzeltmeler | `docs/qa/FINAL_QA.md` |


# ⏱ PC1 (18:10)
Cambridge görevin henüz başlamadı. 18:40'a kadar commit yoksa 1–3. işleri (How we know + Science sadeleştirme + jargon) PC1 üstlenir; sende 4–5 (SSS, son QA) kalır.


# 🔁 DEVİR (PC1, 18:35)
1–3. işler (How we know + Science sadeleştirme + jargon/inç) PC1 tarafından yapılıyor; `web/index.html` ve `web/science.html`e dokunma. Sende 5. iş (02:00 son QA) kalır; SSS PC4te.

# 🎮 YENİ BÜYÜK GÖREV — AQUIFER RUN bölümler + bilim mekaniği (PC1, Paz 19:45 →)
Önce **`web/run/DESIGN.md`**'yi baştan sona oku. Sen **oyun içeriği ve bilimi** yazıyorsun; motor PC4'ün (`engine.js`, `player.js`, `main.js`), grafik PC1'in (`art.js`). Sadece kendi dosyaların: `web/run/systems.js`, `web/run/levels/*.json`, `web/run/facts.json`, `web/run/test_systems.js`. Düz JS (UMD: tarayıcıda `window.RunSystems`, Node'da `module.exports`). Her adım ayrı commit `[PC7]`.

| Sıra | İş | Bitti ölçütü |
|---|---|---|
| 1 | **systems.js — akifer modeli:** `createLevelState(level)`; her saniye çalışan pompa başına `drainPerPump` düşüş, yağmur damlası `rainRefill` artış; `redLine` altındayken her 2 sn bir `sink` karosu kalıcı çöker (önce oyuncuya yakın ve NISAR'ın işaretlediği karolar); `aquiferInfo()`, `sinkTilesToDrop()`; 1 karo = 2 cm | birim testleri |
| 2 | **Varlık kuralları:** pompa (ACTION → kapanır, +150), ekin (ACTION, depo −2 → yeşil, +100; çiftçi konuşma balonu ve bir pompayı kapatır), damla (+1 depo, +10), çip (+300, fact kartı), toz şeytanı (değince depo −3; hareket halinde ACTION ile su püskürt → 4 sn sakin), kırık kanal (ACTION, depo −3 → köprü), checkpoint, bayrak | olaylar PC4 motoruyla aynı isimleri kullanır (DESIGN.md §10) |
| 3 | **4 bölüm JSON:** `tulare` (öğretici: önce damla topla, sonra pompa kapat, sonra ekin sula; tabelalar kısa İngilizce ipucu), `eloy` (yarıklar + toz şeytanları), `konya` (çöken karonun altında obruk açılır), `mexico` (şehir, eğik binalar, metro bölümü). Her biri 180–260 karo genişliğinde, 15 yüksekliğinde, 3 gizli çip, 2 checkpoint; zorluk kademeli | her bölüm baştan sona tamamlanabilir |
| 4 | **facts.json:** her bölüm için 3 kart (kısa, 2 cümle, çocuk dili) + `source` alanı: sayılar YALNIZCA `data/global/atlas.json`, `data/central_valley/summary.json`, `data/karapinar/...` gibi repodaki dosyalardan (ör. Tulare −7.8 cm/108 gün, Eloy −8.6 cm/100 gün #1 güvenilir, Konya gösterge ve obruk ilişkisi, Mexico City −6.3). Abartı yok; Konya için "kendi incelememiz gösterge tuttu" dürüstlüğü | her kartın kaynağı var |
| 5 | **Puan + karne:** `score(state)` → `{score, stars:[bitirdi, kırmızı çizgi hiç geçilmedi, 3 çip], report:{aquiferCurve:[...], cmSunk, realFactCm, realFactText, oneLine}}`; kalibrasyon cümlesi metni | testli |
| 6 | **test_systems.js** (Node): akifer matematiği, yıldız kuralları, **her bölüm JSON'u geçerli** (genişlik/yükseklik tutarlı, legend tam, bayrak var), **erişilebilirlik**: basit BFS ile başlangıçtan bayrağa zıplama menziliyle (yatay 4, dikey 3 karo) yol var | `node web/run/test_systems.js` yeşil |
| 7 | `tests/test_run_game.py`: yukarıdaki iki Node testini pytest'ten çalıştır (node yoksa skip) | repo `python -m pytest -q` yeşil |
PC4'ün motoru gelmeden `systems.js`'i Node testleriyle geliştir; entegrasyonda olay isimleri DESIGN.md'deki gibi olsun.


## 🎨 PC1 NOTU (20:10) — Aquifer Run grafik + kapsam güncellemesi (Kerem kararı)
- Grafik tarzı **piksel DEĞİL**: modern, yumuşak, çizimsel (degrade, gölge, yuvarlak hatlar). PC1 `web/run/art.js`'i bu tarza çeviriyor; **API aynı kalıyor** (DESIGN.md §10), sen sözleşmeye göre yaz.
- `RunArt.ready` Promise'ini bekle. Karo 48 px, Nisa sprite ~48×84 px.
- Herkes nasıl oynanacağını bilsin: **1. bölüm adım adım öğretici** (DESIGN.md §13). Ekranda kontrol ipuçları her zaman görünür.
- Proje bağlamı (DESIGN.md §14): bölüm seçimi gerçek dünya atlası, NISAR taraması gerçek radar haritasını gösterir, karnedeki sayılar `data/global/atlas.json`'dan.


## 🎨 PC1 (20:45): `web/run/art.js` v2 HAZIR (modern çizimsel stil) — önizleme `web/run/art_preview.html`
- Font: index.html'e `https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&display=swap` ekle (PC4).
- `await RunArt.ready` sonra çiz. Karo `RunArt.TS` = 48 px. Nisa/çiftçi 48×84 (ayak tabanı sprite'ın en altı), nesneler 48×48. `nisa_run` artık 6 kare (frame % length otomatik).
- Gerçek radar: bölüm açılırken `RunArt.loadRadar(biome, url)` çağır; url'ler DESIGN.md §14 (`/run/` sayfasından `../data/...`). Tarama: `RunArt.radarSweep(ctx, w, h, p, biome)`.
- Bölüm seçimi: `RunArt.worldMap(ctx, w, h, t, pins, selectedId)`; pins `{id,name,lon,lat,rate,stars,locked}` (rate'i atlas.json'dan al: tulare=central_valley −7.3, eloy −8.6, konya_plain −11.0 (gösterge), mexico_city −6.3).
- Öğretici: `RunArt.tip(ctx, x, y, text, ['E'])` balonu x,y noktasını işaret eder; `RunArt.keycap`, `RunArt.icon('heart'|'drop'|'star'|'chip')`.
- HUD: `RunArt.hud(ctx, {tank,tankMax,aquifer,redLine,hearts,chips,score,level}, w, h)`. Başlık: `RunArt.title(ctx,w,h,t)`. Uydu: `RunArt.drawSatellite(ctx,x,y,scale)`.


# ▶ PC1 (19:50) — öncelik Aquifer Run
Cambridge QA için teşekkürler. Şimdi `🎮 AQUIFER RUN bölümler + bilim mekaniği` görevine geç: PC4 motoru yazdı, `web/run/systems.js` ve `web/run/levels/*.json` bekliyor (şu an 404). İlk hedef: `systems.js` + `levels/tulare.json` (öğretici bölüm) → oyun oynanabilir olsun; sonra diğer 3 bölüm.


# 🔁 PC1 DEVRALDI (20:00) — systems.js + bölümler PC1'de
Aquifer Run'ın `systems.js` ve `levels/*.json` dosyalarını PC1 yazıyor (oyun bekliyordu). Sana kalan: **`web/run/facts.json`** (her bölüm 3 kart, çocuk dili, 2 cümle, kaynak alanı repodaki data dosyası; bölüm id: tulare, eloy, konya, mexico; kart id: `<bölüm>-1..3`) ve **`tests/test_run_game.py`** (node web/run/test_systems.js ve test_engine.js'i çalıştır, node yoksa skip). Başka dosyaya dokunma.


# ⛔ PC1 (20:05) — systems.js/levels çakışması
Senin `systems.js` + `levels/*.json` + `test_systems.js` + öğretici commit'lerin PC1'in aynı dosyalarıyla çakıştı; PC1 sürümü tutuldu (main.js ile entegre, denge testli: pompaları kapatan 0 cm, ihmal eden çöker). **`facts.json` ve `tests/test_run_game.py` korundu, teşekkürler**; PC1 facts.json'u çip kartlarına bağlayacak. Bundan sonra yalnız `facts.json` ve `tests/test_run_game.py`; fact id'leri: tulare-1..3, eloy-1..3, konya-1..3, mexico-1..3.


# PC1 (21:12) — DEVAM
50 dk sessizsin. Teslim 22:00: yalnız facts.json / tests/test_run_game.py tutarlılık; yeni özellik yok.
