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
