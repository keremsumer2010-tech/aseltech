# GÖREV DAĞILIMI — kim, ne, nereye yazar

## 1. Ekip
| ID | Kişi | Araç | Bilgisayar / klasör | Rol |
|---|---|---|---|---|
| PC1 | Kerem (keremsumer2010-tech) | Claude | Kerem / `aseltech` | Yönetmen: görev, denetim, web sitesi, Higgsfield medya, birleştirme, yayın, sunum |
| PC2 | Memir (memir-erdogmus) | Antigravity | Memir / `aseltech` | Veri: NISAR indirme, bölge kesme |
| PC3 | Mehmet (M3hmeT1888) | Claude Code | Mehmet / `aseltech-claude` | Çökme analizi: faz→cm, kümülatif harita |
| PC4 | İbrahim (acikgozibrahim032-hub) | Antigravity | İbrahim / `aseltech` | UK görsel çifti, Karapınar obrukları, kaynaklar, kalibrasyon notu |
| PC5 | Mehmet (M3hmeT1888) | Antigravity | Mehmet / `aseltech-gemini` | Aquifer Manager oyunu, sunum metni |
| PC6 | Mehmet (M3hmeT1888) | Antigravity | Mehmet / `aseltech-gemini2` | GNSS doğrulama verisi, OSM altyapı hatları |

## 2. Sahiplik (yazma alanları)
| Yol | Sahip |
|---|---|
| `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `rules/`, `tasks/` (QUEUE sahiplenme satırı hariç), `docs/MASTER_PLAN.md`, `docs/TODAY_PLAN.md`, `docs/GOREV_DAGILIMI.md`, `docs/URUN_TANIMI.md`, `docs/DEPO_HARITASI.md`, `docs/SOZLUK.md` | PC1 |
| `web/`, `index.html` (kök), `data/catalog.json` | PC1 |
| `pipeline/`, `docs/gunw_structure.md` | PC2 |
| `analysis/`, `data/central_valley/` (meta, disp, points), `data/karapinar/` (sinkholes.geojson HARİÇ), `docs/*_checkpoint_*.png` | PC3 |
| `data/uk/`, `data/karapinar/sinkholes.geojson`, `docs/story/sources.md`, `docs/story/calibration_note.md` | PC4 |
| `game/`, `docs/story/pitch.md` | PC5 |
| `validation/`, `risk/` | PC6 |
| `status/PCx.md` | ilgili PC |
| `docs/qa_report.md` | herkes (sadece ekleme) |
| QUEUE işleri | sahiplenen PC, işin satırında yazan klasör |

## 3. Bağımlılık şeması
```
PC2 ──npz──▶ PC3 ──data/central_valley, data/karapinar──▶ PC1 (web) ──▶ GitHub Pages
PC4 ──data/uk, sinkholes.geojson, sources──────────────▶ PC1
PC5 ──game/, pitch.md──────────────────────────────────▶ PC1
PC6 ──validation/, risk/──▶ Q05 (GNSS karşılaştırma), Q06 (risk indeksi) ──▶ PC1
```
Kritik yol: **PC2 ilk GUNW → PC3 cm haritası → PC1 site**. Bu zinciri hiçbir iş geciktiremez.
Yedek: PC1 kendi bilgisayarında aynı ilk GUNW'yi arka planda indirir/açar (Kerem Earthdata `.netrc`'yi kendisi kurar). PC2 takılırsa zincir PC1'den devam eder.

## 3b. FAZ PLANI (TR saati) — "veri yokken ne yapılır?" cevabı
İlke: **Sözleşme önce.** Formatlar `rules/VERI_SOZLESMESI.md`'de sabit; herkes sahte/örnek veriyle hemen başlar, gerçek veri gelince sadece dosya değişir.
| Faz | Saat | PC1 | PC2 | PC3 | PC4 | PC5 | PC6 |
|---|---|---|---|---|---|---|---|
| 0 Hazırlık | 12:00–12:20 | Repo/denetim; Kerem Earthdata açar | Earthdata + `.netrc` + paketler | Earthdata + `.netrc` + paketler | Kurulum | Kurulum | Kurulum |
| 1 Bağımsız | 12:20–13:30 | Site iskeleti SAHTE veriyle (`web/mock/`), Higgsfield açılış; arka planda yedek GUNW indirme | İlk GUNW + `gunw_structure.md` | `insar.py` + SENTETİK testler; Karapınar kendi indirmesi | UK bulut/radar çifti (girişsiz) | Oyun | GNSS istasyonları (girişsiz) |
| ✔ 13:30 | | **GUNW açıldı mı?** Evet → Faz 2. Hayır → B planı (browse PNG) | | | | | |
| 2 Gerçek veri | 13:30–16:00 | UK çiftini siteye bağla, veri okuyucuyu gerçek yollara hazırla | 6 provisional çift, her biri gelince push | İlk 2 npz gelir gelmez kümülatif hattı çalıştır, her yeni npz'de yeniden üret | Obruk koordinatları | Oyun cilası | OSM altyapı |
| ✔ 15:30 | | **İlk gerçek cm haritası sitede mi?** | | | | | |
| 3 Birleştirme | 16:00–17:00 | Tüm veriyi bağla, oyunu göm | QUEUE Q01 | Karapınar haritası | Kaynaklar + Holme Fen | Sunum metni | QUEUE Q05 |
| 🔒 16:30 | | **ÖZELLİK DONDURMA:** yeni özellik yok, sadece hata düzeltme ve QA | | | | | |
| 4 Yayın + QA | 17:00–17:30 | GitHub Pages yayını | Siteyi telefonda test → `docs/qa_report.md` | Sitedeki sayıları kendi çıktısıyla karşılaştır | Sitedeki kaynak linklerini test et | Oyunu sitede test et | Sitedeki metinlerde yazım/İngilizce kontrolü |
| 5 Prova | 17:30+ | Sunum akışı | Demo sürücüsü provası | Soru-cevap: veri/yöntem | Soru-cevap: kaynaklar | — | — |
Gerçek veri geldikçe siteye girer; PC1 hiçbir zaman "veri bekleyerek" durmaz.

## 4. İki tarafı olan işler (teslim noktası)
| Veren → Alan | Teslim | Ne zaman | Alan taraf beklerken ne yapar |
|---|---|---|---|
| PC2 → PC3 | `docs/gunw_structure.md` | ~13:30 TR | PC3: insar.py + testler + Karapınar kendi indirmesi |
| PC2 → PC3 | `pipeline/subset/central_valley/*.npz` | 13:30–16:00, geldikçe | PC3: Karapınar haritası |
| PC3 → PC1 | `data/central_valley/*` | ~16:30 TR | PC1: sahte veriyle site |
| PC4 → PC1 | `data/uk/*`, `sinkholes.geojson` | 13:30 / 15:30 | PC1: yer tutucu |
| PC5 → PC1 | `game/index.html` | ~16:00 | PC1: oyun butonu yer tutucu |
| PC6 → Q05/Q06 | `validation/`, `risk/` | ~15:00 / 17:30 | — |

## 5. Elenen alternatifler (tekrar açma)
| Fikir | Neden elendi |
|---|---|
| Bangladeş seli / Monsoon Command | Kullanıcı ABD/UK bağlantısı istedi |
| SARlock (radar dedektif oyunu) | Kullanıcı reddetti; oyun öğesi Aquifer Manager'da |
| Orbit Operator | Bir güne sığmaz |
| Sadece iklim analizi | NISAR verisi ~1 yıl; iklim için kısa, jüri geçerlilik puanı düşer |
| Higgsfield site oluşturucu | Gerçek veri bağlamak zor, açık kaynak değil; Higgsfield sadece medya için |
| Bugün MintPy ile zaman serisi | Windows kurulum riski; bugün basit zincir toplamı, MintPy/ATBD Pazar |
| Haziran öncesi veriyi bugünkü demoya katmak | Beta (kalibrasyon öncesi); Pazar ayrı katman |
