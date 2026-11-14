"""Wrapper to run PC3's analysis/cumulative.py for PC2 sites without modifying PC3 files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis"))

import gunw_io  # noqa: E402
import cumulative  # noqa: E402

gunw_io.BBOX.update(
    {
        "delta": (-121.85, 37.95, -121.45, 38.20),
        "delta_p135": (-121.85, 37.95, -121.45, 38.20),
        "konya_plain": (32.4, 37.4, 33.9, 38.1),
        "karapinar_fullyear": (33.3, 37.6, 33.8, 37.9),
        "central_valley_p114": (-120.2, 35.6, -119.0, 36.6),
    }
)

if __name__ == "__main__":
    cumulative.main()
