"""Update data/catalog.json with a data-contract-compliant site entry."""

from __future__ import annotations

import json
from pathlib import Path

QUALITY_NOTES = {
    "provisional": (
        "NISAR data are provisional. Calibration and validation are carried out "
        "by the NISAR project (NASA-JPL and ISRO), not by our team."
    ),
    "beta-precal": (
        "NISAR data are pre-calibration BETA products (before 2026-06-17). "
        "Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO)."
    ),
    "mixed": (
        "NISAR data are provisional. Calibration and validation are carried out "
        "by the NISAR project (NASA-JPL and ISRO), not by our team. This series MIXES "
        "provisional products with pre-calibration BETA products (dates before 2026-06-17); "
        "treat amplitudes before that date with extra caution."
    ),
}


def build_catalog_entry(
    name: str,
    bbox: tuple[float, float, float, float] | list[float],
    meta: dict,
    title: str | None = None,
) -> dict:
    """Construct a catalog.json record matching rules/VERI_SOZLESMESI.md."""
    quality = meta.get("quality", "provisional")
    quality_note = meta.get("quality_note") or QUALITY_NOTES.get(
        quality, QUALITY_NOTES["provisional"]
    )
    rel_path = f"data/{name}/"
    dates = meta.get("dates", [])
    bbox_list = list(bbox)
    return {
        "site": name,
        "title": title or name.replace("_", " ").title(),
        "quality": quality,
        "quality_note": quality_note,
        "path": rel_path,
        "bbox": bbox_list,
        "layers": [
            {
                "id": "motion",
                "title": "Ground motion (cm, line of sight)",
                "kind": "raster_series",
                "file": f"{rel_path}meta.json",
                "png": f"{rel_path}disp/{{date}}.png",
                "dates": dates,
                "bbox": bbox_list,
                "legend": {
                    "vmin": -6.0,
                    "vmax": 6.0,
                    "cmap": "RdBu",
                    "units": "cm",
                    "low": "sinking",
                    "high": "rising",
                },
                "quality": quality,
            }
        ],
    }


def upsert_catalog(
    catalog_path: Path,
    name: str,
    bbox: tuple[float, float, float, float] | list[float],
    meta: dict,
    title: str | None = None,
) -> list[dict]:
    """Insert or update a site entry in data/catalog.json."""
    if catalog_path.exists():
        records = json.loads(catalog_path.read_text(encoding="utf-8"))
    else:
        records = []

    entry = build_catalog_entry(name, bbox, meta, title=title)
    replaced = False
    for idx, rec in enumerate(records):
        if rec.get("site") == name:
            records[idx] = entry
            replaced = True
            break
    if not replaced:
        records.append(entry)

    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    return records
