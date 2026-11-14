# PC2 QA Notları — Konya Ovası İkinci Path Çapraz Kontrolü

Tarih: 2026-11-14 · Yazar: PC2 (Memir) · Kapsam: `data/konya_plain/`, `data/karapinar/`, `data/karapinar_p172/`

## 1. Kapsama Özeti (Konya Ovası `[32.4, 37.4, 33.9, 38.1]`)

- **Ana seri (`data/konya_plain/`, Path 7 Descending, Frame 69, `provisional`):** `2026-06-26 → 2026-10-12` (8 çift, 108 gün). Ovanın tamamını %100 kapsar.
  - Tepe çökme (batı tarım kuşağı, `32.6278°E, 37.8161°N`): **`-9.60 cm` LOS** (dikey tahmin **`-12.1 cm`** @ `37.6°`, referans aralığı `[-14.0, -9.6] cm`).
- **İkinci path — ters geometri (`data/karapinar_p172/`, Path 172 Ascending, `provisional`):** Aynı tarih penceresi `2026-06-26 → 2026-10-12` (8 çift, 108 gün). Ovanın doğu/Karapınar kesimini (`[33.3, 37.6, 33.8, 37.9]`) bağımsız yükselen yörüngeden kapsar.
  - Tepe çökme (`4 km W of Yağmapınar`, `33.6733°E, 37.8393°N`): **`-6.54 cm` LOS** (dikey tahmin **`-8.8 cm`** @ `41.8°`).
- **Not (Path 108 Descending Frame 69):** `lon=[29.82, 33.42]` aralığını kapsadığı için batı (`32.63°E`) kesimini görür fakat doğudaki Karapınar (`33.53°E–33.9°E`) kesimini keser; bu nedenle ova genelinde ana seri Path 7 seçilmiştir.

## 2. Nokta ve Bölge Çapraz Kontrolü (`2026-06-26 → 2026-10-12`)

| Seri / Path | Yön | Kutu | Karapınar (`33.53°E, 37.72°N`) LOS | Bölge Tepe LOS | Dikey Tahmin |
|---|---|---|---:|---:|---:|
| `konya_plain` (Path 7) | Descending | `[32.4, 37.4, 33.9, 38.1]` | `-6.30 cm` (`p04`, `33.5251°E, 37.7218°N`) | `-9.60 cm` | `-12.1 cm` |
| `karapinar` (Path 7) | Descending | `[33.3, 37.6, 33.8, 37.9]` | `-5.93 cm` (`p01`, `33.5306°E, 37.7182°N`) | `-5.90 cm` | `-8.0 cm` |
| `karapinar_p172` (Path 172) | Ascending | `[33.3, 37.6, 33.8, 37.9]` | `-4.73 cm` (`p03`, `33.5306°E, 37.7182°N`) | `-6.54 cm` | `-8.8 cm` |

## 3. Bulgular ve Sonuç

1. **Geniş vs. dar kutu tutarlılığı (Path 7):** Aynı yörünge üzerinde geniş `konya_plain` (`-6.30 cm`) ve yerel `karapinar` (`-5.93 cm`) serileri `2 km W of Karapınar` noktasında **`0.37 cm`** farkla uyumludur.
2. **Alçalan vs. yükselen yörünge tutarlılığı (Path 7 vs. Path 172):** Bağımsız yükselen yörünge (`karapinar_p172`), aynı noktada aynı işarette (**`-4.73 cm` LOS**, fark `1.20 cm` / ~%20) güçlü çökme doğrular; fark, alçalan/yükselen bakış açısı projeksiyonu ve bağımsız referans penceresi seçiminden kaynaklanmaktadır.
3. **Veri kalitesi:** Tüm üç seri `provisional` etiketlidir; iyonosfer düzeltmesi tamdır (`ion=full`).
