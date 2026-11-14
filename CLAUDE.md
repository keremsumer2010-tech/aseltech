# aseltech: giriş noktası (tüm ajanlar ve insanlar önce bunu okur)

NASA Space Apps 2026 · Challenge: **Dancing with the SARs** · Ürün: **NISAR Pulse: Follow the Water**
Takım Taykut · Local Event: Lincoln (UK) · Global teslim: **Paz 15 Kas 23:59 UK = Pzt 02:59 TR** (iç hedef Paz 22:00 TR)

## Proje tek paragrafta

NASA-ISRO uydusu NISAR'ın radar verisiyle (GUNW: yer hareketi, GCOV: radar görüntüsü, SME2: toprak nemi)
tarım bölgelerinde yeraltı suyu pompalandıkça yerin nasıl çöktüğünü ölçüyor, bunu herkesin okuyabileceği
bir web hikâyesine çeviriyoruz: santim haritası, zaman kaydırıcısı, tıkla-grafik, sade İngilizce cümle,
altyapı riski ve GPS doğrulaması. Bölgeler: California Central Valley (ana), Konya/Karapınar, UK (Fens).
Ayrıntı: `docs/URUN_TANIMI.md`.

## Okuma sırası: bu sırayla, eksiksiz oku, sonra işe başla

| # | Dosya | Neden |
|---|---|---|
| 1 | `rules/RULES.md` | Değişmez kurallar. **İlk komuttan önce.** Git güvenliği, dosya sahipliği, veri kalitesi |
| 2 | `docs/GOREV_DAGILIMI.md` | Kim kim, kim neyin sahibi, kim kimi bekliyor. **Burada kendi PC numaranı bul** |
| 3 | `tasks/PCx.md` | Senin görev dosyan (x = kendi numaran) |
| 4 | `rules/VERI_SOZLESMESI.md` | Dosya formatları, bölge sınırları, kalite etiketleri. Veri üreten/okuyan herkes |
| 5 | `docs/ZAMAN_CIZELGESI.md` | **Kim saat kaçta ne yapar, iş bitince sıradaki ne.** Her işten sonra buraya bak |
| 6 | `docs/TODAY_PLAN.md` | Bugünün saat saat hedefi (Lincoln sunumu bugün, demo 17:30 TR) |

**Görevin bitince durma:** `rules/RULES.md` §7.1 hiç boş kalma protokolü → kendi sonraki görevin → `tasks/QUEUE.md` → QA. Her 30-45 dakikada `git pull`.

Gerektiğinde: `docs/MASTER_PLAN.md` (iki günlük ana plan) · `docs/DEPO_HARITASI.md` (hangi klasör ne) ·
`docs/SOZLUK.md` (GUNW, LOS, coherence gibi terimler) · `tasks/QUEUE.md` (ortak iş kuyruğu) · `tasks/BACKLOG.md` (bonus işler).

## Hangi PC'sin?

Klasör adın ve bilgisayarın söyler. Tablo: `docs/GOREV_DAGILIMI.md` §1. Emin değilsen insana sor, tahmin etme.

## Bu dosyanın bakımı

Sadece PC1 (Kerem) değiştirir. Kural değişikliği `rules/`, görev değişikliği `tasks/` altında yapılır;
bu dosya yalnızca giriş noktasıdır, kısa kalır.
