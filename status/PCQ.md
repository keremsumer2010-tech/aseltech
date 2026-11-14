# PCQ durum

- Görev: bağımsız kontrol (1a–1e) → Q13 README → Q15 code review → 30 dk'da bir yeniden kontrol
- Durum: çalışıyor — Tur 1 (`docs/qa/PCQ.md`) ✔ · Q13 README ✔ · Q15 `docs/code_review.md` ✔ (24 test + 2 self-test geçti) → 30 dk'lık tekrar kontrol döngüsü
- Güncelleme: 2026-11-14 15:25 TR (Tur 3: uçtan uca tarayıcı testi — site, Pages kopyası, oyun, 3D, telefon: kırık şey yok; 1 orta + 5 küçük bulgu, `docs/qa/PCQ.md`)
- En kritik: pitch.md hotspot konumu yanlış (Terra Bella olmalı); site cümlesinde küçük değerler için "bank card" ölçeği ve gürültü eşiği yok; Konya katmanında lejant yok.
- Q15 en kritik: Pages yayını `risk/` (oyun kullanıyor) ve `web3d/` kopyalamıyor; `pipeline/download.py` .netrc parolasını Bearer token olarak gönderiyor.
- AI: Claude Code (Opus) → çapraz dosya kontrolü, rapor yazımı
- BLOCKED:
