---
type: mimari
status: acik
date: 2026-11-14
owner: PC1
---

# Sözlük

Projede geçen, dışarıdan gelen birinin bilmesi mümkün olmayan terimler. Konuya göre sıralı.

## Uydu ve radar

| Terim | Ne demek |
|---|---|
| **NISAR** | NASA-ISRO Synthetic Aperture Radar. Temmuz 2025'te fırlatıldı. L-band (~24 cm; tam değer ürünün centerFrequency alanından, ör. 1239 MHz → 24.2 cm) ve S-band |
| **SAR** | Sentetik açıklıklı radar. Kendi sinyalini gönderir; bulut, duman, gece fark etmez |
| **L-band** | ~24 cm dalga boyu. Bitki örtüsünden geçer, tarım alanlarında koherensi C-band'den iyi korur |
| **Backscatter** | Yüzeyden geri dönen sinyal gücü. Pürüzlülük ve nemle değişir |
| **Polarizasyon (HH, HV)** | Gönderilen/alınan dalganın yönü. HV bitki örtüsüne duyarlı |
| **Path / frame / track** | Uydunun geçtiği yörünge şeridi. Aynı path'in çekimleri karşılaştırılır |
| **Revisit** | Aynı yere tekrar uğrama süresi, NISAR'da ~12 gün |

## Ürünler

| Terim | Ne demek |
|---|---|
| **GUNW** | Geocoded Unwrapped Interferogram. İki tarih arasındaki yer hareketini veren ürün. 80 m UTM ızgara |
| **GCOV** | Geocoded Covariance. Radar parlaklık görüntüsü (gamma0, arazi düzeltmeli) |
| **SME2** | Toprak nemi ürünü (Level-3) |
| **Browse PNG** | Ürünün küçük önizleme resmi. Girişsiz iner. **Nicel değil** (`preview`) |
| **CRID** | Composite Release ID; ürün sürümü. PROVISIONAL = `P05023` |
| **PROVISIONAL** | Kalibre edilmiş, kısmen doğrulanmış ürünler; 2026-06-17 ve sonrası çekimler |
| **BETA / pre-calibration** | Kalibrasyon öncesi yayınlanan eski ürünler (Ekim 2025-Ocak 2026 alt kümesi) |
| **ASF DAAC** | Alaska Satellite Facility; NASA'nın SAR arşivi. Arama: Vertex, `asf_search` |
| **Earthdata** | NASA hesap sistemi. `.h5` indirmek için gerekir |

## InSAR (yer hareketi ölçümü)

| Terim | Ne demek |
|---|---|
| **Interferogram** | İki çekim arasındaki faz farkı. Yer hareketi faz farkı olarak görünür |
| **Faz (wrapped / unwrapped)** | Wrapped: -π..π arası tekrar eden halkalar. Unwrapped: halkalar açılmış, sürekli değer. Biz unwrapped kullanırız |
| **Faz → cm** | LOS = −λ/(4π) × unwrapped phase. İşaret ürün dokümanından doğrulanır |
| **LOS** | Line of sight. Uydu eğik baktığı için ölçülen hareket eğik doğrultuda. Dikeye çevirmek için incidence açısı gerekir (yaklaşım: dikey ≈ LOS / cos(incidence), yatay hareket ihmal) |
| **Incidence açısı** | Radar ışınının yere geliş açısı. GUNW metadata cube'unda var |
| **Coherence** | 0-1 arası güvenilirlik. Düşükse (su, değişen tarla) faz anlamsız. Eşik ~0.3 ile maskelenir |
| **Referans noktası** | InSAR göreli ölçer. Hareketsiz kabul edilen bir bölge 0 alınır; her çift aynı referansa göre sıfırlanır |
| **Zincir toplamı** | Ardışık çiftleri (t1→t2, t2→t3 …) toplayarak kümülatif hareket elde etme. Boşluk varsa zincir kopar |
| **Unwrapping hatası** | 2π'nin katı kadar sıçrama. Zincirde birikir; düşük koherenslı bölgelerde sık |
| **MintPy** | Resmi ATBD'nin kullandığı zaman serisi aracı. Windows'ta kurulmazsa WSL / OpenSARLab |
| **Subsidence** | Çökme. Central Valley'de yeraltı suyu pompalamasıyla akifer sıkışır |
| **Kalıcı / geri dönen** | Kil katmanları sıkışınca geri dönmez (kalıcı); kum-çakıl katmanlar su gelince kısmen kalkar (mevsimsel) |

## Doğrulama ve altyapı

| Terim | Ne demek |
|---|---|
| **GNSS / GPS istasyonu** | Yerde sabit, mm hassasiyetle konum ölçen istasyon. InSAR'ı bağımsız doğrulamak için |
| **NGL** | Nevada Geodetic Laboratory; açık GNSS zaman serileri (geodesy.unr.edu) |
| **RMSE** | InSAR ile GNSS arasındaki ortalama fark (cm) |
| **Diferansiyel çökme** | Kısa mesafede farklı miktarda çökme. Kanal ve yollara zarar veren budur (mm/km) |
| **OSM / Overpass** | OpenStreetMap ve sorgu API'si. Lisans: © OpenStreetMap contributors, ODbL |

## Süreç

| Terim | Ne demek |
|---|---|
| **PC1-PC6** | Ajan kimlikleri. Tablo: `docs/GOREV_DAGILIMI.md` §1 |
| **BLOCKED** | Status dosyasındaki dur sinyali. Ajan tahmin etmez, bekler |
| **K-NN** | Kural numarası (`rules/RULES.md`) |
| **E-NN** | Hata kaydı numarası (`rules/RULES.md` §9) |
| **quality** | Veri sınıfı etiketi: provisional / beta-precal / mixed / preview |
