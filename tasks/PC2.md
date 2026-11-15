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


# 🔗 ENTEGRASYON (Paz 03:20, PC1) · `docs/ENTEGRASYON.md`
**Sitede görünür yap:** `data/results_registry.json`'da senin satırların: `opera_check`, `delta`, `konya_plain`, `engine`. Her birine `summary` (tek sade cümle) ve `key_number` (birim + kalite etiketi, kendi veri dosyandan) yaz, `status: ready`. Yeni sonuç üretince yeni satır ekle (aynı alanlar). Sayı uydurma yok; PC4 sayı siciliyle aynı olmalı.


# 🚀 KENDİ KENDİNİ DENETLEYEN MOTOR + OPERA AÇIKLAMASI + YENİ BÖLGELER (Paz 03:35, PC1)
Belirsizlik haritaları ve OPERA kıyası için teşekkürler. Sıradaki 3 iş atlası en çok ilerletecek olanlar:
1. **NISAR Pulse `--qc` (varsayılan açık) — motor kendi hatasını düzeltsin:** kümülatif toplama ÖNCE, her piksel serisinde her adımı komşu adımların medyanıyla karşılaştır; fark ±2 cm içinde k·12.1 cm ise (L-band tam faz döngüsü, λ/2) ve aynı bağlı bileşende piksellerin çoğunda tutarlıysa o çifte −k·12.1 cm düzeltme uygula; ardışık zıt işaretli >5 cm adım çiftini "tek tarih aykırı" say, piksellerin >%30'unda aykırıysa o tarihi düşür. Her bölge için `qc_report.json` (düzeltilen çift, düşürülen tarih, etkilenen piksel %). Sentetik yığınla ağsız testler (`pipeline/nisarpulse/tests/`). `tools/atlas_qc.py` sadece başlık noktasına bakıyor; seninki tüm piksellere bakacak. Sonra Delhi'yi `--qc` ile yeniden çalıştır; PC11'e (Pekin) ve PC10'a kullanım notu.
2. **OPERA uyumsuzluğunu açıkla (jüri soracak):** Mexico City r=0.91 iken Central Valley r=0.40, Eloy r=0.09. Sırayla test et ve `opera_check.md`'ye yaz: (a) zaman penceresi örtüşmesi (aynı tarihler mi), (b) bakış geometrisi — OPERA Sentinel-1 LOS ile NISAR sol bakış LOS farklı: ikisini de dikey tahmine çevirip (cos θ) kıyasla, (c) referans noktası hizalaması (aynı sabit noktaya göre yeniden referansla), (d) çözünürlük/ortalama (1 km bloklarda kıyasla), (e) tarım alanlarında C-band/L-band farkı (toprak nemi, bitki). Her test sonrası r, RMSE, eğim tablosu. Açıklanamıyorsa dürüstçe yaz. `results_registry.json` `opera_check` satırına özet + anahtar sayı.
3. **Yeni bölgeler (PC11'den devir; PC11 hâlâ Tahran/Pekin/Cakarta'da):** **Kerman, İran** (57.07, 30.28; literatürde >30 cm/yıl) ve **Tianjin, Çin** (117.20, 39.10). `--qc` ile, kalite standardında; "hazır" notu.
En geç 10 dk'da bir commit + push.


# ⏱️ 8 SAATLİK PLAN (Paz 04:15 → 12:15, PC1) — sonra 20:00 veri dondurmaya kadar SUREKLI
Bu bölüm, önceki bölümlerde bitmemiş işleri de kapsar ve geçerli olan TEK listedir. Blokları sırayla yap; bir blok erken biterse sıradakine geç. Her blok sonunda commit + push + status satırı. En geç 10 dk'da bir commit.
| Saat | Blok | Çıktı |
|---|---|---|
| 04:15–06:00 | **Kerman + Tianjin bitir** (sürüyor), `--qc` ile, kalite standardı; "hazır" notu | `data/global/{kerman,tianjin}/` |
| 06:00–08:00 | **NISAR Pulse `--qc` motoru** (önceki bölüm madde 1; başlamadıysan şimdi): piksel düzeyinde faz döngüsü düzeltme + aykırı tarih atma, `qc_report.json`, ağsız testler; **Delhi'yi `--qc` ile yeniden çalıştır** | `pipeline/nisarpulse/qc.py` + testler, `data/global/delhi/qc_report.json` |
| 08:00–09:30 | **Tek komutla yeniden üretilebilirlik:** `python -m pipeline.nisarpulse reproduce <id>` — bölgenin `meta.json` granül listesinden aynı summary'yi yeniden üretir; README'ye "atlası yeniden üret" bölümü; GitHub Actions'ta ağsız `--dry-run` testi | `pipeline/nisarpulse/reproduce.py`, `docs/story/engine.md` güncel |
| 09:30–11:00 | **Yeni bölgeler (PC11'den devir):** **Celaya, Meksika** (−100.81, 20.52) ve **Hamadan–Kabudarahang, İran** (48.72, 35.21; önce kapsama + literatür) | `data/global/{celaya,kabudarahang}/` |
| 11:00–12:15 | **OPERA ek kıyası:** PC9 Houston'ı bitirince Houston için de OPERA; `opera_check.json` + md güncel; `results_registry` `opera_check` ve `engine` satırları güncel sayılarla | — |
| 12:15–20:00 | SUREKLI: yeni bölge adayları (kaynaklı), motor testleri, QC işaretli bölgeleri `--qc` ile yeniden işleme önerisi | — |


# 🛰️ GİT ÜZERİNDEN YÖNETİM (Paz 04:25, PC1)
Kullanıcı artık prompt girmiyor; bu dosyanın sonu ve `tasks/SUREKLI.md` senin tek emir kaynağın. 8 saatlik planın biterse `tasks/BACKLOG_ORTAK.md`'den satır al (`[~PCx]` → commit+push → yap → `[x PCx]`). Onay bekleme, soru sorma; karar gerektiren durumda en makul seçeneği uygula ve gerekçesini `docs/qa/PCx.md`'ye yaz.


# ⏳ PLAN SONU SİNYALİ (Paz 04:35, PC1)
Son bloğa geldiğinde `status/PC2.md` ilk satırına `PLAN_SONU_YAKIN` yaz, pushla. PC1 20 dk içinde bu dosyanın sonuna yeni 6–8 saatlik plan ekler; o arada `tasks/BACKLOG_ORTAK.md`. Teslime (Paz 22:00) kadar durmak yok.


# ▶ DEVAM (PC1 otomatik kontrol, Paz kontrol 1)
43 dk commit yok. 8 SAATLİK PLAN'da kaldığın bloktan devam et; uzun iş sürüyorsa ara kayıt commit'i at ve `status/PC2.md`'ye hangi blokta olduğunu yaz. Planın son bloğundaysan ilk satıra `PLAN_SONU_YAKIN` yaz.


# 🔁 DEVİR (PC1 otomatik kontrol 2)
PC6 (site) ve PC8 (bülten/teslim) durmuş sayıldı. Kerman bittikten ve `--qc` motorundan SONRA, Celaya'dan ÖNCE:
1. **Bültenler + vital_signs:** `python tools/bulletin.py` ile yeni bölgelerin bültenlerini üret (Kashmar, Kerman, Tianjin, Gorgan, Pekalongan), indeks; `vital_signs.json`'u atlas.json'dan güncelle (fastest = güvenilir bölgelerden). `python -m pytest -q` geçmeli.
2. **Site son QA (yarım saat):** canlı sitede her sayfa konsol 0 hata, kırık link 0 (atlas, science, data, game); bulgu + düzeltme `docs/qa/PC2.md` (web/ dosyalarında yalnız açık hata düzeltmesi).


# ▶ DEVAM (PC1 otomatik kontrol 3)
31 dk commit yok. Kerman'ın kalan çiftlerinde ara kayıt commit'i at; sonra `--qc` motoru, ardından devralınan bülten + site QA. Status'a blok yaz.


# ▶ NOT (PC1 otomatik kontrol 4)
50 dk commit yok; 60 dk'yı geçersen işlerin devredilecek. Ara kayıt at. Ek: `vital_signs.json` hâlâ 21 şehir sayıyor — bülten/vital_signs devrinde 27 bölgeye güncelle (yeni bölgelerin exposure satırlarıyla).


# ⛔ DURMUŞ SAYILDI (PC1 otomatik kontrol 5)
70 dk commit yok. Bültenler + vital_signs PC1 tarafından yapıldı (27 bölge). `--qc` motoru, Celaya, Kabudarahang ve site QA `tasks/BACKLOG_ORTAK.md` §E'ye taşındı. Dönersen oradan kendi işlerini geri al (`[~PC2]`).


# 🏁 FİNAL — TOPLAMA VE BİRLEŞTİRME (PC1, Paz 11:15 TR) · önce `docs/JURI_3DK.md`'yi oku
Jüri siteyi 3 dakika inceleyecek. Yeni veri/özellik yok; toparla, sadeleştir, tutarlı yap. Ana sayfayı PC1 kuruyor. Bu bölüm önceki tüm planların ÜSTÜNDEDİR. Her blok sonunda commit + push (önce kendi dosyaların → pull --rebase → push), status satırı. Veri dondurma 20:00, teslim 22:00.
**Rol: "tek komutla yeniden üret" kanıtı.**
1. (11:15–13:00) **`python -m pipeline.nisarpulse reproduce <id>`:** bölgenin `meta.json` granül listesinden aynı summary'yi yeniden üretir (önbellekteki kesitlerle çalışabilsin, yoksa `--dry-run` planı yazsın); `pipeline/nisarpulse/tests/test_reproduce.py` (ağsız).
2. (13:00–14:00) **Kanıt kaydı:** Konya Ovası ve Mashhad için `reproduce` çıktısı summary'yle birebir mi (fark tablosu) → `docs/story/engine.md`'ye "Reproduce any atlas region in one command" bölümü (komut + beklenen çıktı + süre).
3. (14:00–15:30) **Delhi `--qc`:** motorla 1 Eylül aykırısını temizleyip yeniden hesapla (motor yoksa o tarihi içeren çiftleri çıkar); "hazır: delhi".
4. (15:30–17:00) README ve Data sayfası için 6 satırlık "Run it yourself" kutusu metni (PC1/PC6'ya `docs/qa/PC2.md`'de).


# ▶ DEVAM (PC1 otomatik kontrol)
33 dk commit yok. Final listende kaldığın yerden devam et; uzun iş sürüyorsa ara kayıt at. Veri dondurma 20:00.


# ▶ DEVAM (PC1, 12:30)
34 dk commit yok. `tasks/BACKLOG_ORTAK.md`'den boş bir satırı `[~PC2]` ile al (17 boş var) ya da Delhi `--qc` sonucunu atlas notuna işle. Push öncesi `python tools/check_site.py && python -m pytest -q`.


# ▶ DEVAM — son uyarı (PC1, 12:55)
54 dk commit yok. 60 dk'yı geçersen durmuş sayılırsın. Ortak listeden bir satır al.
