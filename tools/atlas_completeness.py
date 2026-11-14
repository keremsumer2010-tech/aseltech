"""Check 6-piece completeness for every region in data/global/atlas.json (PC8, ATLAS_MUKEMMEL.md).

Generates `docs/qa/ATLAS_COMPLETENESS.md` with a per-city ✓/✗ matrix and owner summary.
Usage:
  python tools/atlas_completeness.py
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ATLAS_PATH = ROOT / "data" / "global" / "atlas.json"
EXPOSURE_PATH = ROOT / "data" / "global" / "exposure_atlas.json"
OUT_MD = ROOT / "docs" / "qa" / "ATLAS_COMPLETENESS.md"


def _has_disp_png(region_dir: Path) -> bool:
    disp = region_dir / "disp"
    return disp.is_dir() and any(disp.glob("*.png"))


def check_completeness() -> tuple[list[dict[str, Any]], dict[str, int]]:
    atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    exp_ids: set[str] = set()
    if EXPOSURE_PATH.exists():
        exp_data = json.loads(EXPOSURE_PATH.read_text(encoding="utf-8"))
        exp_ids = {c["id"] for c in exp_data.get("cities", []) if isinstance(c, dict) and "id" in c}

    rows: list[dict[str, Any]] = []
    missing_by_owner: dict[str, int] = {
        "PC2/7/9/10/11": 0,
        "PC5": 0,
        "PC4": 0,
        "PC8": 0,
    }

    for reg in atlas.get("regions", []):
        rid = reg["id"]
        rel_path = (reg.get("path") or f"data/global/{rid}/").rstrip("/")
        rdir = ROOT / rel_path
        gdir = ROOT / "data" / "global" / rid

        p1 = (
            (rdir / "summary.json").exists()
            and (rdir / "meta.json").exists()
            and (rdir / "points.json").exists()
            and _has_disp_png(rdir)
        )
        p2 = (rdir / "uncertainty" / "sigma_cm.png").exists() or (gdir / "uncertainty" / "sigma_cm.png").exists()
        p3 = (rdir / "validation_note.json").exists() or (gdir / "validation_note.json").exists()
        p4 = (ROOT / "docs" / "story" / "atlas_cities" / f"{rid}.md").exists()
        p5 = (ROOT / "docs" / "bulletins" / f"{rid}.html").exists()
        p6 = rid in exp_ids

        if not p1:
            missing_by_owner["PC2/7/9/10/11"] += 1
        if not p2:
            missing_by_owner["PC5"] += 1
        if not p3:
            missing_by_owner["PC5"] += 1
        if not p4:
            missing_by_owner["PC4"] += 1
        if not p5:
            missing_by_owner["PC8"] += 1
        if not p6:
            missing_by_owner["PC8"] += 1

        rows.append({
            "id": rid,
            "name": reg.get("name", rid),
            "p1": p1,
            "p2": p2,
            "p3": p3,
            "p4": p4,
            "p5": p5,
            "p6": p6,
            "ok_count": sum((p1, p2, p3, p4, p5, p6)),
        })

    return rows, missing_by_owner


def render_markdown(rows: list[dict[str, Any]], missing_by_owner: dict[str, int]) -> str:
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_cells = len(rows) * 6
    ok_cells = sum(r["ok_count"] for r in rows)
    lines = [
        "# Atlas 6-Piece Completeness Matrix (`docs/ATLAS_MUKEMMEL.md`)",
        "",
        f"**Generated:** {now_utc} · **Regions in `data/global/atlas.json`:** {len(rows)} · **Complete cells:** {ok_cells}/{total_cells}",
        "",
        "| # | City ID | Name | 1. Summary/Disp (`PC2/7/9/10/11`) | 2. `sigma_cm.png` (`PC5`) | 3. `validation_note.json` (`PC5`) | 4. `atlas_cities/<id>.md` (`PC4`) | 5. `bulletins/<id>.html` (`PC8`) | 6. `exposure_atlas.json` (`PC8`) | Score |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for idx, r in enumerate(rows, 1):
        c1 = "✓" if r["p1"] else "✗ (PC2/7/9/10/11)"
        c2 = "✓" if r["p2"] else "✗ (PC5)"
        c3 = "✓" if r["p3"] else "✗ (PC5)"
        c4 = "✓" if r["p4"] else "✗ (PC4)"
        c5 = "✓" if r["p5"] else "✗ (PC8)"
        c6 = "✓" if r["p6"] else "✗ (PC8)"
        lines.append(
            f"| {idx} | `{r['id']}` | {r['name']} | {c1} | {c2} | {c3} | {c4} | {c5} | {c6} | {r['ok_count']}/6 |"
        )

    lines.extend([
        "",
        "## Missing Items by Owner",
        "",
        f"- **PC2/7/9/10/11 (Summary/Disp):** {missing_by_owner['PC2/7/9/10/11']} missing",
        f"- **PC5 (`sigma_cm.png` + `validation_note.json`):** {missing_by_owner['PC5']} missing",
        f"- **PC4 (`docs/story/atlas_cities/<id>.md`):** {missing_by_owner['PC4']} missing",
        f"- **PC8 (`docs/bulletins/<id>.html` + `exposure_atlas.json`):** {missing_by_owner['PC8']} missing",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    rows, missing = check_completeness()
    OUT_MD.write_text(render_markdown(rows, missing), encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(ROOT)} ({len(rows)} regions, missing={missing})")


if __name__ == "__main__":
    main()
