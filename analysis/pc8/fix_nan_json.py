"""Clean any non-standard JSON constants (NaN, Infinity, -Infinity -> null) across data/**/*.json.

Safe & idempotent: preserves key order, UTF-8 encoding, and only rewrites files that actually change.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def _sanitize(obj: Any) -> tuple[Any, int]:
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None, 1
        return obj, 0
    if isinstance(obj, list):
        out = []
        n = 0
        for item in obj:
            v, c = _sanitize(item)
            out.append(v)
            n += c
        return out, n
    if isinstance(obj, dict):
        out = {}
        n = 0
        for k, v in obj.items():
            sv, c = _sanitize(v)
            out[k] = sv
            n += c
        return out, n
    return obj, 0


def clean_tree(data_dir: Path | None = None) -> dict[str, int]:
    base = data_dir or (ROOT / "data")
    checked = 0
    fixed = 0
    replaced_tokens = 0
    for jf in sorted(base.rglob("*.json")):
        checked += 1
        raw = jf.read_text(encoding="utf-8")
        had_non_std = False

        def _parse_const(tok: str) -> float:
            nonlocal had_non_std
            had_non_std = True
            if tok == "NaN":
                return float("nan")
            if tok == "Infinity":
                return float("inf")
            if tok == "-Infinity":
                return float("-inf")
            raise ValueError(f"Unexpected JSON constant: {tok}")

        parsed = json.loads(raw, parse_constant=_parse_const)
        cleaned, count = _sanitize(parsed)
        if had_non_std or count > 0:
            jf.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            fixed += 1
            replaced_tokens += count
            print(f"Fixed {count} non-standard constant(s) in {jf.relative_to(ROOT)}")
    return {"checked": checked, "fixed_files": fixed, "replaced_tokens": replaced_tokens}


if __name__ == "__main__":
    summary = clean_tree()
    print(f"Checked {summary['checked']} JSON files; fixed {summary['fixed_files']} files ({summary['replaced_tokens']} tokens).")
