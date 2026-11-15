// Turkish dictionary for js/i18n.js (loaded only when Turkish is selected).
// Key = English text exactly as on the page, whitespace collapsed.
//   {0}, {1} ... = an inline element inside the text (<b>, <a>, <span>); keep every slot in the Turkish text.
//   #            = any number; numbers are put back in the same order.
// Missing text simply stays in English. To list what is missing: open a page with ?i18n=collect and run
// I18N.missing() in the browser console.
window.I18N_TR = window.I18N_TR || {};

// Dates such as "28 Jun – 14 Oct 2026", "(108 days)": month names and "days" only.
(function () {
  const M = {Jan: 'Oca', Feb: 'Şub', Mar: 'Mar', Apr: 'Nis', May: 'May', Jun: 'Haz', Jul: 'Tem', Aug: 'Ağu',
    Sep: 'Eyl', Oct: 'Eki', Nov: 'Kas', Dec: 'Ara',
    January: 'Ocak', February: 'Şubat', March: 'Mart', April: 'Nisan', June: 'Haziran', July: 'Temmuz',
    August: 'Ağustos', September: 'Eylül', October: 'Ekim', November: 'Kasım', December: 'Aralık'};
  const W = '(?:January|February|March|April|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|days?|UTC)';
  const re = new RegExp('^(?:[\\d.,:\\s–—\\-→()/]|' + W + ')+$');
  window.I18N_TR_PATTERNS = [
    [re, m => m[0].replace(new RegExp('\\b' + W + '\\b', 'g'), w => (w === 'day' || w === 'days' ? 'gün' : (M[w] || w)))]
  ];
})();

// ---- shared: menus, buttons, common words -----------------------------------------------------------
Object.assign(window.I18N_TR, {
  "Home": "Ana sayfa",
  "Atlas": "Atlas",
  "Simulator": "Simülatör",
  "Game": "Oyun",
  "Play Aquifer Run": "Aquifer Run oyna",
  "Science": "Bilim",
  "Data": "Veri",
  "Present": "Sunum",
  "FAQ": "SSS",
  "Sections": "Bölümler",
  "NISAR Vision home": "NISAR Vision ana sayfa",
  "Main navigation": "Ana menü",
  "Team Aseltech": "Aseltech Takımı",
  "Confidence": "Güven",
  "Basin": "Havza",
  "Region": "Bölge",
  "Period": "Dönem",
  "Station": "İstasyon",
  "Close": "Kapat",
  "Next": "İleri",
  "Back": "Geri",
  "Done": "Bitti",
  "Skip tour": "Turu geç",
  "Loading…": "Yükleniyor…",
  "Loading...": "Yükleniyor...",
  "USA": "ABD",
  "Iran": "İran",
  "Mexico": "Meksika",
  "China": "Çin",
  "India": "Hindistan",
  "Indonesia": "Endonezya",
  "Pakistan": "Pakistan",
  "Vietnam": "Vietnam",
  "Thailand": "Tayland",
  "Nigeria": "Nijerya",
  "Bangladesh": "Bangladeş",
  "Italy": "İtalya",
  "Spain": "İspanya",
  "Egypt": "Mısır",
  "Iraq": "Irak",
  "Saudi Arabia": "Suudi Arabistan",
  "United Kingdom": "Birleşik Krallık",
  "Türkiye": "Türkiye",
  "reliable": "güvenilir",
  "indicative": "gösterge",
  "provisional": "geçici",
  "PROVISIONAL": "GEÇİCİ",
  "high": "yüksek",
  "medium": "orta",
  "low": "düşük",
  "HIGH": "YÜKSEK",
  "MEDIUM": "ORTA",
  "LOW": "DÜŞÜK",
  "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.":
    "NISAR verileri geçicidir. Kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yapılmaktadır.",
  "{0}NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.{1}":
    "{0}NISAR verileri geçicidir. Kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yapılmaktadır.{1}",
  "{0}{1} · ASELSAN Vocational and Technical Anatolian High School, Ankara, Türkiye{2}NASA Space Apps Challenge # · Local event: Cambridge, MA (virtual)":
    "{0}{1} · ASELSAN Mesleki ve Teknik Anadolu Lisesi, Ankara, Türkiye{2}NASA Space Apps Challenge # · Yerel etkinlik: Cambridge, MA (sanal)",
  "Data: NASA-ISRO NISAR (provisional) via NASA ASF DAAC · NASA JPL OPERA · Nevada Geodetic Laboratory GNSS · GHSL · OpenStreetMap. Base image: NASA Blue Marble.{0}Open source (MIT): {1} · Built with help from AI assistants (Claude, Gemini); see {2}.":
    "Veri: NASA-ISRO NISAR (geçici), NASA ASF DAAC üzerinden · NASA JPL OPERA · Nevada Jeodezi Laboratuvarı GNSS · GHSL · OpenStreetMap. Arka plan görüntüsü: NASA Blue Marble.{0}Açık kaynak (MIT): {1} · Yapay zekâ asistanlarının (Claude, Gemini) yardımıyla yapıldı; bkz. {2}.",
  "GitHub": "GitHub"
});

// ---- index.html ---------------------------------------------------------------------------------------
Object.assign(window.I18N_TR, {
  "NISAR Vision — Where the Ground Is Sinking, Measured from Space": "NISAR Vision — Yer nerede çöküyor, uzaydan ölçtük",
  "NASA Space Apps # · Dancing with the SARs": "NASA Space Apps # · Dancing with the SARs",
  "Where is the ground sinking? We measured {0} places from space.": "Yer nerede çöküyor? {0} yeri uzaydan ölçtük.",
  "Using the first data from NASA and ISRO's new {0} radar satellite, we built one open method that turns radar echoes into centimetres of ground sinking, ran it on {1} basins over the same {2} days, and checked every number.":
    "NASA ve ISRO'nun yeni {0} radar uydusunun ilk verileriyle, radar yankılarını santimetre cinsinden yer çökmesine çeviren tek ve açık bir yöntem kurduk; bunu aynı {2} gün boyunca {1} havzada çalıştırdık ve her sayıyı kontrol ettik.",
  "Open the interactive atlas": "Etkileşimli atlası aç",
  "Play the simulator": "Simülatörü oyna",
  "Play the simulator →": "Simülatörü oyna →",
  "Key numbers": "Temel sayılar",
  "# reliable, # indicative": "# güvenilir, # gösterge",
  "basins measured with one method": "havza, tek yöntemle ölçüldü",
  "basins counted": "havza sayıldı",
  "basins our own error check flagged": "havzayı kendi hata kontrolümüz işaretledi",
  "shown as indicative until re-processed": "yeniden işlenene kadar gösterge olarak gösteriliyor",
  "people live on ground that is sinking": "kişi çöken zeminde yaşıyor",
  "people live on ground that is sinking{0}{1}": "kişi çöken zeminde yaşıyor{0}{1}",
  "it sank more than # cm (# inches) in one summer": "zemin bir yazda # cm'den (# inç) fazla çöktü",
  "of land that is sinking{0}{1}": "çöken arazi{0}{1}",
  "more than # cm (# inches) in one summer": "bir yazda # cm'den (# inç) fazla",
  "sank more than # cm (# inches) in one summer, measured basins": "bir yazda # cm'den (# inç) fazla çöktü, ölçülen havzalar",
  "{0} people live on ground that is sinking (more than # cm in one summer)": "{0} kişi çöken zeminde yaşıyor (bir yazda # cm'den fazla)",
  "{0} where ground sank ># cm": "{0} kişi, zeminin ># cm çöktüğü yerde",
  "underground water storage lost for good": "kalıcı olarak kaybedilen yeraltı suyu deposu",
  "agreement with # GPS stations": "# GPS istasyonuyla uyum",
  "caught our own # cm error": "kendi # cm'lik hatamızı yakaladı",
  "learn the physics in # s": "fiziği # saniyede öğren",
  "one command, any region": "tek komut, her bölge",
  "What we built · in one look": "Ne yaptık · tek bakışta",
  "Nine things we made. Each one is a section below.": "Yaptığımız dokuz şey. Her biri aşağıda bir bölüm.",
  "A global subsidence atlas": "Küresel çökme atlası",
  "Global atlas": "Küresel atlas",
  "Sinking rate": "Çökme hızı",
  "People exposed": "Etkilenen insanlar",
  "Water lost": "Kaybedilen su",
  "Infrastructure": "Altyapı",
  "GPS proof": "GPS kanıtı",
  "Self-check": "Öz denetim",
  "Bulletins": "Bültenler",
  "Open engine": "Açık motor",
  "{0} ground motion maps for {1} basins on three continents, all made the same way from NISAR's first radar data and ranked on the same {2} days.":
    "{0} üç kıtada {1} havza için yer hareketi haritaları; hepsi NISAR'ın ilk radar verisinden aynı yöntemle yapıldı ve aynı {2} güne göre sıralandı.",
  "{0} for the first time you can compare sinking in Türkiye, Iran, Mexico, California and Asia side by side, with the same ruler.":
    "{0} Türkiye, İran, Meksika, Kaliforniya ve Asya'daki çökmeyi ilk kez aynı cetvelle yan yana karşılaştırabilirsiniz.",
  "What it is:": "Nedir:",
  "Why it matters:": "Neden önemli:",
  "Open the atlas →": "Atlası aç →",
  "World map of the measured basins: filled circles are reliable measurements, rings are indicative; the five fastest are labelled":
    "Ölçülen havzaların dünya haritası: dolu daireler güvenilir ölçümler, halkalar gösterge niteliğinde; en hızlı beş tanesi etiketli",
  "One of the # maps: Konya Closed Basin, Türkiye, # Jun – # Oct # Red = sinking; star = fastest # km block (# cm).":
    "# haritadan biri: Konya Kapalı Havzası, Türkiye, # Haz – # Eki # Kırmızı = çökme; yıldız = en hızlı # km'lik blok (# cm).",
  "Konya Closed Basin ground motion map with Konya and Karapınar marked: red areas sank up to # cm between June and October #":
    "Konya ve Karapınar işaretli Konya Kapalı Havzası yer hareketi haritası: kırmızı alanlar Haziran ile Ekim #2 arasında #1 cm'ye kadar çöktü",
  "Fastest-sinking reliable basins": "En hızlı çöken güvenilir havzalar",
  "{0} per # days at the Konya Plain, the fastest reliable basin": "{0} / # gün, Konya Ovası'nda, en hızlı çöken güvenilir havza",
  "cm per # days, toward or away from the satellite. {0}": "# günde cm, uyduya doğru ya da uydudan uzağa. {0}",
  "Fastest reliable basins, cm per # days toward or away from the satellite, common window ### to ###; # more basins are indicative only. NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.":
    "En hızlı güvenilir havzalar, # günde cm, uyduya doğru ya da uydudan uzağa, ortak dönem ### – ###; # havza daha yalnızca gösterge niteliğinde. NISAR verileri geçicidir. Kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yapılmaktadır.",
  "Data window": "Veri dönemi",
  "# cm / # days": "# cm / # gün",
  "Konya Plain, Türkiye": "Konya Ovası, Türkiye",
  "Konya Plain": "Konya Ovası",
  "Central Valley, California": "Central Valley, Kaliforniya",
  "Central Valley (Tulare Basin)": "Central Valley (Tulare Havzası)",
  "Türkiye · caution": "Türkiye · dikkat",
  "medium · low coverage, caution": "orta · düşük kapsama, dikkat",
  "Who lives on sinking ground": "Çöken zeminde kimler yaşıyor",
  "{0} each atlas map overlaid with a population map (GHSL #), counting only sinking larger than twice the measurement noise.":
    "{0} her atlas haritası bir nüfus haritasıyla (GHSL #) üst üste kondu; yalnızca ölçüm gürültüsünün iki katından büyük çökmeler sayıldı.",
  "{0} it turns centimetres into people, the number a city or ministry needs.":
    "{0} santimetreleri insan sayısına çeviriyor; bir belediyenin ya da bakanlığın ihtiyaç duyduğu sayı bu.",
  "Water storage lost for good": "Kalıcı olarak kaybedilen su deposu",
  "{0} eleven months of NISAR data split into ground that bounces back each winter and ground that does not. The part that does not come back is squeezed clay: aquifer space lost forever.":
    "{0} on bir aylık NISAR verisi, her kış geri kabaran zemin ile geri gelmeyen zemin olarak ayrıldı. Geri gelmeyen kısım sıkışmış kildir: sonsuza dek kaybedilmiş akifer hacmi.",
  "{0} water managers count it in cubic kilometres, so we did too.": "{0} su yöneticileri bunu kilometreküp olarak sayar, biz de öyle yaptık.",
  "{0} lost permanently in the Central Valley": "{0} Central Valley'de kalıcı olarak kaybedildi",
  "Eleven months of ground motion west of Earlimart: a small winter rise, then a steep summer drop, split into a permanent trend and a seasonal cycle":
    "Earlimart'ın batısında on bir aylık yer hareketi: kışın küçük bir yükselme, ardından yazın dik bir düşüş; kalıcı eğilim ve mevsimsel döngü olarak ayrıldı",
  "Earlimart, Central Valley: permanent trend vs seasonal cycle (mixed beta + provisional data).":
    "Earlimart, Central Valley: kalıcı eğilim ve mevsimsel döngü (karışık beta + geçici veri).",
  "Canals and railways at risk": "Risk altındaki kanallar ve demiryolları",
  "{0} every canal, road and railway line in the Central Valley checked for uneven sinking, with a probability that includes our measurement error.":
    "{0} Central Valley'deki her kanal, yol ve demiryolu hattı düzensiz çökmeye karşı kontrol edildi; olasılık hesabına ölçüm hatamız da dahil.",
  "{0} uneven sinking cracks canals and tilts tracks; engineers can see which section to inspect first.":
    "{0} düzensiz çökme kanalları çatlatır, rayları eğer; mühendisler önce hangi kesimi incelemeleri gerektiğini görebilir.",
  "{0} sections flagged": "{0} kesim işaretlendi",
  "{0} sections on ground tilting more than # mm per km": "{0} kesim, km başına # mm'den fazla eğilen zeminde",
  "Bar chart: probability that sinking differs by more than # cm along each line, highest for the Exeter and Goshen rail subdivisions and the Friant-Kern Canal":
    "Çubuk grafik: her hat boyunca çökmenin # cm'den fazla farklılaşma olasılığı; en yüksek Exeter ve Goshen demiryolu kesimleri ile Friant-Kern Kanalı'nda",
  "Chance of more than # cm uneven sinking per line (screening, not a safety rating).":
    "Hat başına # cm'den fazla düzensiz çökme olasılığı (ön tarama, güvenlik derecelendirmesi değildir).",
  "Proof on the ground": "Sahada kanıt",
  "{0} a comparison with # permanent GPS stations in California's Central Valley, where the ground moved up to # cm away from the satellite in # days.":
    "{0} Kaliforniya'nın Central Valley bölgesindeki #1 sabit GPS istasyonuyla karşılaştırma; burada zemin #3 günde uydudan uzağa #2 cm'ye kadar hareket etti.",
  "{0} GPS stations are the reference that engineers trust. NISAR and GPS tell the same story, station by station.":
    "{0} GPS istasyonları mühendislerin güvendiği referanstır. NISAR ve GPS, istasyon istasyon aynı hikâyeyi anlatıyor.",
  "{0} agreement with GPS, typical difference # cm": "{0} GPS ile uyum, tipik fark # cm",
  "{0} at # stations": "{0} # istasyonda",
  "NISAR versus GPS at # stations: the points follow the one-to-one line": "# istasyonda NISAR ve GPS: noktalar bire bir çizgisini izliyor",
  "NISAR vs GPS, Central Valley, # Jun – # Oct #": "NISAR ve GPS, Central Valley, # Haz – # Eki #",
  "We also compared with NASA JPL's OPERA product: over Mexico City the pattern matches at # points (r = #), although OPERA covers winter and NISAR summer.":
    "NASA JPL'in OPERA ürünüyle de karşılaştırdık: Mexico City üzerinde desen # noktada örtüşüyor (r = #), oysa OPERA kışı, NISAR yazı kapsıyor.",
  "A check that catches our own errors": "Kendi hatalarımızı yakalayan bir kontrol",
  "{0} an automatic test on every basin's time series. It looks for jumps of exactly one radar phase cycle (# cm) and for single bad dates.":
    "{0} her havzanın zaman serisinde otomatik bir test. Tam bir radar faz döngüsü (# cm) büyüklüğündeki sıçramaları ve tek tük hatalı tarihleri arar.",
  "{0} it caught our first number one. Semarang's # cm was one processing jump; re-processed, the real peak on the coast is # cm.":
    "{0} ilk bir numaramızı yakaladı. Semarang'ın # cm'si tek bir işleme sıçramasıydı; yeniden işlenince kıyıdaki gerçek tepe değer # cm.",
  "{0} basins flagged and shown as indicative": "{0} havza işaretlendi ve gösterge olarak gösteriliyor",
  "Semarang. Grey: old headline point inland, one # cm jump at the last date. Blue: new headline point on the subsiding north coast.":
    "Semarang. Gri: iç kesimdeki eski manşet noktası, son tarihte tek bir # cm sıçrama. Mavi: çöken kuzey kıyısındaki yeni manşet noktası.",
  "A one-page bulletin for every basin": "Her havza için tek sayfalık bülten",
  "{0} {1} printable bulletins in the style of NASA disaster products: rate, worst areas, people affected, confidence, revision history.":
    "{0} NASA afet ürünleri tarzında {1} yazdırılabilir bülten: hız, en kötü bölgeler, etkilenen insanlar, güven düzeyi, revizyon geçmişi.",
  "{0} a water manager does not read papers; one page with the number and its reliability is what they use.":
    "{0} bir su yöneticisi makale okumaz; kullandığı şey, sayıyı ve güvenilirliğini gösteren tek bir sayfadır.",
  "{0} one-page reports": "{0} tek sayfalık rapor",
  "NISAR Vision Bulletin": "NISAR Vision Bülteni",
  "NP-KONYA_PLAIN## · provisional": "NP-KONYA_PLAIN## · geçici",
  "Open the Konya Plain bulletin →": "Konya Ovası bültenini aç →",
  "A simulator anyone can play": "Herkesin oynayabileceği bir simülatör",
  "{0} run a farming valley for # months. Pump more and earn more, but watch the ground sink and part of it never come back.":
    "{0} bir tarım vadisini # ay yönet. Daha çok pompala, daha çok kazan; ama zeminin çöktüğünü ve bir kısmının hiç geri gelmediğini izle.",
  "{0} the model reproduces what NISAR measured, so students and farmers learn from real data, in # seconds.":
    "{0} model NISAR'ın ölçtüğünü yeniden üretiyor; öğrenciler ve çiftçiler # saniyede gerçek veriden öğreniyor.",
  "Simulator preview: valley map, sinking chart and water sliders (#-month aquifer model).":
    "Simülatör önizlemesi: vadi haritası, çökme grafiği ve su kaydırıcıları (#-aylık akifer modeli).",
  "Simulator screen: valley map, sinking chart and water sliders": "Simülatör ekranı: vadi haritası, çökme grafiği ve su kaydırıcıları",
  "An open engine anyone can re-run": "Herkesin yeniden çalıştırabileceği açık bir motor",
  "{0} NISAR Vision, the pipeline behind every number here. One command searches NASA's archive, downloads, measures and checks a new region.":
    "{0} NISAR Vision, buradaki her sayının arkasındaki işlem hattı. Tek komut NASA arşivini tarar, indirir, ölçer ve yeni bir bölgeyi kontrol eder.",
  "{0} any agency or student can repeat our atlas for their own city, and check our work.":
    "{0} her kurum ya da öğrenci atlasımızı kendi şehri için tekrarlayabilir ve çalışmamızı denetleyebilir.",
  "Get the code and data →": "Kodu ve veriyi al →",
  "{0} gone for good": "{0} kalıcı olarak gitti",
  "{0} basins, same {1} days": "{0} havza, aynı {1} gün",
  "Click to enlarge full screen": "Tam ekran büyütmek için tıkla",
  "{0} Click to enlarge": "{0} Büyütmek için tıkla",
  "Close enlarged view": "Büyütülmüş görünümü kapat",
  "Enlarged figure view": "Büyütülmüş şekil görünümü",
  "Enlarged image view": "Büyütülmüş görsel görünümü"
});

// ---- place names (only those with an established Turkish form) ---------------------------------------
Object.assign(window.I18N_TR, {
  "Sacramento–San Joaquin Delta": "Sacramento–San Joaquin Deltası",
  "Mexico City": "Meksiko",
  "Ho Chi Minh City": "Ho Chi Minh Kenti",
  "Beijing": "Pekin",
  "Tehran": "Tahran",
  "Isfahan": "İsfahan",
  "Mashhad": "Meşhed",
  "Jakarta": "Cakarta",
  "Taiwan": "Tayvan",
  "Konya Plain (LOS)": "Konya Ovası (LOS)",
  "Konya Plain {0}": "Konya Ovası {0}",
  "Beijing {0}": "Pekin {0}",
  "(China)": "(Çin)"
});

// Repeated shapes on the atlas: "#1 · Konya Plain", "Select Konya Plain", "Iran · {0}", "{0} · Iran", changelog lines.
window.I18N_TR_PATTERNS.push(
  [/^(#\d+) · (.+)$/, (m, t) => m[1] + ' · ' + t(m[2])],
  [/^Select (#\d+ )?(.+)$/, (m, t) => 'Seç: ' + (m[1] || '') + t(m[2])],
  [/^Cumulative ground motion map for (.+)$/, (m, t) => t(m[1]) + ' için kümülatif yer hareketi haritası'],
  [/^\{0\} · (.+)$/, (m, t) => '{0} · ' + t(m[1])],
  [/^(.+) · \{0\}$/, (m, t) => t(m[1]) + ' · {0}'],
  [/^\{0\} — (.+)$/, m => '{0} — ' + m[1]
    .replace(/\bregions\b/, 'bölge').replace(/\badded:/, 'eklendi:')
    .replace('Initial historical corrections (off-basin re-referencing and phase-cycle QC)',
      'İlk geçmiş düzeltmeler (havza dışı yeniden referanslama ve faz döngüsü kalite kontrolü)')]
);

// ---- atlas.html -----------------------------------------------------------------------------------------
Object.assign(window.I18N_TR, {
  "Global Subsidence Atlas # (# Regions) — NISAR Vision": "Küresel Çökme Atlası # (# Bölge) — NISAR Vision",
  "Global Atlas · #": "Küresel Atlas · #",
  "Sinking basins worldwide": "Dünyada çöken havzalar",
  "Measured from NASA-ISRO NISAR {0} radar pairs with the same open pipeline, ranked by line-of-sight (LOS) rate per # days.":
    "NASA-ISRO NISAR {0} radar çiftlerinden aynı açık işlem hattıyla ölçüldü; # günlük görüş hattı (LOS) hızına göre sıralandı.",
  "Atlas Vital Signs": "Atlasın temel göstergeleri",
  "Cities measured": "Ölçülen şehirler",
  "# NISAR provisional": "# NISAR geçici",
  "Fastest-sinking place": "En hızlı çöken yer",
  "LOS rate per # days": "# günde LOS hızı",
  "Land that is sinking": "Çöken arazi",
  "km² across measured basins, sank more than # cm in one summer (about # days)": "km², ölçülen havzalarda; bir yazda (yaklaşık #2 gün) #1 cm'den fazla çöktü",
  "People on sinking ground": "Çöken zemindeki insanlar",
  "live where ground sank more than # cm in one summer (GHSL population estimate)": "zeminin bir yazda # cm'den fazla çöktüğü yerde yaşıyor (GHSL nüfus tahmini)",
  "Global atlas controls and region details": "Küresel atlas kontrolleri ve bölge ayrıntıları",
  "Regions": "Bölgeler",
  "Reliable": "Güvenilir",
  "Indicative only": "Yalnızca gösterge",
  "How to read this map (# steps)": "Bu harita nasıl okunur (# adım)",
  "LOS vs. vertical:": "LOS ve düşey:",
  "{0} Numbers show radar line-of-sight (LOS) motion; use {1} to toggle approximate vertical (LOS / cos θ).":
    "{0} Sayılar radarın görüş hattı (LOS) yönündeki hareketi gösterir; yaklaşık düşey değere (LOS / cos θ) geçmek için {1} kullanın.",
  "Color scale:": "Renk ölçeği:",
  "{0} Deeper red marks faster sinking (cm or cm/#d over the #-day common window); pale tones mark near-zero motion.":
    "{0} Koyu kırmızı daha hızlı çökmeyi gösterir (#2-günlük ortak dönemde cm ya da cm/#1g); soluk tonlar sıfıra yakın hareketi gösterir.",
  "Confidence badge:": "Güven rozeti:",
  "{0} {1} / {2} badges indicate consistent multi-reference stacks and solid valid coverage ({3}).":
    "{0} {1} / {2} rozetleri, birden çok referansla tutarlı yığınları ve sağlam geçerli kapsamayı ({3}) gösterir.",
  "see method": "yönteme bak",
  "Indicative only:": "Yalnızca gösterge:",
  "{0} Low-coverage scenes or QC-flagged series (phase-cycle jumps or single-date spikes) are separated as {1}.":
    "{0} Düşük kapsamalı sahneler ya da kalite kontrolde işaretlenen seriler (faz döngüsü sıçramaları veya tek tarihli sıçramalar) {1} olarak ayrılır.",
  "indicative only": "yalnızca gösterge",
  "Search, filter and display options": "Arama, filtre ve görünüm seçenekleri",
  "Search city or country...": "Şehir veya ülke ara...",
  "Search city or country": "Şehir veya ülke ara",
  "Filter by confidence": "Güvene göre filtrele",
  "Filter by country": "Ülkeye göre filtrele",
  "All confidence": "Tüm güven düzeyleri",
  "Reliable only": "Yalnızca güvenilir",
  "All countries": "Tüm ülkeler",
  "Sort: Fastest Rate": "Sırala: En hızlı",
  "Sort: Largest Area": "Sırala: En geniş alan",
  "Switch ranking between fastest rate and largest sinking area": "Sıralamayı en hızlı çökme ile en geniş çöken alan arasında değiştir",
  "Values: LOS": "Değerler: LOS",
  "Values: Vertical (est.)": "Değerler: Düşey (tahmini)",
  "Compare two cities": "İki şehri karşılaştır",
  "Compare regions": "Bölgeleri karşılaştır",
  "Close comparison": "Karşılaştırmayı kapat",
  "First region to compare": "Karşılaştırılacak ilk bölge",
  "Second region to compare": "Karşılaştırılacak ikinci bölge",
  "Interactive #D globe of measured regions": "Ölçülen bölgelerin etkileşimli #B küresi",
  "Top # reliable sinking basins": "En hızlı çöken # güvenilir havza",
  "Top # Basins {0}": "İlk # Havza {0}",
  "(#-d window)": "(#-günlük dönem)",
  "Click to select": "Seçmek için tıkla",
  "All # basins ↓": "Tüm # havza ↓",
  "Map layer": "Harita katmanı",
  "Subsidence": "Çökme",
  "Uncertainty (σ)": "Belirsizlik (σ)",
  "Uncertainty": "Belirsizlik",
  "Tour top #": "İlk # turu",
  "Stop tour": "Turu durdur",
  "? How to use": "? Nasıl kullanılır",
  "How to use": "Nasıl kullanılır",
  "Step-by-step guide to this page": "Bu sayfanın adım adım rehberi",
  "Offline basemap: NASA Blue Marble": "Çevrimdışı altlık harita: NASA Blue Marble",
  "Rate (cm / # days, LOS)": "Hız (cm / # gün, LOS)",
  "Uncertainty σ (cm, LOS)": "Belirsizlik σ (cm, LOS)",
  "Confidence class": "Güven sınıfı",
  "High confidence": "Yüksek güven",
  "Medium confidence": "Orta güven",
  "Low · indicative only": "Düşük · yalnızca gösterge",
  "low · indicative only": "düşük · yalnızca gösterge",
  "NISAR now": "NISAR şimdi",
  "{0} {1}NISAR now": "{0} {1}NISAR şimdi",
  "· real orbit (SGP# CelesTrak TLE)": "· gerçek yörünge (SGP# CelesTrak TLE)",
  "NISAR's real position, ground track and radar swath (SGP# from CelesTrak TLE)": "NISAR'ın gerçek konumu, yer izi ve radar şeridi (CelesTrak TLE'den SGP#)",
  "{0}spacecraft position": "{0}uydu konumu",
  "{0}ground track (±# min)": "{0}yer izi (±# dk)",
  "{0}radar swath, last # min (left-looking, ≈# km)": "{0}radar şeridi, son # dk (sola bakan, ≈# km)",
  "Fastest-sinking places ranking tables": "En hızlı çöken yerlerin sıralama tabloları",
  "Ranking · ranked by common #-day window (# Jun – # Sep #)": "Sıralama · ortak #-günlük döneme göre (# Haz – # Eyl #)",
  "Fastest-sinking places in our # NISAR atlas (ranked by common #-day window)": "# NISAR atlasımızda en hızlı çöken yerler (ortak #-günlük döneme göre)",
  "All values are line-of-sight ({0}) displacement from {1} NISAR L# GUNW data, ranked by rate per # days over the common #-day window (# Jun – # Sep #) with #% confidence intervals ({2}) where available. Low-confidence regions are separated as {3}. {4}":
    "Tüm değerler {1} NISAR L#1 GUNW verisinden görüş hattı ({0}) yer değiştirmesidir; ortak #3-günlük dönemde (#4 Haz – #5 Eyl #6) #2 günlük hıza göre sıralanmıştır, mümkün olanlarda %#7 güven aralıkları ({2}) verilmiştir. Düşük güvenli bölgeler {3} olarak ayrılmıştır. {4}",
  "Reliable measurements": "Güvenilir ölçümler",
  "Indicative only (low confidence)": "Yalnızca gösterge (düşük güven)",
  "Common rate (cm/#d)": "Ortak hız (cm/#g)",
  "Area (< # cm)": "Alan (< # cm)",
  "Area < # cm": "Alan < # cm",
  "Max LOS": "En büyük LOS",
  "Conf": "Güven",
  "Area": "Alan",
  "Rate": "Hız",
  "Rate (LOS)": "Hız (LOS)",
  "Max vertical (est.)": "En büyük düşey (tahmini)",
  "Vertical (est.)": "Düşey (tahmini)",
  "Yearly rate (est.)": "Yıllık hız (tahmini)",
  "(largest area < # cm)": "(en geniş alan < # cm)",
  "People (<# cm)": "İnsanlar (<# cm)",
  "Pairs / Valid px": "Çift / Geçerli piksel",
  "# pairs · #%": "# çift · %#",
  "# pairs · —": "# çift · —",
  "Ref. spread": "Referans yayılımı",
  "Robustness": "Sağlamlık",
  "Detectable": "Tespit edilebilir",
  "Yes (SNR #)": "Evet (SNR #)",
  "Low chain noise (< # cm)": "Düşük zincir gürültüsü (< # cm)",
  "Moderate noise (#–# cm)": "Orta gürültü (#–# cm)",
  "High noise (> # cm)": "Yüksek gürültü (> # cm)",
  "#nd percentile (p#)": "#. yüzdelik (p#)",
  "Peak point (p#) time series (cm, LOS)": "Tepe noktası (p#) zaman serisi (cm, LOS)",
  "Peak point (p#) overlay (cm, LOS)": "Tepe noktası (p#) katmanı (cm, LOS)",
  "±#σ band": "±#σ bandı",
  "Overlay shows per-pixel σ where available.": "Katman, mümkün olan yerlerde piksel başına σ gösterir.",
  "Time slider for cumulative displacement": "Kümülatif yer değiştirme için zaman kaydırıcısı",
  "Play": "Oynat",
  "# cm (sinking)": "# cm (çökme)",
  "# cm/#d (LOS) · medium": "# cm/#g (LOS) · orta",
  "{0}Rate: # cm/#d{1}Max LOS: # cm{2}Vert (est.): # cm{3}{4}": "{0}Hız: # cm/#g{1}En büyük LOS: # cm{2}Düşey (tahmini): # cm{3}{4}",
  "City card →": "Şehir kartı →",
  "Open bulletin →": "Bülteni aç →",
  "Open in Explorer →": "Gezginde aç →",
  "Manage this valley in the simulator →": "Bu vadiyi simülatörde yönet →",
  "Validation note (lit. # to # regional GNSS; > # in agricultural bowls cm/yr):": "Doğrulama notu (literatür: bölgesel GNSS # – #; tarım çanaklarında > # cm/yıl):",
  "{0} #-day summer peak (# cm LOS, # cm vertical est., # cm/yr LOS est.) is ##x higher than multi-year InSAR (> # cm/yr) due to peak summer agricultural pumping, wide bbox (#x# deg), low valid pixel fraction (#%), and # reference sensitivity.":
    "{0} #1-günlük yaz tepe değeri (#2 cm LOS, #3 cm tahmini düşey, #4 cm/yıl tahmini LOS), çok yıllık InSAR'dan (> #7 cm/yıl) #5#6x daha yüksek; nedenleri yazın en yoğun tarımsal pompalama, geniş sınır kutusu (#8x#9 derece), düşük geçerli piksel oranı (%#10) ve #11 referans hassasiyetidir.",
  "{0} NISAR L# GUNW (PROVISIONAL, CRID P#) via ASF DAAC, track # descending frame #; https://nisar-docs.asf.alaska.edu/gunw":
    "{0} NISAR L# GUNW (GEÇİCİ, CRID P#), ASF DAAC üzerinden, iz # alçalan çerçeve #; https://nisar-docs.asf.alaska.edu/gunw",
  "Source:": "Kaynak:",
  "Quality control: {0} regions flagged (time-series check) — {1}": "Kalite kontrol: {0} bölge işaretlendi (zaman serisi kontrolü) — {1}",
  "What changed — latest # atlas updates": "Neler değişti — atlasın son # güncellemesi",
  "Loading changelog…": "Değişiklik günlüğü yükleniyor…",
  "Data downloads and citation": "Veri indirme ve atıf",
  "Data & citation": "Veri ve atıf",
  "Download the global atlas tables and open documentation for methods and data sources:": "Küresel atlas tablolarını indirin; yöntemler ve veri kaynakları için açık belgelere bakın:",
  "Data dictionary": "Veri sözlüğü",
  "Atlas methods": "Atlas yöntemleri",
  "Sources & DOIs": "Kaynaklar ve DOI'ler",
  "NISAR Global Subsidence Atlas #": "NISAR Küresel Çökme Atlası #",
  "NISAR Global Subsidence Atlas # (provisional)": "NISAR Küresel Çökme Atlası # (geçici)",
  "Team Aseltech (#). {0}. Derived from NASA-ISRO NISAR L# GUNW products via Alaska Satellite Facility DAAC. NISAR data are provisional; calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.":
    "Aseltech Takımı (#). {0}. NASA-ISRO NISAR L# GUNW ürünlerinden, Alaska Satellite Facility DAAC üzerinden türetilmiştir. NISAR verileri geçicidir; kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yapılmaktadır.",
  "NASA-ISRO NISAR L# GUNW (provisional) · Ranked by LOS rate per # days · Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.":
    "NASA-ISRO NISAR L# GUNW (geçici) · # günlük LOS hızına göre sıralı · Kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yapılmaktadır.",
  "Open source on GitHub": "GitHub'da açık kaynak",
  "Toggle attribution": "Kaynak bilgisini aç/kapat",
  "Zoom in": "Yakınlaştır",
  "Zoom out": "Uzaklaştır",
  "Use Ctrl + scroll to zoom the map": "Haritayı yakınlaştırmak için Ctrl + kaydırma kullanın",
  "Use two fingers to move the map": "Haritayı taşımak için iki parmak kullanın",
  // tour (js/tour_atlas.js)
  "Welcome to the Subsidence Atlas": "Çökme Atlası'na hoş geldiniz",
  "Every place on this page is sinking because groundwater is pumped out faster than it refills, measured by the NASA-ISRO NISAR radar satellite. This one-minute tour shows you how to read it.":
    "Bu sayfadaki her yer, yeraltı suyu dolduğundan daha hızlı çekildiği için çöküyor; ölçümler NASA-ISRO NISAR radar uydusuna ait. Bu bir dakikalık tur, sayfayı nasıl okuyacağınızı gösteriyor.",
  "The headline numbers": "Manşet sayılar",
  "How many cities we measured, the fastest-sinking place, how much land is sinking (more than # cm, # inches, in one summer), and roughly how many people live on it.":
    "Kaç şehri ölçtüğümüz, en hızlı çöken yer, ne kadar arazinin çöktüğü (bir yazda # cm'den, # inçten fazla) ve kabaca kaç kişinin orada yaşadığı.",
  "The globe": "Küre",
  "Each dot is a measured basin; the colour shows how fast it sinks. Drag to turn the globe, scroll or pinch to zoom, and {0} to open that place.":
    "Her nokta ölçülmüş bir havza; renk ne kadar hızlı çöktüğünü gösteriyor. Küreyi döndürmek için sürükleyin, yakınlaştırmak için kaydırın ya da iki parmakla açın; o yeri açmak için {0}.",
  "click a dot": "bir noktaya tıklayın",
  "Top # at a glance": "Bir bakışta ilk #",
  "The five fastest-sinking basins we trust most. Click a row to fly there.": "En çok güvendiğimiz, en hızlı çöken beş havza. Oraya uçmak için bir satıra tıklayın.",
  "Change what the map shows": "Haritanın ne gösterdiğini değiştirin",
  "{0} shows how much the ground moved, {1} how sure the measurement is, and {2} which places are reliable and which are only indicative.":
    "{0} zeminin ne kadar hareket ettiğini, {1} ölçümün ne kadar kesin olduğunu, {2} ise hangi yerlerin güvenilir, hangilerinin yalnızca gösterge olduğunu gösterir.",
  "Let the map present": "Haritanın sunmasına izin verin",
  "{0} flies through the five fastest basins automatically. Handy when you show this to someone.":
    "{0} en hızlı beş havzayı otomatik olarak gezer. Birine gösterirken işe yarar.",
  "Find and compare": "Bulun ve karşılaştırın",
  "Search a city, filter by confidence or country, rank by speed or by area, switch between line-of-sight and vertical values, or put two cities side by side.":
    "Bir şehir arayın, güvene ya da ülkeye göre filtreleyin, hıza ya da alana göre sıralayın, görüş hattı ile düşey değerler arasında geçiş yapın veya iki şehri yan yana koyun.",
  "Details below ↓": "Ayrıntılar aşağıda ↓",
  "Every measured place": "Ölçülen her yer",
  "The full ranked list. Click a place to see its sinking over time, its map and the caveats for that measurement.":
    "Sıralı tam liste. Bir yere tıklayın; zaman içindeki çökmesini, haritasını ve o ölçümle ilgili uyarıları görün.",
  "Rankings and downloads": "Sıralamalar ve indirmeler",
  "Further down: ranking tables for reliable and indicative places, the change log, and open downloads (JSON, GeoJSON, CSV) with a citation.":
    "Aşağıda: güvenilir ve gösterge niteliğindeki yerlerin sıralama tabloları, değişiklik günlüğü ve atıf bilgisiyle açık indirmeler (JSON, GeoJSON, CSV).",
  "See this again": "Tekrar izleyin",
  "That is it. Press {0} any time to replay this tour.": "Hepsi bu. Bu turu yeniden izlemek için istediğiniz zaman {0} düğmesine basın."
});

// ---- game/ (simulator) ----------------------------------------------------------------------------------
window.I18N_TR_PATTERNS.push(
  [/^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) (\d+)$/, m => ({JAN: 'OCA', FEB: 'ŞUB', MAR: 'MAR', APR: 'NİS', MAY: 'MAY', JUN: 'HAZ',
    JUL: 'TEM', AUG: 'AĞU', SEP: 'EYL', OCT: 'EKİ', NOV: 'KAS', DEC: 'ARA'})[m[1]] + ' ' + m[2]],
  [/^Differential subsidence reached ([\d.,−-]+) mm\/km near (.+), cutting canal conveyance by ([\d.,]+)%\. \(Reference bottleneck threshold vs\. NISAR gradients\)\.$/,
    m => `${m[2]} yakınında farklı çökme ${m[1]} mm/km'ye ulaştı ve kanalın taşıma kapasitesini %${m[3]} düşürdü. (Referans darboğaz eşiği ile NISAR eğimleri karşılaştırması.)`],
  [/^Domestic & Shallow Wells Failing in (.+)$/, m => `${m[1]} bölgesinde evsel ve sığ kuyular kuruyor`],
  [/^Readout: (.+)$/, m => `Gösterge: ${m[1]}`],
  [/^(.+) Freeboard & Conveyance Loss$/, (m, t) => `${t(m[1])}: Serbest Yükseklik ve Taşıma Kaybı`],
  [/^(Terra Bella|W\. Karapinar) vs NISAR (\d+)$/, m => `${m[1]} ve NISAR ${m[2]}`],
  [/^(Terra Bella|W\. Karapinar) vs (\d+) NISAR$/, m => `${m[1]} ve ${m[2]} NISAR`]
);

Object.assign(window.I18N_TR, {
  "NISAR Vision — Groundwater Simulator": "NISAR Vision — Yeraltı Suyu Simülatörü",
  "Groundwater Simulator": "Yeraltı Suyu Simülatörü",
  "NASA-ISRO NISAR · Interactive simulation": "NASA-ISRO NISAR · Etkileşimli simülasyon",
  "Provisional NISAR": "Geçici NISAR",
  "NISAR data are provisional. Calibration and validation are carried out by NASA-JPL and ISRO.": "NISAR verileri geçicidir. Kalibrasyon ve doğrulama NASA-JPL ve ISRO tarafından yapılmaktadır.",
  "Scenario": "Senaryo",
  "# Baseline": "# Temel durum",
  "Over-Pump": "Aşırı Pompalama",
  "Over-Pump · Click to stop": "Aşırı Pompalama · Durdurmak için tıkla",
  "SGMA Balance": "SGMA Dengesi",
  "? Guide": "? Rehber",
  "Classroom": "Sınıf",
  "Classroom mode: # lesson scenarios & discussion questions": "Sınıf modu: # ders senaryosu ve tartışma soruları",
  "Quick demo (# s) ⚡": "Hızlı demo (# sn) ⚡",
  "Quick demo (# s): automated #-month Over-Pump scenario": "Hızlı demo (# sn): otomatik #-aylık Aşırı Pompalama senaryosu",
  "Play an automated #-second run of the Over-Pump scenario": "Aşırı Pompalama senaryosunun otomatik #-saniyelik çalışmasını oynat",
  "Click to stop quick demo": "Hızlı demoyu durdurmak için tıkla",
  "⚡ QUICK DEMO · MONTH #/#": "⚡ HIZLI DEMO · AY #/#",
  "Stop demo ⏹": "Demoyu durdur ⏹",
  "Sources and model tests": "Kaynaklar ve model testleri",
  "WY#: Below Normal (#% Cap)": "SY#: Normalin Altında (%# Tavan)",
  "WY#: Below Normal (#% Surface Cap)": "SY#: Normalin Altında (%# Yüzey Suyu Tavanı)",
  "WY#: Above Normal (#% Surface Cap)": "SY#: Normalin Üstünde (%# Yüzey Suyu Tavanı)",
  "WY#: Critical (#% Surface Cap)": "SY#: Kritik (%# Yüzey Suyu Tavanı)",
  "WY#: Dry (#% Surface Cap)": "SY#: Kurak (%# Yüzey Suyu Tavanı)",
  "Satellite map with simulated sinking": "Simüle edilen çökmeyi gösteren uydu haritası",
  "Map overlay": "Harita katmanı",
  "Live Simulation": "Canlı Simülasyon",
  "Blend (Sim + NISAR)": "Karışım (Sim + NISAR)",
  "# NISAR Raster": "# NISAR Rasterı",
  "Study basin": "Çalışma havzası",
  "Tulare Basin, USA": "Tulare Havzası, ABD",
  "Konya Basin, Türkiye": "Konya Havzası, Türkiye",
  "Tulare Basin": "Tulare Havzası",
  "California, USA": "Kaliforniya, ABD",
  "Konya, Türkiye": "Konya, Türkiye",
  "Karapınar sub-basin, Konya Closed Basin": "Karapınar alt havzası, Konya Kapalı Havzası",
  "Canal tilt legend": "Kanal eğimi açıklaması",
  "Canal tilt": "Kanal eğimi",
  "{0}Low · under # mm/km": "{0}Düşük · # mm/km altı",
  "{0}Moderate · #–# mm/km": "{0}Orta · #–# mm/km",
  "{0}High · over # mm/km": "{0}Yüksek · # mm/km üstü",
  "{0}# mapped sinkholes": "{0}# haritalanmış obruk",
  "Month # of # · Autumn": "Ay # / # · Sonbahar",
  "Month # of # · Autumn · early year": "Ay # / # · Sonbahar · yıl başı",
  "Month # of # · Winter · wet recharge": "Ay # / # · Kış · yağışla beslenme",
  "Month # of # · Spring · snowmelt": "Ay # / # · İlkbahar · kar erimesi",
  "Month # of # · Summer · peak pumping": "Ay # / # · Yaz · en yoğun pompalama",
  "Subsidence over time": "Zaman içinde çökme",
  "Drag or scroll to see other months": "Diğer ayları görmek için sürükleyin ya da kaydırın",
  "Terra Bella vs # NISAR": "Terra Bella ve # NISAR",
  "Total sinking": "Toplam çökme",
  "Elastic: # cm": "Esnek: # cm",
  "Permanent": "Kalıcı",
  "Elastic Safe": "Esnek, güvenli",
  "Collapsing": "Çöküyor",
  "Farm revenue": "Çiftlik geliri",
  "#% cropped": "%# ekili",
  "Click a district on the map": "Haritada bir ilçeye tıklayın",
  "{0}Total sinking{1}Permanent{2}NISAR #": "{0}Toplam çökme{1}Kalıcı{2}NISAR #",
  "Water controls": "Su kontrolleri",
  "Monthly water use": "Aylık su kullanımı",
  "Applies to every district": "Tüm ilçelere uygulanır",
  "Groundwater pumping": "Yeraltı suyu pompalama",
  "Groundwater{0}pumping": "Yeraltı suyu{0}pompalama",
  "Canal water": "Kanal suyu",
  "Canal{0}water": "Kanal{0}suyu",
  "Land left to rest": "Dinlendirilen arazi",
  "Land left{0}to rest": "Dinlendirilen{0}arazi",
  "Not available this water year": "Bu su yılında kullanılamaz",
  "What happened": "Neler oldu",
  "Advance one month →": "Bir ay ilerle →",
  "+# months": "+# ay",
  "Simulate # months with the current settings": "Mevcut ayarlarla # ay simüle et",
  "Reset": "Sıfırla",
  "# months": "# ay",
  "# months later": "# ay sonra",
  "# Months Complete": "# Ay Tamamlandı",
  // start window
  "Choose a valley": "Bir vadi seçin",
  "Pick a valley": "Bir vadi seçin",
  "You run the water for a farming valley for {0}. Pump groundwater and the farms earn money, but the ground sinks. Pump too much, and part of that sinking never comes back.":
    "Bir tarım vadisinin suyunu {0} boyunca siz yönetiyorsunuz. Yeraltı suyu pompalarsanız çiftlikler para kazanır ama zemin çöker. Fazla pompalarsanız bu çökmenin bir kısmı hiç geri gelmez.",
  "{0}{1}Groundwater, canal water and how much land rests.": "{0}{1}Yeraltı suyu, kanal suyu ve ne kadar arazinin dinleneceği.",
  "{0}{1}Watch wells, canals and the ground respond.": "{0}{1}Kuyuların, kanalların ve zeminin tepkisini izleyin.",
  "{0}{1}Both were measured from space by NISAR in #": "{0}{1}İkisi de # yılında NISAR tarafından uzaydan ölçüldü",
  "Set the water": "Suyu ayarlayın",
  "Move month by month": "Ay ay ilerleyin",
  "Checking the model against {0}…": "Model {0} ile karşılaştırılıyor…",
  "Calibrated to ../data/central_valley/summary.json (# cm vert / # cm LOS)": "../data/central_valley/summary.json ile kalibre edildi (# cm düşey / # cm LOS)",
  "Start simulation →": "Simülasyonu başlat →",
  "Simulation ready — October #": "Simülasyon hazır — Ekim #",
  "Simulation ready — Tulare Basin, October #": "Simülasyon hazır — Tulare Havzası, Ekim #",
  "Simulation ready — Konya Closed Basin, October #": "Simülasyon hazır — Konya Kapalı Havzası, Ekim #",
  "Starting point tuned to match NASA-ISRO NISAR provisional measurements (### → ###).": "Başlangıç noktası NASA-ISRO NISAR geçici ölçümleriyle uyuşacak şekilde ayarlandı (### → ###).",
  "Starting water levels tuned to match NASA-ISRO NISAR provisional path # (Jun–Oct #).": "Başlangıç su seviyeleri NASA-ISRO NISAR geçici yörünge # ile uyuşacak şekilde ayarlandı (Haz–Eki #).",
  "Konya Closed Basin, #-day NISAR window": "Konya Kapalı Havzası, #-günlük NISAR dönemi",
  "Tulare Basin, #-day NISAR window": "Tulare Havzası, #-günlük NISAR dönemi",
  "sank in # days of summer # (# cm vertical)": "#2 yazının #1 gününde çöktü (#3 cm düşey)",
  "sank in # days of summer # (# cm vertical), near # sinkholes": "#2 yazının #1 gününde çöktü (#3 cm düşey), #4 obruğun yakınında",
  "Karapınar (# cm) is a sub-basin inside {0}": "Karapınar (# cm), {0} içindeki bir alt havzadır",
  "Konya": "Konya",
  "Konya Basin": "Konya Havzası",
  // events, water years
  "Water Year # Declaration: Above Normal Year": "Su Yılı # İlanı: Normalin Üstünde Yıl",
  "Water Year # Declaration: Below Normal Year": "Su Yılı # İlanı: Normalin Altında Yıl",
  "Water Year # Declaration: Dry Year": "Su Yılı # İlanı: Kurak Yıl",
  "Water Year # Declaration: Critical Year": "Su Yılı # İlanı: Kritik Yıl",
  "California DWR SJV Water Year Index sets WY# to Above Normal. Full or near-full surface deliveries (#% cap) available.":
    "Kaliforniya DWR SJV Su Yılı Endeksi SY# için Normalin Üstünde dedi. Tam ya da tama yakın yüzey suyu teslimatı (%# tavan) mevcut.",
  "California DWR SJV Water Year Index sets WY# to Dry. Surface allocations capped at #% under seasonal quota rules.":
    "Kaliforniya DWR SJV Su Yılı Endeksi SY# için Kurak dedi. Yüzey suyu payları mevsimlik kota kurallarıyla %# ile sınırlandı.",
  "California DWR SJV Water Year Index sets WY# to Critical. Surface allocations capped at #% under seasonal quota rules.":
    "Kaliforniya DWR SJV Su Yılı Endeksi SY# için Kritik dedi. Yüzey suyu payları mevsimlik kota kurallarıyla %# ile sınırlandı.",
  "Anatolian Interior Precipitation Index (illustrative) sets WY# to Below Normal. Full or near-full surface deliveries (#% cap) available.":
    "İç Anadolu Yağış Endeksi (temsili) SY# için Normalin Altında dedi. Tam ya da tama yakın yüzey suyu teslimatı (%# tavan) mevcut.",
  "Water table dropped to # m depth, dewatering #/# tracked representative wells (illustrative threshold).":
    "Su tablası # m derinliğe indi; izlenen # / # temsili kuyu kurudu (temsili eşik).",
  "Sinkhole risk indicator elevated in W. Karapinar": "Batı Karapınar'da obruk risk göstergesi yükseldi",
  "Subsidence reached # cm below historical groundwater lows near # documented obruks (## km ring NISAR mean # cm). Indicator only; does not predict collapse of individual sinkholes.":
    "Belgelenmiş #2 obruğun yakınında, yeraltı suyu tarihî en düşük seviyesinin altında çökme #1 cm'ye ulaştı (#3#4 km halka NISAR ortalaması #5 cm). Yalnızca göstergedir; tek tek obrukların çökmesini öngörmez.",
  "California Aqueduct": "California Su Kemeri",
  "Karapinar D# Corridor": "Karapınar D# Koridoru",
  "Friant-Kern Canal": "Friant-Kern Kanalı",
  "Alta East Branch Canal": "Alta Doğu Kolu Kanalı",
  "California Aqueduct (West)": "California Su Kemeri (Batı)",
  "Tulare Irrigation District Canal": "Tulare Sulama Bölgesi Kanalı",
  // end window
  "Your valley vs what NISAR measured": "Sizin vadiniz ve NISAR'ın ölçtüğü",
  "Quick demo result (Over-Pump # months)": "Hızlı demo sonucu (Aşırı Pompalama, # ay)",
  "What this means: Heavy groundwater pumping dropped levels past historical lows, locking in # cm of permanent clay collapse near Terra Bella. Even future wet winters cannot restore that lost underground pore storage.":
    "Bunun anlamı: Yoğun yeraltı suyu pompalaması seviyeleri tarihî en düşük değerlerin altına indirdi ve Terra Bella yakınında # cm kalıcı kil çökmesine yol açtı. Gelecekteki yağışlı kışlar bile kaybedilen yeraltı gözenek deposunu geri getiremez.",
  "What this means: Limiting groundwater extraction balanced winter recharge and kept permanent collapse to # cm across the basin. Surface corridor gradients stayed within safe design limits.":
    "Bunun anlamı: Yeraltı suyu çekimini sınırlamak kış beslenmesini dengeledi ve havza genelinde kalıcı çökmeyi # cm'de tuttu. Yüzey koridorlarının eğimleri güvenli tasarım sınırları içinde kaldı.",
  "What this means: Summer irrigation temporarily pushed hotspots past historical lows, causing # cm of permanent clay collapse near W. Karapinar. Reducing summer pumping peaks before dry years protects surface corridors and shallow wells. Sinkhole risk indicators are elevated near mapped obruks (indicator only).":
    "Bunun anlamı: Yaz sulaması sıcak noktaları geçici olarak tarihî en düşük seviyelerin altına itti ve Batı Karapınar yakınında # cm kalıcı kil çökmesine yol açtı. Kurak yıllardan önce yaz pompalama tepe değerlerini azaltmak yüzey koridorlarını ve sığ kuyuları korur. Haritalanmış obrukların yakınında obruk risk göstergeleri yüksek (yalnızca gösterge).",
  "Figure # Simulated sinking per district against the # NISAR vertical estimate. Data: NASA-ISRO NISAR, ASF DAAC. Analysis: Team Aseltech.":
    "Şekil # İlçe başına simüle edilen çökme ve # NISAR düşey tahmini. Veri: NASA-ISRO NISAR, ASF DAAC. Analiz: Aseltech Takımı.",
  "Your # months vs NISAR # by district": "İlçe bazında sizin # ayınız ve NISAR #",
  "Your simulation": "Sizin simülasyonunuz",
  "Most sinking": "En fazla çökme",
  "Permanent part": "Kalıcı kısım",
  "Largest canal capacity loss": "En büyük kanal kapasite kaybı",
  "Wells run dry": "Kuruyan kuyular",
  "# wells": "# kuyu",
  "NISAR # (real)": "NISAR # (gerçek)",
  "#-day peak, line of sight": "#-günlük tepe değer, görüş hattı",
  "Same, as vertical": "Aynısı, düşey olarak",
  "Summer rate, per year": "Yaz hızı, yıllık",
  "High-risk sections mapped": "Haritalanan yüksek riskli kesimler",
  "# / # segments": "# / # kesim",
  "# / # corridors · # obruks": "# / # koridor · # obruk",
  "GPS check": "GPS kontrolü",
  "# (RMSE # cm)": "# (RMSE # cm)",
  "# cm (#% irreversible)": "# cm (%# geri dönüşsüz)",
  "# cm/yr LOS": "# cm/yıl LOS",
  "#–# km Obruk Ring NISAR Mean": "#–# km Obruk Halkası NISAR Ortalaması",
  "#-day NISAR repeat & sinkholes:": "#-günlük NISAR tekrarı ve obruklar:",
  "#-day NISAR monitoring & Karapınar sinkholes:": "#-günlük NISAR izlemesi ve Karapınar obrukları:",
  "See where else the ground is sinking → Atlas": "Yerin başka nerede çöktüğünü görün → Atlas",
  "Atlas: Konya Plain (rank # # cm / # cm/#d common) →": "Atlas: Konya Ovası (sıra # # cm / # cm/#g ortak) →",
  "Copy summary": "Özeti kopyala",
  "Inspect map": "Haritayı incele",
  "Play again": "Yeniden oyna",
  "# cm simulated vs # cm measured · error # %": "# cm simüle, # cm ölçülen · hata %#",
  "error: #%": "hata: %#",
  "vertical, cm": "düşey, cm",
  "# cm (Terra Bella)": "# cm (Terra Bella)",
  "# cm LOS": "# cm LOS",
  "# cm → # cm LOS → # cm": "# cm → # cm LOS → # cm",
  // classroom
  "Classroom Mode": "Sınıf Modu",
  "Classroom scenarios": "Sınıf senaryoları",
  "Educator Lesson Plan · #-Minute Lab (Grades #–#)": "Öğretmen Ders Planı · #-Dakikalık Laboratuvar (#–#. sınıflar)",
  "Run one of the three #-month scenarios in one click on the active valley, then use the discussion questions below with {0}.":
    "Etkin vadide üç #-aylık senaryodan birini tek tıkla çalıştırın, ardından aşağıdaki tartışma sorularını {0} ile kullanın.",
  "Normal Year": "Normal Yıl",
  "Multi-Year Drought": "Çok Yıllık Kuraklık",
  "Sustainable Pumping": "Sürdürülebilir Pompalama",
  "Below Normal → Above Normal · #% pump · #% canal · #% fallow": "Normalin Altında → Normalin Üstünde · %# pompa · %# kanal · %# nadas",
  "Dry → Critical · #% pump · #% canal · #% fallow": "Kurak → Kritik · %# pompa · %# kanal · %# nadas",
  "Below Normal → Dry · #% pump · #% canal · #% fallow": "Normalin Altında → Kurak · %# pompa · %# kanal · %# nadas",
  "Scenario #": "Senaryo #",
  "Scenario # · Lesson Plan Trial A": "Senaryo # · Ders Planı Deneme A",
  "Scenario # · Lesson Plan Trial B": "Senaryo # · Ders Planı Deneme B",
  "Tulare Basin · Scenario #: Normal Year (Below Normal → Above Normal · #% Pump)": "Tulare Havzası · Senaryo #: Normal Yıl (Normalin Altında → Normalin Üstünde · %# Pompa)",
  "Tulare Basin · Scenario #: Multi-Year Drought (Dry → Critical · #% Pump)": "Tulare Havzası · Senaryo #: Çok Yıllık Kuraklık (Kurak → Kritik · %# Pompa)",
  "Tulare Basin · Scenario #: Sustainable Pumping (Below Normal → Dry · #% Pump · #% Fallow)": "Tulare Havzası · Senaryo #: Sürdürülebilir Pompalama (Normalin Altında → Kurak · %# Pompa · %# Nadas)",
  "Classroom debrief": "Sınıf değerlendirmesi",
  "# Classroom Discussion Questions": "# Sınıf Tartışma Sorusu",
  "Elastic vs. permanent compaction:": "Esnek ve kalıcı sıkışma:",
  "Elastic rebound vs. permanent clay compaction:": "Esnek geri kabarma ve kalıcı kil sıkışması:",
  "Canal tilt (mm/km) vs. uniform sinking:": "Kanal eğimi (mm/km) ve düzgün çökme:",
  "Canal tilt (mm/km) vs. total depth:": "Kanal eğimi (mm/km) ve toplam derinlik:",
  "{0} Why does winter recharge lift the ground slightly while drawdown below {1} locks in permanent sinking?":
    "{0} Neden kış beslenmesi zemini biraz yükseltirken {1} altına inen su seviyesi kalıcı çökmeye yol açar?",
  "{0} Why does winter recharge restore part of the land height while pumping below the preconsolidation head ({1}) locks in permanent compaction?":
    "{0} Neden kış beslenmesi arazi yüksekliğinin bir kısmını geri getirirken ön konsolidasyon yükünün ({1}) altına pompalama kalıcı sıkışmaya yol açar?",
  "{0} Why do gradients like {1} (Tulare Irrigation District Canal) and {2} (California Aqueduct) disrupt gravity flow more than uniform sinking?":
    "{0} Neden {1} (Tulare Sulama Bölgesi Kanalı) ve {2} (California Su Kemeri) gibi eğimler, cazibeli akışı düzgün çökmeden daha çok bozar?",
  "{0} Why does {1} on the California Aqueduct or {2} on the Tulare Canal disrupt gravity flow more than uniform sinking?":
    "{0} Neden California Su Kemeri'ndeki {1} ya da Tulare Kanalı'ndaki {2}, cazibeli akışı düzgün çökmeden daha çok bozar?",
  "#-day NISAR repeat & sinkholes": "#-günlük NISAR tekrarı ve obruklar",
  "{0} How can managers in Tulare and Konya ({1} faster sinking within # km of mapped sinkholes) use #-day updates without claiming exact collapse dates?":
    "{0} Tulare ve Konya'daki yöneticiler (haritalanmış obrukların # km yakınında {1} daha hızlı çökme), kesin çökme tarihi iddia etmeden #-günlük güncellemeleri nasıl kullanabilir?",
  "{0} How does {1} faster sinking within # km of # mapped sinkholes guide field priorities without predicting an exact collapse date?":
    "{0} #2 haritalanmış obruğun #1 km yakınındaki {1} daha hızlı çökme, kesin bir çökme tarihi öngörmeden saha önceliklerini nasıl yönlendirir?",
  "income $#M → $#M · sinking # → # cm": "gelir $#M → $#M · çökme # → # cm",
  "water # → # m · permanent # → # cm": "su # → # m · kalıcı # → # cm",
  // sources & verification window
  "Sources & verification": "Kaynaklar ve doğrulama",
  "Sources or model tests": "Kaynaklar ya da model testleri",
  "Sources & parameters": "Kaynaklar ve parametreler",
  "Model verification": "Model doğrulaması",
  "How the model works and how it was checked": "Model nasıl çalışıyor ve nasıl kontrol edildi",
  "One-dimensional Terzaghi compaction: clay springs back while the water stays above its lowest level ever ({0}) and is squeezed for good below it. Specific yield {1} = #; pumping scale {2} = #":
    "Tek boyutlu Terzaghi sıkışması: su şimdiye kadarki en düşük seviyesinin ({0}) üstünde kaldıkça kil geri kabarır, altına inince kalıcı olarak sıkışır. Özgül verim {1} = #; pompalama ölçeği {2} = #",
  "Parameter": "Parametre",
  "Value": "Değer",
  "Provenance / Tag": "Kaynak / Etiket",
  "Model": "Model",
  "Physics": "Fizik",
  "Calibration": "Kalibrasyon",
  "Integrity": "Bütünlük",
  "Reference data": "Referans veri",
  "Check and pass criterion": "Kontrol ve geçme ölçütü",
  "Measured result": "Ölçülen sonuç",
  "Status": "Durum",
  "PASS": "GEÇTİ",
  "SOURCED": "KAYNAKLI",
  "ILLUSTRATIVE": "TEMSİLİ",
  "Run": "Çalıştır",
  "Running the model checks in your browser…": "Model kontrolleri tarayıcınızda çalışıyor…",
  "Each check runs the simulation model live in this browser against the repository's NISAR data files (data/central_valley, data/karapinar). Results are computed now, not stored.":
    "Her kontrol, simülasyon modelini bu tarayıcıda canlı olarak deponun NISAR veri dosyalarına (data/central_valley, data/karapinar) karşı çalıştırır. Sonuçlar kayıtlı değil, şu anda hesaplanır.",
  "# / # passed": "# / # geçti",
  "Specific Yield (S_y)": "Özgül Verim (S_y)",
  "Elastic Skeletal Storage (S_ske)": "Esnek İskelet Depolaması (S_ske)",
  "Inelastic Skeletal Storage (S_skv)": "Esnek Olmayan İskelet Depolaması (S_skv)",
  "Compressible Clay Interbeds (b#)": "Sıkışabilir Kil Ara Katmanları (b#)",
  "(Aggregate thickness)": "(Toplam kalınlık)",
  "(dimensionless)": "(birimsiz)",
  "Model Check Factor (k)": "Model Kontrol Katsayısı (k)",
  "(Multiplier (Tulare Basin, USA #-day benchmark))": "(Çarpan (Tulare Havzası, ABD #-günlük referans))",
  "Critical-year surface water cap": "Kritik yıl yüzey suyu tavanı",
  "Water Year Probabilities & Caps": "Su Yılı Olasılıkları ve Tavanları",
  "(Probability / %)": "(Olasılık / %)",
  "Formula from DWR WSIHIST; class probabilities illustrative": "Formül DWR WSIHIST'ten; sınıf olasılıkları temsilidir",
  "DWR #-class weights (#–#% cap) {0}": "DWR #-sınıflı ağırlıklar (%#–# tavan) {0}",
  "Canal Capacity Loss Curve": "Kanal Kapasite Kaybı Eğrisi",
  "(% conveyance drop)": "(% taşıma düşüşü)",
  "Up to #% above # mm/km {0}": "#2 mm/km üstünde %#1'e kadar {0}",
  "Friant-Kern >#% capacity loss verified (FWA/KVPR); onset threshold illustrative": "Friant-Kern'de >%# kapasite kaybı doğrulandı (FWA/KVPR); başlangıç eşiği temsilidir",
  "Well Failure Depths & Crop Prices": "Kuyu Kuruma Derinlikleri ve Ürün Fiyatları",
  "(wells / USD)": "(kuyular / USD)",
  "Representative depths & $/ha {0}": "Temsili derinlikler ve $/ha {0}",
  "Baseline Demand / Recharge": "Temel Talep / Beslenme",
  "Stylized regional baseline per district": "İlçe başına sadeleştirilmiş bölgesel temel durum",
  "#–# m across districts {0}": "İlçeler arasında #–# m {0}",
  "Simplified Tulare bucket irrigation demand curve": "Sadeleştirilmiş Tulare kova tipi sulama talep eğrisi",
  "Validation GNSS r (CAHA)": "Doğrulama GNSS r (CAHA)",
  "CVHM SUB aggregate interbeds (Corcoran Clay alone <= # m per Page #)": "CVHM SUB toplam ara katmanları (yalnızca Corcoran Kili <= # m, Page #)",
  "Order of magnitude (~#x S_ske), Sneed (#) USGS OFR ## (>=#x ratio); exact value not verified": "Büyüklük mertebesi (~#x S_ske), Sneed (#) USGS OFR ## (>=#x oran); kesin değer doğrulanmadı",
  "Order of magnitude, Sneed (#) USGS OFR ##; exact m^# value not verified in full PDF": "Büyüklük mertebesi, Sneed (#) USGS OFR ##; kesin m^# değeri tam PDF'te doğrulanmadı",
  "Williamson, Prudic & Swain (#) USGS PP #-D — Tulare/SJV cited average # (range #–#)": "Williamson, Prudic & Swain (#) USGS PP #-D — Tulare/SJV için verilen ortalama # (aralık #–#)",
  "Source: ../data/central_valley/summary.json": "Kaynak: ../data/central_valley/summary.json",
  "Source: ../data/karapinar/summary.json": "Kaynak: ../data/karapinar/summary.json",
  "Source: California DWR SJV Water Year Index": "Kaynak: Kaliforniya DWR SJV Su Yılı Endeksi",
  "Source: Anatolian Interior Precipitation Index (illustrative)": "Kaynak: İç Anadolu Yağış Endeksi (temsili)",
  "Source: Illustrative well-depth curve calibrated to SJV shallow domestic wells": "Kaynak: SJV sığ evsel kuyularına göre kalibre edilmiş temsili kuyu derinliği eğrisi",
  "Source: data/central_valley/assets.json / USGS SIR ##": "Kaynak: data/central_valley/assets.json / USGS SIR ##",
  "Source: data/karapinar/assets.json & sinkholes.geojson (indicator only)": "Kaynak: data/karapinar/assets.json ve sinkholes.geojson (yalnızca gösterge)",
  "Model check against NISAR (PASS ±#% · Tulare Basin):": "NISAR'a karşı model kontrolü (GEÇTİ ±%# · Tulare Havzası):",
  "Model check against NISAR (PASS ±#% · Konya Closed Basin):": "NISAR'a karşı model kontrolü (GEÇTİ ±%# · Konya Kapalı Havzası):",
  "{0} Under baseline summer pumping for the #-day NISAR window (### → ###), the model simulates {1} vertical ({2} LOS) at Terra Bella / Pixley Corridor vs {3} vertical ({4} LOS; ref range #…# cm LOS) measured by NISAR ({5}, extraction scale factor {6}).":
    "{0} #-günlük NISAR döneminde (### → ###) temel yaz pompalamasıyla model, Terra Bella / Pixley Koridoru'nda {1} düşey ({2} LOS) simüle ediyor; NISAR'ın ölçtüğü ise {3} düşey ({4} LOS; referans aralığı #…# cm LOS) ({5}, çekim ölçek katsayısı {6}).",
  "{0} Under baseline summer pumping for the #-day NISAR window (### → ###), the model simulates {1} vertical ({2} LOS) at West Karapinar Core vs {3} vertical ({4} LOS; # deg incidence; # documented obruks) measured by NISAR ({5}, extraction scale factor {6}).":
    "{0} #-günlük NISAR döneminde (### → ###) temel yaz pompalamasıyla model, Batı Karapınar Merkezi'nde {1} düşey ({2} LOS) simüle ediyor; NISAR'ın ölçtüğü ise {3} düşey ({4} LOS; # derece geliş açısı; # belgelenmiş obruk) ({5}, çekim ölçek katsayısı {6}).",
  "Simulated vertical sinking within ±# % of NISAR (summary.json)": "Simüle edilen düşey çökme NISAR'ın ±%# içinde (summary.json)",
  "Terra Bella (p#) carries the NISAR value from points.json (# cm LOS)": "Terra Bella (p#), points.json'daki NISAR değerini taşıyor (# cm LOS)",
  "Measured points loaded from repository data": "Ölçülen noktalar depo verisinden yüklendi",
  "Line-of-sight ↔ vertical conversion": "Görüş hattı ↔ düşey dönüşümü",
  "Round trip at #° incidence returns the input (|error| < #⁻⁹ cm)": "#° geliş açısında gidiş-dönüş girdiyi geri veriyor (|hata| < #⁻⁹ cm)",
  "Permanent clay compaction does not recover": "Kalıcı kil sıkışması geri dönmez",
  "After a wet winter the water rises, but permanent sinking stays locked in": "Yağışlı bir kıştan sonra su yükselir ama kalıcı çökme olduğu yerde kalır",
  "Permanent sinking only accumulates": "Kalıcı çökme yalnızca birikir",
  "With pumping switched on and off every # months, permanent sinking never decreases": "Pompalama her # ayda bir açılıp kapatıldığında kalıcı çökme hiç azalmıyor",
  "More pumping, more sinking": "Daha çok pompalama, daha çok çökme",
  "# % pumping sinks more than # %, which sinks more than conservation (# %, # % fallow)": "%# pompalama %#'den fazla çökertir, o da tasarruftan (%#, %# nadas) fazla çökertir",
  "# %: # cm · # %: # cm · conservation: # cm": "%#: # cm · %#: # cm · tasarruf: # cm",
  "No pumping, wet years: no permanent sinking": "Pompalama yok, yağışlı yıllar: kalıcı çökme yok",
  "Permanent compaction stays at # cm in every district (|value| < # cm)": "Kalıcı sıkışma her ilçede # cm'de kalıyor (|değer| < # cm)",
  "largest permanent value # cm across # districts": "#2 ilçede en büyük kalıcı değer #1 cm",
  "Physical limits respected under extreme pumping": "Aşırı pompalamada fiziksel sınırlara uyuluyor",
  "Surface water held at ≤ # % and no NaN or infinite value over # months": "Yüzey suyu ≤ %# düzeyinde tutuluyor; # ay boyunca NaN ya da sonsuz değer yok",
  "max surface # % · # months · finite: true": "en fazla yüzey %# · # ay · sonlu: evet",
  "Canal capacity loss stays within #–# % and dry wells never exceed the wells modelled": "Kanal kapasite kaybı %#–# içinde kalıyor ve kuru kuyu sayısı modellenen kuyu sayısını hiç aşmıyor",
  "max canal loss # % · max dry wells #": "en büyük kanal kaybı %# · en fazla kuru kuyu #",
  "Fallowing trades income for ground": "Nadas, geliri zemine karşı takas eder",
  "Resting # % of land lowers farm income and does not increase sinking": "Arazinin %#'ini dinlendirmek çiftlik gelirini düşürür ve çökmeyi artırmaz",
  "Reproducible results": "Tekrarlanabilir sonuçlar",
  "Two runs with identical inputs give identical outputs in every district": "Aynı girdilerle iki çalıştırma her ilçede aynı çıktıyı veriyor",
  "# districts compared · Terra Bella # cm both runs": "# ilçe karşılaştırıldı · Terra Bella iki çalıştırmada da # cm",
  "Sinkhole risk indicator responds to heavy pumping": "Obruk risk göstergesi yoğun pompalamaya tepki veriyor",
  "# Konya districts load from NISAR data; two dry years at # % raise the indicator": "# Konya ilçesi NISAR verisinden yükleniyor; %# ile iki kurak yıl göstergeyi yükseltiyor",
  "# districts · p# # cm LOS · indicator raised": "# ilçe · p# # cm LOS · gösterge yükseldi",
  "# districts · p# = # cm LOS": "# ilçe · p# = # cm LOS",
  "# months checked · final permanent # cm": "# ay kontrol edildi · son kalıcı değer # cm",
  "#-second run": "#-saniyelik çalışma",
  "model.js v#": "model.js v#",
  "Springs back": "Geri kabarır",
  "Drought & Groundwater Withdrawal": "Kuraklık ve Yeraltı Suyu Çekimi",
  "Levees & Dams": "Setler ve Barajlar",
  "Sinkholes & Cavern Collapse": "Obruklar ve Mağara Çökmesi",
  "Soil Moisture & Water Resources": "Toprak Nemi ve Su Kaynakları",
  "Policy response": "Politika tepkisi",
  "Data: NASA-ISRO NISAR (provisional), ASF DAAC, NGL GNSS, OpenStreetMap. Well depths and crop prices are illustrative.":
    "Veri: NASA-ISRO NISAR (geçici), ASF DAAC, NGL GNSS, OpenStreetMap. Kuyu derinlikleri ve ürün fiyatları temsilidir.",
  "NASA Space Apps Challenge Resources & Land Subsidence StoryMap Framework": "NASA Space Apps Challenge Kaynakları ve Arazi Çökmesi StoryMap Çerçevesi",
  "NISAR Land Subsidence StoryMap": "NISAR Arazi Çökmesi StoryMap",
  "# NASA NISAR Land Subsidence StoryMap (#–# UAVSAR → # Spaceborne NISAR):": "# NASA NISAR Arazi Çökmesi StoryMap (#–# UAVSAR → # uzaydan NISAR):",
  "{0} NASA's official {1} (Peacock, A., An, K., Pinto, N., & Lou, Y., # {2}, Zenodo, {3}) demonstrated with airborne L-band UAVSAR that groundwater pumping in California's Central Valley formed a deep subsidence bowl and sank segments of the {4} by more than # inches (># cm, or ~#–# cm/yr) between # and # (Miller et al. #; Jones et al. #). Our # simulator and risk dossier extend that exact framework from space using provisional NISAR L# GUNW radar (recording # cm LOS / # mm/km tilt along the California Aqueduct in # summer days), GPS validation, and OpenStreetMap conveyance networks.":
    "{0} NASA'nın resmî {1} (Peacock, A., An, K., Pinto, N., & Lou, Y., #1 {2}, Zenodo, {3}), havadan L-bant UAVSAR ile Kaliforniya'nın Central Valley bölgesinde yeraltı suyu pompalamasının derin bir çökme çanağı oluşturduğunu ve #6 ile #7 arasında {4} kesimlerini #2 inçten (>#3 cm, yani ~#4–#5 cm/yıl) fazla çökerttiğini gösterdi (Miller vd. #8; Jones vd. #9). #10 simülatörümüz ve risk dosyamız, aynı çerçeveyi geçici NISAR L#11 GUNW radarı (California Su Kemeri boyunca #14 yaz gününde #12 cm LOS / #13 mm/km eğim kaydı), GPS doğrulaması ve OpenStreetMap su iletim ağlarıyla uzaydan genişletiyor.",
  "NISAR Applications White Papers ({0}):": "NISAR Uygulama Teknik Raporları ({0}):",
  "{0} {1} (early centimetre-scale deformation monitoring), {2} (surface-water curtailment → pumping → clay compaction), {3} (precursor deformation in carbonate terrains such as Karapınar, indicator only), {4}, and {5}.":
    "{0} {1} (erken santimetre ölçekli deformasyon izleme), {2} (yüzey suyu kısıtlaması → pompalama → kil sıkışması), {3} (Karapınar gibi karbonatlı arazilerde öncü deformasyon, yalnızca gösterge), {4} ve {5}.",
  "NISAR Data User Guide & SAR Education:": "NISAR Veri Kullanıcı Kılavuzu ve SAR Eğitimi:",
  "{0} {1}, {2}, {3}, and {4}.": "{0} {1}, {2}, {3} ve {4}.",
  "ASF NISAR Data User Guide": "ASF NISAR Veri Kullanıcı Kılavuzu",
  "NASA Earthdata Intro to SAR": "NASA Earthdata SAR'a Giriş",
  "NASA ARSET SAR Trainings": "NASA ARSET SAR Eğitimleri",
  "NASA Societal Benefits": "NASA Toplumsal Faydalar",
  "NASA/JPL UAVSAR Postcards": "NASA/JPL UAVSAR Kartpostalları",
  "NISAR ArcGIS Storymaps": "NISAR ArcGIS Storymaps",
  // tour (game/tour_steps.js)
  "How the simulator works": "Simülatör nasıl çalışır",
  "You run the water for a farming valley, month by month. Pump too much groundwater and the ground sinks for good, the same thing NISAR measures from space. Here is a quick look around.":
    "Bir tarım vadisinin suyunu ay ay siz yönetiyorsunuz. Fazla yeraltı suyu pompalarsanız zemin kalıcı olarak çöker; NISAR'ın uzaydan ölçtüğü de tam olarak bu. İşte hızlı bir tanıtım.",
  "The valley": "Vadi",
  "The colours show how far each district has sunk in the simulation. Canals change colour as the ground under them tilts and they lose capacity.":
    "Renkler her ilçenin simülasyonda ne kadar çöktüğünü gösteriyor. Kanallar, altlarındaki zemin eğildikçe ve kapasite kaybettikçe renk değiştiriyor.",
  "Compare with the satellite": "Uyduyla karşılaştırın",
  "{0} is your valley. {1} is what the radar really measured. {2} lays one over the other.":
    "{0} sizin vadiniz. {1} radarın gerçekten ölçtüğü. {2} ikisini üst üste koyar.",
  "Pick a basin": "Bir havza seçin",
  "Switch between the Tulare Basin in California and the Konya Basin in Türkiye.": "Kaliforniya'daki Tulare Havzası ile Türkiye'deki Konya Havzası arasında geçiş yapın.",
  "Your three controls": "Üç kontrolünüz",
  "Drag the bars: how much {0} to pump, how much {1} arrives by canal, and how much farmland to {2} (leave unplanted). Less pumping means less sinking, but also less farm income.":
    "Çubukları sürükleyin: ne kadar {0} pompalanacağı, kanalla ne kadar {1} geleceği ve ne kadar tarım arazisinin {2} (ekilmeden bırakılacağı). Daha az pompalama daha az çökme demek, ama aynı zamanda daha az çiftlik geliri.",
  "groundwater": "yeraltı suyu",
  "surface water": "yüzey suyu",
  "fallow": "nadasa bırakılacağı",
  "Move time forward": "Zamanı ilerletin",
  "Each press runs one month with your settings. {0} jumps ahead, {1} starts over. Keyboard: {2} or {3}.":
    "Her basış ayarlarınızla bir ay çalıştırır. {0} ileri atlar, {1} baştan başlatır. Klavye: {2} ya da {3}.",
  "+6 months": "+6 ay",
  "Space": "Boşluk",
  "Sinking over time": "Zaman içinde çökme",
  "Your sinking month by month, next to the # NISAR measurement for the same place.": "Ay ay sizin çökmeniz, aynı yer için # NISAR ölçümünün yanında.",
  "The trade-off": "Denge",
  "Total and permanent sinking against farm revenue. The goal is to keep the farms running without sinking the ground for good.":
    "Toplam ve kalıcı çökme ile çiftlik geliri karşı karşıya. Amaç, zemini kalıcı olarak çökertmeden çiftlikleri ayakta tutmak.",
  "Wells running dry, canals losing capacity, drought years: every month’s events are written here.":
    "Kuruyan kuyular, kapasite kaybeden kanallar, kurak yıllar: her ayın olayları buraya yazılır.",
  "Ready-made scenarios": "Hazır senaryolar",
  "Try {0} or {1} (California’s groundwater law) to see the two extremes, or press {2} for a #-second automatic run.":
    "İki ucu görmek için {0} ya da {1} (Kaliforniya'nın yeraltı suyu yasası) deneyin veya #-saniyelik otomatik çalışma için {2} düğmesine basın.",
  "Quick demo": "Hızlı demo",
  "That is all. Press {0} any time to replay this tour.": "Hepsi bu. Bu turu yeniden izlemek için istediğiniz zaman {0} düğmesine basın.",
  "Guide": "Rehber"
});

// ---- science.html -----------------------------------------------------------------------------------------
Object.assign(window.I18N_TR, {
  "Science & Method (#-Region Atlas) — NISAR Vision": "Bilim ve Yöntem (#-Bölgelik Atlas) — NISAR Vision",
  "Science & method": "Bilim ve yöntem",
  "From radar phase to centimetres": "Radar fazından santimetreye",
  "Everything we show is computed from NASA-ISRO NISAR Level# products with open, tested code. This page explains each step, the corrections we apply, how we checked the result, and what it cannot tell you.":
    "Gösterdiğimiz her şey NASA-ISRO NISAR Seviye-# ürünlerinden açık ve test edilmiş kodla hesaplanıyor. Bu sayfa her adımı, uyguladığımız düzeltmeleri, sonucu nasıl kontrol ettiğimizi ve sonucun neyi söyleyemeyeceğini açıklıyor.",
  "Results": "Sonuçlar",
  "Results registry": "Sonuç kaydı",
  "In short": "Kısaca",
  "What was measured.": "Ne ölçüldü.",
  "{0} NISAR radar image pairs over California, Türkiye and the UK, June–October # turned into centimetres of ground motion with tested, open code.":
    "{0} Kaliforniya, Türkiye ve Birleşik Krallık üzerindeki NISAR radar görüntü çiftleri (Haziran–Ekim #), test edilmiş açık kodla santimetre cinsinden yer hareketine çevrildi.",
  "The main result.": "Ana sonuç.",
  "{0} Parts of California's Central Valley moved up to {1} cm away from the satellite in # days; depending on the stable area used as reference the value lies between {2} cm.":
    "{0} Kaliforniya'nın Central Valley bölgesinin bazı kesimleri # günde uydudan uzağa {1} cm'ye kadar hareket etti; referans alınan sabit bölgeye göre değer {2} cm arasında değişiyor.",
  "How we checked it.": "Nasıl kontrol ettik.",
  "{0} Against {1} GPS stations (typical difference about {2} cm where the ground sinks) and against a second, independent satellite pass from the opposite direction.":
    "{0} {1} GPS istasyonuyla (zeminin çöktüğü yerlerde tipik fark yaklaşık {2} cm) ve ters yönden geçen ikinci, bağımsız bir uydu geçişiyle.",
  "What it means.": "Ne anlama geliyor.",
  "{0} Uneven sinking tilts canals and roads; in Karapınar the ground sank faster close to documented sinkholes. Over London no movement above the noise was found.":
    "{0} Düzensiz çökme kanalları ve yolları eğiyor; Karapınar'da zemin belgelenmiş obrukların yakınında daha hızlı çöktü. Londra üzerinde gürültünün üstünde hareket bulunmadı.",
  "What it cannot tell.": "Neyi söyleyemez.",
  "{0} One summer only, so yearly rates are estimates; the satellite sees the ground at a slant; NISAR data are still provisional.":
    "{0} Yalnızca bir yaz var, bu yüzden yıllık hızlar tahmindir; uydu zemini eğik açıyla görür; NISAR verileri hâlâ geçicidir.",
  "Key findings": "Temel bulgular",
  "# · Data": "# · Veri",
  "# Data": "# Veri",
  "# · Phase → centimetres": "# · Faz → santimetre",
  "# Phase → cm": "# Faz → cm",
  "# · Time series": "# · Zaman serisi",
  "# Time series": "# Zaman serisi",
  "# · Validation against GPS": "# · GPS ile doğrulama",
  "# Validation": "# Doğrulama",
  "# · Infrastructure risk index": "# · Altyapı risk endeksi",
  "# Risk index": "# Risk endeksi",
  "# · Limits": "# · Sınırlar",
  "# Limits": "# Sınırlar",
  "# · Calibration status": "# · Kalibrasyon durumu (İngilizce rapor)",
  "# Calibration status": "# Kalibrasyon durumu",
  "# · Sources": "# · Kaynaklar (İngilizce rapor)",
  "# Sources": "# Kaynaklar",
  "Comparison with published studies": "Yayımlanmış çalışmalarla karşılaştırma (İngilizce rapor)",
  "Uncertainty budget": "Belirsizlik bütçesi (İngilizce rapor)",
  "Validation report": "Doğrulama raporu (İngilizce rapor)",
  "Infrastructure risk dossier": "Altyapı risk dosyası (İngilizce rapor)",
  "Global Atlas time-series QC (Top # check)": "Küresel Atlas zaman serisi kalite kontrolü (İlk # kontrolü) (İngilizce rapor)",
  "Learn more": "Daha fazla bilgi",
  "Product": "Ürün",
  "What it is": "Nedir",
  "Use here": "Burada kullanımı",
  "Geocoded unwrapped interferogram, # m UTM grid, HH polarisation, with coherence, connected components and ionosphere phase screen":
    "Coğrafi kodlanmış, faz açılmış interferogram; # m UTM ızgarası, HH polarizasyonu; koherans, bağlı bileşenler ve iyonosfer faz perdesiyle",
  "Ground motion: Central Valley (track # # pairs; check with track # # pairs), Karapınar (track # # pairs), London (track # # pairs)":
    "Yer hareketi: Central Valley (iz #1, #2 çift; iz #3 ile kontrol, #4 çift), Karapınar (iz #5, #6 çift), Londra (iz #7, #8 çift)",
  "Radiometrically terrain-corrected backscatter (γ⁰)": "Radyometrik olarak arazi düzeltmeli geri saçılım (γ⁰)",
  "Radar view of the Fens (quick-look)": "Fens'in radar görünümü (hızlı bakış)",
  "Soil moisture": "Toprak nemi",
  "Irrigation timing vs sinking ({0})": "Sulama zamanlaması ve çökme ({0})",
  "All products come from NASA's Alaska Satellite Facility DAAC (search: {0}). Measurements on the main page use only {1} products (composite release P#) whose two dates are on or after # June #":
    "Tüm ürünler NASA'nın Alaska Satellite Facility DAAC'sinden geliyor (arama: {0}). Ana sayfadaki ölçümler yalnızca iki tarihi de #2 Haziran #3 veya sonrası olan {1} ürünlerini (birleşik sürüm P#1) kullanıyor",
  "NISAR data are provisional (product code P# from ###; validated status from ###); calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.":
    "NISAR verileri geçicidir (#2#3#4 tarihinden itibaren ürün kodu P#1; #5#6#7 tarihinden itibaren doğrulanmış durum); kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yapılmaktadır.",
  "Find and download NISAR data yourself: {0} · our guide {1}.": "NISAR verisini kendiniz bulun ve indirin: {0} · rehberimiz {1}.",
  "“Reproduce our data in # steps”": "“Verimizi # adımda yeniden üretin”",
  "λ = c / f{0} (read from each file; # MHz → # m for track #){1}d{2} = −λ / (#π) · (φ{3} − φ{4}){5}negative d{6} = motion away from the satellite (subsidence)":
    "λ = c / f{0} (her dosyadan okunur; iz #3 için #1 MHz → #2 m){1}d{2} = −λ / (#4π) · (φ{3} − φ{4}){5}negatif d{6} = uydudan uzaklaşan hareket (çökme)",
  "The sign convention follows ISCE# (interferogram = reference × conj(secondary)) and MintPy's NISAR reader. Pixels with coherence < # or connected component # are masked, as are small isolated patches and pixels that jump by half a phase cycle from their # m neighbourhood (unwrapping errors). From each pair a plane plus a linear elevation term (Copernicus DEM) is removed to reduce long-wavelength and height-dependent atmospheric delay. Every pair is referenced to the same stable, highly coherent area. Vertical estimates assume no horizontal motion: d{0} ≈ d{1} / cos θ{2}.":
    "İşaret kuralı ISCE# (interferogram = referans × eşlenik(ikincil)) ve MintPy'nin NISAR okuyucusunu izler. Koheransı < # olan ya da bağlı bileşeni # olan pikseller maskelenir; küçük yalıtılmış parçalar ve # m'lik komşuluğundan yarım faz döngüsü sıçrayan pikseller (faz açma hataları) de maskelenir. Uzun dalga boylu ve yüksekliğe bağlı atmosferik gecikmeyi azaltmak için her çiftten bir düzlem ve doğrusal bir yükseklik terimi (Copernicus DEM) çıkarılır. Her çift aynı sabit ve yüksek koheranslı alana referanslanır. Düşey tahminler yatay hareket olmadığını varsayar: d{0} ≈ d{1} / cos θ{2}.",
  "Consecutive pairs (# to # days apart; # Jun → # Oct # for track #) are summed into a cumulative map. A chain with any gap is not joined. Headline numbers are the most negative median of ~# km blocks with ≥ # % valid pixels and within-block standard deviation ≤ # cm, so single-pixel unwrapping errors cannot set the headline. Re-referencing the whole chain to up to two other stable areas at least # km away moves the Central Valley maximum between {0} cm (line of sight); we report the range. Two orbits looking from opposite sides (tracks # and #) let us also separate vertical from east–west motion ({1}).":
    "Ardışık çiftler (#1 ile #2 gün arayla; iz #6 için #3 Haz → #4 Eki #5) toplanarak kümülatif bir harita oluşturulur. Boşluğu olan bir zincir birleştirilmez. Manşet sayılar, geçerli pikseli ≥ %#8 ve blok içi standart sapması ≤ #9 cm olan ~#7 km'lik blokların en negatif medyanıdır; böylece tek piksellik faz açma hataları manşeti belirleyemez. Tüm zinciri en az #10 km uzaktaki en fazla iki başka sabit alana yeniden referanslamak Central Valley maksimumunu {0} cm (görüş hattı) arasında oynatır; aralığı raporluyoruz. Karşıt yönlerden bakan iki yörünge (iz #11 ve #12) düşey hareketi doğu–batı hareketinden de ayırmamızı sağlıyor ({1}).",
  "We compared the NISAR vertical estimate with daily \"up\" positions from # continuous GPS stations (Nevada Geodetic Laboratory) over the same dates.":
    "NISAR düşey tahminini aynı tarihlerde # sürekli GPS istasyonunun (Nevada Jeodezi Laboratuvarı) günlük \"yukarı\" konumlarıyla karşılaştırdık.",
  "Correlation r": "Korelasyon r",
  "RMSE (cm)": "RMSE (cm)",
  "GPS end (cm)": "GPS son (cm)",
  "NISAR end (cm)": "NISAR son (cm)",
  "# of # stations agree with r ≥ # (median RMSE # cm). The stations that disagree are nearly stable, where the motion is smaller than the noise of a single season.":
    "#2 istasyondan #1 tanesi r ≥ #3 ile uyuşuyor (medyan RMSE #4 cm). Uyuşmayan istasyonlar neredeyse sabit; orada hareket tek bir mevsimin gürültüsünden küçük.",
  "For every canal, major road and railway segment from OpenStreetMap longer than # km, we sample the cumulative map along the line and compute the sinking gradient (mm per km) and the total sinking. {0}: gradient ≥ # mm/km with sinking ≥ # cm, or total sinking ≥ # cm. {1}: gradient ≥ # mm/km with sinking ≥ # cm, or total sinking ≥ # cm. Gradients matter because uneven sinking tilts canals and reduces their capacity.":
    "OpenStreetMap'teki # km'den uzun her kanal, ana yol ve demiryolu kesimi için kümülatif haritayı hat boyunca örnekleyip çökme eğimini (km başına mm) ve toplam çökmeyi hesaplıyoruz. {0}: eğim ≥ # mm/km ve çökme ≥ # cm, ya da toplam çökme ≥ # cm. {1}: eğim ≥ # mm/km ve çökme ≥ # cm, ya da toplam çökme ≥ # cm. Eğimler önemli, çünkü düzensiz çökme kanalları eğer ve kapasitelerini düşürür.",
  "High": "Yüksek",
  "Medium": "Orta",
  "Radar measures along its slanted line of sight; horizontal motion would bias the vertical estimate.": "Radar eğik görüş hattı boyunca ölçer; yatay hareket düşey tahmini saptırabilir.",
  "Troposphere and ionosphere add centimetre-level noise per pair; summing pairs accumulates it.": "Troposfer ve iyonosfer her çifte santimetre düzeyinde gürültü ekler; çiftleri toplamak bu gürültüyü biriktirir.",
  "Yearly rates extrapolated from one irrigation season overstate the net annual rate, because part of summer subsidence recovers in winter.":
    "Tek bir sulama mevsiminden çıkarılan yıllık hızlar net yıllık hızı olduğundan büyük gösterir, çünkü yaz çökmesinin bir kısmı kışın geri gelir.",
  "Data are provisional and may change when the NISAR project releases validated products.": "Veriler geçicidir ve NISAR projesi doğrulanmış ürünleri yayımladığında değişebilir.",
  "Detectability and minimum detectable rate": "Tespit edilebilirlik ve en küçük tespit edilebilir hız",
  "Calibration status of the NISAR products we used": "Kullandığımız NISAR ürünlerinin kalibrasyon durumu",
  "Provisional (P#; Validated >= ###)": "Geçici (P#; Doğrulanmış >= ###)",
  "Read →": "Oku →",
  "NISAR mission (NASA JPL)": "NISAR görevi (NASA JPL)",
  "NISAR data user guide (ASF)": "NISAR veri kullanıcı kılavuzu (ASF)",
  "What is synthetic aperture radar? (NASA Earthdata)": "Sentetik açıklıklı radar nedir? (NASA Earthdata)",
  "{0} — wavelength, polarisation, how radar sees the ground.": "{0} — dalga boyu, polarizasyon, radarın zemini nasıl gördüğü.",
  "NISAR StoryMap: Land Subsidence": "NISAR StoryMap: Arazi Çökmesi",
  "{0} — how radar sees sinking from groundwater pumping (Central Valley example).": "{0} — radarın yeraltı suyu pompalamasından kaynaklanan çökmeyi nasıl gördüğü (Central Valley örneği).",
  "NISAR applications": "NISAR uygulamaları",
  "{0} — NASA papers on subsidence, groundwater, levees and dams, sinkholes and food security.": "{0} — çökme, yeraltı suyu, setler ve barajlar, obruklar ve gıda güvenliği üzerine NASA çalışmaları.",
  "UAVSAR postcards": "UAVSAR kartpostalları",
  "{0} — airborne L-band radar images, the predecessor of NISAR's view.": "{0} — havadan L-bant radar görüntüleri, NISAR'ın bakışının öncülü.",
  "NASA ARSET trainings": "NASA ARSET eğitimleri",
  "{0} — free online courses on SAR and NISAR.": "{0} — SAR ve NISAR üzerine ücretsiz çevrimiçi kurslar.",
  "{0} and the {1}.": "{0} ve {1}.",
  "SAR tutorial in Python (Canadian Space Agency)": "Python ile SAR eğitimi (Kanada Uzay Ajansı)",
  "USGS: Land subsidence in California": "USGS: Kaliforniya'da arazi çökmesi",
  "Central Valley": "Central Valley",
  "United Kingdom": "Birleşik Krallık",
  "Konya Closed Basin: Konya, Çumra and Karapınar": "Konya Kapalı Havzası: Konya, Çumra ve Karapınar",
  "Full year: winter rebound vs permanent compaction": "Tam yıl: kış geri kabarması ve kalıcı sıkışma",
  "Station": "İstasyon",
  // results registry
  "Global atlas": "Küresel atlas",
  "Global subsidence atlas (common-window ranked)": "Küresel çökme atlası (ortak döneme göre sıralı)",
  "# sinking regions ranked over a common #-day summer window (### to ###) using provisional NISAR GUNW chains.":
    "# çöken bölge, geçici NISAR GUNW zincirleriyle ortak #-günlük yaz dönemine (### – ###) göre sıralandı.",
  "# regions (# reliable, # indicative); top reliable # cm/#d (Konya Plain)": "# bölge (# güvenilir, # gösterge); en hızlı güvenilir # cm/#g (Konya Ovası)",
  "# cm/#d (Konya Plain, # regions, provisional)": "# cm/#g (Konya Ovası, # bölge, geçici)",
  "Across # regions in the # Global Subsidence Atlas (# reliable, # indicative), Eloy leads reliable basins at # cm/#d over the #-day common window, followed by Central Valley, Mexico City, Semarang, and Houston; Konya Plain (# cm/#d) is kept indicative following our own validation audit.":
    "#2 Küresel Çökme Atlası'ndaki #1 bölgede (#3 güvenilir, #4 gösterge), #7 günlük ortak dönemde #5 cm/#6g ile güvenilir havzalarda Eloy ilk sırada; onu Orta Vadi, Mexico City, Semarang ve Houston izliyor. Konya Ovası (#8 cm/#9g) kendi doğrulama denetimimiz sonucunda gösterge olarak tutuluyor.",
  "# regions (# reliable, # indicative); top reliable # cm/#d (Eloy)": "# bölge (# güvenilir, # gösterge); en hızlı güvenilir # cm/#g (Eloy)",
  "# cm/#d (Eloy, # regions, provisional)": "# cm/#g (Eloy, # bölge, geçici)",
  "A satellite number is only useful if you can trust it. We tested ours three ways.":
    "Uydudan gelen bir sayı ancak ona güvenebiliyorsan işe yarar. Bizimkini üç yolla test ettik.",
  "Basins with thin coverage or failed checks stay \"indicative\". Even Konya, our strongest signal, stays indicative after our own review.":
    "Kapsamı zayıf ya da kontrollerden geçemeyen havzalar \"gösterge\" olarak kalır. En güçlü sinyalimiz Konya bile kendi incelememizden sonra gösterge olarak kalıyor.",
  "Checked against the ground":
    "Yerde doğrulandı",
  "For kids: Water Hero →":
    "Çocuklar için: Water Hero →",
  "How it works, step by step →":
    "Adım adım nasıl çalışıyor →",
  "How we know it's right":
    "Doğru olduğunu nereden biliyoruz",
  "Indonesia · caution":
    "Endonezya · dikkat",
  "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team. {0}":
    "NISAR verileri geçicidir. Kalibrasyon ve doğrulama bizim ekibimiz tarafından değil, NISAR projesi (NASA-JPL ve ISRO) tarafından yapılmaktadır. {0}",
  "Play Aquifer Run →":
    "Aquifer Run'ı oyna →",
  "Radar can jump by exactly one wave cycle (# cm). An automatic test checks every basin for these jumps and bad dates; flagged basins are not ranked.":
    "Radar tam bir dalga döngüsü (# cm) kadar sıçrayabilir. Otomatik bir test her havzada bu sıçramaları ve hatalı tarihleri arar; işaretlenen havzalar sıralamaya girmez.",
  "Rates in {0} (centimetres per # days; # in = # cm) along satellite {1} (line of sight: toward or away from the radar), from NASA-JPL {2} (Geocoded Unwrapped Interferogram: paired radar images processed to show ground movement). {3}":
    "Hızlar {0} cinsinden (# günde santimetre; # inç = # cm), uydunun {1} yönünde (bakış doğrultusu: radara doğru ya da radardan uzağa), NASA-JPL {2} ürünlerinden (Coğrafi Konumlu Açılmış İnterferogram: yer hareketini göstermek için işlenmiş radar görüntü çiftleri). {3}",
  "Ten permanent GPS stations in California measured the same sinking as the satellite. Typical difference: about # cm (# in).":
    "Kaliforniya'daki on kalıcı GPS istasyonu uydunun ölçtüğü çökmenin aynısını ölçtü. Tipik fark: yaklaşık # cm (# inç).",
  "We hunt for our own mistakes":
    "Kendi hatalarımızı avlıyoruz",
  "We only rank what passes":
    "Yalnızca kontrolden geçeni sıralıyoruz",
  "{0} a comparison with # permanent GPS stations in California's Central Valley, where the ground moved up to # cm (# in) away from the satellite in # days.":
    "{0} Kaliforniya Orta Vadisi'ndeki #1 kalıcı GPS istasyonuyla karşılaştırma; burada yer #4 günde uydudan #2 cm'ye (#3 inç) kadar uzaklaştı.",
  "{0} an automatic test on every basin's time series. It looks for jumps of exactly one radar phase cycle (# cm / # in) and for single bad dates.":
    "{0} her havzanın zaman serisinde otomatik bir test. Tam bir radar faz döngüsü (# cm / # inç) kadar sıçramaları ve tek tek hatalı tarihleri arar.",
  "{0} caught":
    "{0} yakalandı",
  "{0} it caught our first number one. Semarang's # cm (# in) was one processing jump; re-processed, the real peak on the coast is # cm (# in).":
    "{0} ilk bir numaramızı yakaladı. Semarang'ın # cm'si (# inç) tek bir işleme sıçramasıydı; yeniden işlenince kıyıdaki gerçek tepe değer # cm (# inç).",
  "{0} per # days at Eloy, Arizona, the fastest reliable basin. Konya Plain shows a stronger signal (# cm / # in) but our own review keeps it indicative.":
    "{0} Eloy, Arizona'da # günde; en hızlı güvenilir havza. Konya Ovası daha güçlü bir sinyal gösteriyor (# cm / # inç) ama kendi incelememiz onu gösterge olarak tutuyor.",
  "▶ #-min video":
    "▶ # dk video",
  "Selected region details":
    "Seçilen bölgenin ayrıntıları",
  "We used NASA-ISRO NISAR {0} L# {1} (Geocoded Unwrapped Interferogram) radar pairs to measure ground sinking in # basins over the same # days. Rates are in {2} (centimeters per # days; # in = # cm) along satellite {3} (line-of-sight: toward or away from the radar), where deeper red means faster sinking and pale tones mean near-zero motion. Low-coverage basins or series flagged by our automated quality checks are marked {4} so you always know which numbers are rock-solid.":
    "NASA-ISRO NISAR {0} L# {1} (Coğrafi Konumlu Açılmış İnterferogram) radar çiftleriyle # havzada aynı # gün boyunca yer çökmesini ölçtük. Hızlar {2} cinsindendir (# günde santimetre; # inç = # cm), uydunun {3} yönünde (bakış doğrultusu: radara doğru ya da radardan uzağa); koyu kırmızı daha hızlı çökme, soluk tonlar sıfıra yakın hareket demektir. Kapsamı düşük havzalar ya da otomatik kalite kontrollerimizin işaretlediği seriler {4} olarak gösterilir; böylece hangi sayıların sağlam olduğunu her zaman bilirsiniz.",
  "km² across measured basins, sank more than # cm (# in) in one summer (~# days)":
    "km², ölçülen havzalarda; bir yazda (~#3 gün) #1 cm'den (#2 inç) fazla çöktü",
  "live where ground sank more than # cm (# in) in one summer (GHSL population estimate)":
    "kişi, bir yazda # cm'den (# inç) fazla çöken zeminde yaşıyor (GHSL nüfus tahmini)",
  "medium · indicative only":
    "orta · yalnızca gösterge",
  "very high · indicative only":
    "çok yüksek · yalnızca gösterge",
  "Beat \"doing nothing\"":
    "\"Hiçbir şey yapmamayı\" geç",
  "Beat \"doing nothing\" (the # settings). Grade appears after the first full year, month # (now #/#).":
    "\"Hiçbir şey yapmamayı\" (# ayarları) geç. Not, ilk tam yıldan sonra, #. ayda çıkar (şu an #/#).",
  "Goal: at least #% of the income of doing nothing":
    "Hedef: hiçbir şey yapmamanın gelirinin en az %#'i",
  "Goal: at most half the permanent sinking of doing nothing":
    "Hedef: hiçbir şey yapmamanın kalıcı çökmesinin en fazla yarısı",
  "Goal: fewer dry wells than doing nothing, canal loss under #%":
    "Hedef: hiçbir şey yapmamaktan daha az kuruyan kuyu, kanal kaybı %# altında",
  "Protect wells & canals":
    "Kuyuları ve kanalları koru",
  "Your grade appears after month #":
    "Notun #. aydan sonra çıkar",
  "{0}{1}Keep #% of farm income while cutting permanent sinking in half. Graded A–F after the first year.":
    "{0}{1}Kalıcı çökmeyi yarıya indirirken çiftlik gelirinin %#'ini koru. İlk yıldan sonra A–F arası not alırsın.",
  "# dry wells · canal #%":
    "# kuruyan kuyu · kanal %#",
  "# Why do you report motion along the satellite's line of sight?":
    "#. Hareketi neden uydunun bakış doğrultusunda veriyorsunuz?",
  "# Why compare the same # days?":
    "#. Neden aynı # günü karşılaştırıyorsunuz?",
  "# How does the quality check work?":
    "#. Kalite kontrolü nasıl çalışıyor?",
  "# Why is Konya marked indicative?":
    "#. Konya neden gösterge olarak işaretli?",
  "# How did you check the satellite measurements with GPS?":
    "#. Uydu ölçümlerini GPS ile nasıl kontrol ettiniz?",
  "# What does “provisional” mean?":
    "#. “Geçici” ne demek?",
  "# Why is NASA's OPERA product not the headline comparison?":
    "#. NASA'nın OPERA ürünü neden ana karşılaştırma değil?",
  "# How did you estimate the exposed population?":
    "#. Etkilenen nüfusu nasıl tahmin ettiniz?",
  "# What does “permanent water storage loss” mean here?":
    "#. Burada “kalıcı su depolama kaybı” ne demek?",
  "# Can another team reproduce the results?":
    "#. Başka bir ekip sonuçları yeniden üretebilir mi?",
  "# What are the main limits?":
    "#. Başlıca sınırlar neler?",
  "# How can a city use the atlas?":
    "#. Bir şehir atlası nasıl kullanabilir?",
  "# km³ per year":
    "yılda # km³",
  "It is the estimated aquifer storage loss associated with ground compaction that does not recover in the seasonal cycle. The current Central Valley estimate is {0}; it is a model-based estimate, not a direct water-meter reading.":
    "Mevsimlik döngüde geri gelmeyen zemin sıkışmasına bağlı tahmini akifer depolama kaybıdır. Orta Vadi için güncel tahmin {0}; bu doğrudan bir su sayacı okuması değil, modele dayalı bir tahmindir.",
  "Its summer signal is stronger than the longer-term context supports, and the result depends on the reference and valid-pixel coverage. We keep it visible for transparency but leave it out of the reliable ranking.":
    "Yaz sinyali uzun dönemli bağlamın desteklediğinden güçlü ve sonuç referansa ve geçerli piksel kapsamına bağlı. Şeffaflık için görünür tutuyoruz ama güvenilir sıralamanın dışında bırakıyoruz.",
  "OPERA provides an independent shape check for Mexico City, but its comparison window is {0}, while NISAR covers {1}. Because the seasons differ, it is not a same-time validation.":
    "OPERA, Mexico City için bağımsız bir desen kontrolü sağlıyor ama karşılaştırma dönemi {0}, NISAR ise {1} dönemini kapsıyor. Mevsimler farklı olduğu için aynı zamanlı bir doğrulama değil.",
  "Radar measures movement toward or away from the satellite most directly. Turning that into vertical movement requires an assumption about horizontal motion, so we label line-of-sight (LOS) values clearly.":
    "Radar en doğrudan uyduya doğru ya da uydudan uzağa hareketi ölçer. Bunu dikey harekete çevirmek yatay hareket hakkında bir varsayım gerektirir; bu yüzden bakış doğrultusu (LOS) değerlerini açıkça etiketliyoruz.",
  "The atlas covers one shared summer window and uses provisional products, so it cannot establish a long-term annual trend. Radar observes a slanted view, and horizontal movement or atmospheric noise can affect a vertical estimate.":
    "Atlas tek bir ortak yaz dönemini kapsıyor ve geçici ürünler kullanıyor; bu yüzden uzun vadeli yıllık bir eğilim ortaya koyamaz. Radar eğik bakar; yatay hareket ya da atmosferik gürültü dikey tahmini etkileyebilir.",
  "The atlas uses the common window {0} so basin rates use the same part of the season. This improves comparability, though it does not make one summer a long-term trend.":
    "Atlas ortak {0} dönemini kullanıyor; böylece havza hızları mevsimin aynı bölümünden geliyor. Bu karşılaştırılabilirliği artırır ama tek bir yazı uzun vadeli bir eğilime çevirmez.",
  "These are early NISAR products that have not completed the mission team's calibration and validation. The NISAR project (NASA-JPL and ISRO) performs those steps; our team does not.":
    "Bunlar görev ekibinin kalibrasyon ve doğrulamasını henüz tamamlamamış erken NISAR ürünleri. Bu adımları bizim ekibimiz değil, NISAR projesi (NASA-JPL ve ISRO) yapıyor.",
  "Use it to identify places that may deserve a closer look, then compare the signal with local survey, groundwater, and infrastructure records. It is a screening tool, not a safety rating or a substitute for local engineering review.":
    "Daha yakından bakılması gereken yerleri bulmak için kullanın, sonra sinyali yerel ölçüm, yeraltı suyu ve altyapı kayıtlarıyla karşılaştırın. Bir tarama aracıdır; güvenlik derecesi ya da yerel mühendislik incelemesinin yerine geçmez.",
  "We compared NISAR with # continuous GPS stations in California's Central Valley. The agreement is {0}, with {1} at the final date.":
    "NISAR'ı Kaliforniya Orta Vadisi'ndeki # sürekli GPS istasyonuyla karşılaştırdık. Uyum {0}, son tarihte {1}.",
  "We overlaid the atlas movement screen on the {0} population grid and counted people where measured sinking exceeds {1}. The global summary reports {2} people across the measured basins.":
    "Atlas hareket haritasını {0} nüfus ızgarasının üzerine koyduk ve ölçülen çökmenin {1} değerini aştığı yerlerdeki insanları saydık. Küresel özet, ölçülen havzalarda {2} kişi bildiriyor.",
  "We screen each time series for sudden jumps that look like a radar phase error and review suspicious dates and reference areas. The review corrected Semarang's headline from # cm (# in) to # cm (# in); flagged basins stay indicative while under review.":
    "Her zaman serisini radar faz hatasına benzeyen ani sıçramalar için tarıyor, şüpheli tarihleri ve referans alanlarını inceliyoruz. İnceleme, Semarang'ın ana değerini # cm'den (# inç) # cm'ye (# inç) düzeltti; işaretlenen havzalar inceleme sürerken gösterge olarak kalıyor.",
  "Yes: the code, input products, quality labels, and result files are open in the repository. The documented pipeline can be rerun for a selected basin, and its checks expose the inputs and assumptions.":
    "Evet: kod, girdi ürünleri, kalite etiketleri ve sonuç dosyaları depoda açık. Belgelenmiş hat seçilen bir havza için yeniden çalıştırılabilir ve kontrolleri girdileri ve varsayımları gösterir.",
  "All # basins are measured over the same # days. Only the # that pass every check are ranked; the rest are shown as \"indicative\".":
    "# havzanın hepsi aynı # günde ölçülüyor. Yalnızca her kontrolden geçen # tanesi sıralanıyor; geri kalanlar \"gösterge\" olarak gösteriliyor.",
  "Comparing two passes shows how far the ground moved toward or away from the satellite (its \"line of sight\"), to a fraction of a centimetre.":
    "İki geçişi karşılaştırmak, yerin uyduya doğru ya da uydudan uzağa (\"bakış doğrultusu\") ne kadar hareket ettiğini santimetrenin kesirlerine kadar gösterir.",
  "Every basin's time series is tested for jumps of exactly one radar wave cycle (# cm) and for bad dates. Ten GPS stations check the result on the ground.":
    "Her havzanın zaman serisi tam bir radar dalga döngüsü (# cm) kadar sıçramalar ve hatalı tarihler için test ediliyor. On GPS istasyonu sonucu yerde kontrol ediyor.",
  "Four steps, each one checked. Plain English first; the technical details are folded further down for anyone who wants them.":
    "Dört adım, her biri kontrol edildi. Önce sade anlatım; teknik ayrıntılar isteyenler için aşağıda katlanmış durumda.",
  "Geocoded unwrapped interferogram: a pair of radar images processed to show ground movement":
    "Coğrafi konumlu açılmış interferogram: yer hareketini göstermek için işlenmiş bir radar görüntü çifti",
  "Ground motion: Central Valley, Karapınar and London":
    "Yer hareketi: Orta Vadi, Karapınar ve Londra",
  "How it works in four steps":
    "Dört adımda nasıl çalışıyor",
  "How we turn radar echoes into centimetres":
    "Radar yankılarını santimetreye nasıl çeviriyoruz",
  "Interferometric synthetic aperture radar (InSAR) compares radar echoes from separate satellite passes. It measures movement along the satellite's line of sight (LOS), toward or away from the satellite; a rate in cm/#d means centimetres per # days.":
    "İnterferometrik yapay açıklıklı radar (InSAR), ayrı uydu geçişlerinden gelen radar yankılarını karşılaştırır. Uydunun bakış doğrultusundaki (LOS) hareketi, yani uyduya doğru ya da uydudan uzağa hareketi ölçer; cm/#g cinsinden bir hız # günde santimetre demektir.",
  "NISAR flies over the same spot every # days and bounces microwaves off the ground, day or night, through clouds.":
    "NISAR aynı noktanın üzerinden # günde bir geçer ve gece gündüz, bulutların içinden mikrodalgaları yere gönderip yankısını alır.",
  "Satellite versus GPS at # stations":
    "# istasyonda uydu ve GPS",
  "Semarang before and after the error check":
    "Hata kontrolünden önce ve sonra Semarang",
  "Step #: satellite vs GPS, r = #":
    "Adım #: uydu ve GPS, r = #.",
  "Step #: the check caught a one-cycle jump in Semarang.":
    "Adım #: kontrol Semarang'da tek döngülük bir sıçramayı yakaladı.",
  "Step #: the atlas (filled = reliable, ring = indicative).":
    "Adım #: atlas (dolu = güvenilir, halka = gösterge).",
  "World map of the measured basins":
    "Ölçülen havzaların dünya haritası",
  "{0} # basins pass every check; the fastest is Eloy, Arizona at # cm (# in) per # days. About # people live on ground that sank more than # cm (# in) in one summer.":
    "{0} #1 havza her kontrolden geçiyor; en hızlısı #4 günde #2 cm (#3 inç) ile Eloy, Arizona. Yaklaşık #5 kişi bir yazda #6 cm'den (#7 inç) fazla çöken zeminde yaşıyor.",
  "{0} # sinking basins on three continents, all with the same open method and the same #-day window (# Jun – # Sep #), from provisional NISAR radar data.":
    "{0} üç kıtada # çöken havza; hepsi aynı açık yöntemle ve aynı # günlük dönemde (# Haz – # Eyl #), geçici NISAR radar verisinden.",
  "{0} Against # GPS stations: r = # and RMSE # cm (# in) at the final date, plus a second satellite view from the opposite direction.":
    "{0} # GPS istasyonuna karşı: son tarihte r = # ve RMSE # cm (# inç); ayrıca karşı yönden ikinci bir uydu görünümü.",
  "±# day":
    "±# gün",
  "Beat \"doing nothing\" (the # settings) on all three.":
    "Üç hedefte de \"hiçbir şey yapmamayı\" (# ayarları) geç.",
  "# regions; # cm GNSS median RMSE (provisional)": "# bölge; # cm GNSS medyan RMSE (geçici)",
  "Methods, uncertainty limits, GNSS/OPERA cross-checks, and #-region ATLAS v# results for provisional NISAR L-band GUNW interferometry across Central Valley, Konya Basin, UK Fens, and global subsidence basins.":
    "Central Valley, Konya Havzası, Birleşik Krallık Fens ve küresel çökme havzalarında geçici NISAR L-bant GUNW interferometrisi için yöntemler, belirsizlik sınırları, GNSS/OPERA çapraz kontrolleri ve #-bölgelik ATLAS v# sonuçları.",
  "Technical note (NASA report style)": "Teknik not (NASA rapor tarzı)",
  "GNSS validation": "GNSS doğrulaması",
  "# cm median RMSE (# GPS, provisional)": "# cm medyan RMSE (# GPS, geçici)",
  "Across # Nevada Geodetic Laboratory GPS stations in the San Joaquin Valley, # stations agree with NISAR vertical estimates (r >= # median RMSE # cm; all# median RMSE # cm, peak CAHA r = #).":
    "San Joaquin Vadisi'ndeki #1 Nevada Jeodezi Laboratuvarı GPS istasyonundan #2 tanesi NISAR düşey tahminleriyle uyuşuyor (r >= #3, medyan RMSE #4 cm; tümü #5, medyan RMSE #6 cm, en yüksek CAHA r = #7).",
  "NISAR vs NASA JPL OPERA DISP-S# cross-check": "NISAR ile NASA JPL OPERA DISP-S# çapraz kontrolü",
  "r = # (Mexico City, provisional)": "r = # (Meksiko, geçici)",
  "Against non-overlapping NASA OPERA DISP-S# frames, NISAR correlates strongly in steady clay-compaction Mexico City (r = # n = #) and moderately in Central Valley comparing Summer # OPERA against Summer # NISAR (r = # n = #), while seasonal spring-vs-summer mismatch and #% C-band masking explain Eloy (r = # n = #).":
    "Örtüşmeyen NASA OPERA DISP-S# çerçevelerine karşı NISAR, düzenli kil sıkışması olan Meksiko'da güçlü (r = #2, n = #3), Central Valley'de Yaz #4 OPERA ile Yaz #5 NISAR karşılaştırmasında orta düzeyde (r = #6, n = #7) korelasyon gösteriyor; Eloy'daki (r = #9, n = #10) zayıf uyumu ise mevsimsel ilkbahar-yaz uyumsuzluğu ve %#8 C-bant maskelemesi açıklıyor.",
  "Central Valley peak subsidence reached # cm (# Jun–# Oct #):": "Central Valley'de tepe çökme # cm'ye ulaştı (# Haz–# Eki #):",
  "Karapınar basin subsided up to # cm (# Jun–# Oct #):": "Karapınar havzası # cm'ye kadar çöktü (# Haz–# Eki #):",
  "Independent GPS stations confirm # to # cm (RMSE) accuracy in sinking areas (# Jun–# Oct #):": "Bağımsız GPS istasyonları çöken alanlarda # ile # cm (RMSE) doğruluğu doğruluyor (# Haz–# Eki #):",
  "An independent satellite track reproduces the same sinking pattern (# Jun–# Oct #):": "Bağımsız bir uydu izi aynı çökme desenini yeniden üretiyor (# Haz–# Eki #):",
  "Radar phase noise is #× smaller than the peak signal (±# cm CV, ±# cm Karapınar):": "Radar faz gürültüsü tepe sinyalden #× küçük (±# cm CV, ±# cm Karapınar):",
  "Central Valley canals and railways cross steep subsidence gradients (# Jun–# Oct #):": "Central Valley kanalları ve demiryolları dik çökme eğimlerinden geçiyor (# Haz–# Eki #):",
  "Subsidence in Karapınar concentrates around sinkholes (# Jun–# Oct #):": "Karapınar'da çökme obrukların çevresinde yoğunlaşıyor (# Haz–# Eki #):",
  "Mid-summer irrigation moisture precedes late-summer subsidence (# Jun–# Oct #):": "Yaz ortası sulama nemi yaz sonu çökmesinden önce geliyor (# Haz–# Eki #):",
  "Full year": "Tam yıl",
  "# cm/yr permanent at Earlimart (# cm #-d LOS, mixed)": "Earlimart'ta # cm/yıl kalıcı (# cm, #-g LOS, karışık)",
  "Over # days (### to ### # mixed beta-precal + provisional pairs), peak cumulative LOS subsidence at Earlimart reaches # cm (# cm vertical est.; #-reference range # to # cm). Harmonic decomposition separates a valley median permanent rate of # cm/yr (# cm/yr at Earlimart p#) from # cm seasonal amplitude.":
    "#1 gün boyunca (#2#3#4 – #5#6#7, #8 karışık beta-ön kalibrasyon + geçici çift) Earlimart'ta tepe kümülatif LOS çökmesi #9 cm'ye ulaşıyor (#10 cm tahmini düşey; #11-referans aralığı #12 – #13 cm). Harmonik ayrıştırma, vadide medyan #14 cm/yıl kalıcı hızı (Earlimart p#16'da #15 cm/yıl) #17 cm'lik mevsimsel genlikten ayırıyor.",
  "Permanent aquifer storage loss (O#)": "Kalıcı akifer depolama kaybı (O#)",
  "# km#/yr (mixed, estimate)": "# km#/yıl (karışık, tahmin)",
  "Integrating permanent vertical compaction across # km# in the Tulare Basin yields # km#/yr permanent aquifer storage loss (#-reference range ## km#/yr).":
    "Tulare Havzası'nda # km# boyunca kalıcı düşey sıkışmayı toplamak # km#/yıl kalıcı akifer depolama kaybı veriyor (#-referans aralığı ## km#/yıl).",
  "Probabilistic engineering risk for canals and roads (O#)": "Kanallar ve yollar için olasılıksal mühendislik riski (O#)",
  "# lines evaluated": "# hat değerlendirildi",
  "Monte Carlo analysis of # Central Valley infrastructure segments evaluating angular distortion beta and differential settlement exceedance.":
    "Açısal bozulma betası ve farklı oturma aşımını değerlendiren # Central Valley altyapı kesiminin Monte Carlo analizi.",
  "People and crops on sinking ground": "Çöken zemindeki insanlar ve ürünler",
  "# people (< # cm/#d, provisional)": "# kişi (< # cm/#g, geçici)",
  "Across # measured atlas regions, # km# sinks faster than # cm per # days, affecting # residents (# below # cm/#d, excluding nested Karapinar).":
    "Ölçülen #1 atlas bölgesinde #2 km#3 alan #5 günde #4 cm'den hızlı çöküyor ve #6 kişiyi etkiliyor (#8 cm/#9g altında #7, iç içe Karapınar hariç).",
  "Detectability": "Tespit edilebilirlik",
  "# cm/#d #-sigma (#/# detectable, provisional)": "# cm/#g #-sigma (#/# tespit edilebilir, geçici)",
  "All # audited summer basins exceed #-sigma formal radar phase-noise thresholds (## cm/#d, SNR ##), while UK London Clay sets an empirical scene-level #-sigma atmospheric floor of # cm.":
    "Denetlenen #1 yaz havzasının hepsi #2-sigma biçimsel radar faz gürültüsü eşiklerini aşıyor (#3#4 cm/#5g, SNR #6#7); Birleşik Krallık London Clay ise sahne düzeyinde #9 cm'lik deneysel #8-sigma atmosferik taban belirliyor.",
  "Uncertainty": "Belirsizlik",
  "# cm local / # cm scene-wide (SNR #x#x, provisional)": "# cm yerel / # cm sahne geneli (SNR #x#x, geçici)",
  "Over # provisional Central Valley pairs (# d), local phase-noise RMS averages # cm/pair (# cm local to # cm scene-wide cumulative), placing the # cm LOS peak #x#x above noise.":
    "# geçici Central Valley çifti (# g) boyunca yerel faz gürültüsü RMS ortalaması çift başına # cm (yerel # cm ile sahne geneli # cm kümülatif); bu da # cm LOS tepesini gürültünün #x#x üstüne koyuyor.",
  "Literature": "Literatür",
  "Published InSAR & GNSS literature rates (# basins)": "Yayımlanmış InSAR ve GNSS literatür hızları (# havza)",
  "#/# regions sourced (DOI-linked)": "#/# bölge kaynaklı (DOI bağlantılı)",
  "Aggregated peer-reviewed vertical subsidence rates with verified DOIs and agreement notes alongside common #-day and full-window NISAR L-band rates.":
    "Doğrulanmış DOI'leri ve uyum notlarıyla hakemli düşey çökme hızları; ortak #-günlük ve tam dönem NISAR L-bant hızlarıyla yan yana.",
  "Literature and first-measurement audit": "Literatür ve ilk ölçüm denetimi",
  "Qualified atlas wording only (provisional)": "Yalnızca sınırlandırılmış atlas ifadeleri (geçici)",
  "Literature audit excludes individual first-with-NISAR claims for Mexico City (already published by NASA-JPL) and checks peer-reviewed InSAR/GNSS rates across atlas basins using provisional GUNW data.":
    "Literatür denetimi, Meksiko için tek tek \"NISAR ile ilk\" iddialarını dışarıda bırakıyor (NASA-JPL zaten yayımladı) ve geçici GUNW verisiyle atlas havzalarındaki hakemli InSAR/GNSS hızlarını kontrol ediyor.",
  "Independent check of the atlas top ranks": "Atlasın üst sıralarının bağımsız kontrolü",
  "Independent literature & QC audit (ranks #–#)": "Bağımsız literatür ve kalite kontrol denetimi (sıralar #–#)",
  "# consistent / # caution / # suspect (provisional)": "# tutarlı / # dikkat / # şüpheli (geçici)",
  "Step-by-step p# time-series QC and peer-reviewed literature comparison across reliable ranks #–# (Mexico City to Quetta); # consistent, # caution (Houston, Quetta), # suspect.":
    "Güvenilir #2–#3 sıralarında (Meksiko'dan Quetta'ya) adım adım p#1 zaman serisi kalite kontrolü ve hakemli literatür karşılaştırması; # tutarlı, # dikkat (Houston, Quetta), # şüpheli.",
  "Ranking robustness: reference, coherence and box variants": "Sıralama sağlamlığı: referans, koherans ve kutu varyantları",
  "# global cities audited": "# küresel şehir denetlendi",
  "Reference and spatial box variants across # global cities show rank stability under alternative unwrapping baselines.":
    "# küresel şehirde referans ve mekânsal kutu varyantları, alternatif faz açma tabanları altında sıralamanın kararlı kaldığını gösteriyor.",
  "Global atlas transparent changelog": "Küresel atlasın şeffaf değişiklik günlüğü",
  "Tehran #-># cm (off-basin ref); Semarang #-># cm (phase jump removed)": "Tahran #-># cm (havza dışı referans); Semarang #-># cm (faz sıçraması kaldırıldı)",
  "Machine-readable log of every region addition, QC flag, confidence change, and headline correction (># cm) across atlas builds.":
    "Atlas sürümleri boyunca her bölge ekleme, kalite kontrol işareti, güven değişikliği ve manşet düzeltmesinin (># cm) makinece okunabilir günlüğü.",
  "Groundwater Simulator: #-month aquifer simulator": "Yeraltı Suyu Simülatörü: #-aylık akifer simülatörü",
  "#/# model tests, calibration error #%": "#/# model testi, kalibrasyon hatası %#",
  "Interactive browser simulator calibrated to Terra Bella #–# compaction and Karapınar NISAR rates, linking pumping decisions to permanent clay compaction and canal tilt.":
    "Terra Bella #–# sıkışmasına ve Karapınar NISAR hızlarına göre kalibre edilmiş etkileşimli tarayıcı simülatörü; pompalama kararlarını kalıcı kil sıkışması ve kanal eğimiyle ilişkilendiriyor.",
  "NISAR Vision: one-command open engine (O#)": "NISAR Vision: tek komutlu açık motor (O#)",
  "#/# unit tests (offline QC + CLI)": "#/# birim testi (çevrimdışı kalite kontrol + CLI)",
  "NISAR Vision automates CMR search, #-MB subsetting, pixel-level cycle-jump and single-date QC (--qc), quality metrics, and coverage reporting from a single --center lon,lat command.":
    "NISAR Vision; CMR aramasını, #-MB alt küme çıkarmayı, piksel düzeyinde döngü sıçraması ve tek tarih kalite kontrolünü (--qc), kalite ölçütlerini ve kapsama raporunu tek bir --center lon,lat komutuyla otomatikleştiriyor.",
  "Offline #-stop presentation deck": "Çevrimdışı #-duraklı sunum",
  "# stops (offline-ready, # AI imagery)": "# durak (çevrimdışı hazır, # yapay zekâ görseli)",
  "Keyboard-navigable full-screen walkthrough (# Global Atlas, # Self-Checking QC, # GPS Validation, # People & # Water Loss, # Tilt & # Bulletins, # Simulator & # Open Engine) working offline from local assets.":
    "Klavyeyle gezilebilen tam ekran anlatım (# Küresel Atlas, # Öz Denetimli Kalite Kontrol, # GPS Doğrulaması, # İnsanlar ve # Su Kaybı, # Eğim ve # Bültenler, # Simülatör ve # Açık Motor); yerel dosyalardan çevrimdışı çalışıyor.",
  "Engagement": "Katılım",
  "NASA Space Apps # submission package": "NASA Space Apps # teslim paketi",
  "All live URLs HTTP # verified": "Tüm canlı URL'ler HTTP # ile doğrulandı",
  "Complete Space Apps delivery checklist, HTTP# verified live URLs, NASA/ESA/JRC data inventory, and AI usage disclosure.":
    "Eksiksiz Space Apps teslim kontrol listesi, HTTP# ile doğrulanmış canlı URL'ler, NASA/ESA/JRC veri envanteri ve yapay zekâ kullanım beyanı.",
  "London Clay detection limit and Holme Fen": "London Clay tespit sınırı ve Holme Fen",
  "# cm #-sigma limit (below detection, provisional)": "# cm #-sigma sınırı (tespit altında, geçici)",
  "Over Greater London (# Jun# Oct # # pairs), #-km block atmospheric noise (#-sigma = # cm) exceeds expected ## cm seasonal clay motion, leaving zero detected blocks.":
    "Büyük Londra üzerinde (# Haz# Eki # # çift) #-km'lik blok atmosferik gürültüsü (#-sigma = # cm) beklenen ## cm'lik mevsimsel kil hareketini aşıyor; tespit edilen blok kalmıyor.",
  "Over London's clay the same method found no motion above the #σ noise level (about # cm): small seasonal clay movement is below what one summer of data can resolve.":
    "Londra'nın kili üzerinde aynı yöntem #σ gürültü düzeyinin (yaklaşık # cm) üstünde hareket bulmadı: küçük mevsimsel kil hareketi tek bir yazlık verinin ayırt edebileceğinin altında.",
  "Which polarization shows crop-stage change (Fens)": "Hangi polarizasyon ürün evresi değişimini gösterir (Fens)",
  "# dB HV dynamic range": "# dB HV dinamik aralık",
  "Comparison of HH, HV, and cross-ratio backscatter in the Fens shows HV cross-polarization is the most interpretable channel for canopy volume scattering.":
    "Fens'te HH, HV ve çapraz oran geri saçılımının karşılaştırması, bitki örtüsü hacim saçılımı için en yorumlanabilir kanalın HV çapraz polarizasyonu olduğunu gösteriyor.",
  "Sacramento–San Joaquin Delta levees": "Sacramento–San Joaquin Deltası setleri",
  "Over the Sacramento-San Joaquin Delta (### to ### # provisional pairs), #-km block peak LOS subsidence is # cm (#-reference range # to # cm).":
    "Sacramento-San Joaquin Deltası üzerinde (### – ### # geçici çift) #-km'lik blok tepe LOS çökmesi # cm (#-referans aralığı # – # cm).",
  "# cm LOS (# d, provisional)": "# cm LOS (# g, geçici)",
  "Groundwater and crop drivers": "Yeraltı suyu ve ürün etkenleri",
  "p = ## (N = # non-significant, provisional)": "p = ## (N = # anlamlı değil, geçici)",
  "Across N = # summer epochs in Central Valley, preliminary soil-moisture and irrigation-index correlations (r = ##) remain statistically non-significant (p = ## vs |r_crit| = ##).":
    "Central Valley'de N = # yaz döneminde ön toprak nemi ve sulama endeksi korelasyonları (r = ##) istatistiksel olarak anlamlı değil (p = ##, |r_crit| = ##).",
  "Karapınar sinkholes and subsidence: statistical test": "Karapınar obrukları ve çökme: istatistiksel test",
  "p = # rigid-shift (p = # blocks, provisional)": "p = # katı kaydırma (p = # blok, geçici)",
  "Around # verified Karapınar sinkholes, # km block permutations (p = #) and # rigid constellation shifts (p = #) show # to # cm deeper LOS subsidence within ## km.":
    "Doğrulanmış #1 Karapınar obruğunun çevresinde #2 km'lik blok permütasyonları (p = #3) ve #4 katı küme kaydırması (p = #5), #8#9 km içinde #6 – #7 cm daha derin LOS çökmesi gösteriyor.",
  "L-band NISAR vs C-band Sentinel#": "L-bant NISAR ve C-bant Sentinel#",
  "#% summer coherence (#-GPS RMSE # cm, mixed)": "%# yaz koheransı (#-GPS RMSE # cm, karışık)",
  "In California's Tulare Basin, L-band NISAR retains #%#% usable phase over irrigated crops (#-GPS r = # #-core RMSE = # cm) and matches published C-band trends (# +/- # cm/yr vs # to # cm/yr).":
    "Kaliforniya'nın Tulare Havzası'nda L-bant NISAR sulanan ürünler üzerinde %#%# kullanılabilir faz koruyor (#-GPS r = # #-çekirdek RMSE = # cm) ve yayımlanmış C-bant eğilimleriyle uyuşuyor (# +/- # cm/yıl ile # – # cm/yıl).",
  "Global Atlas QC": "Küresel Atlas kalite kontrolü",
  "# of # regions flagged · provisional": "#2 bölgeden #1 tanesi işaretlendi · geçici",
  "Every headline value is checked against its own time series; steps of one full L-band phase cycle (# cm) or a single bad acquisition move a region to indicative only.":
    "Her manşet değer kendi zaman serisine karşı kontrol ediliyor; tam bir L-bant faz döngüsü (# cm) büyüklüğündeki sıçramalar ya da tek bir hatalı çekim bir bölgeyi yalnızca gösterge sınıfına taşıyor.",
  "Across # regions in the # Global Subsidence Atlas (# reliable, # indicative), Konya Plain leads reliable basins at # cm/#d over the #-day common window (# cm LOS, low-coverage caution), followed by Eloy, Central Valley, Kashmar, and Mashhad.":
    "#2 Küresel Çökme Atlası'ndaki #1 bölge içinde (#3 güvenilir, #4 gösterge), Konya Ovası #7-günlük ortak dönemde #5 cm/#6g ile güvenilir havzaların başında (#8 cm LOS, düşük kapsama nedeniyle dikkat); ardından Eloy, Central Valley, Kashmar ve Meşhed geliyor.",
  "Across the Konya Plain (### to ### # provisional pairs), #-km block peak LOS subsidence reaches # cm (#-reference range # to # cm) and is confirmed by ascending Path #":
    "Konya Ovası genelinde (### – ### # geçici çift) #-km'lik blok tepe LOS çökmesi # cm'ye ulaşıyor (#-referans aralığı # – # cm) ve yükselen Yörünge # ile doğrulanıyor",
  "Where the ground is sinking fastest in #": "# yılında yerin en hızlı çöktüğü yerler",
  "# Headline Quantitative Findings": "# Manşet Nicel Bulgular",
  "Key Quantitative Findings & GNSS Validation Analysis": "Temel Nicel Bulgular ve GNSS Doğrulama Analizi",
  "{0} Across the southern San Joaquin Valley ({1}), # km block-median ground motion along the radar line of sight (LOS, the direction between the satellite and the ground) reached # cm ({2}, # km N of Terra Bella on the eastern margin) and # cm in the valley interior ({3}, # km S of Lemoore; overall range # to # cm depending on reference point; median Cramér–Rao phase-noise uncertainty ±# cm). Assuming purely vertical motion at the #° radar look angle gives # cm vertical (estimate) and an annualized summer-only rate of # cm/yr LOS (estimate), with # km² sinking faster than # cm and # km² faster than # cm ({4}, {5}, {6}, {7}).":
    "{0} Güney San Joaquin Vadisi'nde ({1}) radar görüş hattı (LOS, uydu ile zemin arasındaki doğrultu) boyunca # km'lik blok medyanı yer hareketi # cm'ye ({2}, doğu kenarında Terra Bella'nın # km kuzeyi) ve vadi içinde # cm'ye ({3}, Lemoore'un # km güneyi; referans noktasına göre genel aralık # – # cm; medyan Cramér–Rao faz gürültüsü belirsizliği ±# cm) ulaştı. #° radar bakış açısında tamamen düşey hareket varsayımı # cm düşey (tahmin) ve yalnızca yaza dayalı yıllıklaştırılmış # cm/yıl LOS (tahmin) hız veriyor; # km² alan # cm'den, # km² alan # cm'den hızlı çöküyor ({4}, {5}, {6}, {7}).",
  "{0} In Central Anatolia ({1}), # km block-median LOS displacement reached # cm (±# cm median Cramér–Rao uncertainty), corresponding to # cm vertical (estimate) at the #° look angle and an annualized summer-only rate of # cm/yr LOS (estimate). Cumulative subsidence exceeded # cm across # km² and # cm across # km² ({2}, {3}, {4}).":
    "{0} İç Anadolu'da ({1}) #1 km'lik blok medyanı LOS yer değiştirmesi #2 cm'ye ulaştı (±#3 cm medyan Cramér–Rao belirsizliği); bu, #5° bakış açısında #4 cm düşeye (tahmin) ve yalnızca yaza dayalı yıllıklaştırılmış #6 cm/yıl LOS hıza (tahmin) karşılık geliyor. Kümülatif çökme #8 km²'de #7 cm'yi, #10 km²'de #9 cm'yi aştı ({2}, {3}, {4}).",
  "{0} Comparing NISAR vertical estimates against # continuous Nevada Geodetic Laboratory GNSS stations yields an overall median root-mean-square error (RMSE) of # cm (range #–# cm) and median correlation r = # Across the four actively sinking interior Tulare Basin stations ({1}, {2}, {3}, {4}), InSAR matches GPS with #–# cm RMSE, r = #–# and # cm mean bias ({5}).":
    "{0} NISAR düşey tahminlerini # sürekli Nevada Jeodezi Laboratuvarı GNSS istasyonuyla karşılaştırmak, genel medyan kök ortalama kare hatası (RMSE) olarak # cm (aralık #–# cm) ve medyan korelasyon r = # veriyor. Tulare Havzası içinde aktif çöken dört istasyonda ({1}, {2}, {3}, {4}) InSAR, GPS ile #–# cm RMSE, r = #–# ve # cm ortalama sapmayla uyuşuyor ({5}).",
  "{0} Over # common # km blocks shared by ascending Track # and descending Track # vertical-projected cumulative displacements correlate positively (r = # RMSE # cm, median difference # cm; #nd-percentile peak # cm on Track # vs. # cm on Track #), confirming that subsidence reflects real ground motion rather than a single-track processing artifact ({1}).":
    "{0} Yükselen İz #3 ile alçalan İz #4'ün paylaştığı #1 ortak #2 km'lik blokta düşeye izdüşürülmüş kümülatif yer değiştirmeler pozitif korelasyon gösteriyor (r = #5, RMSE #6 cm, medyan fark #7 cm; #8. yüzdelik tepe İz #10 için #9 cm, İz #12 için #11 cm); bu da çökmenin tek bir izin işleme hatası değil, gerçek yer hareketi olduğunu doğruluyor ({1}).",
  "{0} Using the Cramér–Rao bound (a theoretical lower bound on random radar phase noise derived from pixel coherence, which measures how consistently the surface reflects radar waves across passes, at nominal L = # looks), median cumulative phase noise is ±# cm (#th–#th percentile #–# cm; ±# cm if L = #) over Central Valley's # pairs and ±# cm (#–# cm; ±# cm if L = #) over Karapınar's # pairs. Peak subsidence signals (# to # cm LOS) exceed this formal phase noise by more than #×, though unmodeled atmospheric water-vapor delay (~#–# cm per pair) remains outside this bound ({1}, {2}).":
    "{0} Cramér–Rao sınırını kullanarak (yüzeyin radar dalgalarını geçişler boyunca ne kadar tutarlı yansıttığını ölçen piksel koheransından türetilen, rastgele radar faz gürültüsü için teorik bir alt sınır; nominal L = #1 bakış) medyan kümülatif faz gürültüsü Central Valley'nin #9 çiftinde ±#2 cm (#3.–#4. yüzdelik #5–#6 cm; L = #8 ise ±#7 cm), Karapınar'ın #15 çiftinde ±#10 cm (#11–#12 cm; L = #14 ise ±#13 cm). Tepe çökme sinyalleri (#16 – #17 cm LOS) bu biçimsel faz gürültüsünü #18×'ten fazla aşıyor; ancak modellenmemiş atmosferik su buharı gecikmesi (çift başına ~#19–#20 cm) bu sınırın dışında kalıyor ({1}, {2}).",
  "{0} Out of # evaluated infrastructure segments ≥ # km long (from # mapped features), # segments (#%) are classified high risk (gradient ≥ # mm/km with subsidence ≤ # cm, or ≤ # cm total) and # (#%) medium risk, led by the Tulare Irrigation District Canal at # mm/km longitudinal gradient and # cm peak LOS displacement ({1}).":
    "{0} Değerlendirilen ≥ #2 km uzunluğundaki #1 altyapı kesiminden (#3 haritalanmış öğeden) #4 kesim (%#5) yüksek riskli (eğim ≥ #6 mm/km ve çökme ≤ #7 cm, ya da toplam ≤ #8 cm), #9 kesim (%#10) orta riskli sınıflandı; başta #11 mm/km boyuna eğim ve #12 cm tepe LOS yer değiştirmesiyle Tulare Sulama Bölgesi Kanalı geliyor ({1}).",
  "{0} Areas within #–# km and #–# km of # cataloged sinkholes ({1}) average # cm (#% > # cm) and # cm (#% > # cm) LOS displacement, sinking # cm and # cm more than background terrain beyond # km (# cm mean). Ten road and canal segments rank high risk, topped by secondary highway ## (# mm/km gradient, # cm peak LOS, # m from {2}), while {3} averages # cm within # km ({4}).":
    "{0} Kataloglanmış #5 obruğun ({1}) #1–#2 km ve #3–#4 km çevresindeki alanlar ortalama #6 cm (%#7 > #8 cm) ve #9 cm (%#10 > #11 cm) LOS yer değiştirmesi gösteriyor; #14 km ötesindeki arka plan araziden (#15 cm ortalama) #12 cm ve #13 cm daha fazla çöküyor. On yol ve kanal kesimi yüksek riskli; başta #16#17 numaralı ikincil karayolu geliyor (#18 mm/km eğim, #19 cm tepe LOS, {2} noktasından #20 m), {3} ise #22 km içinde ortalama #21 cm ({4}).",
  "{0} Comparing NISAR L# soil moisture (#–# m³/m³) and HV radar backscatter (# to # dB) against Terra Bella ({1}) LOS subsidence (# to # cm) yields r = # for the normalized irrigation index and r = # at a #-day lagged soil moisture signal ({2}).":
    "{0} NISAR L#1 toprak nemi (#2–#3 m³/m³) ve HV radar geri saçılımını (#4 – #5 dB) Terra Bella ({1}) LOS çökmesiyle (#6 – #7 cm) karşılaştırmak, normalleştirilmiş sulama endeksi için r = #8, #10-gün gecikmeli toprak nemi sinyali için r = #9 veriyor ({2}).",
  "# Q# — Statistical Interpretation of GNSS Validation ({0})": "# S# — GNSS Doğrulamasının İstatistiksel Yorumu ({0})",
  "This comparison evaluates all # continuous Nevada Geodetic Laboratory GNSS stations across # common NISAR dates (# Jun–# Oct #), using #×# block-median vertical InSAR estimates ({0}) and #-day ({1}) median GNSS vertical positions zero-referenced to # Jun #":
    "Bu karşılaştırma, #2 ortak NISAR tarihinde (#3 Haz–#4 Eki #5) #1 sürekli Nevada Jeodezi Laboratuvarı GNSS istasyonunun tamamını, #6×#7 blok medyanı düşey InSAR tahminlerini ({0}) ve #9 Haz #10 tarihine sıfırlanmış #8-günlük ({1}) medyan GNSS düşey konumlarını kullanarak değerlendiriyor",
  "# Moving vs. Stable Station Groups ({0} threshold = # cm)": "# Hareketli ve Sabit İstasyon Grupları ({0} eşiği = # cm)",
  "Station Group": "İstasyon Grubu",
  "Stations ({0})": "İstasyonlar ({0})",
  "Median RMSE (cm)": "Medyan RMSE (cm)",
  "Mean RMSE (cm)": "Ortalama RMSE (cm)",
  "RMSE Range (cm)": "RMSE Aralığı (cm)",
  "Median Pearson {0}": "Medyan Pearson {0}",
  "Mean Pearson {0}": "Ortalama Pearson {0}",
  "Median End Diff ({0}, cm)": "Medyan Son Fark ({0}, cm)",
  "Mean Bias (cm)": "Ortalama Sapma (cm)",
  "All Stations": "Tüm İstasyonlar",
  "Moving ({0})": "Hareketli ({0})",
  "Interior Moving (excl. {0})": "İç Kesim Hareketli ({0} hariç)",
  "Stable ({0})": "Sabit ({0})",
  "# Statistical Interpretation": "# İstatistiksel Yorum",
  "Across all ten Central Valley GPS stations, provisional NISAR vertical displacement reproduces independent GPS trajectories with a median RMSE of # cm (# cm median across moving sites with {0} vs. # cm across stable sites), while Pearson correlation diverges sharply between moving stations (median #; #–# at interior Tulare Basin stations {1}, {2}, {3}, and {4}) and stable stations (median #). This contrast occurs because Pearson correlation measures linear covariance relative to true signal variance: at stable stations ({5}), real ground motion approaches zero and epoch-to-epoch differences are dominated by ~#–# cm unmodeled tropospheric wet-delay fluctuations (plus long-wavelength plane/DEM removal residuals), producing near-zero or slightly negative correlation even when absolute error stays near # cm RMSE. At high-signal basin stations and western-margin site {6} (# cm RMSE due to a single # cm atmospheric spike on # Sep #), RMSE bounds absolute accuracy while correlation reflects trajectory agreement only where deformation exceeds atmospheric noise.":
    "Central Valley'deki on GPS istasyonunun tamamında geçici NISAR düşey yer değiştirmesi, bağımsız GPS gidişatlarını #1 cm medyan RMSE ile yeniden üretiyor ({0} olan hareketli noktalarda medyan #2 cm, sabit noktalarda #3 cm); Pearson korelasyonu ise hareketli istasyonlar (medyan #4; Tulare Havzası içindeki {1}, {2}, {3} ve {4} istasyonlarında #5–#6) ile sabit istasyonlar (medyan #7) arasında keskin biçimde ayrışıyor. Bunun nedeni, Pearson korelasyonunun doğrusal kovaryansı gerçek sinyal varyansına göre ölçmesi: sabit istasyonlarda ({5}) gerçek yer hareketi sıfıra yaklaşıyor ve dönemden döneme farklara ~#8–#9 cm'lik modellenmemiş troposferik ıslak gecikme dalgalanmaları (ve uzun dalga boylu düzlem/DEM çıkarma artıkları) hâkim oluyor; bu da mutlak hata #10 cm RMSE civarında kalsa bile sıfıra yakın ya da hafif negatif korelasyon üretiyor. Yüksek sinyalli havza istasyonlarında ve batı kenarındaki {6} noktasında (#13 Eyl #14 tarihindeki tek bir #12 cm'lik atmosferik sıçrama nedeniyle #11 cm RMSE), RMSE mutlak doğruluğu sınırlarken korelasyon, gidişat uyumunu yalnızca deformasyonun atmosferik gürültüyü aştığı yerlerde yansıtıyor.",
  "# Per-Station Verification Summary": "# İstasyon Bazında Doğrulama Özeti",
  "Regime": "Rejim",
  "Moving": "Hareketli",
  "Moving (basin margin)": "Hareketli (havza kenarı)",
  "Stable": "Sabit",
  "InSAR Vert End (cm)": "InSAR Düşey Son (cm)",
  "GNSS End (cm)": "GNSS Son (cm)",
  "End Diff (cm)": "Son Fark (cm)",
  "Look Angle {0} (deg)": "Bakış Açısı {0} (derece)",
  "Max {0} (cm)": "En büyük {0} (cm)",
  "{0} Range": "{0} Aralığı",
  "Methods": "Yöntemler",
  "Risk dossier": "Risk dosyası",
  "Konya Plain, Türkiye": "Konya Ovası, Türkiye"
});

// ---- data.html ----------------------------------------------------------------------------------------------
Object.assign(window.I18N_TR, {
  "Data & Downloads (# Regions) — NISAR Vision": "Veri ve İndirmeler (# Bölge) — NISAR Vision",
  "Open data": "Açık veri",
  "Every number, downloadable": "Her sayı indirilebilir",
  "All derived datasets are plain JSON, GeoJSON and PNG files you can open in any tool. The code that produced them is in the {0} (MIT licence).":
    "Türetilmiş tüm veri setleri, herhangi bir araçla açabileceğiniz düz JSON, GeoJSON ve PNG dosyalarıdır. Bunları üreten kod {0} içinde (MIT lisansı).",
  "repository": "depo",
  "Dataset": "Veri seti",
  "File": "Dosya",
  "Quality": "Kalite",
  "Global": "Küresel",
  "All": "Tümü",
  "MIXED": "KARIŞIK",
  "PREVIEW": "ÖNİZLEME",
  "reference": "referans",
  "Global subsidence atlas (GeoJSON)": "Küresel çökme atlası (GeoJSON)",
  "Global subsidence atlas (CSV table)": "Küresel çökme atlası (CSV tablosu)",
  "Global subsidence atlas (all measured regions)": "Küresel çökme atlası (ölçülen tüm bölgeler)",
  "Atlas data dictionary": "Atlas veri sözlüğü",
  "Global Atlas documentation: {0} · {1}": "Küresel Atlas belgeleri: {0} · {1}",
  "Central Valley, California — summer #": "Central Valley, Kaliforniya — # yazı",
  "Central Valley, California — full year (Nov # – Oct #)": "Central Valley, Kaliforniya — tam yıl (Kas # – Eki #)",
  "Karapınar, Türkiye — track #": "Karapınar, Türkiye — iz #",
  "Karapınar, Türkiye — track # (second orbit)": "Karapınar, Türkiye — iz # (ikinci yörünge)",
  "London clay, UK (result: below detection)": "Londra kili, Birleşik Krallık (sonuç: tespit sınırının altında)",
  "The Fens, UK — radar through cloud": "Fens, Birleşik Krallık — bulutun içinden radar",
  "The Fens, UK — crop radar signal": "Fens, Birleşik Krallık — ürün radar sinyali",
  "Headline numbers": "Manşet sayılar",
  "Point time series": "Nokta zaman serisi",
  "Clickable ~#–# km grid": "Tıklanabilir ~#–# km ızgara",
  "Ground motion (cm, line of sight)": "Yer hareketi (cm, görüş hattı)",
  "Measurement uncertainty (#σ, cm)": "Ölçüm belirsizliği (#σ, cm)",
  "Infrastructure risk (canals, roads, rail)": "Altyapı riski (kanallar, yollar, demiryolu)",
  "Radar brightness, HV (dB)": "Radar parlaklığı, HV (dB)",
  "GPS comparison": "GPS karşılaştırması",
  "Vertical and east–west motion (two orbits)": "Düşey ve doğu–batı hareketi (iki yörünge)",
  "Soil moisture and irrigation drivers": "Toprak nemi ve sulama etkenleri",
  "Area sinking more than # / # cm": "# / # cm'den fazla çöken alan",
  "Permanent trend (cm/yr)": "Kalıcı eğilim (cm/yıl)",
  "Documented sinkholes": "Belgelenmiş obruklar",
  "Signal vs noise test": "Sinyal ve gürültü testi",
  "Field radar time series (HH, HV)": "Tarla radar zaman serisi (HH, HV)",
  "NISAR radar image, ### (quick-look)": "NISAR radar görüntüsü, ### (hızlı bakış)",
  "Verified numbers registry": "Doğrulanmış sayılar kaydı",
  "Data catalogue (everything above)": "Veri kataloğu (yukarıdakilerin hepsi)",
  "Source data": "Kaynak veri",
  "NASA-ISRO NISAR L# GUNW / GCOV and L# SME# products from the {0}. GPS time series: {1}. Infrastructure: © OpenStreetMap contributors (ODbL). Optical imagery: NASA GIBS / Worldview (VIIRS).":
    "NASA-ISRO NISAR L# GUNW / GCOV ve L# SME# ürünleri {0} kaynağından. GPS zaman serileri: {1}. Altyapı: © OpenStreetMap katkıcıları (ODbL). Optik görüntüler: NASA GIBS / Worldview (VIIRS).",
  "Alaska Satellite Facility DAAC": "Alaska Satellite Facility DAAC",
  "Nevada Geodetic Laboratory": "Nevada Jeodezi Laboratuvarı",
  "Reproduce our data in # steps": "Verimizi # adımda yeniden üretin",
  "Needs Python #+ and {0}. Without an Earthdata login you can still open every file on this page.":
    "Python #+ ve {0} gerekir. Earthdata hesabı olmadan da bu sayfadaki her dosyayı açabilirsiniz.",
  "Get a free NASA Earthdata login": "Ücretsiz bir NASA Earthdata hesabı alın",
  "{0} at {1} and put it in your {2} file (instructions in the {3}).": "{0}: {1} adresinden alın ve {2} dosyanıza ekleyin (talimatlar {3} içinde).",
  "Find the radar pairs.": "Radar çiftlerini bulun.",
  "(or with Python) search for NISAR": "(ya da Python ile) NISAR",
  "products over your area, with both dates on or after # June # and release": "ürünlerini bölgeniz için arayın; iki tarih de # Haziran # veya sonrası, sürüm",
  "(provisional). Our list:": "(geçici) olsun. Bizim listemiz:",
  "Download and cut": "İndirin ve kesin",
  "{0} each pair to the study box (about # GB in, # MB out): {1} (track # frame #).": "{0}: her çifti çalışma kutusuna göre (yaklaşık # GB girdi, # MB çıktı): {1} (iz #, çerçeve #).",
  "Turn phase into centimetres and add the pairs up:": "Fazı santimetreye çevirin ve çiftleri toplayın:",
  "{0} {1}. This writes the maps, points and summary listed above.": "{0} {1}. Bu komut yukarıda listelenen haritaları, noktaları ve özeti yazar.",
  "Check your result": "Sonucunuzu kontrol edin",
  "{0} against ours ({1}) and against GPS: {2}. All tests: {3}.": "{0}: bizimkiyle ({1}) ve GPS ile karşılaştırın: {2}. Tüm testler: {3}."
});

// ---- explorer.html ------------------------------------------------------------------------------------------
Object.assign(window.I18N_TR, {
  "Explore the data (# Regions) — NISAR Vision": "Veriyi keşfet (# Bölge) — NISAR Vision",
  "Explore the data": "Veriyi keşfet",
  "Choose a region and a layer, move through the dates, then click anywhere on the map to see how that spot moved.":
    "Bir bölge ve bir katman seçin, tarihler arasında ilerleyin, sonra o noktanın nasıl hareket ettiğini görmek için haritada herhangi bir yere tıklayın.",
  "Explorer controls": "Gezgin kontrolleri",
  "Date": "Tarih",
  "Play through the dates": "Tarihleri oynat",
  "Click the map to see one spot.": "Bir noktayı görmek için haritaya tıklayın.",
  "{0} Ground motion (cm, line of sight)": "{0} Yer hareketi (cm, görüş hattı)",
  "{0} Measurement uncertainty (#σ, cm)": "{0} Ölçüm belirsizliği (#σ, cm)",
  "{0} Infrastructure risk (canals, roads, rail)": "{0} Altyapı riski (kanallar, yollar, demiryolu)",
  "{0} Radar brightness, HV (dB)": "{0} Radar parlaklığı, HV (dB)"
});

// ---- present.html -------------------------------------------------------------------------------------------
Object.assign(window.I18N_TR, {
  "NISAR Vision — Presentation Mode (# Stops)": "NISAR Vision — Sunum Modu (# Durak)",
  "NISAR Vision · Presentation Mode": "NISAR Vision · Sunum Modu",
  "Presentation stops": "Sunum durakları",
  "Previous stop": "Önceki durak",
  "Next stop": "Sonraki durak",
  "← Prev": "← Önceki",
  "Next →": "Sonraki →",
  "Fullscreen": "Tam ekran",
  "Toggle fullscreen (F)": "Tam ekranı aç/kapat (F)",
  "Keys: ← / → or Space · F fullscreen": "Tuşlar: ← / → ya da Boşluk · F tam ekran",
  "Stop # of # · Intro & # Atlas (#:#–#:#)": "Durak # / # · Giriş ve # Atlas (#:#–#:#)",
  "Stop # of # · # Self-Checking QC (#:#–#:#)": "Durak # / # · # Öz Denetimli Kalite Kontrol (#:#–#:#)",
  "Stop # of # · # GPS & Validation (#:#–#:#)": "Durak # / # · # GPS ve Doğrulama (#:#–#:#)",
  "Stop # of # · # People & # Water Lost (#:#–#:#)": "Durak # / # · # İnsanlar ve # Kaybedilen Su (#:#–#:#)",
  "Stop # of # · # Infrastructure & # Bulletins (#:#–#:#)": "Durak # / # · # Altyapı ve # Bültenler (#:#–#:#)",
  "Stop # of # · # Simulator & # Open Engine (#:#–#:#)": "Durak # / # · # Simülatör ve # Açık Motor (#:#–#:#)",
  "Where is the ground sinking? # basins on one #-day ruler.": "Yer nerede çöküyor? Tek bir #2-günlük cetvelde #1 havza.",
  "We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: # basins (# reliable, # indicative) measured with one open pipeline on the same # days (# Jun – # Sep #), led by Konya Plain at # cm/#d (medium, caution).":
    "NASA-ISRO NISAR radar verisinin ilk aylarını kendini denetleyen küresel bir çökme atlasına dönüştürdük: aynı #4 günde (#5 Haz – #6 Eyl #7) tek açık işlem hattıyla ölçülen #1 havza (#2 güvenilir, #3 gösterge); başta #8 cm/#9g ile Konya Ovası (orta, dikkat).",
  "Top # reliable regions by common #-day rate": "Ortak #2-günlük hıza göre ilk #1 güvenilir bölge",
  "Common (cm/#d)": "Ortak (cm/#g)",
  "Konya Plain (Türkiye)": "Konya Ovası (Türkiye)",
  "Eloy (USA)": "Eloy (ABD)",
  "Central Valley (USA)": "Central Valley (ABD)",
  "Kashmar (Iran)": "Kashmar (İran)",
  "Mashhad (Iran)": "Meşhed (İran)",
  "medium (caution)": "orta (dikkat)",
  "medium (GNSS r=#)": "orta (GNSS r=#)",
  "Open Global Atlas →": "Küresel Atlası Aç →",
  "View Indicative Filter": "Gösterge Filtresini Gör",
  "Get Code & Data": "Kodu ve Veriyi Al",
  "{0} Data: NASA-ISRO NISAR, ASF DAAC. Analysis: Team Aseltech ({1}, {2}).": "{0} Veri: NASA-ISRO NISAR, ASF DAAC. Analiz: Aseltech Takımı ({1}, {2}).",
  "{0} Data: NASA-ISRO NISAR, ASF DAAC; NGL GNSS; NASA JPL OPERA. Analysis: Team Aseltech ({1}, {2}).": "{0} Veri: NASA-ISRO NISAR, ASF DAAC; NGL GNSS; NASA JPL OPERA. Analiz: Aseltech Takımı ({1}, {2}).",
  "{0} Data: NASA-ISRO NISAR, ASF DAAC; GHSL E# Analysis: Team Aseltech ({1}, {2}).": "{0} Veri: NASA-ISRO NISAR, ASF DAAC; GHSL E# Analiz: Aseltech Takımı ({1}, {2}).",
  "{0} Data: NASA-ISRO NISAR, ASF DAAC; OpenStreetMap. Analysis: Team Aseltech ({1}, {2}).": "{0} Veri: NASA-ISRO NISAR, ASF DAAC; OpenStreetMap. Analiz: Aseltech Takımı ({1}, {2}).",
  "{0} Analysis: Team Aseltech ({1}, {2}, {3}).": "{0} Analiz: Aseltech Takımı ({1}, {2}, {3}).",
  "{0} Model calibrated to USGS/NGL Terra Bella compaction and NISAR rates ({1}, {2}).": "{0} Model USGS/NGL Terra Bella sıkışmasına ve NISAR hızlarına göre kalibre edildi ({1}, {2}).",
  "# Global Atlas": "# Küresel Atlas",
  "# Self-Caught QC": "# Kendi Yakaladığımız Hata",
  "# Results & GNSS": "# Sonuçlar ve GNSS",
  "# Home Summary": "# Ana Sayfa Özeti",
  "# Konya Plain": "# Konya Ovası",
  "# Simulator": "# Simülatör",
  "A check that catches our own errors": "Kendi hatalarımızı yakalayan bir kontrol",
  "Automated time-series checks flagged # cm full L-band phase-cycle jumps; Semarang dropped from # to # cm (## reliable), Tehran updated # to # cm, and # flagged basins stay indicative only.":
    "Otomatik zaman serisi kontrolleri # cm'lik tam L-bant faz döngüsü sıçramalarını işaretledi; Semarang # cm'den # cm'ye indi (## güvenilir), Tahran # cm'den # cm'ye güncellendi ve işaretlenen # havza yalnızca gösterge olarak kalıyor.",
  "Full L-band phase-cycle unwrapping jump threshold caught at epoch #–#": "Tam L-bant faz döngüsü açma sıçrama eşiği #–# döneminde yakalandı",
  "Semarang re-processed coastal subsidence (## reliable, # cm/#d)": "Semarang yeniden işlenmiş kıyı çökmesi (## güvenilir, # cm/#g)",
  "Tehran reference moved off-basin after QC review": "Tahran referansı kalite kontrol incelemesinden sonra havza dışına taşındı",
  "# Flagged": "# İşaretli",
  "Bangkok, Beijing, Delhi, Gorgan, Pekalongan isolated as indicative only": "Bangkok, Pekin, Delhi, Gorgan, Pekalongan yalnızca gösterge olarak ayrıldı",
  "Inspect QC Rules →": "Kalite Kontrol Kurallarını İncele →",
  "See All Checks in Science →": "Tüm Kontrolleri Bilim Sayfasında Gör →",
  "Proof on the ground and uncertainty": "Sahada kanıt ve belirsizlik",
  "Provisional NISAR motion tracks # permanent Central Valley GPS stations (r = # # cm median RMSE), beats ≈ # cm formal phase noise, and includes a Mexico City OPERA pattern check (r = # winter vs summer).":
    "Geçici NISAR hareketi # sabit Central Valley GPS istasyonunu izliyor (r = # # cm medyan RMSE), ≈ # cm biçimsel faz gürültüsünü aşıyor ve bir Meksiko OPERA desen kontrolü içeriyor (r = #, kışa karşı yaz).",
  "#-station Central Valley GPS agreement (# cm median RMSE, # cm final)": "#-istasyonlu Central Valley GPS uyumu (# cm medyan RMSE, # cm son)",
  "Mexico City OPERA shape check (winter vs summer; CV r = # Eloy r = #)": "Meksiko OPERA şekil kontrolü (kışa karşı yaz; CV r = # Eloy r = #)",
  "Formal pixel phase noise (# cm median); #/# literature checks": "Biçimsel piksel faz gürültüsü (# cm medyan); #/# literatür kontrolü",
  "London Clay negative control: below_detection (#% within ±# cm)": "London Clay negatif kontrolü: tespit altında (%# ±# cm içinde)",
  "Time-Series Explorer": "Zaman Serisi Gezgini",
  "# M people on sinking ground & # km³/yr water lost": "Çöken zeminde # M kişi ve # km³/yıl kaybedilen su",
  "Overlaying GHSL # population counts # residents on # km² sinking > # cm, while # months of NISAR data isolate # km³/yr of permanent Central Valley aquifer storage lost.":
    "GHSL #1 nüfus verisini üst üste koymak, #4 cm'den fazla çöken #3 km² alanda #2 kişi sayıyor; #5 aylık NISAR verisi ise Central Valley'de kalıcı olarak kaybedilen #6 km³/yıl akifer deposunu ayırıyor.",
  "# M people": "# M kişi",
  "# residents on # km² sinking > # cm (GHSL # # basins)": "#3 cm'den fazla çöken #2 km² alanda #1 kişi (GHSL #4, #5 havza)",
  "Permanent Central Valley aquifer storage lost (mixed #-month chain)": "Central Valley'de kalıcı olarak kaybedilen akifer deposu (karışık #-aylık zincir)",
  "Earlimart permanent compaction vs # cm seasonal rebound (R² = #)": "Earlimart'ta kalıcı sıkışma ve # cm mevsimsel geri kabarma (R² = #)",
  "Central Valley area sinking > # cm LOS in # days (# cm peak)": "Central Valley'de #2 günde #1 cm LOS'tan fazla çöken alan (#3 cm tepe)",
  "Open Exposure & Storage Data →": "Etkilenme ve Depolama Verisini Aç →",
  "Open Home Page": "Ana Sayfayı Aç",
  "# / # tilting corridors & # one-page bulletins": "# / # eğilen koridor ve # tek sayfalık bülten",
  "Every canal, road and railway in the Central Valley is screened for uneven sinking with uncertainty bounds, and every atlas basin gets a printable one-page NASA-style monitoring bulletin.":
    "Central Valley'deki her kanal, yol ve demiryolu belirsizlik sınırlarıyla düzensiz çökmeye karşı taranıyor ve her atlas havzası yazdırılabilir, tek sayfalık NASA tarzı bir izleme bülteni alıyor.",
  "Peak differential tilt on the Tulare Irrigation District Canal": "Tulare Sulama Bölgesi Kanalı'nda en büyük farklı eğim",
  "Infrastructure segments > # mm/km tilt (±#% top# #% rank-invariant)": "# mm/km'den fazla eğilen altyapı kesimleri (±%#, ilk # %# sıralamadan bağımsız)",
  "Printable A# NASA-style monitoring bulletins with confidence & revision log": "Güven düzeyi ve revizyon günlüğüyle yazdırılabilir A# NASA tarzı izleme bültenleri",
  "Karapınar sinking < # km vs > # km from # mapped sinkholes (p = #)": "Karapınar'da #3 haritalanmış obruğa < #1 km ve > #2 km uzaklıkta çökme (p = #4)",
  "#× sinkholes": "#× obruk",
  "# bulletins": "# bülten",
  "See Tilt Methodology": "Eğim Yöntemini Gör",
  "Open Konya Plain Bulletin →": "Konya Ovası Bültenini Aç →",
  "A #-second simulator & an open one-command engine": "#-saniyelik bir simülatör ve tek komutlu açık bir motor",
  "Test # months of pumping choices in the NISAR Vision groundwater simulator, calibrated to NISAR rates, or reproduce any basin from public NASA ASF data with one open command.":
    "NISAR hızlarına göre kalibre edilmiş NISAR Vision yeraltı suyu simülatöründe # aylık pompalama kararlarını deneyin ya da herhangi bir havzayı açık NASA ASF verisinden tek bir açık komutla yeniden üretin.",
  "NISAR Vision groundwater simulator, #-month groundwater subsidence simulator interface": "NISAR Vision yeraltı suyu simülatörü, #-aylık yeraltı suyu çökme simülatörü arayüzü",
  "Launch Simulator →": "Simülatörü Başlat →",
  "Open Central Valley": "Central Valley'i Aç",
  "r = # (# pts)": "r = # (# nokta)"
});

// ---- faq.html (questions and answers from docs/story/judge_faq.md) --------------------------------------
Object.assign(window.I18N_TR, {
  "FAQ (# Jury Questions) — NISAR Vision": "SSS (# Jüri Sorusu) — NISAR Vision",
  "Frequently asked": "Sık sorulanlar",
  "Questions": "Sorular",
  "Judge & Engineer FAQ ({0})": "Jüri ve Mühendis SSS ({0})",
  "# What does {0} mean for these NISAR measurements?": "# {0} bu NISAR ölçümleri için ne anlama geliyor?",
  "Every science layer in our atlas uses NASA-ISRO NISAR Level# {0} products ({1}, acquired on or after {2}), which are still in early mission operations. Pre-calibration {3} granules ({4}) are excluded from our headline atlas and isolated into a separate {5} seasonal dataset. {6}":
    "Atlasımızdaki her bilim katmanı NASA-ISRO NISAR Seviye-# {0} ürünlerini ({1}, {2} veya sonrasında çekilmiş) kullanıyor; bunlar hâlâ görevin erken işletim dönemindedir. Kalibrasyon öncesi {3} veri parçaları ({4}) manşet atlasımızdan çıkarıldı ve ayrı bir {5} mevsimsel veri setine ayrıldı. {6}",
  "# Why report Line-of-Sight (LOS) displacement instead of pure vertical sinking?": "# Neden saf düşey çökme yerine görüş hattı (LOS) yer değiştirmesini raporluyorsunuz?",
  "InSAR measures one-dimensional motion along the radar's slanted Line of Sight ({0} incidence in Central Valley, {1} in Karapınar), so we keep base maps in honest LOS ({2}). Vertical figures ({3}, e.g., {4} vs. {5} LOS in Central Valley) are explicitly labeled as {6}. In California, dual-orbit Track # ascending vs. Track # descending ({7} # km blocks, {8} sign agreement for {9}) further isolates {10} vertical subsidence with {11} east-west motion at Alpaugh.":
    "InSAR, radarın eğik görüş hattı boyunca tek boyutlu hareketi ölçer (Central Valley'de {0}, Karapınar'da {1} geliş açısı); bu yüzden temel haritaları dürüstçe LOS cinsinden tutuyoruz ({2}). Düşey değerler ({3}; örneğin Central Valley'de {4}, LOS {5}) açıkça {6} olarak etiketlenir. Kaliforniya'da yükselen İz # ile alçalan İz # çift yörüngesi ({7} # km'lik blok, {9} için {8} işaret uyumu), Alpaugh'da {10} düşey çökmeyi {11} doğu-batı hareketinden ayrıca ayırıyor.",
  "estimates": "tahmin",
  "# Why rank # basins on a #-day common window instead of annual {0} rates?": "# Neden # havzayı yıllık {0} hızlar yerine #-günlük ortak bir döneme göre sıralıyorsunuz?",
  "Summer-only linear extrapolation ({0}) overstates net multi-year subsidence because confined aquifers rebound elastically during winter recharge. Ranking all {1} basins on the identical {2}-day common window ({3} to {4}, normalized to {5} LOS) compares seasonal drawdown fairly without site-specific tuning.":
    "Yalnızca yaza dayalı doğrusal dışdeğerleme ({0}) çok yıllık net çökmeyi olduğundan büyük gösterir, çünkü basınçlı akiferler kış beslenmesi sırasında esnek olarak geri kabarır. {1} havzanın hepsini aynı {2}-günlük ortak dönemde ({3} – {4}, {5} LOS'a normalleştirilmiş) sıralamak, mevsimsel su düşüşünü yere özel ayar yapmadan adil biçimde karşılaştırır.",
  "# How well do NISAR measurements match independent continuous GPS stations?": "# NISAR ölçümleri bağımsız sürekli GPS istasyonlarıyla ne kadar uyuşuyor?",
  "Across {0} continuous Nevada Geodetic Laboratory ({1}) GPS stations in California's Central Valley, NISAR vertical estimates achieve {2} cross-station correlation and {3} ({4} across {5} core Tulare stations). This GPS comparison is our primary independent validation.":
    "Kaliforniya'nın Central Valley bölgesindeki {0} sürekli Nevada Jeodezi Laboratuvarı ({1}) GPS istasyonunda NISAR düşey tahminleri istasyonlar arası {2} korelasyon ve {3} ({5} çekirdek Tulare istasyonunda {4}) elde ediyor. Bu GPS karşılaştırması birincil bağımsız doğrulamamızdır.",
  "{0} median RMSE": "{0} medyan RMSE",
  "# Why is NASA JPL's OPERA DISP-S# product a secondary check rather than a headline KPI?": "# NASA JPL'in OPERA DISP-S# ürünü neden manşet bir gösterge değil de ikincil bir kontrol?",
  "Over Mexico City, our NISAR spatial pattern matches NASA JPL's {0} product at {1} points ({2}), although OPERA covers winter and NISAR covers summer ({3} days of temporal overlap). In the Central Valley and at Eloy, agreement is weak ({4} and {5}) because observation seasons, agricultural C-band masking ({6} masked in Eloy), and viewing geometry differ.":
    "Meksiko üzerinde NISAR mekânsal desenimiz NASA JPL'in {0} ürünüyle {1} noktada örtüşüyor ({2}); oysa OPERA kışı, NISAR yazı kapsıyor ({3} gün zaman örtüşmesi). Central Valley'de ve Eloy'da uyum zayıf ({4} ve {5}), çünkü gözlem mevsimleri, tarımsal C-bant maskelemesi (Eloy'da {6} maskeli) ve bakış geometrisi farklı.",
  "# How does your self-checking QC catch unwrapping and reference errors?": "# Öz denetimli kalite kontrolünüz faz açma ve referans hatalarını nasıl yakalıyor?",
  "{0} scans every basin's step-by-step time series for {1} full L-band phase-cycle jumps, opposite-sign single-date spikes, and off-basin reference bias. It caught a {2} unwrapping jump in Semarang ({3} → {4} coastal peak after fixing) and a {5} phase jump in Beijing, downgrading {6} of {7} basins ({8}, {9}, {10}, {11}, {12}, {13}, {14}, etc.) to {15}.":
    "{0}, her havzanın adım adım zaman serisini {1} tam L-bant faz döngüsü sıçramaları, ters işaretli tek tarihli sıçramalar ve havza dışı referans sapması için tarar. Semarang'da {2} faz açma sıçramasını (düzeltmeden sonra kıyı tepesi {3} → {4}) ve Pekin'de {5} faz sıçramasını yakaladı; {7} havzadan {6} tanesini ({8}, {9}, {10}, {11}, {12}, {13}, {14} vb.) {15} sınıfına indirdi.",
  "# Why does ## Konya Plain ({0}) carry an {1} coverage caution?": "# ## Konya Ovası ({0}) neden {1} kapsama uyarısı taşıyor?",
  "Across the Konya Closed Basin ({0} days, {1} LOS peak), agricultural harvest and surface scatter leave only {2} coherent valid pixels across the wide {3} box ({4} reference spread). We therefore highlight ## Konya Plain with an explicit low-coverage caution alongside {5} faster subsidence within {6} of {7} verified Karapınar sinkholes.":
    "Konya Kapalı Havzası genelinde ({0} gün, {1} LOS tepe), tarımsal hasat ve yüzey saçılımı geniş {3} kutusunda yalnızca {2} koherant geçerli piksel bırakıyor ({4} referans yayılımı). Bu yüzden ## Konya Ovası'nı açık bir düşük kapsama uyarısıyla vurguluyoruz; yanında doğrulanmış {7} Karapınar obruğunun {6} yakınında {5} daha hızlı çökme var.",
  "# Why is Querétaro excluded from the #-basin global atlas?": "# Querétaro neden #-havzalık küresel atlastan çıkarıldı?",
  "In our diagnostic test ({0}), Querétaro showed {1}—over an order of magnitude above INEGI's {2} literature rate—with {3} of pixels driven by a single-date spike and no independently verified off-basin reference. Following our QC gate, {4} excludes Querétaro from the {5}-basin atlas rather than publishing an unverified outlier.":
    "Tanı testimizde ({0}) Querétaro {1} gösterdi; bu, INEGI'nin {2} literatür hızının bir mertebeden fazla üstündeydi; piksellerin {3} kadarı tek tarihli bir sıçramadan kaynaklanıyordu ve bağımsız olarak doğrulanmış havza dışı bir referans yoktu. Kalite kontrol kapımıza uyarak {4}, doğrulanmamış bir aykırı değeri yayımlamak yerine Querétaro'yu {5}-havzalık atlastan çıkarıyor.",
  "# How did you calculate {0} ({1}) people living on sinking ground?": "# Çöken zeminde yaşayan {0} ({1}) kişiyi nasıl hesapladınız?",
  "We intersected {0} ({1}) population grids with pixels sinking faster than {2} per {3} days {4} exceeding each basin's {5} formal noise floor ({6} total; {7} below {8}). Nested {9} is excluded from the sum to avoid double-counting inside {10}.":
    "{0} ({1}) nüfus ızgaralarını, {3} günde {2}'den hızlı çöken {4} ve her havzanın {5} biçimsel gürültü tabanını aşan piksellerle kesiştirdik (toplam {6}; {8} altında {7}). {10} içinde iki kez sayılmasın diye iç içe {9} toplamdan çıkarıldı.",
  "and": "ve",
  "# How was {0} permanent aquifer storage loss separated from seasonal bounce?": "# {0} kalıcı akifer depolama kaybı mevsimsel geri kabarmadan nasıl ayrıldı?",
  "Near Earlimart ({0}), an {1}-month {2} chain ({3} beta-precal + {4} provisional pairs) decomposes ({5}) {6} LOS permanent clay compaction from {7} peak-to-peak elastic seasonal rebound. Integrating permanent vertical compaction across {8} ({9}) yields an estimated {10} ({11} #-ref range) permanent aquifer storage-capacity loss.":
    "Earlimart yakınında ({0}) {1}-aylık bir {2} zinciri ({3} beta-ön kalibrasyon + {4} geçici çift), {6} LOS kalıcı kil sıkışmasını {7} tepeden tepeye esnek mevsimsel geri kabarmadan ayırıyor ({5}). Kalıcı düşey sıkışmayı {8} ({9}) boyunca toplamak tahmini {10} ({11} #-referans aralığı) kalıcı akifer depolama kapasitesi kaybı veriyor.",
  "mixed": "karışık",
  "beta": "beta",
  "# Are the {0} infrastructure flags structural safety assessments, and how does the simulator connect?": "# {0} altyapı işaretleri yapısal güvenlik değerlendirmesi mi, simülatör buna nasıl bağlanıyor?",
  "No—the {0} of {1} OpenStreetMap canal, road, and rail segments exceeding {2} differential tilt are strictly a {3} to prioritize field leveling, not a structural safety assessment. Our #-month {4} ({5}) calibrates a Terzaghi clay-compaction model directly to NISAR's Terra Bella summer rate ({6} vertical est., {7}).":
    "Hayır. {2} farklı eğimi aşan {1} OpenStreetMap kanal, yol ve demiryolu kesiminden {0} tanesi kesinlikle saha nivelmanına öncelik vermek için bir {3}; yapısal güvenlik değerlendirmesi değil. #-aylık {4} ({5}), bir Terzaghi kil sıkışması modelini doğrudan NISAR'ın Terra Bella yaz hızına ({6} tahmini düşey, {7}) göre kalibre ediyor.",
  "preliminary screening index": "ön tarama endeksi",
  "# Can an external engineer reproduce your pipeline, and what DEM/AI safeguards apply?": "# Dışarıdan bir mühendis işlem hattınızı yeniden üretebilir mi, hangi DEM/yapay zekâ güvenceleri var?",
  "Yes—any {0} basin can be reproduced from public NASA ASF {1} granules with {2}, using {3} strictly for elevation-dependent tropospheric delay correction ({4} and {5} verify every number). Code and text drafts used Claude Code, Gemini/Antigravity, and OpenAI Codex with human/test verification, and {6} appear anywhere on the site.":
    "Evet. Her {0} havza, açık NASA ASF {1} veri parçalarından {2} ile yeniden üretilebilir; {3} yalnızca yüksekliğe bağlı troposferik gecikme düzeltmesi için kullanılıyor (her sayıyı {4} ve {5} doğruluyor). Kod ve metin taslaklarında insan ve test doğrulamasıyla Claude Code, Gemini/Antigravity ve OpenAI Codex kullanıldı; sitede hiçbir yerde {6} yok.",
  "zero AI-generated images": "yapay zekâyla üretilmiş görsel",
  "How does this relate to NASA's NISAR StoryMap?": "Bunun NASA'nın NISAR StoryMap'iyle ilişkisi ne?",
  "NASA's {0} (Peacock et al. # NISAR ArcGIS StoryMaps) explains how radar detects sinking from groundwater pumping, using the California Central Valley and the California Aqueduct as its example: NASA's airborne radar UAVSAR saw over # inches of subsidence in parts of a “subsidence bowl” between # and # (Miller et al. # {1} # #; Jones et al. #). The StoryMap describes what NISAR {2} do. Our project is that next step with real # NISAR data: the same valley measured from orbit, checked against GPS stations and a second satellite pass, and turned into a risk list for canals and roads.":
    "NASA'nın {0} çalışması (Peacock vd. #1 NISAR ArcGIS StoryMaps), radarın yeraltı suyu pompalamasından kaynaklanan çökmeyi nasıl tespit ettiğini Kaliforniya Central Valley ve California Su Kemeri örneğiyle anlatıyor: NASA'nın havadan radarı UAVSAR, #3 ile #4 arasında bir \"çökme çanağının\" bazı kesimlerinde #2 inçten fazla çökme gördü (Miller vd. #5 {1} #6 #7; Jones vd. #8). StoryMap, NISAR'ın ne yapacağını ({2}) anlatıyor. Bizim projemiz gerçek #9 NISAR verisiyle o bir sonraki adım: aynı vadi yörüngeden ölçüldü, GPS istasyonları ve ikinci bir uydu geçişiyle kontrol edildi ve kanallar ile yollar için bir risk listesine dönüştürüldü.",
  "will": "yapacağını",
  "Land Subsidence StoryMap": "Arazi Çökmesi StoryMap",
  "How we used AI": "Yapay zekâyı nasıl kullandık",
  "Code, analysis scripts and text were written with the help of AI assistants (Anthropic Claude, Google Gemini) and checked by the team: every number comes from the data files, every scientific claim has a source, and tests cover the core conversions. The site uses no AI-generated images: every map and chart shows real measurements.":
    "Kod, analiz betikleri ve metinler yapay zekâ asistanlarının (Anthropic Claude, Google Gemini) yardımıyla yazıldı ve ekip tarafından kontrol edildi: her sayı veri dosyalarından geliyor, her bilimsel iddianın bir kaynağı var ve testler temel dönüşümleri kapsıyor. Sitede yapay zekâyla üretilmiş görsel yok: her harita ve grafik gerçek ölçümleri gösteriyor."
});

// ---- simulator: every water-year class and end-of-run summary (game/model.js, game/game.js) --------------
(function () {
  const WY = {'Wet': 'Yağışlı', 'Above Normal': 'Normalin Üstünde', 'Below Normal': 'Normalin Altında', 'Dry': 'Kurak', 'Critical': 'Kritik'};
  const CLS = '(Wet|Above Normal|Below Normal|Dry|Critical)';
  const SRC = {'California DWR SJV Water Year Index': 'Kaliforniya DWR SJV Su Yılı Endeksi',
    'Anatolian Interior Precipitation Index (illustrative)': 'İç Anadolu Yağış Endeksi (temsili)'};
  const place = n => (n === 'W. Karapinar' ? 'Batı Karapınar' : n);
  const sink = s => (s ? ' Haritalanmış obrukların yakınında obruk risk göstergeleri yüksek (yalnızca gösterge).' : '');
  const SINK = '( Sinkhole risk indicators are elevated near mapped obruks \\(indicator only\\)\\.)?';
  function cap(s) {
    let m = s.match(/^Full or near-full surface deliveries \(([\d.]+)% cap\) available\.$/);
    if (m) return `Tam ya da tama yakın yüzey suyu teslimatı (%${m[1]} tavan) mevcut.`;
    m = s.match(/^Surface allocations capped at ([\d.]+)% under seasonal quota rules\.$/);
    if (m) return `Yüzey suyu payları mevsimlik kota kurallarıyla %${m[1]} ile sınırlandı.`;
    return s;
  }
  window.I18N_TR_PATTERNS.push(
    [new RegExp('^(California DWR SJV Water Year Index|Anatolian Interior Precipitation Index \\(illustrative\\)) sets WY(\\d+) to ' + CLS + '\\. (.+)$'),
      m => `${SRC[m[1]]} SY${m[2]} için ${WY[m[3]]} dedi. ${cap(m[4])}`],
    [new RegExp('^WY(\\d+): ' + CLS + ' \\(([\\d.]+)% (Surface )?Cap\\)$'),
      m => `SY${m[1]}: ${WY[m[2]]} (%${m[3]} ${m[4] ? 'Yüzey Suyu ' : ''}Tavan${m[4] ? 'ı' : ''})`],
    [new RegExp('^Water Year (\\d+) Declaration: ' + CLS + ' Year$'),
      m => `Su Yılı ${m[1]} İlanı: ${WY[m[2]]} Yıl`],
    [new RegExp('^What this means: Heavy groundwater pumping dropped levels past historical lows, locking in (\\S+) cm of permanent clay collapse near (.+?)\\. Even future wet winters cannot restore that lost underground pore storage\\.' + SINK + '$'),
      m => `Bunun anlamı: Yoğun yeraltı suyu pompalaması seviyeleri tarihî en düşük değerlerin altına indirdi ve ${place(m[2])} yakınında ${m[1]} cm kalıcı kil çökmesine yol açtı. Gelecekteki yağışlı kışlar bile kaybedilen yeraltı gözenek deposunu geri getiremez.${sink(m[3])}`],
    [new RegExp('^What this means: Summer irrigation temporarily pushed hotspots past historical lows, causing (\\S+) cm of permanent clay collapse near (.+?)\\. Reducing summer pumping peaks before dry years protects surface corridors and shallow wells\\.' + SINK + '$'),
      m => `Bunun anlamı: Yaz sulaması sıcak noktaları geçici olarak tarihî en düşük seviyelerin altına itti ve ${place(m[2])} yakınında ${m[1]} cm kalıcı kil çökmesine yol açtı. Kurak yıllardan önce yaz pompalama tepe değerlerini azaltmak yüzey koridorlarını ve sığ kuyuları korur.${sink(m[3])}`]
  );
})();

Object.assign(window.I18N_TR, {
  "Result": "Sonuç",
  "Wet": "Yağışlı",
  "Above Normal": "Normalin Üstünde",
  "Below Normal": "Normalin Altında",
  "Dry": "Kurak",
  "Critical": "Kritik"
});

// ---- texts changed on 15 Nov after the atlas update (Eloy #1, Konya indicative) ----
Object.assign(window.I18N_TR, {
  "low · indicative (#% valid pixels, under review)": "düşük · gösterge (%# geçerli piksel, inceleniyor)",
  "{0} per # days at Eloy, Arizona, the fastest reliable basin. Konya Plain shows a stronger signal (#) but our own review keeps it indicative.": "{0} / # gün, Arizona'daki Eloy'da, en hızlı çöken güvenilir havza. Konya Ovası daha güçlü bir sinyal (#) gösteriyor ama kendi incelememiz onu gösterge olarak tutuyor.",
  "We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: # basins (# reliable, # indicative) measured with one open pipeline on the same # days (# Jun – # Sep #), led by Eloy, Arizona at # cm/#d; Konya Plain (#) stays indicative after our own review.": "NASA-ISRO NISAR radar verisinin ilk aylarını kendini denetleyen küresel bir çökme atlasına dönüştürdük: aynı #4 günde (#5 Haz – #6 Eyl #7) tek açık işlem hattıyla ölçülen #1 havza (#2 güvenilir, #3 gösterge); başta #8 cm/#9g ile Arizona'daki Eloy geliyor; Konya Ovası (#10) kendi incelememizden sonra gösterge olarak kalıyor.",
  "Mexico City (Mexico)": "Meksiko (Meksika)",
  "Rank": "Sıra",
  "# Jun – # Sept": "# Haz – # Eyl"
});

// ---- headings after the 15 Nov uncertainty.md cleanup (Q27 and copy markers removed) ----
Object.assign(window.I18N_TR, {
  "# Statistical Interpretation of GNSS Validation ({0})": "# GNSS Doğrulamasının İstatistiksel Yorumu ({0})",
  "Statistical Interpretation of GNSS Validation ({0})": "GNSS Doğrulamasının İstatistiksel Yorumu ({0})",
  "# Summary: How We Know the Signal Is Real": "# Özet: Sinyalin Gerçek Olduğunu Nasıl Biliyoruz",
  "Summary: How We Know the Signal Is Real": "Özet: Sinyalin Gerçek Olduğunu Nasıl Biliyoruz",
  "InSAR Uncertainty Budget & GNSS Validation Synthesis": "InSAR Belirsizlik Bütçesi ve GNSS Doğrulama Sentezi"
});
