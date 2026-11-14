"""Capture demo_v2_scene.html frame-by-frame in headless Chrome and encode 1080p + 720p MP4 via ffmpeg."""
from __future__ import annotations

import http.server
import pathlib
import shutil
import socketserver
import subprocess
import tempfile
import threading

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_1080 = ROOT / "docs/story/media/demo_30s_v2.mp4"
OUT_720 = ROOT / "docs/story/media/demo_30s_v2_web.mp4"


def run_capture() -> None:
    frames_dir = pathlib.Path(tempfile.mkdtemp(prefix="nisar_demo_v2_"))
    done_event = threading.Event()
    received = {"count": 0}

    class CaptureHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def log_message(self, format, *args):
            pass

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            if self.path.startswith("/frame/"):
                idx = int(self.path.split("/")[-1])
                (frames_dir / f"{idx:04d}.png").write_bytes(body)
                received["count"] += 1
                if received["count"] % 150 == 0:
                    print(f"  Captured {received['count']}/900 frames...")
            elif self.path == "/done":
                done_event.set()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), CaptureHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    url = f"http://127.0.0.1:{port}/analysis/pc6/demo_v2_scene.html?capture=1"
    print(f"Launching headless Chrome on {url} ...")
    user_data = frames_dir / "chrome_profile"
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
            "--window-size=1920,1080",
            f"--user-data-dir={user_data}",
            url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        ok = done_event.wait(timeout=300)
        if not ok:
            raise RuntimeError(f"Capture timed out after 300s (received {received['count']} frames)")
        print(f"All {received['count']} frames captured cleanly!")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        httpd.shutdown()

    pattern = str(frames_dir / "%04d.png")
    OUT_1080.parent.mkdir(parents=True, exist_ok=True)

    print(f"Encoding 1080p -> {OUT_1080} ...")
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", "30", "-i", pattern,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            "-movflags", "+faststart", str(OUT_1080),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"Encoding 720p web -> {OUT_720} ...")
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", "30", "-i", pattern,
            "-vf", "scale=1280:720",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24",
            "-movflags", "+faststart", str(OUT_720),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    shutil.rmtree(frames_dir, ignore_errors=True)

    for out in (OUT_1080, OUT_720):
        probe = subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=width,height,codec_name,duration",
                "-of", "default=noprint_wrappers=1", str(out),
            ],
            text=True,
        ).strip().replace("\n", " | ")
        mb = out.stat().st_size / 1e6
        print(f"Verified {out.name}: {mb:.2f} MB | {probe}")


if __name__ == "__main__":
    run_capture()
