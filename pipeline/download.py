"""Authenticated streaming downloader for NISAR products into raw/ (gitignored)."""

from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MIN_FREE_GB = 20.0
CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB


def read_earthdata_token() -> str:
    """Read Bearer token/password from ~/.netrc or ~/_netrc without logging it."""
    for name in (".netrc", "_netrc"):
        p = Path.home() / name
        if p.exists():
            tokens = p.read_text(encoding="utf-8").split()
            for i, tok in enumerate(tokens):
                if tok == "password" and i + 1 < len(tokens):
                    return tokens[i + 1]
    raise RuntimeError("No Earthdata credentials found in ~/.netrc or ~/_netrc")


def check_disk_space(target_dir: Path, min_free_gb: float = MIN_FREE_GB) -> float:
    target_dir.mkdir(parents=True, exist_ok=True)
    _, _, free = shutil.disk_usage(target_dir)
    free_gb = free / (1024**3)
    if free_gb < min_free_gb:
        raise RuntimeError(
            f"Disk free space {free_gb:.2f} GB < {min_free_gb:.1f} GB limit (RULES §8)"
        )
    return free_gb


def _make_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def download_file(
    url: str, dest: Path, timeout: int = 120, max_attempts: int = 5
) -> tuple[Path, float]:
    """Download url to dest using Bearer token auth with resume. Returns (path, speed_mb_s)."""
    check_disk_space(dest.parent)
    if dest.exists() and dest.stat().st_size > 100 * 1024 * 1024:
        with dest.open("rb") as f:
            if f.read(8) == b"\x89HDF\r\n\x1a\n":
                return dest, 0.0

    token = read_earthdata_token()
    tmp_path = dest.with_suffix(dest.suffix + ".part")
    session = _make_session()

    t0 = time.monotonic()
    bytes_this_run = 0

    for attempt in range(1, max_attempts + 1):
        existing = tmp_path.stat().st_size if tmp_path.exists() else 0
        headers = {"Authorization": f"Bearer {token}"}
        if existing > 0:
            headers["Range"] = f"bytes={existing}-"

        try:
            with session.get(
                url,
                headers=headers,
                stream=True,
                allow_redirects=True,
                timeout=timeout,
            ) as resp:
                if resp.status_code in (401, 403):
                    raise PermissionError(
                        f"HTTP {resp.status_code} access denied for {dest.name}"
                    )
                if resp.status_code == 416:
                    # Already fully downloaded
                    break
                resp.raise_for_status()

                mode = "ab" if resp.status_code == 206 and existing > 0 else "wb"
                if mode == "wb" and existing > 0:
                    existing = 0

                with tmp_path.open(mode) as f:
                    for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                            bytes_this_run += len(chunk)
            break
        except (requests.RequestException, OSError) as exc:
            if attempt == max_attempts:
                raise
            wait_s = min(2**attempt, 16)
            print(f"Attempt {attempt}/{max_attempts} failed ({type(exc).__name__}), retrying in {wait_s}s...")
            time.sleep(wait_s)

    with tmp_path.open("rb") as f:
        magic = f.read(8)
    if magic != b"\x89HDF\r\n\x1a\n":
        tmp_path.unlink(missing_ok=True)
        raise ValueError(f"Downloaded file {dest.name} is not a valid HDF5 file")

    os.replace(tmp_path, dest)
    elapsed = max(time.monotonic() - t0, 1e-3)
    speed_mb_s = (bytes_this_run / (1024 * 1024)) / elapsed
    return dest, speed_mb_s


if __name__ == "__main__":
    import argparse
    import csv

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--date1", required=True)
    parser.add_argument("--date2", required=True)
    parser.add_argument("--crid", default="P05023")
    parser.add_argument("--raw-dir", type=Path, default=Path("raw"))
    args = parser.parse_args()

    with args.csv_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    match = [
        r
        for r in rows
        if r["date1"] == args.date1 and r["date2"] == args.date2 and r["crid"] == args.crid
    ]
    if not match:
        raise SystemExit(f"No match for {args.date1}->{args.date2} crid={args.crid}")

    row = match[0]
    dest = args.raw_dir / f"{row['granule']}.h5"
    path, speed = download_file(row["url"], dest)
    size_mb = path.stat().st_size / (1024 * 1024)
    print(f"Downloaded {path.name} ({size_mb:.1f} MB) at {speed:.2f} MB/s")
