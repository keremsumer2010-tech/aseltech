"""Generate or verify data/global/vital_signs.json from atlas.json and exposure_atlas.json."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "data" / "global" / "atlas.json"
EXPOSURE_PATH = ROOT / "data" / "global" / "exposure_atlas.json"
VITAL_PATH = ROOT / "data" / "global" / "vital_signs.json"

CALIBRATION_NOTICE = (
    "NISAR data are provisional. Calibration and validation are carried out by "
    "the NISAR project (NASA-JPL and ISRO), not by our team."
)


def compute_vital_signs(generated_utc: str | None = None) -> dict:
    """Build vital_signs payload from atlas.json and exposure_atlas.json."""
    atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    exposure = json.loads(EXPOSURE_PATH.read_text(encoding="utf-8"))

    regions = atlas.get("regions", [])
    reliable = [r for r in regions if not r.get("indicative_only")]
    reliable.sort(
        key=lambda r: (
            r.get("rate_cm_per_100d_common")
            if r.get("rate_cm_per_100d_common") is not None
            else r.get("rate_cm_per_100d", 999.0)
        )
    )
    if not reliable:
        raise RuntimeError("No reliable regions found in atlas.json")

    top = reliable[0]
    rate_val = (
        top["rate_cm_per_100d_common"]
        if top.get("rate_cm_per_100d_common") is not None
        else top["rate_cm_per_100d"]
    )
    common_win = atlas.get("common_window")
    if isinstance(common_win, list) and len(common_win) >= 2:
        win_start, win_end = common_win[0], common_win[1]
    elif isinstance(common_win, dict):
        win_start = common_win.get("start", "2026-06-28")
        win_end = common_win.get("end", "2026-09-29")
    else:
        win_start, win_end = "2026-06-28", "2026-09-29"

    totals = exposure.get("totals_excluding_nested_karapinar")
    if not totals:
        cities = [c for c in exposure.get("cities", []) if c.get("id") != "karapinar"]
        totals = {
            "people_lt_minus2cm": sum(c.get("people_lt_minus2cm", 0) for c in cities),
            "people_lt_minus5cm": sum(c.get("people_lt_minus5cm", 0) for c in cities),
            "area_km2_lt_minus5cm": round(
                sum(c.get("area_km2_lt_minus5cm", 0.0) for c in cities), 2
            ),
        }

    ts = generated_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "generated_utc": ts,
        "quality": "provisional",
        "quality_note": CALIBRATION_NOTICE,
        "cities_measured": atlas.get("n_regions", len(regions)),
        "cities_measured_source": "data/global/atlas.json (n_regions)",
        "fastest": {
            "id": top["id"],
            "name": top["name"],
            "country": top.get("country", ""),
            "rate_cm_per_100d": rate_val,
            "rate_basis": f"common window {win_start}→{win_end}",
            "source": "data/global/atlas.json (fastest among reliable regions; QC-flagged regions excluded)",
        },
        "area_km2_lt_minus5cm": totals["area_km2_lt_minus5cm"],
        "area_km2_lt_minus5cm_source": "data/global/exposure_atlas.json (sum excluding nested karapinar)",
        "people_on_sinking_ground": totals["people_lt_minus5cm"],
        "people_on_sinking_ground_threshold": "< -5 cm (108-day equivalent, |disp| >= 2*sigma)",
        "people_on_sinking_ground_gt2cm": totals["people_lt_minus2cm"],
        "people_on_sinking_ground_source": "data/global/exposure_atlas.json (GHSL GHS-POP E2025 R2023A 3ss, excluding nested karapinar)",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify data/global/vital_signs.json matches atlas.json + exposure_atlas.json without writing.",
    )
    args = parser.parse_args()

    existing = (
        json.loads(VITAL_PATH.read_text(encoding="utf-8"))
        if VITAL_PATH.exists()
        else None
    )
    expected = compute_vital_signs(
        generated_utc=existing.get("generated_utc") if existing else None
    )

    if args.check:
        if existing != expected:
            print("OUT OF SYNC: data/global/vital_signs.json does not match atlas.json + exposure_atlas.json")
            return 1
        print(f"OK: vital_signs.json matches ({expected['cities_measured']} regions, fastest={expected['fastest']['id']} {expected['fastest']['rate_cm_per_100d']} cm/100d)")
        return 0

    VITAL_PATH.write_text(json.dumps(expected, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {VITAL_PATH} ({expected['cities_measured']} regions, fastest={expected['fastest']['id']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
