---
type: gorev
id: PC2
owner: Memir (memir-erdogmus)
tool: Antigravity (Gemini)
status: acik
date: 2026-11-14
depends_on: []
feeds: [PC3]
---

# PC2 · Veri: GUNW arama, indirme, kesme

> **Saat saat sıra ve iş bitince sıradaki iş: `docs/ZAMAN_CIZELGESI.md`.** Atanmış QUEUE işlerin orada.

> **ACİL (PC1, 13:15):** npz'lerde `ion` boş geliyor (shape (0,)). PC3'ün kümülatif hattı iyonosfer ekranını çıkarıyor; tüm çiftler aynı şekilde işlenmeli.
> `science/LSAR/GUNW/grids/frequencyA/unwrappedInterferogram/HH/ionospherePhaseScreen` katmanını `ion` olarak (unw ile aynı kesit ve boyut) kaydet.
> Mevcut 2 dosyayı (06-28→07-10, 09-08→09-20) da `ion` ile yeniden üret (indirme ~2 dk). Ayrıca `status/PC2.md`'yi doldur (şu an boş).

## Kimlik
Memir'in bilgisayarı, Antigravity. Ana hattın ilk halkası: **PC3 senin dosyalarını bekliyor.**

## Yazma alanın
`pipeline/` (script, csv, `subset/`) · `docs/gunw_structure.md` · `data/<site>/drivers.json` (Pazar) · `status/PC2.md`

## Başlamadan
- [ ] `rules/RULES.md` (özellikle K-9 kimlik, §8 disk) ve `rules/VERI_SOZLESMESI.md` §2-§4 okundu
- [ ] Boş disk ≥ 50 GB

---

## Görev 1 · Hesap, liste, ilk dosya (12:00-13:30) · **ACİL**

1. https://urs.earthdata.nasa.gov hesabı. **Şifreyi insan girer.** Ajan `~/.netrc` şablonunu hazırlar
   (`machine urs.earthdata.nasa.gov login <BURAYA> password <BURAYA>`), değerleri insan yazar. Ajan dosyayı okumaz, yazdırmaz.
2. `pip install asf_search h5py numpy matplotlib`
3. `pipeline/search.py`: Central Valley bbox, GUNW, path 34 → `pipeline/central_valley_gunw.csv`
   Sütunlar: `granule, date1, date2, crid, url, size_mb, quality`
   (`quality` = her iki tarih ≥ 2026-06-17 ise `provisional`, değilse `beta-precal`).
4. İlk dosya: **2026-09-08 → 2026-09-20** çifti. `raw/` altına indir.
5. HDF5 ağacını `docs/gunw_structure.md`'ye yaz: unwrapped phase, coherence, x/y, EPSG, dalga boyu, incidence yolları;
   veri tipleri ve birimler; dosyadaki kalite/sürüm/kalibrasyon attribute'ları (değerleriyle).
6. **Hemen push.**

**Bitti sayılır eğer:** csv'de path 34 çiftleri listeli; `gunw_structure.md` gerçek dosyadan (`h5py` ile) üretilmiş ve push edilmiş.

## Görev 2 · 6 provisional çifti kes (13:30-16:00)

Sırayla (her biri bittikçe push, K-13):
```
2026-06-28→07-10 · 07-10→07-22 · 07-22→08-15 · 08-15→08-27 · 08-27→09-08 · 09-08→09-20
```
`pipeline/subset.py`: bbox'ı kes → `pipeline/subset/central_valley/<t1>_<t2>.npz`
- İçerik ve tip: `rules/VERI_SOZLESMESI.md` §4.1 (`unw` float32, `coh` uint8, `np.savez_compressed`, ≤ 20 MB).
- Sadece CRID `P05023` (PROVISIONAL). Kesimden sonra ham `.h5` silinir.
- Aynı anda diskte en fazla 5 ham dosya.

**Bitti sayılır eğer:** 6 npz push edildi; her biri `np.load` ile açılıp boyut ve NaN oranı status'a yazıldı.

## Görev 3 · Pazar: tam yıl ve toprak nemi

- Beta-precal dahil tam zincir (2025-11-24 → 2026-10-14) → **ayrı klasör** `pipeline/subset/central_valley_beta/`.
  Zincirde boşluk varsa (ardışık çift yok) listele, status'a yaz.
- SME2 toprak nemi → `data/central_valley/drivers.json` (sözleşme §4.2; çökme serisini PC3'ten al).

---

## En kritik iş
`docs/gunw_structure.md`'yi 13:30'dan önce push etmek. PC3 okuma kodunu buna göre yazacak.

## B planı
- `.h5` indirilemiyorsa (Access denied, yavaş bağlantı): BLOCKED + hata metni. PC1 browse PNG planına geçer;
  sen browse PNG'leri (girişsiz) `pipeline/browse/central_valley/` altına indir.
- İndirme çok yavaşsa (< 5 MB/s): çift sayısını 4'e indir, PC1'e status'ta yaz.

## Yapma
- `.h5`'i repoya ekleme. `git add -A` yok.
- Provisional ile beta'yı aynı klasöre koyma.

## Rapor
`status/PC2.md`: kaç dosya bitti, indirme hızı, her npz'nin boyutu ve NaN oranı, hata varsa `BLOCKED:` + hata metni, `AI:` satırı.

---
# 14:10 YENİ PAKET (öncelik sırası; harika gidiyor)
1. **Q01 Karapınar** kalan provisional çiftler (iyonosferli) → bitince PC3'e status'ta haber.
2. **Q04 SME2 toprak nemi** → `data/central_valley/drivers.json` (sitenin "Why it happens" grafiği bunu bekliyor).
3. **Q03 GCOV** 6 provisional tarih HV dB → `data/central_valley/gcov/` + meta.json.
4. **path 114 desteği**: PC3 Q21 için kendi indirmesini yapıyor; isterse `pipeline/central_valley_p114_gunw.csv` listesini sen üret (status'ta sor).
5. **Q07 tam yıl zinciri** — 22:00'de başlat, gece sürsün (`pipeline/subset/central_valley_beta/`, `quality: beta-precal` / provisional ayrı). Bilgisayar uykuya geçmesin.
6. **Q10 Fens ekin ritmi** (zaman kalırsa).

---
# 15:00 ÖNCELİK DEĞİŞİKLİĞİ
1. **Q07 tam yıl zincirini ŞİMDİ başlat** (22:00 değil). 2025-11-24 → 2026-10-14, sadece P05023, `pipeline/subset/central_valley_beta/`; 17 Haziran öncesi çiftler `quality: beta-precal`, sonrası `provisional` (her npz'de). İndirme hızı yüksek; sırayla indir-kes-sil.
2. Q01 Karapınar bitti mi kontrol et (son çift); bitmediyse önce onu bitir.
3. Q03 GCOV (6 tarih) → `data/central_valley/gcov/`.
4. **Karapınar ikinci geçiş (path 172)** provisional çiftleri → `pipeline/subset/karapinar_p172/` (PC3'ün Konya çapraz kontrolü için).
Her adımda status/PC2.md'yi güncelle (panel commit mesajını `[PC2] ...` biçiminde bekliyor).

---
# 15:05 EK İŞ (PC7 Earthdata kullanamıyor) — Q07'den önce, kısa
**Fens GCOV alt kümeleri**: `fens` bbox (-0.3, 52.4, 0.4, 52.9), 2026-06-17 sonrası provisional GCOV tarihleri (en fazla 8 tarih, mümkünse aynı path), HH ve HV gamma0 → dB, bbox kes → `pipeline/subset/fens_gcov/<YYYY-MM-DD>.npz` (`hh_db`, `hv_db`, `x`, `y`, `epsg`, `date`, `granule`, `quality`). Her dosya < 20 MB. Bitince status'ta "fens_gcov hazır" yaz (PC7 analiz edecek). Sonra Q07'ye dön.

---
# 15:50 BÜYÜK PAKET — "Handbook'un kendi örneği + Konya'nın tamamı" (PC2 tüm veri işlerini bitirdi, mükemmel. Sırayla; bitince sormadan sıradakine)
Artık sadece indirmiyorsun: PC3'ün hattını (`analysis/cumulative.py ... --data-dir <klasör>`) KENDİN çalıştırıp haritayı da üretiyorsun (PC3 dosyalarını değiştirme; gerekirse `pipeline/pc2/` altında sarmalayıcı).
Yazma alanına eklendi: `pipeline/subset/delta/` · `data/delta/` · `pipeline/subset/konya_plain/` · `data/konya_plain/` · `pipeline/subset/karapinar_fullyear/` · `data/karapinar_fullyear/` · `data/karapinar/drivers.json` · `docs/story/delta.md` · `docs/story/konya_plain.md` · `docs/story/media/pc2_*.png`.
Aynı bilgisayarda PC10 da indiriyor: aynı anda en fazla 1 dosya, ham dosyayı kesince sil, boş disk < 20 GB ise dur. Sadece provisional (≥2026-06-17) — tam yıl işi hariç (orada beta ayrı etiketli).

1. **Sacramento–San Joaquin Delta setleri (NISAR Handbook Şekil 2-4'ün kendisi!)** — Handbook §2.4'te NISAR'ın izleyeceği örnek olarak bu setlerin çökmesi gösteriliyor. Bbox yaklaşık −121.85, 37.95, −121.45, 38.20 (kontrol et). ASF'de GUNW provisional kapsama → ardışık çiftler → kes → `data/delta/` (meta, disp, points, summary). Ardından OSM'den set (levee/dike) hatları (Overpass: `man_made=dyke` veya `embankment`) ve setler boyunca çökme profili → `docs/story/delta.md` + `docs/story/media/pc2_delta.png`. Sade İngilizce 4–5 cümle: "Handbook bunu örnek verdi, biz 2026 verisiyle ölçtük."
2. **Konya Ovası'nın tamamı** — bbox 32.4, 37.4, 33.9, 38.1 (CLAUDE.md `konya`), path 108 (veya kapsamı en iyi path) provisional zincir → `data/konya_plain/`. Konya şehri ve ova genelindeki çökme alanlarını göster. `docs/story/konya_plain.md` + `docs/story/media/pc2_konya_plain.png`. Türkiye'nin "Local Impact" bölümü için en güçlü görsel bu olacak.
3. **Karapınar tam yıl** — path 7, 2025-10-17 → 2026-10-12 tam zincir (beta-precal + provisional, her npz'de doğru quality) → `pipeline/subset/karapinar_fullyear/` → `data/karapinar_fullyear/` (`quality: mixed`). Kış–yaz "dansı" Türkiye için de görülsün; PC9 kalıcı/geri dönen ayrımını buna da uygulayabilir.
4. **Karapınar sebep verisi** — SME2 toprak nemi + GCOV HV (provisional tarihler) → `data/karapinar/drivers.json` (Central Valley'deki biçimin aynısı).
5. **Sürekli:** her 30 dk `git pull`; `docs/qa/*.md` içinde veri dosyaların hakkındaki bulguları düzelt; boş kalırsa Delta için ikinci path ile çapraz kontrol.
Her dosyada push; status/PC2.md'yi `[PC2]` önekli commit'lerle güncelle.

> **16:15 CHALLENGE UYUMU:** Delta ve Konya Ovası metinlerinde "physical drivers" (A11) ve "actionable insight" (A5) birer cümleyle açık olsun: kim ne yapmalı (set bakımı önceliği, kuyu izni/izleme).

> **16:25 PC1 — KAYNAKLAR ENTEGRASYONU:** `docs/KAYNAKLAR_ANALIZI.md`'yi oku; §4'te senin satırındaki işleri mevcut işine ek olarak yap (özellikle §1 NASA Land Subsidence StoryMap çerçevesi). Kendi cümlenle özetle, link ve atıf ver.

> **18:55 PC1:** Lincoln geçti. `docs/AKSAM_PLANI.md`'deki kendi satırına geç (akşam → Pazar). Durma.

> **19:45 PC1 — TEK SIRA ARTIK BURASI:** `docs/CALISMA_HARITASI.md` içindeki kendi bölümün. Yukarıdan aşağı yap, bitince "ASLA BOŞ KALMA" döngüsü. Teslime kadar durma.

---
# 20:00 PC1 — SIRA (çalışma haritası + ek)
1. Central Valley path 114 tam yıl alt kümelerini bitir (22 çift) → ardından `analysis/cumulative.py central_valley --data-dir data/central_valley_p114_fullyear` (mixed etiket). Bitince status'a "p114_fullyear hazır" yaz (PC9 kıyaslayacak).
2. Karapınar tam yıl (`data/karapinar_fullyear/`) eksik çift kaldıysa tamamla; `summary.json` kalite notu doğru mu kontrol et.
3. Karapınar sebep verisi (`data/karapinar/drivers.json`) — çalışma haritası madde 2.
4. Konya Ovası ikinci path çapraz kontrol → `docs/qa/PC2.md`.
5. `pipeline/README.md`: her script ne yapar, hangi komutla çalışır, çıktısı nereye (Data sayfasındaki "5 adım" ile tutarlı).
6. Sonra "ASLA BOŞ KALMA" döngüsü (hata ayıklama dahil).

---
# 20:10 PC1 — ÖZGÜN KATKI O3 (sahibi sensin; `docs/OZGUN_KATKILAR.md` §O3)
Sıra: (a) çalışan indirmeyi (p114 tam yıl) bitir → (b) O3 → (c) 20:00 listesinin kalanı.
O3 "NISAR Pulse" komut satırı aracı — adım adım:
1. `pipeline/nisarpulse/` paketi: `__main__.py` (argparse), `search.py`, `fetch.py`, `process.py`, `catalog.py`. Mevcut `pipeline/*.py` ve `analysis/*.py` fonksiyonlarını import ederek sarmala, DEĞİŞTİRME.
2. Komut: `python -m pipeline.nisarpulse run --name <ad> --bbox w,s,e,n --start ... --end ... [--track N] [--quality provisional|mixed] [--dry-run] [--resume]`. Çıktı: `data/<ad>/meta.json, disp/, points.json, summary.json` (sözleşme) + `data/catalog.json` kaydı.
3. `--dry-run`: ASF araması, bulunan çift sayısı, toplam boyut, zincir boşlukları; hiçbir şey indirmez.
4. Testler (ağsız): bbox ayrıştırma, çift zinciri oluşturma (boşluk tespiti), quality etiketleme kuralı (≥2026-06-17 provisional), catalog güncellemesi → `pipeline/nisarpulse/tests/`. `python -m pytest pipeline/nisarpulse -q` geçmeli.
5. `.github/workflows/tests.yml`: push'ta sadece testler (indirme yok). PC1 izniyle `.github/` altına sadece bu dosyayı ekle; `pages.yml`'e DOKUNMA.
6. Kanıt: aracı küçük bir bölgede uçtan uca çalıştır (ör. Delta veya küçük bir Konya alt kutusu) ve komutu + süreyi `docs/story/engine.md`'ye yaz. "5 dakikada başla" bölümüyle `pipeline/nisarpulse/README.md`.
Yazma alanına eklendi: `pipeline/nisarpulse/`, `.github/workflows/tests.yml`, `docs/story/engine.md`.

---
# 20:50 PC1 — BÜYÜK GÖREV: `docs/ATLAS_PLANI.md`
Şu anki küçük işini bitir, sonra SORMADAN `docs/ATLAS_PLANI.md` içindeki kendi bölümüne geç ve yukarıdan aşağı yap. Teslime kadar durma; bitince ASLA BOŞ KALMA döngüsü (hata ayıklama dahil).


# 🌍 ATLAS FİNAL — PC2 (Paz 00:20, PC1) · plan: `docs/ATLAS_FINAL.md`
1. Kendi 5 şehrini bitir (Isfahan, Rafsanjan, Mashhad, Quetta, Delhi), her birinde "hazır" notu.
2. **NISAR vs OPERA (NASA'nın kendi çökme ürünü) çapraz kontrolü:** JPL OPERA DISP-S1 (ASF, Earthdata) ile aynı dönem ve kutuda: Central Valley (`pipeline/subset/opera_disp` varsa kullan), Houston/Katy, Eloy, Mexico City (kapsama varsa). Ortak piksellerde r, RMSE, eğim; LOS geometri farkı notu. Çıktı `data/global/opera_check.json` (`{id, r, rmse_cm, slope, n, period, note}`), `docs/story/opera_check.md`, `docs/story/media/pc2_opera_*.png`.
3. NISAR Pulse testleri ve `docs/story/engine.md` "N şehirde çalıştı" güncel kanıt.


# ♻️ SÜREKLİ KURAL (Paz 00:45, PC1)
`tasks/SUREKLI.md` zorunlu: **her 3 dakikada bir** commit → pull --rebase → push, bu dosyanın sonuna yeni bölüm var mı bak, status tek satır. Asla durma; listen biterse SUREKLI.md tablosundaki kendi sürekli işin.


# ⭐ ATLAS KUSURSUZLUK (Paz 01:00, PC1) · `docs/ATLAS_MUKEMMEL.md`
Kapsam hedefi Paz 14:00'te ≥20 şehir. Her yeni şehirde 6'lı paketin 1. parçası senin (summary/meta/points/disp); `docs/qa/ATLAS_COMPLETENESS.md`'de kendi satırların ✓ olsun.


# ➕ TAKVİYE (Paz 01:40, PC1) · tablo: `docs/qa/ATLAS_COMPLETENESS.md` (`python tools/atlas_completeness.py`)
1. Delhi'yi bitir (5/5), "hazır" notu. 2. Sonra NISAR vs OPERA (`ATLAS FİNAL` madde 2).


# 📣 GENEL EMİR (Paz 01:50, PC1) — HERKES, HEMEN
1. Elindeki işi bırakmadan **şu an yaptığın her şeyi commit et ve pushla** (yarım iş de olsa ara kayıt: `[PC2] ara kayit: <ne>`). `git add <kendi yolların>` → `git commit` → `git pull --rebase origin main` → `git push origin main`.
2. `status/PC2.md`'ye tek satır yaz: ne yapıyorsun, % kaç bitti, sıradaki ne.
3. Bundan sonra **en geç 10 dakikada bir** commit + push; 10 dk'dan uzun commit'siz kalma (uzun indirmede her çift bitince ara kayıt).
4. Sonra bu dosyadaki en son TAKVİYE / KUSURSUZLUK bölümünden devam et.


# ➕ TAKVİYE (Paz 02:05, PC1 otomatik kontrol)
1. Delhi tamam (5/5). Şimdi **NISAR vs OPERA** (`ATLAS FİNAL` madde 2): önce Central Valley (`pipeline/subset/opera_disp`), sonra Houston/Eloy/Mexico City; `data/global/opera_check.json` + `docs/story/opera_check.md`.


# ➕ TAKVİYE (Paz 02:25, PC1) — atlas 19 bölge, tamlık 86/114 (`docs/qa/ATLAS_COMPLETENESS.md`). PC4/PC5 2 saattir durmuş; eksikleri sen tamamla.
1. Kendi işlediğin şehirler için: **mashhad, delhi, quetta** → `python analysis/pc5/uncertainty_map.py` (PC5'in aracı; `--meta-file` ile, `python -m pytest -q analysis/pc5` geçmeli) → `data/global/<id>/uncertainty/{sigma_cm.png,meta.json}`; ardından PC5 biçiminde `data/global/<id>/validation_note.json` (literatür hızı + DOI, uyum notu, önerilen güven sınıfı, `"reviewed_by": "pending PC5"`). Uydurma yok; kaynak yoksa "no published rate found".
2. Sonra NISAR vs OPERA'yı tamamla (`opera_check.md`).


# 🔬 PC1 BAĞIMSIZ KONTROL SONUCU (Paz 02:55) · `docs/story/atlas_top5_check.md`
**Delhi:** 1 Eylül 2026 tarihli görüntü bozuk görünüyor (−10.0 sonra +8.1 cm). O tarihi içeren iki çifti kontrol et (iyonosfer/unwrapping), gerekirse çıkarıp yeniden hesapla, `docs/qa/PC2.md`'ye yaz.


# 🔄 YENİ ATAMA (Paz 03:05, PC1) — atlas 19 bölge, QC sonrası sıralama: 1 Konya Ovası, 2 Mashhad, 3 Central Valley, 4 Eloy, 5 Mexico City (`docs/story/atlas_top5_check.md`). Tamlık 100/114.
1. **Belirsizlik haritası (sadece harita; notu PC4 yazacak):** mashhad, delhi, quetta → `python analysis/pc5/uncertainty_map.py` → `data/global/<id>/uncertainty/`.
2. **Delhi 1 Eylül** görüntüsünü kontrol et (QC işareti), gerekirse o tarihi içeren çiftleri çıkarıp yeniden hesapla.
3. OPERA kıyası bitti mi? `opera_check.json`'u PC10'a "hazır" notuyla bildir.
