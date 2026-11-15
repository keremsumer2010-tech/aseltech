# NASA Space Apps 2026 — Başvuru Formu Türkçe Kopyası (`docs/story/submission_form_tr.md`)

**Sahibi:** PC4 · **Kaynak:** [`docs/story/submission_form.md`](submission_form.md) · **Amaç:** Kerem formu doldururken birebir Türkçe referans.

---

## Proje Adı & Kısa Özet
- **Kısa Başlık:** `NISAR Vision: Tracking Land Subsidence from Space`
- **Tam Başlık:** `NISAR Vision — Follow the Water: Tracking Silent Land Subsidence with L-Band SAR`
- **Ultra Kısa Özet (`141 / 150 karakter`):** NISAR radarından kendi kendini denetleyen küresel çökme atlası: 29 havza, tek açık hat, aynı 93 gün, her sayı dosyasına izlenebilir.
- **Standart Özet (`282 / 500 karakter`):** NASA-ISRO NISAR radar verisinin ilk aylarını kendi kendini denetleyen bir küresel çökme atlasına dönüştürdük: aynı 93 günde tek açık işlem hattıyla ölçülen 29 havza, dosyasına kadar izlenebilen her sayı ve GPS, NASA OPERA ürünü ile literatüre karşı denetlenmiş her manşet.

---

## 6 Temel Space Apps Sorusu (Ana Sayfadaki 9 İşe Göre)

### 1. Ne yapar? (What does it do?)
NISAR Vision, NASA-ISRO NISAR L-bant radar verisinin (24 cm dalga boyu; NASA-JPL ve ISRO tarafından fazı açılmış Level-2 GUNW ürünleri) ilk aylarını aynı 93 günlük ortak pencerede (`2026-06-28` – `2026-09-29`) 29 havzayı kapsayan kendi kendini denetleyen küresel bir yer çökmesi atlasına dönüştürür:
- **01 Küresel Atlas:** 29 havzayı tek açık işlem hattıyla ölçer (16 havza kalite kontrolünden geçer, 13 havza yalnızca gösterge niteliğindedir; en hızlısı Konya Ovası `-11.0 cm/100 gün`).
- **02 Kendi Hatamızı Yakalayan QC:** Otomatik zaman serisi kontrolleri Semarang'daki `12.1 cm`'lik tam L-bant faz döngüsü sıçramasını (`-12.1` → `-6.2 cm`) ve Tahran (`-3.5` → `-7.4 cm` LOS) ile Pekin'deki havza dışı referans sapmasını yakaladı.
- **03 GPS Doğrulaması:** Ana ölçüm uydu görüş hattıdır (LOS); dikey değer tahmindir. Kaliforniya dikey tahminleri 10 sürekli Nevada Geodetic Laboratory GPS istasyonuyla `r = 0.924` (medyan RMSE `1.00 cm`) uyum gösterir. İkincil OPERA kontrolü Mexico City'de 10 noktada `r = 0.912` verir, ancak OPERA kış / NISAR yaz dönemini kapsar (Central Valley `r = 0.40`, Eloy `r = 0.09`).
- **04 Etkilenen İnsan:** Yer değiştirmeyi GHSL GHS-POP E2025 (`100 m`) ile kesiştirerek 108 günde `-5 cm`'den hızlı çöken `511.65 km²` alanda `1.200.716` (`1.20 M`) kişinin yaşadığını hesaplar.
- **05 Kalıcı Su Kaybı:** Mevsimsel esnemeyi kalıcı kil sıkışmasından ayırarak Central Valley'de yılda `0.3174 km³/yıl` (`~0.32 km³/yıl`) kalıcı akifer depolama kaybını hesaplar.
- **06 Altyapı Ön Taraması:** Diferansiyel eğim taraması 645 kanal, yol ve demiryolu koridorunun 81'ini (`> 10 mm/km`) işaretler — bu bir ön tarama indeksidir, yapısal güvenlik değerlendirmesi DEĞİLDİR.
- **07 Erken Uyarı Bültenleri:** `tools/bulletin.py` ile A4 baskıya hazır 29 bölgesel izleme bülteni (`docs/bulletins/`) üretir.
- **08 Yeraltı Suyu Simülatörü:** Terra Bella hızlarına kalibre edilmiş 24 aylık etkileşimli Terzaghi sıkışma simülatörü (`game/`).
- **09 Açık Motor:** Copernicus DEM GLO-90'ı yalnızca yüksekliğe bağlı troposfer gecikmesi düzeltmesi için kullanarak tek komutla (`python -m pipeline.nisarvision`) herhangi bir havzayı yeniden üretir.

> *NISAR verileri ön/geçici (provisional) niteliktedir. Kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yürütülmektedir.*

---

### 2. Faydaları nelerdir? (What are the benefits?)
- **Su Kurulları ve Kanal İşletmecileri:** 645 OpenStreetMap koridorunda (`81` işaretli `> 10 mm/km`) yapılan eğim ön taraması, cazibeli sulama kanalları kapasite kaybetmeden önce maliyetli saha nivelman ekiplerinin önceliklendirilmesine yardımcı olur (yapısal güvenlik değerlendirmesi değildir, ön taramadır).
- **Belediyeler ve Afet Planlamacıları:** 29 standart A4 izleme bülteni, gigabaytlarca HDF5 interferogramını sade haritalara, etkilenen nüfus sayılarına (GHSL) ve güven etiketlerine dönüştürür.
- **Havza Toplulukları, Öğrenciler ve Eğitimciler:** Sade İngilizce kartlar, bulut altı UK Fens radar karşılaştırması, 3B yüzey görüntüleyici (`web3d/`) ve 24 aylık Yeraltı Suyu Simülatörü L-bant SAR fiziğini anlaşılır yeraltı suyu okuryazarlığına çevirir.

---

### 3. Hedeflenen etki nedir? (What is the intended impact?)
Yeraltı suyu çekimi ve turba drenajından kaynaklanan yer çökmesi, kanallar eğimini kaybedene, seddeler oturana veya obruklar açılana kadar sessiz ve yavaş ilerler. NISAR Vision, izlemeyi hasar sonrası tek seferlik tepkilerden şeffaf ve tekrarlanabilir 93 günlük havza takibine taşır. Açık ve kendi kendini denetleyen bir atlasta `1.20 M` etkilenen sakini ve `0.3174 km³/yıl` kalıcı akifer depolama kaybını görünür kılarak yerel su yönetimlerinin ve araştırmacıların havzaları ortak zaman penceresinde adil biçimde karşılaştırmasını ve her sayıyı açık NASA ASF verisinden yeniden üretmesini sağlar.

---

### 4. Hangi araçlar ve programlama dilleri kullanıldı? (What tools and coding languages did you use?)
- **Diller:** Python (`%68.8`), JavaScript (`%17.1`), HTML (`%8.4`), CSS (`%5.7`).
- **Bilimsel Python Yığını:** HDF5 alt kümeleme, koherans/bağlı bileşen maskeleme, yüksekliğe bağlı troposfer düzeltmesi (Copernicus DEM GLO-90), faz sıçraması QC ve otomatik tutarlılık testleri için `NumPy`, `SciPy`, `h5py`, `Rasterio`, `PyProj`, `Matplotlib`, `Pillow`, `Requests`, `asf_search` ve `pytest`.
- **Web, 3B ve Simülatör:** MapLibre GL JS (2B hikâye haritası ve çok bölgeli gezgin), Three.js (3B havza ve obruk görüntüleyici), HTML5 Canvas (grafikler ve 24 aylık Yeraltı Suyu Simülatörü) ve GitHub Pages (sunucusuz statik barındırma).
- **Yapay Zekâ Beyanı:** Kod, analiz betikleri ve dokümantasyon taslaklarında ekip incelemesi ve test doğrulamasıyla birlikte Anthropic Claude (`Claude Code`), Google Gemini (`Antigravity / Gemini CLI`) ve OpenAI Codex'ten yararlanılmıştır. Sitede hiçbir yapay zekâ üretimi görsel kullanılmamıştır; tüm görseller yalnızca uydu, GNSS ve açık coğrafi verilerden üretilmiştir.

---

### 5. Projeyi yaratıcı kılan nedir? (What makes your project creative?)
Erken dönem geçici radar çıktılarını hatasız varsaymak yerine, kendi faz açma ve referans seçimlerini denetleyen kendi kendini kontrol eden bir atlas kurduk. Otomatik QC (`tools/atlas_qc.py`), Semarang'daki `12.1 cm`'lik tam L-bant faz döngüsü sıçramasını ve Tahran ile Pekin'deki havza dışı referans sapmasını yakalayıp belirsizliği gizlemek yerine 29 havzanın 13'ünü yalnızca gösterge niteliğinde işaretledi. Bu açık bilimsel hattı tarayıcı içi 3B görüntüleyici, 29 basılabilir A4 bülten ve Terra Bella hızına kalibre edilmiş 24 aylık Terzaghi Yeraltı Suyu Simülatörü ile birleştirerek herkesin aşırı çekimin kalıcı kil çökmesine etkisini test etmesini sağladık.

---

### 6. Hangi faktörleri göz önünde bulundurdunuz? (What factors did you consider?)
1. **Ürün Olgunluğu:** 17 Haziran 2026 öncesi kalibrasyon öncesi beta sahnelerini (`beta-precal`) geçici `CRID P05023` yaz sahnelerinden ayırdık ve 11 aylık ayrıştırmayı açıkça `mixed` olarak etiketledik.
2. **Adil 93 Günlük Pencere ve Geometri:** Tüm 29 havza aynı 93 günlük ortak pencereyi (`2026-06-28` – `2026-09-29`) kullanır; ana ölçümler uydu görüş hattında (LOS) tutulur, dikey değer tahmin olarak etiketlenir ve mümkün olan yerlerde çift yörüngeyle çapraz kontrol edilir.
3. **Gürültü Eşiği ve Tespit Sınırları:** GHSL nüfus maruziyeti yalnızca her havzanın `2-sigma` gürültü tabanını aşan pikselleri sayar; Londra Kili tek sezonluk tespit sınırının altında (`3.62 cm` `3-sigma` vs beklenen `0.5–2.0 cm`) raporlanır.
4. **Atmosferik Düzeltme Kapsamı:** Copernicus DEM GLO-90 yalnızca yüksekliğe bağlı troposfer gecikmesi düzeltmesi için kullanılır.
5. **İkincil Kontrol Uyarıları:** Birincil doğrulama GPS'tir (`r = 0.924`, 10 istasyon); NASA JPL OPERA ikincil kontrol olarak kış/yaz ve bakış geometrisi uyarılarıyla birlikte verilir.
6. **Mühendislik ve Görsel Dürüstlük:** Altyapı eğim bayrakları (`81/645`) yalnızca ön tarama olarak sunulur (yapısal güvenlik değerlendirmesi değildir) ve sitede hiç yapay zekâ üretimi görsel yoktur.
