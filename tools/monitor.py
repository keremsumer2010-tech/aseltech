"""Terminal team monitor: who is working right now? (PC1)
Usage (repo root):  python tools/monitor.py   — refreshes every 60 s, Ctrl+C to stop.
Reads origin/main only (git fetch); never changes your working tree."""
import os, re, subprocess, sys, time
from datetime import datetime, timezone

PCS = [("PC2", "Memir", "Delta, Konya Ovası"), ("PC3", "Mehmet", "Claude Code · site"), ("PC4", "İbrahim", "metin, slayt, kaynak"),
       ("PC5", "Mehmet", "AG-1 · bilim paketi"), ("PC6", "Mehmet", "AG-2 · oyun + medya"), ("PC7", "Kerem", "Codex · QA, Fens"),
       ("PC8", "Mehmet", "AG-3 · UK metin, Konya p172"), ("PC9", "Mehmet-2", "AG · tam yıl Q08"), ("PC10", "Memir", "AG-2 · küresel vitrin"), ("PC11", "salciserem2031", "Antigravity · atlas yeniden hesap")]
G, Y, R, D, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[90m", "\033[1m", "\033[0m"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout

def status_line(pc):
    txt = git("show", f"origin/main:status/{pc}.md")
    durum = next((l.strip("- ").strip() for l in txt.splitlines() if re.match(r"^\s*-\s*(Durum|Şu an)", l, re.I)), "")
    blk = next((l.split(":", 1)[1].strip() for l in txt.splitlines() if "BLOCKED:" in l), "")
    blocked = bool(blk) and not re.match(r"^[*`_ ]*(yok|none|no|-|—)", blk, re.I)
    return durum, blocked, blk

def main():
    os.system("")  # enable ANSI on Windows
    while True:
        git("fetch", "-q", "origin", "main")
        log = git("log", "origin/main", "-300", "--format=%ct\t%s").splitlines()
        now = datetime.now(timezone.utc).timestamp()
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{B}aseltech — canlı takım durumu{X}   {datetime.now():%H:%M:%S}   (60 sn'de bir yenilenir, Ctrl+C çıkış)\n")
        print(f"{'PC':<5}{'Kim':<11}{'Rol':<24}{'Durum':<14}{'Son commit':<12}Son iş")
        print("-" * 118)
        for pc, who, role in PCS:
            rx = re.compile(rf"^\[?{pc}(\]|:|\s)")
            last = next(((float(t), s) for t, s in (l.split("\t", 1) for l in log if "\t" in l) if rx.match(s)), None)
            durum, blocked, blk = status_line(pc)
            if blocked: st, c = "ENGELLİ", R
            elif last is None: st, c = "başlamadı", D
            else:
                m = (now - last[0]) / 60
                st, c = ("AKTİF", G) if m < 20 else (("yavaş", Y) if m < 45 else ("SESSİZ", R))
            age = "—" if last is None else f"{int((now - last[0]) / 60)} dk önce"
            msg = (blk if blocked else (last[1] if last else durum))[:60]
            print(f"{pc:<5}{who:<11}{role:<24}{c}{st:<14}{X}{age:<12}{msg}")
        print(f"\n{D}AKTİF: <20 dk · yavaş: 20–45 dk · SESSİZ: >45 dk · ENGELLİ: status dosyasında BLOCKED{X}")
        try: time.sleep(60)
        except KeyboardInterrupt: sys.exit(0)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: pass
