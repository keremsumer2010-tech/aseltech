#!/usr/bin/env python3
"""Build the <=3 min (115s) 1080p overview video with English subtitles for Cambridge, MA virtual judges.

Follows the nine-work flow on web/index.html using real site screenshots and pipeline figures.
Output: docs/story/media/nisar_vision_overview.mp4
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
MEDIA_ROOT = REPO_ROOT / "docs" / "story" / "media"
OUT_MP4 = MEDIA_ROOT / "nisar_vision_overview.mp4"

WIDTH = 1920
HEIGHT = 1080
TOP_H = 64
SUB_H = 152
CANVAS_H = HEIGHT - TOP_H - SUB_H
FPS = 25

BG_HEX = (11, 15, 20)        # #0b0f14
PANEL_HEX = (18, 25, 35)     # #121923
BORDER_HEX = (34, 48, 65)    # #223041
TEXT_HEX = (230, 237, 243)   # #e6edf3
MUTED_HEX = (139, 155, 176)  # #8b9bb0
ACCENT_HEX = (77, 163, 255)  # #4da3ff

SCENES = [
    {
        "image": "site_home_desk.png",
        "duration": 10,
        "tag": "00 · INTRO · CAMBRIDGE, MA (VIRTUAL)",
        "sub": "NISAR Vision turns NASA-ISRO NISAR L-band radar into a self-checking global subsidence atlas: 29 basins, 93 days, every number traceable.",
    },
    {
        "image": "site_atlas_desk.png",
        "duration": 12,
        "tag": "01 · GLOBAL SUBSIDENCE ATLAS (29 BASINS)",
        "sub": "#1 Eloy, Arizona sinks -8.6 cm/100d (-3.4 in/100d) along satellite line-of-sight; 4 of 15 reliable basins are in the U.S. (Eloy, Central Valley, Houston, Delta).",
    },
    {
        "image": "pc10_semarang_qc.png",
        "duration": 12,
        "tag": "02 · SELF-CHECKING QUALITY CONTROL",
        "sub": "Automated checks caught a 12.1 cm (4.8 in) phase-cycle jump in Semarang (-12.1 to -6.2 cm) and flagged 14 low-coverage basins like Konya Plain as indicative.",
    },
    {
        "image": "validation_scatter.png",
        "duration": 12,
        "tag": "03 · GROUND TRUTH (GPS & OPERA)",
        "sub": "Vertical estimates match 10 California GPS stations at r = 0.924 (1.00 cm median RMSE), plus secondary winter-vs-summer OPERA comparison in Mexico City (r = 0.912).",
    },
    {
        "image": "pc8_exposure.png",
        "duration": 11,
        "tag": "04 · POPULATION EXPOSURE (GHSL E2025)",
        "sub": "Intersecting displacement above each city's 2-sigma noise floor with GHSL maps 1,167,429 residents on 477.72 km2 sinking faster than -5 cm (-2.0 in) per summer.",
    },
    {
        "image": "pc8_storage_loss.png",
        "duration": 11,
        "tag": "05 · PERMANENT AQUIFER STORAGE LOSS",
        "sub": "Separating seasonal elastic rebound from permanent clay compaction in California's Central Valley yields 0.3174 km3/yr of groundwater storage lost for good.",
    },
    {
        "image": "pc7_risk_prob.png",
        "duration": 11,
        "tag": "06 · INFRASTRUCTURE PRE-SCREENING",
        "sub": "Differential tilt screening flags 81 of 645 canal, road, and rail corridors (>10 mm/km) — a pre-screening index for leveling teams, not a structural safety rating.",
    },
    {
        "image": "site_bulletin_desk.png",
        "duration": 11,
        "tag": "07 · EARLY-WARNING A4 BULLETINS",
        "sub": "One command builds 29 NASA Disasters-style A4 monitoring bulletins reporting sinking rates, GHSL population exposure, confidence badges, and calibration notices.",
    },
    {
        "image": "site_game_desk.png",
        "duration": 11,
        "tag": "08 · 24-MONTH AQUIFER SIMULATOR",
        "sub": "An interactive Terzaghi compaction simulator calibrated to Terra Bella rates lets students and water managers test 24 months of pumping in 30 seconds.",
    },
    {
        "image": "pc1_atlas_world.png",
        "duration": 14,
        "tag": "09 · OPEN ENGINE & CALIBRATION NOTICE",
        "sub": "Reproduce any basin via python -m pipeline.nisarvision. NISAR data are provisional; calibration and validation are carried out by NASA-JPL and ISRO, not by our team.",
    },
]


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if mono:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "DejaVuSansMono.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_frame(scene: dict, idx: int, total: int, t_start: float, total_dur: float) -> Image.Image:
    frame = Image.new("RGB", (WIDTH, HEIGHT), BG_HEX)
    draw = ImageDraw.Draw(frame)

    font_hdr = load_font(20, bold=True)
    font_tag = load_font(18, bold=True, mono=True)
    font_sub = load_font(29, bold=True)

    # Top header bar
    draw.rectangle([0, 0, WIDTH, TOP_H], fill=PANEL_HEX)
    draw.line([(0, TOP_H), (WIDTH, TOP_H)], fill=BORDER_HEX, width=2)
    draw.text((48, 20), "NISAR Vision — Follow the Water · NASA Space Apps 2026 (Cambridge, MA Virtual)", font=font_hdr, fill=TEXT_HEX)
    right_lbl = f"Scene {idx + 1}/{total}"
    rb = draw.textbbox((0, 0), right_lbl, font=font_tag)
    draw.text((WIDTH - 48 - (rb[2] - rb[0]), 21), right_lbl, font=font_tag, fill=ACCENT_HEX)

    # Load and fit visual cleanly inside CANVAS_H
    img_path = MEDIA_ROOT / scene["image"]
    if not img_path.is_file():
        raise FileNotFoundError(f"Missing media file: {img_path}")
    src = Image.open(img_path).convert("RGB")
    max_w, max_h = WIDTH - 96, CANVAS_H - 36
    scale = min(max_w / src.width, max_h / src.height)
    new_w, new_h = int(src.width * scale), int(src.height * scale)
    lanczos = getattr(Image, "Resampling", Image).LANCZOS
    resized = src.resize((new_w, new_h), lanczos)
    px = (WIDTH - new_w) // 2
    py = TOP_H + (CANVAS_H - new_h) // 2
    draw.rectangle([px - 2, py - 2, px + new_w + 1, py + new_h + 1], outline=BORDER_HEX, width=2)
    frame.paste(resized, (px, py))

    # Bottom subtitle strip
    sub_y0 = HEIGHT - SUB_H
    draw.rectangle([0, sub_y0, WIDTH, HEIGHT], fill=PANEL_HEX)
    draw.line([(0, sub_y0), (WIDTH, sub_y0)], fill=BORDER_HEX, width=2)
    prog_w = int(WIDTH * min(1.0, max(0.0, (t_start + scene["duration"]) / total_dur)))
    draw.line([(0, sub_y0 + 1), (prog_w, sub_y0 + 1)], fill=ACCENT_HEX, width=4)

    draw.text((48, sub_y0 + 16), scene["tag"], font=font_tag, fill=ACCENT_HEX)
    wrapped = textwrap.wrap(scene["sub"], width=94)
    line_y = sub_y0 + 50
    for line in wrapped[:2]:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, line_y), line, font=font_sub, fill=TEXT_HEX)
        line_y += 40

    return frame


def main() -> int:
    total_dur = float(sum(s["duration"] for s in SCENES))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        concat_lines = []
        t_cur = 0.0
        for idx, scene in enumerate(SCENES):
            frame = render_frame(scene, idx, len(SCENES), t_cur, total_dur)
            png_path = tmp_dir / f"scene_{idx:02d}.png"
            frame.save(png_path, format="PNG")
            concat_lines.append(f"file '{png_path.as_posix()}'")
            concat_lines.append(f"duration {scene['duration']}")
            t_cur += scene["duration"]
        # Repeat last file as required by ffmpeg concat demuxer
        concat_lines.append(f"file '{(tmp_dir / f'scene_{len(SCENES)-1:02d}.png').as_posix()}'")

        concat_file = tmp_dir / "concat.txt"
        concat_file.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-vf", f"fps={FPS},format=yuv420p",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-movflags", "+faststart",
            str(OUT_MP4),
        ]
        subprocess.run(cmd, check=True)

    size_mb = OUT_MP4.stat().st_size / (1024 * 1024)
    print(f"Created {OUT_MP4.relative_to(REPO_ROOT)}: {total_dur:.0f}s, {size_mb:.2f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
