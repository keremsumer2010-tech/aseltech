# aseltech — NISAR Pulse: Follow the Water (TÜM ajanlar önce bunu okur)

NASA Space Apps 2026 · Challenge "Dancing with the SARs" · Team Taykut · Local event: Lincoln (UK).
NISAR radar verisinden yer çökmesini (Central Valley ABD, Karapınar TR) ve bulutlar altındaki İngiltere'yi gösteren,
herkesin okuyabileceği açık kaynak web hikâyesi + Aquifer Manager oyunu.
**Lincoln sunumu BUGÜN (Cmt 14 Kas), demo 17:30 TR. Küresel teslim Paz 23:59 UK = Pzt 02:59 TR.**

## Okuma sırası (başlarken bir kez, sonra sadece değişeni — rules/RULES.md K-1)
1. `rules/RULES.md` — K-1…K-14: git akışı, yasaklar, çakışma, "bitti" tanımı, hiç boş kalma, kalibrasyon, hata kaydı
2. `rules/VERI_SOZLESMESI.md` — bölgeler, kalite sınıfları, tüm dosya formatları ve sahipleri
3. `docs/GOREV_DAGILIMI.md` — kim kim, sahiplik, bağımlılıklar
4. `tasks/PCx.md` — SENİN görevlerin (kimliğini bilmiyorsan: AGENTS.md veya klasör adına bak, yoksa insana sor)
5. Gerektiğinde: `docs/URUN_TANIMI.md`, `docs/DEPO_HARITASI.md`, `docs/SOZLUK.md`, `docs/MASTER_PLAN.md`, `tasks/QUEUE.md`

## Asla unutma (özet — ayrıntı RULES.md)
- Sadece kendi yazma alanın; `git add <yol>`, asla `git add -A`. Push öncesi `git pull --rebase`.
- İş bitince SORMADAN sıradakine geç: kendi görev → QUEUE → QA. Engel → `BLOCKED` yaz, başka işe geç.
- Uydurma sayı/koordinat/link yok. Kalibrasyon NISAR projesinin işi; kalite etiketi zorunlu. AI görseli = etiketli, veri değil.
- Şifre isteme/görme. Sitede görünen her metin İngilizce.

## Resmi kaynaklar
- NISAR Science Users' Handbook 2. baskı (Ekim 2025): §2.4 uygulamalar, §5 ürünler, §6 algoritmalar, §7 hata kaynakları
- Solid Earth ATBD: https://github.com/nisar-solid/ATBD · L3 Cookbook: https://github.com/ASFOpenSARlab/NISAR_ATBD_Cookbook
- Veri: ASF (`platform=NISAR`); `.h5` Earthdata girişi ister, browse PNG girişsiz.
