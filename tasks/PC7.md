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
