---
type: gorev
id: PC3
owner: Mehmet (M3hmeT1888)
tool: Claude Code
folder: aseltech-claude
status: acik
date: 2026-11-14
depends_on: [PC2]
feeds: [PC1, PC5, PC6]
---

# PC3 · Çökme analizi: faz → santim

> **Saat saat sıra ve iş bitince sıradaki iş: `docs/ZAMAN_CIZELGESI.md`.** Atanmış QUEUE işlerin orada.

> **PC1 14:15:** PC5 çalışmıyor; işlerini sen yürütüyorsun (decompose.py için teşekkürler). Yeni sıra:
> 1) **`docs/story/game_model.md`** (tasks/PC5.md 14:10 paketi madde 1) — PC6'nın oyunu bunu bekliyor, 45 dk içinde bitir.
> 2) Q21 path 114 → 3) Q22 → 4) belirsizlik bütçesi (PC5 Görev 2) → 5) Q26/Q27. PC5'in yazma alanı (`analysis/decomp/`, `docs/story/uncertainty.md`, `docs/story/game_model.md`) artık senin de.

> **15:45 PC1:** Site işini (tasks/PC9.md'nin eski 11 maddesi, git geçmişinde `f045994`) sen yürütüyorsun — devam et, artık `web/` (panel.html hariç) ve `data/catalog.json` resmen SENİN. Tam yıl analizi (Q08) PC9'a geçti; sen siteye odaklan. PC9'un `docs/story/fullyear.md`, PC8'in `docs/story/uk_findings.md`, PC10'un `docs/story/global_showcase.md`, PC5'in `key_findings_public.md` dosyaları geldikçe siteye bağla.

## Kimlik
Mehmet'in bilgisayarı, **`aseltech-claude`** klasörü, Claude Code. Aynı bilgisayarda PC5 ve PC6 da çalışıyor;
onların klasörlerine (`aseltech-gemini`, `aseltech-gemini2`) dokunma.

## Yazma alanın
`analysis/` (kod, test, `out/`) · `data/<site>/{meta,points,summary,decomp}.json` · `data/<site>/disp/` ·
`data/*_fullyear/` · `docs/karapinar_checkpoint_cm.png` · `status/PC3.md`

**Dikkat:** `data/karapinar/sinkholes.geojson` PC4'ün. Script'in `data/karapinar/` klasörünü silmez, temizlemez.

## Başlamadan
- [ ] `rules/RULES.md` (özellikle §5 bilimsel doğruluk) ve `rules/VERI_SOZLESMESI.md` tamamı okundu
- [ ] PC2 ile aynı anda büyük indirme yapma (aynı internet değil ama aynı bilgisayarda PC6 da indirebilir; sırayla)

---

## Görev 1 · Dönüşüm modülü ve kontrol haritası (12:00-14:00)

1. Earthdata hesabı (şifreyi insan girer), `.netrc`. `pip install asf_search h5py numpy matplotlib pytest`
2. `analysis/insar.py`:
   - `phase_to_cm(unw, wavelength_m)` → LOS cm
   - `mask_coherence(arr, coh, thr=0.3)` → düşük koherens NaN
   - `reference(arr, ref_rc, radius=3)` → referans penceresinin medyanını çıkar
   - `los_to_vertical(cm, incidence_deg)` → yaklaşım: `cm / cos(incidence)`
   - İşaret konvansiyonunu ürün dokümanından veya https://github.com/nisar-solid/ATBD kodundan **doğrula**, satır ve link yorum olarak yaz.
3. `analysis/test_insar.py`: bilinen girdi → bilinen çıktı (örn. 2π faz = λ/2 = 11.92 cm büyüklük; işaret testi; NaN maskesi; referans sonrası referans pikseli 0).
   `pytest -q` geçmeli; **çıktı status'a yapıştırılır** (K-1).
4. Karapınar: GUNW path 7, **2026-09-18 → 09-30** çifti → `docs/karapinar_checkpoint_cm.png` (renk çubuğu, cm, başlıkta tarih ve `PROVISIONAL`).

**Bitti sayılır eğer:** pytest çıktısı status'ta; kontrol haritası makul aralıkta (tek çiftte genelde birkaç cm altı) ve push edildi.

## Görev 2 · Central Valley kümülatif (PC2 npz geldikçe, 14:00-17:00)

`analysis/cumulative.py central_valley`:
1. `pipeline/subset/central_valley/*.npz` → tarih sırası; **zincirde boşluk varsa dur ve status'a yaz.**
2. Her çift: cm'e çevir → koherens maskesi → **aynı referans penceresine göre sıfırla** → topla.
3. Referans bölgesi: az hareketli, yüksek koherensli (örn. vadi kenarındaki sert kaya / tepe eteği). Seçimi ve gerekçesini status'a yaz.
4. Çıktılar (`rules/VERI_SOZLESMESI.md` §4):
   - `data/central_valley/meta.json` (`quality: "provisional"`, `quality_note`)
   - `data/central_valley/disp/<date>.png`: şeffaf arka plan, bbox'a oturur, **vmin/vmax tüm tarihlerde sabit**
   - `data/central_valley/points.json`: 10-15 nokta (en çok çöken 5, orta 5, referans yakını 2; isimleri yakın yer adından)
   - `data/central_valley/summary.json`: maks çökme, dönem, yıllık hız tahmini (`estimate`), referans
   - `analysis/out/central_valley_cum.npz` (PC6 için sayısal ızgara)
5. **Literatür kıyası:** USGS/JPL'nin Central Valley çökme hızlarıyla mertebe kontrolü, kaynak linkiyle status'a. Mertebe tutmuyorsa yayınlama, BLOCKED.

"Kalibre ettik" deme; ürünü NISAR projesinin işlediği hâliyle kullandığımızı yaz.

**Bitti sayılır eğer:** PNG'ler açılıp gözle kontrol edildi (işaret: çöken yer çöken renkte), JSON'lar parse ediliyor, literatür kıyası status'ta, push edildi.

## Görev 3 · Karapınar (zaman kalırsa bugün, yoksa Pazar)
Aynı hat → `data/karapinar/{meta,points,summary}.json`, `disp/`.

## Pazar
Tam yıl (`beta-precal` dahil) → **ayrı** `data/central_valley_fullyear/` + `quality: "mixed"`.
Kalıcı/geri dönen ayrımı orada (trend + mevsimsel genlik) → `decomp.json`. Kış verisi yetersizse dürüstçe yaz.

---

## En kritik iş
İşaret ve referans. Yanlış işaret = "yer yükseliyor" diyen harita. Farklı referanslı çiftleri toplamak = anlamsız kümülatif.

## B planı
- PC2 npz'leri 15:30'a kadar gelmezse: Karapınar kontrol çiftini tek başına `data/karapinar/` olarak yayınla (tek tarih).
- Unwrapping sıçramaları çoksa: koherens eşiğini 0.4'e çıkar, maskelenen oranı status'a yaz.

## Yapma
- Beta ile provisional'ı aynı toplamda kullanma.
- Sayı uydurma; ölçemediğini `estimate` diye işaretle.

## Rapor
`status/PC3.md`: maks çökme (cm, hangi nokta), referans noktası ve gerekçesi, kullanılan çift sayısı, pytest çıktısı, literatür kıyası, `AI:` satırı.

---
# 14:10 YENİ PAKET (öncelik sırası)
1. **Q21 ikinci geçiş (path 114) doğrulaması** — en güçlü kanıt. Provisional ardışık çiftler, aynı hat, aynı referans bölgesi mantığı; path 34 ile ortak tarih aralığında nokta nokta fark + korelasyon + saçılım grafiği PNG (`docs/cv_p34_vs_p114.png`). Sonuç ve yorum `docs/qa/PC3.md`.
2. **Q22 dikey/doğu-batı ayrıştırması** (iki geçiş farklı bakış yönündeyse) → `data/central_valley/vertical.json` + PNG. Değilse neden yapılamadığını yaz.
3. **Referans duyarlılığı raporu**: 3 farklı referans bölgesiyle maks çökme aralığı (−6.2…−7.8 bulmuşsun) → summary.json'a `range_cm` ve `method_note`'a ekle.
4. **Karapınar ↔ obruk**: PC6'nın Q28'ine girdi olacak `analysis/out/karapinar_cum.npz` (sözleşme §5 biçimi) hazır mı kontrol et, değilse üret.
5. **Pazar hazırlığı**: Q08 için `analysis/decomp` (PC5) arayüzünü oku, tam yıl zinciri gelince tek komutla çalışacak `analysis/run_fullyear.py` iskeletini yaz (beta/mixed ayrı klasör kuralıyla).

---
# 15:00 SIRA
1. Q21'i bitir (path 114 ↔ 34) → sonuç `docs/qa/PC3.md` + `data/central_valley_p114/` + `docs/cv_p34_vs_p114.png`. PC1 siteye "independent second track" kutusu ekleyecek: kısa İngilizce özet cümlesini status'a yaz.
2. Q22 dikey/doğu-batı.
3. PC2 Q07 npz'leri geldikçe: `data/central_valley_fullyear/` (mixed) kümülatif + Q08 kalıcı/geri dönen (`analysis/decomp/run_decomp.py`). beta ve provisional ayrı etiketli.
4. PC2 path 172 gelince Karapınar çapraz kontrolü (Q21'in Konya versiyonu).

---
# 16:15 CHALLENGE UYUMU (docs/CHALLENGE_UYUM.md) — site için yeni işler (sırayla)
1. **A3 Explorer/dashboard sayfası** → `web/explorer.html`: bölge seç (Central Valley, Karapınar, Konya Ovası, Delta, UK, küresel şehirler — `data/catalog.json`'dan), katman seç (çökme, belirsizlik, risk, GCOV HV), tarih kaydırıcı, haritaya tıkla → o noktanın zaman serisi + o tarihteki değer. Menüye "Explore" ekle.
2. **A5 "Who can use this"** bölümü (ana sayfa, simülatörden önce): 5 kart — Scientists (veri + yöntem indir), Water & canal managers (risk listesi), Educators (simülatör + ders planı `docs/story/lesson_plan.md`), Decision-makers (anahtar bulgular), Public (hikâye). Metinler PC4'ten.
3. **A13 "What NISAR can do next"** bölümü (sona doğru): PC4'ün `docs/story/future_applications.md` dosyasından.
4. **A7/B6 "Why Konya matters to us"** kutusu (Konya bölümünde): PC4'ün `docs/story/team_story.md` taslağından (ekip onaylayınca).
5. **A12 polarizasyon paneli**: PC7'nin `data/fens/crops.json` ve `docs/story/polarization.md` sonuçlarıyla UK bölümüne "HH vs HV" küçük grafik + 1 cümle (pürüzlülük/dielektrik).
6. **B1/B3 kutuları**: PC5'in Sentinel-1 (C-band) karşılaştırması ve PC8'in nüfus/ürün maruziyeti sonuçlarını ilgili bölümlere bağla.
7. **C. Learn more**: Science sayfası sonuna challenge Resources bağlantıları (PC4 listesi).
8. Yeni veriler: PC2 Delta/Konya Ovası, PC9 tam yıl, PC10 küresel şehirler geldikçe bağla.

> **16:25 PC1 — KAYNAKLAR ENTEGRASYONU:** `docs/KAYNAKLAR_ANALIZI.md`'yi oku; §4'te senin satırındaki işleri mevcut işine ek olarak yap (özellikle §1 NASA Land Subsidence StoryMap çerçevesi). Kendi cümlenle özetle, link ve atıf ver.

> **18:55 PC1:** Lincoln geçti. `docs/AKSAM_PLANI.md`'deki kendi satırına geç (akşam → Pazar). Durma.

> **19:45 PC1 — TEK SIRA ARTIK BURASI:** `docs/CALISMA_HARITASI.md` içindeki kendi bölümün. Yukarıdan aşağı yap, bitince "ASLA BOŞ KALMA" döngüsü. Teslime kadar durma.

> **20:10 PC1:** `docs/OZGUN_KATKILAR.md` — O1 (PC8), O2 (PC7), O3 (PC2) ve teknik not (PC4) hazır oldukça siteye bağla: ana sayfaya "What is new in our work" 3 kart, Science'a O1/O2 bölümleri, Data'ya `nisarpulse` kurulumu, teknik not bağlantısı.

---
# 20:50 PC1 — BÜYÜK GÖREV: `docs/ATLAS_PLANI.md`
Şu anki küçük işini bitir, sonra SORMADAN `docs/ATLAS_PLANI.md` içindeki kendi bölümüne geç ve yukarıdan aşağı yap. Teslime kadar durma; bitince ASLA BOŞ KALMA döngüsü (hata ayıklama dahil).
