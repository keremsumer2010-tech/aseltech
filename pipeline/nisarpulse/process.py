"""Wrapper around analysis/cumulative.py without modifying upstream analysis code."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def run_cumulative(
    name: str,
    bbox: tuple[float, float, float, float],
    data_dir: Path | None = None,
    quality_mode: str = "provisional",
) -> tuple[Path, dict, dict]:
    """Register site bbox at runtime and invoke analysis/cumulative.py."""
    analysis_dir = str(ROOT / "analysis")
    if analysis_dir not in sys.path:
        sys.path.insert(0, analysis_dir)

    import cumulative  # noqa: E402
    import gunw_io  # noqa: E402

    gunw_io.BBOX[name] = bbox
    out_dir = data_dir or (ROOT / "data" / name)
    argv_backup = list(sys.argv)
    try:
        sys.argv = ["cumulative.py", name, "--data-dir", str(out_dir)]
        if quality_mode == "mixed":
            sys.argv.append("--mixed")
        cumulative.main()
    finally:
        sys.argv = argv_backup

    meta = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))
    summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    return out_dir, meta, summary
