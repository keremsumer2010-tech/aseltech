"""Build a self-contained Aquifer Run zip for itch.io (HTML5 game upload). PC1.

The web version reaches outside web/run/ (world map image, radar images, site links). itch.io needs
everything inside one zip with index.html at its root, so this copies those files in and rewrites
the paths. Site links point to the live NISAR Vision site.

Usage: python tools/build_itch.py   ->  dist/aquifer_run_itch.zip  (dist/ is not part of the site)
"""
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "web" / "run"
SITE = "https://nisar-vision.pages.dev/"
OUT_DIR = ROOT / "dist" / "aquifer_run_itch"
ZIP = ROOT / "dist" / "aquifer_run_itch.zip"
GAME_JS = ["art.js", "engine.js", "player.js", "systems.js", "main.js"]


def main():
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    (OUT_DIR / "levels").mkdir(parents=True)
    (OUT_DIR / "assets").mkdir()

    # index.html: no PWA bits inside the itch.io frame, local logo path
    html = (RUN / "index.html").read_text(encoding="utf-8")
    html = re.sub(r'<link rel="manifest"[^>]*>\n?', "", html)
    html = re.sub(r"<script>if \('serviceWorker'.*?</script>\n?", "", html)
    html = html.replace("../assets/", "assets/")
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8", newline="\n")

    for name in GAME_JS:
        s = (RUN / name).read_text(encoding="utf-8")
        s = s.replace("'../assets/", "'assets/")
        s = s.replace("'../atlas.html", "'" + SITE + "atlas.html").replace("'../index.html'", "'" + SITE + "'")
        if "../" in s:
            raise SystemExit(name + " still has a ../ path: fix build_itch.py")
        (OUT_DIR / name).write_text(s, encoding="utf-8", newline="\n")

    for lv in sorted((RUN / "levels").glob("*.json")):
        d = json.loads(lv.read_text(encoding="utf-8"))
        radar = d.get("radar")
        if radar and radar.startswith("../data/"):
            src = ROOT / radar[3:]
            dst = OUT_DIR / radar[3:]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            d["radar"] = radar[3:]
        (OUT_DIR / "levels" / lv.name).write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    for a in ["atlas_world.jpg", "logo_mark_64.png", "logo_mark_192.png"]:
        shutil.copy2(ROOT / "web" / "assets" / a, OUT_DIR / "assets" / a)

    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT_DIR.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(OUT_DIR).as_posix())
    n = sum(1 for f in OUT_DIR.rglob("*") if f.is_file())
    print(f"{ZIP.relative_to(ROOT)}: {n} files, {ZIP.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
