# CHALLENGE "RESOURCES" SEKMESİ — kaynak kaynak analiz ve entegrasyon (PC1, 16:25)
Her kaynak PC1 tarafından açıldı/okundu. "Nasıl kullanıyoruz" sütunu bağlayıcıdır; sorumlu PC kendi dosyasına işler. Alıntı yapma, kendi cümlenle özetle ve link ver.

## 1. En önemli bulgu: NASA'nın kendi "Land Subsidence" StoryMap'i bizim konumuz
- **NISAR StoryMaps → Land Subsidence**: https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828
  Atıf: Peacock, A., An, K., Pinto, N., & Lou, Y. (2024). NISAR ArcGIS Storymaps. Zenodo. https://doi.org/10.5281/zenodo.10818833
- İçerik (özet): yeraltı suyu pompalamasıyla çökme küresel bir sorun; **örnek vaka California Central Valley ve California Aqueduct** — UAVSAR (havadan L-band radar) ile 2013–2017 arasında su kanalı boyunca "subsidence bowl", bazı yerlerde 40 inçten fazla çökme (Miller et al. 2020; Jones et al. 2020). **Mexico City** de örnek olarak geçiyor. StoryMap, SAR'ın pompalama ayarı ve kanal güçlendirme önceliği için karar destek olabileceğini söylüyor.
- **Bizim çerçevemiz (herkes kullanacak):** "NASA's NISAR StoryMap showed the Central Valley subsidence bowl with airborne radar (2013–2017). We measured the same valley — and the same aqueduct — from space with NISAR in 2026, checked it against GPS, and ranked the canal and road segments at risk." Bu, jüriye projenin NASA'nın kendi anlatısının 2026 güncellemesi olduğunu gösterir.

## 2. NISAR Applications White Papers (https://science.nasa.gov/mission/nisar/societal-benefits/) — bizimle ilgili 6 tanesi
| White paper | Ana fikir (özet) | Nerede kullanıyoruz | Sorumlu |
|---|---|---|---|
| Subsidence (PDF: NISAR_Applications_Subsidence.pdf) | Çökme yavaş ve göze görünmez; hasar ortaya çıkana kadar fark edilmez; uzaydan radar erken tespit sağlar | "Why monitor" cümlesi; future_applications | PC4, PC3 |
| Drought and Groundwater Withdrawal | Kuraklık → yüzey suyu azalır → pompalama artar → çökme altyapıyı etkiler | Hikâyenin sebep zinciri; drivers_analysis | PC5, PC4 |
| Levees and Dams | Setlerin denetimi çoğunlukla gözle/yerinde; NISAR hareket ve sızıntı için erken uyarı | Delta setleri bölümü | PC2 |
| Sinkholes and Cavern Collapse | Çözünebilir kayaçta (kireçtaşı) obruk oluşumu; yavaş veya ani çöküş; radarla öncül hareket | Karapınar bölümü (tahmin iddiası yok) | PC2, PC5 |
| Food Security (Crop Area Monitoring) | NISAR iki haftada bir, havadan bağımsız ekin alanı haritası | Fens polarizasyon/ekin ritmi | PC7 |
| Soil Moisture and Water Resources | Radar toprak nemine duyarlı (dielektrik) | SME2 sebep analizi | PC5 |
PDF'ler: `https://assets.science.nasa.gov/content/dam/science/missions/nisar/nisar-jpl/pdf/NISAR_Applications_<Ad>.pdf` (Subsidence, Drought_and_Groundwater_Withdrawal1, Levees_and_Dams1, Sinkholes1, Food_Security1).

## 3. Diğer kaynaklar
| Kaynak | Ne | Nasıl kullanıyoruz | Sorumlu |
|---|---|---|---|
| NISAR Data User Guide (https://nisar-docs.asf.alaska.edu/) | Ürün yapıları, GUNW katmanları, düzeltmeler | Science sayfası yöntem atıfları (iyonosfer ekranı uygulanmamış notu vb.) | PC3, PC4 |
| ASF Vertex (https://search.asf.alaska.edu/) · NASA Earthdata Search | Veri arama/indirme | Data sayfasına "Reproduce our data in 5 steps" (platform=NISAR, GUNW, bbox, tarih, P05023) | PC3 + PC4 metin |
| Intro to SAR (https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar) | Dalga boyu, polarizasyon, saçılma mekanizmaları | Polarizasyon paneli ve sözlük cümleleri; "Learn more" | PC7, PC4 |
| Intro to Remote Sensing | Aktif/pasif algılama temelleri | "Learn more" + ders planı | PC4 |
| NASA ARSET Trainings (https://appliedsciences.nasa.gov/get-involved/training) | SAR/NISAR eğitimleri (İngilizce ve İspanyolca) | Eğitimciler kartı + lesson_plan "further learning" | PC4 |
| UAVSAR Postcards (https://uavsar.jpl.nasa.gov/education/postcards.html) | Havadan L-band radar yanlış renk örnekleri | "Learn more"; StoryMap'teki UAVSAR çalışmasıyla bağ | PC4 |
| CSA SAR Python Tutorial (https://github.com/asc-csa/Synthetic_Aperture_Radar_Tutorial) | Python/QGIS ile SAR | README "further learning" | PC4 |
| RCM / RADARSAT-1 (C-band, Kanada) · SAOCOM (L-band, Arjantin) | Diğer SAR görevleri | B1 "farklı frekans": cross_sensor.md'de NISAR L-band ile C-band (Sentinel-1/RCM) ve diğer L-band (SAOCOM) farkı 2–3 cümle | PC5 |

## 4. Somut entegrasyon listesi (PC'ler kendi görev dosyalarındaki 16:25 notuna göre yapacak)
- PC3 (site): Chapter 3'e "NASA StoryMap → 2026 NISAR" kutusu + atıf; Data sayfasına "Reproduce in 5 steps"; Science sonuna "Learn more (challenge resources)"; FAQ'e "How does this relate to NASA's StoryMap?".
- PC4: sources.md'ye 1–3. bölümlerin tamamı (doğrulanmış); project_page/pitch'e StoryMap çerçevesi; audiences/lesson_plan'e ARSET + Intro to SAR.
- PC5: literature_comparison'a StoryMap/Miller 2020/Jones 2020 (UAVSAR aqueduct) satırı; drivers_analysis'e Drought white paper; cross_sensor'a RCM/SAOCOM notu.
- PC6: risk_dossier'de California Aqueduct satırına UAVSAR 2013–2017 kıyası (kaynaklı, büyüklük mertebesi); oyunda "Sources" sekmesine StoryMap + white papers.
- PC2: delta.md ← Levees and Dams; konya_plain/Karapınar ← Sinkholes white paper.
- PC7: polarization.md ← Food Security + Intro to SAR.
- PC10: Mexico City ← StoryMap'teki Mexico City örneği.
