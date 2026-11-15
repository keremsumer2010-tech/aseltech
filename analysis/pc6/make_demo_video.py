#!/usr/bin/env python3
"""Assemble the <=30s real-data project demo video (1080p MP4 with burned subtitles)."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[2]
MEDIA_ROOT = REPO_ROOT / "docs" / "story" / "media"
OUT_MP4 = MEDIA_ROOT / "demo_30s.mp4"

WIDTH = 1920
HEIGHT = 1080
CANVAS_H = 940
SUB_H = HEIGHT - CANVAS_H  # 140 px clean bottom band for subtitles
FPS = 24

BG_HEX = (11, 15, 20)        # #0b0f14
PANEL_HEX = (18, 25, 35)     # #121923
BORDER_HEX = (34, 48, 65)    # #223041
TEXT_HEX = (230, 237, 243)   # #e6edf3
MUTED_HEX = (139, 155, 176)  # #8b9bb0
ACCENT_HEX = (77, 163, 255)  # #4da3ff
WARN_HEX = (245, 185, 66)    # #f5b942


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Resolve crisp TrueType font on Windows/Linux with clean fallback."""
    if mono:
        candidates = [
            "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
            "DejaVuSansMono.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def ffprobe_duration(video_path: Path) -> float:
    """Return exact duration in seconds from ffprobe."""
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        text=True,
    ).strip()
    return float(out)


def render_subtitle_strip(
    subtitle_text: str,
    scene_label: str,
    t_start: float,
    total_dur: float,
) -> Image.Image:
    """Render a 1920x140 bottom bar containing the English subtitle and subtle timeline progress."""
    strip = Image.new("RGB", (WIDTH, SUB_H), BG_HEX)
    draw = ImageDraw.Draw(strip)

    # Top divider + thin progress indicator
    draw.line([(0, 0), (WIDTH, 0)], fill=BORDER_HEX, width=2)
    prog_w = int(WIDTH * min(1.0, max(0.0, t_start / total_dur)))
    if prog_w > 0:
        draw.line([(0, 1), (prog_w, 1)], fill=ACCENT_HEX, width=3)

    font_tag = load_font(18, bold=True, mono=True)
    font_sub = load_font(30, bold=True)

    # Scene indicator badge on left
    draw.text((48, 16), scene_label, font=font_tag, fill=MUTED_HEX)

    # Centered subtitle wrapped nicely within 1760px
    wrapped = textwrap.wrap(subtitle_text, width=84)
    line_y = 46 if len(wrapped) <= 1 else 38
    for line in wrapped[:2]:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, line_y), line, font=font_sub, fill=TEXT_HEX)
        line_y += 38

    return strip


def fit_image_canvas(src_img: Image.Image, header_text: str | None = None) -> Image.Image:
    """Fit a raster PNG cleanly onto 1920x940 dark slate preserving aspect ratio."""
    canvas = Image.new("RGB", (WIDTH, CANVAS_H), BG_HEX)
    top_pad = 58 if header_text else 20
    avail_w = WIDTH - 64
    avail_h = CANVAS_H - top_pad - 16

    iw, ih = src_img.size
    scale = min(avail_w / iw, avail_h / ih)
    nw = max(2, int(round(iw * scale)))
    nh = max(2, int(round(ih * scale)))
    resized = src_img.convert("RGB").resize((nw, nh), Image.Resampling.LANCZOS)

    px = (WIDTH - nw) // 2
    py = top_pad + (avail_h - nh) // 2
    canvas.paste(resized, (px, py))

    draw = ImageDraw.Draw(canvas)
    draw.rectangle([px - 2, py - 2, px + nw + 1, py + nh + 1], outline=BORDER_HEX, width=2)

    if header_text:
        font_h = load_font(26, bold=True)
        draw.text((48, 16), header_text, font=font_h, fill=ACCENT_HEX)

    return canvas


def build_title_card() -> Image.Image:
    """Render 1920x940 opening card for NISAR Vision — Team Taykut (zero AI imagery, no agency logos)."""
    canvas = Image.new("RGB", (WIDTH, CANVAS_H), BG_HEX)
    draw = ImageDraw.Draw(canvas)

    # Subtle structural grid lines
    for gx in range(120, WIDTH, 240):
        draw.line([(gx, 60), (gx, CANVAS_H - 60)], fill=(18, 26, 36), width=1)
    for gy in range(80, CANVAS_H, 180):
        draw.line([(80, gy), (WIDTH - 80, gy)], fill=(18, 26, 36), width=1)

    card_x0, card_y0, card_x1, card_y1 = 160, 180, WIDTH - 160, CANVAS_H - 170
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=14, fill=PANEL_HEX, outline=BORDER_HEX, width=2)
    draw.rectangle([card_x0, card_y0 + 36, card_x0 + 8, card_y1 - 36], fill=ACCENT_HEX)

    font_pill = load_font(22, bold=True, mono=True)
    font_title = load_font(74, bold=True)
    font_sub = load_font(34, bold=False)
    font_meta = load_font(24, bold=False, mono=True)

    draw.text((220, 235), "PROVISIONAL NASA-ISRO NISAR L-BAND RADAR  ·  2026", font=font_pill, fill=WARN_HEX)
    draw.text((220, 305), "NISAR Vision — Team Taykut", font=font_title, fill=TEXT_HEX)
    draw.text(
        (220, 415),
        "Track and Visualize Surface Change: Patterns and Rhythms of Subsidence",
        font=font_sub,
        fill=ACCENT_HEX,
    )
    draw.text(
        (220, 505),
        "Sites: Tulare Basin, California (2026-06-28 to 2026-10-14) & Karapinar / Konya, Turkiye",
        font=font_meta,
        fill=MUTED_HEX,
    )
    draw.text(
        (220, 555),
        "Validation: 10 NGL GPS Stations  |  Risk: 645 Central Valley + 64 Karapinar OSM Assets",
        font=font_meta,
        fill=MUTED_HEX,
    )
    return canvas


def build_closing_card() -> Image.Image:
    """Render 1920x940 closing card with live URL and mandatory provisional calibration credit."""
    canvas = Image.new("RGB", (WIDTH, CANVAS_H), BG_HEX)
    draw = ImageDraw.Draw(canvas)

    card_x0, card_y0, card_x1, card_y1 = 160, 175, WIDTH - 160, CANVAS_H - 165
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=14, fill=PANEL_HEX, outline=BORDER_HEX, width=2)
    draw.rectangle([card_x0, card_y0 + 36, card_x0 + 8, card_y1 - 36], fill=ACCENT_HEX)

    font_pill = load_font(22, bold=True, mono=True)
    font_title = load_font(54, bold=True)
    font_url = load_font(38, bold=True, mono=True)
    font_note = load_font(25, bold=False)

    draw.text((220, 235), "INTERACTIVE STORY MAP, 3D BASIN & SIMULATOR", font=font_pill, fill=WARN_HEX)
    draw.text((220, 295), "Explore NISAR Vision Online", font=font_title, fill=TEXT_HEX)
    draw.text((220, 390), "https://keremsumer2010-tech.github.io/aseltech/", font=font_url, fill=ACCENT_HEX)
    draw.text(
        (220, 485),
        "Data: NASA-ISRO NISAR, provisional (L2 GUNW / L2 GCOV via ASF DAAC).",
        font=font_note,
        fill=TEXT_HEX,
    )
    draw.text(
        (220, 530),
        "Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.",
        font=font_note,
        fill=MUTED_HEX,
    )
    draw.text(
        (220, 575),
        "Corroborated with Nevada Geodetic Laboratory GNSS and OpenStreetMap infrastructure layers. Team Taykut.",
        font=font_note,
        fill=MUTED_HEX,
    )
    return canvas


def encode_still_clip(top_img: Image.Image, sub_img: Image.Image, duration_s: float, out_path: Path, tmp_dir: Path, stem: str) -> None:
    """Combine 1920x940 slide + 1920x140 subtitle strip and encode as crisp 1080p MP4 segment."""
    frame = Image.new("RGB", (WIDTH, HEIGHT), BG_HEX)
    frame.paste(top_img, (0, 0))
    frame.paste(sub_img, (0, CANVAS_H))
    png_path = tmp_dir / f"{stem}.png"
    frame.save(png_path, optimize=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        str(png_path),
        "-t",
        f"{duration_s:.3f}",
        "-r",
        str(FPS),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "medium",
        "-crf",
        "19",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def encode_video_clip(src_mp4: Path, sub_img: Image.Image, duration_s: float, out_path: Path, tmp_dir: Path, stem: str) -> None:
    """Retime real-data MP4 cleanly into exact duration_s within 1920x940 top area + subtitle strip."""
    src_dur = ffprobe_duration(src_mp4)
    speed_pts = duration_s / max(0.1, src_dur)

    sub_png = tmp_dir / f"{stem}_sub.png"
    sub_img.save(sub_png, optimize=True)

    filter_complex = (
        f"[0:v]setpts={speed_pts:.6f}*PTS,"
        f"scale={WIDTH}:{CANVAS_H}:force_original_aspect_ratio=decrease:flags=lanczos,"
        f"pad={WIDTH}:{CANVAS_H}:(ow-iw)/2:(oh-ih)/2:color=#0b0f14[top];"
        f"[1:v]scale={WIDTH}:{SUB_H}[bot];"
        f"[top][bot]vstack=inputs=2[v]"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src_mp4),
        "-loop",
        "1",
        "-i",
        str(sub_png),
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-t",
        f"{duration_s:.3f}",
        "-r",
        str(FPS),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "medium",
        "-crf",
        "19",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> int:
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("ERROR: ffmpeg/ffprobe not found on PATH.", file=sys.stderr)
        return 1

    cv_mp4 = MEDIA_ROOT / "cv_subsidence.mp4"
    val_png = MEDIA_ROOT / "validation_scatter.png"
    risk4_png = MEDIA_ROOT / "risk_4.png"
    kp_mp4 = MEDIA_ROOT / "kp_subsidence.mp4"
    game_png = REPO_ROOT / "docs" / "game_v3.png"

    for p in (cv_mp4, val_png, risk4_png, kp_mp4, game_png):
        if not p.exists():
            print(f"ERROR: Required source asset missing: {p}", file=sys.stderr)
            return 1

    # Total = 2.0 + 8.0 + 4.0 + 4.0 + 6.0 + 3.0 + 2.6 = 29.6 s (strictly <= 29.8 s < 30.0 s)
    total_dur = 29.6
    scenes = [
        ("01_title", 0.0, 2.0, "SCENE 1/7  ·  TRACK AND VISUALIZE SURFACE CHANGE",
         "When deep groundwater is pumped faster than rain refills it, the ground itself sinks."),
        ("02_cv_anim", 2.0, 8.0, "SCENE 2/7  ·  PATTERNS AND RHYTHMS: TULARE BASIN, CA (2026-06-28 → 2026-10-14)",
         "In California's Tulare Basin, provisional NISAR tracks up to -7.8 cm LOS (-10.1 cm vertical) across 108 days."),
        ("03_validation", 10.0, 4.0, "SCENE 3/7  ·  GROUND-TRUTH VALIDATION: 10 NGL GPS STATIONS",
         "Independent NGL GPS stations agree across 10 sites (Pearson r = 0.924, final RMSE = 1.37 cm)."),
        ("04_risk4", 14.0, 4.0, "SCENE 4/7  ·  ACTIONABLE INSIGHTS: CALIFORNIA AQUEDUCT RISK PROFILE",
         "Sinking warps major canals: California Aqueduct gradient hits 49.12 mm/km (-7.42 cm LOS); Tulare Canal hits 57.01 mm/km."),
        ("05_kp_anim", 18.0, 6.0, "SCENE 5/7  ·  PATTERNS AND RHYTHMS: KONYA CLOSED BASIN / KARAPINAR, TURKIYE",
         "In Turkiye's Konya Closed Basin, Karapinar sank -5.9 cm LOS (-8.0 cm vertical) near 29 mapped sinkholes."),
        ("06_game", 24.0, 3.0, "SCENE 6/7  ·  INTERACTIVE SIMULATOR & CLASSROOM MODE",
         "Valley Under Pressure turns NISAR observations into a 24-month trade-off with Classroom Mode scenarios and discussion."),
        ("07_closing", 27.0, 2.6, "SCENE 7/7  ·  OPEN DATA, NASA STORYMAP FRAMEWORK & ATTRIBUTION",
         "Data: NASA-ISRO NISAR (provisional, JPL/ISRO calibration), ASF DAAC, NGL GNSS, and OpenStreetMap."),
    ]

    with tempfile.TemporaryDirectory(prefix="nisar_demo_") as td:
        tmp_dir = Path(td)
        seg_paths: list[Path] = []

        for key, t0, dur, label, sub_text in scenes:
            seg_out = tmp_dir / f"{key}.mp4"
            sub_strip = render_subtitle_strip(sub_text, label, t0, total_dur)

            if key == "01_title":
                encode_still_clip(build_title_card(), sub_strip, dur, seg_out, tmp_dir, key)
            elif key == "02_cv_anim":
                encode_video_clip(cv_mp4, sub_strip, dur, seg_out, tmp_dir, key)
            elif key == "03_validation":
                with Image.open(val_png) as im:
                    top = fit_image_canvas(im, "GPS Validation — NISAR Vertical Estimate vs. NGL Stations (108 Days)")
                encode_still_clip(top, sub_strip, dur, seg_out, tmp_dir, key)
            elif key == "04_risk4":
                with Image.open(risk4_png) as im:
                    top = fit_image_canvas(im, "Critical Infrastructure Profile — #4 California Aqueduct (102.82 km)")
                encode_still_clip(top, sub_strip, dur, seg_out, tmp_dir, key)
            elif key == "05_kp_anim":
                encode_video_clip(kp_mp4, sub_strip, dur, seg_out, tmp_dir, key)
            elif key == "06_game":
                with Image.open(game_png) as im:
                    top = fit_image_canvas(im, "Decision Simulator — 24-Month Pumping, Canal Gradient & Clay Collapse Model")
                encode_still_clip(top, sub_strip, dur, seg_out, tmp_dir, key)
            elif key == "07_closing":
                encode_still_clip(build_closing_card(), sub_strip, dur, seg_out, tmp_dir, key)

            seg_paths.append(seg_out)

        concat_txt = tmp_dir / "concat.txt"
        concat_txt.write_text("\n".join(f"file '{p.as_posix()}'" for p in seg_paths) + "\n", encoding="utf-8")

        MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_txt),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-preset",
                "medium",
                "-crf",
                "20",
                "-movflags",
                "+faststart",
                str(OUT_MP4),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    final_dur = ffprobe_duration(OUT_MP4)
    size_mb = OUT_MP4.stat().st_size / (1024 * 1024)
    print(f"Generated {OUT_MP4.relative_to(REPO_ROOT)}: duration={final_dur:.2f}s, size={size_mb:.2f} MB")
    if final_dur > 29.95:
        print(f"ERROR: Duration {final_dur:.2f}s exceeds 30s Space Apps limit!", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
