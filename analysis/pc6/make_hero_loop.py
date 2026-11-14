#!/usr/bin/env python3
"""Capture Central Valley Esri World Imagery via headless Chrome and build seamless hero loop videos.

Writes:
  - docs/story/media/hero_loop.mp4  (1920x1080, 12s, silent, <= 1.5 MB)
  - docs/story/media/hero_loop.webm (1920x1080, 12s, silent, <= 1.5 MB)
  - docs/story/media/hero_poster.webp (1920x1080, <= 150 KB)

Owner: PC6 (B30 / S-31)
"""
from __future__ import annotations

import base64
import http.server
import math
import shutil
import socketserver
import subprocess
import tempfile
import threading
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parents[2]
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_DIR = ROOT / "docs" / "story" / "media"
OUT_MP4 = OUT_DIR / "hero_loop.mp4"
OUT_WEBM = OUT_DIR / "hero_loop.webm"
OUT_POSTER = OUT_DIR / "hero_poster.webp"

CAPTURE_W, CAPTURE_H = 2400, 1350
OUT_W, OUT_H = 1920, 1080
FPS = 24
DURATION_S = 12
N_FRAMES = FPS * DURATION_S

SCENE_HTML = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<style>html,body,#map{{margin:0;padding:0;width:{CAPTURE_W}px;height:{CAPTURE_H}px;background:#05080f;overflow:hidden}}</style>
</head>
<body>
<div id="map"></div>
<script>
const map = new maplibregl.Map({{
  container: 'map',
  style: {{
    version: 8,
    sources: {{
      sat: {{
        type: 'raster',
        tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}'],
        tileSize: 256,
        maxzoom: 18
      }}
    }},
    layers: [
      {{id: 'bg', type: 'background', paint: {{'background-color': '#05080f'}}}},
      {{id: 'sat', type: 'raster', source: 'sat'}}
    ]
  }},
  center: [-119.50, 36.10],
  zoom: 8.85,
  bearing: -12,
  pitch: 0,
  interactive: false,
  attributionControl: false,
  preserveDrawingBuffer: true,
  fadeDuration: 0,
  renderWorldCopies: false
}});
map.once('idle', async () => {{
  await new Promise(r => setTimeout(r, 800));
  const dataUrl = map.getCanvas().toDataURL('image/png');
  await fetch('/capture', {{method: 'POST', body: dataUrl}});
}});
</script>
</body>
</html>
"""


def capture_satellite_canvas(work_dir: Path) -> Path:
    done = threading.Event()
    raw_png = work_dir / "raw_sat.png"

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def do_GET(self):
            body = SCENE_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            data_url = self.rfile.read(length).decode("utf-8")
            _, b64 = data_url.split(",", 1)
            raw_png.write_bytes(base64.b64decode(b64))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            done.set()

    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    user_data = work_dir / "chrome_profile"
    proc = subprocess.Popen(
        [
            CHROME,
            "--headless=new",
            "--enable-webgl",
            "--use-gl=angle",
            "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader",
            "--ignore-gpu-blocklist",
            "--disable-gpu-sandbox",
            "--no-sandbox",
            f"--window-size={CAPTURE_W},{CAPTURE_H}",
            f"--user-data-dir={user_data}",
            f"http://127.0.0.1:{port}/",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        if not done.wait(timeout=120):
            raise RuntimeError("Timed out waiting for headless Chrome Esri satellite capture")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        httpd.shutdown()
    return raw_png


def make_gradient_mask() -> tuple[np.ndarray, np.ndarray]:
    """Left-dark gradient overlay matching hero title contrast."""
    x = np.linspace(0.0, 1.0, OUT_W, dtype=np.float32)[None, :]
    y = np.linspace(0.0, 1.0, OUT_H, dtype=np.float32)[:, None]
    # Stronger on left (0.80) fading to right (0.20), plus slight top/bottom vignette
    alpha_x = 0.80 * np.exp(-2.4 * x) + 0.18
    alpha_y = 0.10 * np.abs(2.0 * y - 1.0) ** 2
    alpha = np.clip(alpha_x + alpha_y, 0.0, 0.88)[..., None]
    tint = np.array([7.0, 11.0, 20.0], dtype=np.float32)[None, None, :]
    return 1.0 - alpha, alpha * tint


def render_frames(raw_png: Path, frames_dir: Path) -> None:
    base = Image.open(raw_png).convert("RGB")
    base = ImageEnhance.Color(base).enhance(0.68)
    base = ImageEnhance.Brightness(base).enhance(0.62)

    inv_a, tint_a = make_gradient_mask()
    cx0, cy0 = CAPTURE_W * 0.50, CAPTURE_H * 0.50
    base_cw, base_ch = 2160.0, 1215.0  # 16:9 crop inside 2400x1350

    for i in range(N_FRAMES):
        u = 0.5 * (1.0 - math.cos(2.0 * math.pi * i / N_FRAMES))
        scale = 1.0 + 0.06 * u
        cw = base_cw / scale
        ch = base_ch / scale
        cx = cx0 + 70.0 * u
        cy = cy0 - 35.0 * u
        box = (cx - cw * 0.5, cy - ch * 0.5, cx + cw * 0.5, cy + ch * 0.5)
        crop = base.crop(box).resize((OUT_W, OUT_H), Image.Resampling.BICUBIC)
        arr = np.asarray(crop, dtype=np.float32)
        shaded = np.clip(arr * inv_a + tint_a, 0, 255).astype(np.uint8)
        frame = Image.fromarray(shaded, mode="RGB")
        frame.save(frames_dir / f"{i:04d}.png", compress_level=1)

    # Save poster WebP <= 150 KB
    poster_src = Image.open(frames_dir / "0000.png")
    for q in (82, 72, 62, 52):
        poster_src.save(OUT_POSTER, format="WEBP", quality=q, method=6)
        if OUT_POSTER.stat().st_size <= 150_000:
            break


def encode_videos(frames_dir: Path) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pattern = str(frames_dir / "%04d.png")

    # MP4 <= 1.5 MB
    for crf in (25, 27, 29):
        subprocess.run(
            [
                "ffmpeg", "-y", "-framerate", str(FPS), "-i", pattern,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
                "-crf", str(crf), "-preset", "slow", "-movflags", "+faststart",
                str(OUT_MP4),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if OUT_MP4.stat().st_size <= 1_500_000:
            break

    # WebM <= 1.5 MB
    for br in ("750k", "550k", "420k"):
        subprocess.run(
            [
                "ffmpeg", "-y", "-framerate", str(FPS), "-i", pattern,
                "-c:v", "libvpx-vp9", "-pix_fmt", "yuv420p", "-an",
                "-b:v", br, "-crf", "32", "-deadline", "good", "-cpu-used", "2",
                str(OUT_WEBM),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if OUT_WEBM.stat().st_size <= 1_500_000:
            break


def main() -> None:
    work_dir = Path(tempfile.mkdtemp(prefix="nisar_hero_loop_"))
    frames_dir = work_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    try:
        raw_png = capture_satellite_canvas(work_dir)
        render_frames(raw_png, frames_dir)
        encode_videos(frames_dir)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)

    for p in (OUT_MP4, OUT_WEBM, OUT_POSTER):
        kb = p.stat().st_size / 1024.0
        print(f"{p.name}: {kb:.1f} KB")
        if p in (OUT_MP4, OUT_WEBM):
            probe = subprocess.check_output(
                [
                    "ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=width,height,codec_name,duration",
                    "-of", "default=noprint_wrappers=1", str(p),
                ],
                text=True,
            ).strip().replace("\n", " | ")
            print(f"  {probe}")


if __name__ == "__main__":
    main()
