#!/usr/bin/env python3
"""Capture 1600x900 screenshot of game/index.html (Terra Bella, Blend layer, +6 months) via headless Chrome CDP.

Writes:
  - docs/game_v4.png (1600x900)
  - web/assets/simulator.jpg (1600x900, <= 150 KB)

Owner: PC6 (B35 / S-35)
"""
from __future__ import annotations

import base64
import hashlib
import http.server
import io
import json
import os
import shutil
import socket
import socketserver
import struct
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_PNG = ROOT / "docs" / "game_v4.png"
OUT_JPG = ROOT / "web" / "assets" / "simulator.jpg"


class SimpleWS:
    """Minimal RFC 6455 WebSocket client using Python stdlib only."""

    def __init__(self, ws_url: str) -> None:
        assert ws_url.startswith("ws://")
        rest = ws_url[5:]
        host_port, path = rest.split("/", 1)
        host, port_s = host_port.split(":")
        self.sock = socket.create_connection((host, int(port_s)), timeout=30)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET /{path} HTTP/1.1\r\n"
            f"Host: {host_port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode("ascii"))
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.sock.recv(4096)
        self._buf = buf.split(b"\r\n\r\n", 1)[1]
        self._msg_id = 0

    def _recv_exact(self, n: int) -> bytes:
        while len(self._buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("WebSocket closed")
            self._buf += chunk
        out, self._buf = self._buf[:n], self._buf[n:]
        return out

    def _send_text(self, text: str) -> None:
        data = text.encode("utf-8")
        mask = os.urandom(4)
        header = bytearray([0x81])
        n = len(data)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", n))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", n))
        header.extend(mask)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        self.sock.sendall(bytes(header) + masked)

    def _recv_frame(self) -> str:
        while True:
            b1, b2 = self._recv_exact(2)
            opcode = b1 & 0x0F
            length = b2 & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8))[0]
            if b2 & 0x80:
                mask = self._recv_exact(4)
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(self._recv_exact(length)))
            else:
                payload = self._recv_exact(length)
            if opcode == 0x8:
                raise ConnectionError("WebSocket closed")
            if opcode == 0x9:  # ping -> pong
                continue
            if opcode == 0x1:
                return payload.decode("utf-8")

    def call(self, method: str, params: dict | None = None) -> dict:
        self._msg_id += 1
        mid = self._msg_id
        self._send_text(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self._recv_frame())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"CDP error: {msg['error']}")
                return msg.get("result", {})

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass


def main() -> None:
    class StaticHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def log_message(self, format, *args):
            pass

    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), StaticHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    # Find free port for CDP
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    cdp_port = s.getsockname()[1]
    s.close()

    work_dir = Path(tempfile.mkdtemp(prefix="nisar_game_shot_"))
    user_data = work_dir / "chrome_profile"
    url = f"http://127.0.0.1:{port}/game/index.html"
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
            "--window-size=1600,900",
            f"--remote-debugging-port={cdp_port}",
            f"--user-data-dir={user_data}",
            url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        ws_url = None
        for _ in range(40):
            try:
                pages = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{cdp_port}/json/list", timeout=2).read())
                for p in pages:
                    if p.get("type") == "page" and "webSocketDebuggerUrl" in p:
                        ws_url = p["webSocketDebuggerUrl"]
                        break
                if ws_url:
                    break
            except Exception:
                time.sleep(0.25)
        if not ws_url:
            raise RuntimeError("Could not connect to Chrome DevTools")

        ws = SimpleWS(ws_url)
        ws.call("Emulation.setDeviceMetricsOverride", {
            "width": 1600, "height": 900, "deviceScaleFactor": 1, "mobile": False
        })
        # Wait for #startBtn and map tiles to settle
        time.sleep(4.0)
        ws.call("Runtime.evaluate", {
            "expression": """(() => {
                const startBtn = document.getElementById('startBtn');
                if (startBtn) startBtn.click();
                const blendBtn = document.querySelector('.layer-btn[data-overlay="blend"]');
                if (blendBtn) blendBtn.click();
                const ffBtn = document.getElementById('fastForwardBtn');
                if (ffBtn) ffBtn.click();
                return document.getElementById('monthPill')?.textContent || 'ok';
            })()""",
            "returnByValue": True,
        })
        # Wait for satellite tiles + animations + chart render
        time.sleep(5.0)
        shot = ws.call("Page.captureScreenshot", {"format": "png"})
        ws.close()

        png_bytes = base64.b64decode(shot["data"])
        OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
        OUT_JPG.parent.mkdir(parents=True, exist_ok=True)
        OUT_PNG.write_bytes(png_bytes)

        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        if img.size != (1600, 900):
            img = img.resize((1600, 900), Image.Resampling.LANCZOS)
        for q in (88, 82, 76, 70, 64, 58):
            img.save(OUT_JPG, format="JPEG", quality=q, optimize=True)
            if OUT_JPG.stat().st_size <= 150_000:
                break

        print(f"Saved {OUT_PNG} ({OUT_PNG.stat().st_size / 1024:.1f} KB)")
        print(f"Saved {OUT_JPG} ({OUT_JPG.stat().st_size / 1024:.1f} KB, size={img.size})")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        httpd.shutdown()
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
