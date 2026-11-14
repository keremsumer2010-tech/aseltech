"""Build data/global/atlas.json from all site summary.json files (PC10, KALITE STANDARDI §1-§4)."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

CORE_REGIONS = [
    ("konya_plain", "Konya Plain", "Türkiye", ROOT / "data" / "konya_plain"),
    ("central_valley", "Central Valley (Tulare Basin)", "USA", ROOT / "data" / "central_valley"),
    ("karapinar", "Karapınar, Konya", "Türkiye", ROOT / "data" / "karapinar"),
    ("delta", "Sacramento–San Joaquin Delta", "USA", ROOT / "data" / "delta"),
]

GLOBAL_META = {
    "mexico_city": ("Mexico City", "Mexico"),
    "tehran": ("Tehran", "Iran"),
    "isfahan": ("Isfahan", "Iran"),
    "rafsanjan": ("Rafsanjan", "Iran"),
    "mashhad": ("Mashhad", "Iran"),
    "jakarta": ("Jakarta", "Indonesia"),
    "beijing": ("Beijing", "China"),
    "bangkok": ("Bangkok", "Thailand"),
    "ho_chi_minh": ("Ho Chi Minh City", "Vietnam"),
    "semarang": ("Semarang", "Indonesia"),
    "hanoi": ("Hanoi", "Vietnam"),
    "yunlin": ("Yunlin", "Taiwan"),
}


def _find_cum_stats(site_id: str) -> tuple[float | None, float | None]:
    """Return (p2_cm, valid_fraction) from analysis/out/<tag>_cum.npz or _pair_stats.json if available."""
    out_dir = ROOT / "analysis" / "out"
    p2_val = None
    valid_frac = None

    for tag in (site_id, f"global_{site_id}"):
        ps = out_dir / f"{tag}_pair_stats.json"
        if ps.exists():
            try:
                d = json.loads(ps.read_text(encoding="utf-8"))
                if "valid_frac_full_chain" in d:
                    valid_frac = round(float(d["valid_frac_full_chain"]), 3)
            except Exception:
                pass
        cum_f = out_dir / f"{tag}_cum.npz"
        if cum_f.exists():
            try:
                with np.load(cum_f, allow_pickle=False) as d:
                    arr = d["cum_cm"]
                    fin = arr[np.isfinite(arr)]
                    if fin.size > 0:
                        p2_val = round(float(np.percentile(fin, 2)), 1)
                    if valid_frac is None:
                        valid_frac = round(float(np.isfinite(arr).mean()), 3)
            except Exception:
                pass
        if p2_val is not None or valid_frac is not None:
            break
    return p2_val, valid_frac


def _compute_confidence(
    valid_frac: float | None,
    ref_range: list | None,
    max_cm: float | None,
    n_refs: int | None,
    val_note: dict | None,
) -> str:
    if val_note and val_note.get("confidence") in ("high", "medium", "low"):
        return val_note["confidence"]

    if valid_frac is not None and valid_frac < 0.15:
        return "low"
    if n_refs is not None and n_refs < 2 and (valid_frac is None or valid_frac < 0.40):
        return "low"

    ref_ratio = None
    if ref_range and len(ref_range) >= 2 and max_cm and abs(max_cm) > 0:
        ref_ratio = abs(max(ref_range) - min(ref_range)) / abs(max_cm)

    if ref_ratio is not None and ref_ratio >= 0.70:
        return "medium" if (valid_frac is not None and valid_frac >= 0.40) else "low"

    if (valid_frac is not None and valid_frac >= 0.40) and (ref_ratio is None or ref_ratio < 0.30):
        return "high"

    return "medium"


def _load_entry(site_id: str, name: str, country: str, ddir: Path, rel_path: str) -> dict | None:
    sf = ddir / "summary.json"
    if not sf.exists():
        return None
    s = json.loads(sf.read_text(encoding="utf-8"))

    t0, t1 = s["period"]
    days = max((date.fromisoformat(t1) - date.fromisoformat(t0)).days, 1)
    max_cm = float(s["max_subsidence_cm"])
    rate_100d = s.get("rate_cm_per_100d")
    if rate_100d is None:
        rate_100d = round(max_cm / days * 100.0, 1)

    p2_cm = s.get("p2_cm")
    valid_frac = s.get("valid_fraction")
    if p2_cm is None or valid_frac is None:
        p2_npz, vf_npz = _find_cum_stats(site_id)
        if p2_cm is None:
            p2_cm = p2_npz
        if valid_frac is None:
            valid_frac = vf_npz

    ref_range = s.get("range_cm") or s.get("max_subsidence_range_cm")
    n_refs = s.get("n_references")

    val_note = None
    vn_file = ddir / "validation_note.json"
    if vn_file.exists():
        try:
            val_note = json.loads(vn_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    conf = _compute_confidence(valid_frac, ref_range, max_cm, n_refs, val_note)

    loc = s.get("max_subsidence_location") or s.get("reference_point") or {}
    return {
        "id": site_id,
        "name": name,
        "country": country,
        "lon": loc.get("lon"),
        "lat": loc.get("lat"),
        "max_cm_los": round(max_cm, 1),
        "p2_cm": p2_cm,
        "rate_cm_per_100d": round(float(rate_100d), 1),
        "max_cm_vertical_est": s.get("max_subsidence_vertical_cm_estimate"),
        "period": s["period"],
        "days": days,
        "n_pairs": s.get("n_pairs"),
        "quality": s.get("quality", "provisional"),
        "rate_cm_per_yr_estimate": s.get("rate_cm_per_yr_estimate"),
        "valid_fraction": valid_frac,
        "ref_range_cm": ref_range,
        "confidence": conf,
        "indicative_only": conf == "low",
        "coverage": "ok",
        "path": rel_path,
        "note": (val_note.get("note", "") if val_note else ""),
    }


def main() -> None:
    entries: list[dict] = []

    for sid, name, country, ddir in CORE_REGIONS:
        e = _load_entry(sid, name, country, ddir, f"data/{sid}/")
        if e:
            entries.append(e)

    global_dir = ROOT / "data" / "global"
    if global_dir.exists():
        for sub in sorted(global_dir.iterdir()):
            if not sub.is_dir():
                continue
            sid = sub.name
            name, country = GLOBAL_META.get(sid, (sid.replace("_", " ").title(), ""))
            e = _load_entry(sid, name, country, sub, f"data/global/{sid}/")
            if e:
                entries.append(e)

    # Sort by rate_cm_per_100d ascending (most negative = fastest subsidence first)
    entries.sort(key=lambda r: (r["rate_cm_per_100d"], r["max_cm_los"]))
    for idx, e in enumerate(entries, 1):
        e["rank"] = idx

    reliable = [dict(e) for e in entries if e["confidence"] in ("high", "medium")]
    for idx, e in enumerate(reliable, 1):
        e["rank_reliable"] = idx

    indicative = [dict(e) for e in entries if e["confidence"] == "low"]
    for idx, e in enumerate(indicative, 1):
        e["rank_indicative"] = idx

    atlas = {
        "title": "NISAR Pulse global subsidence atlas 2026",
        "status": "Generated by PC10 pipeline/pc10/build_atlas.py (KALITE STANDARDI §1-§4)",
        "quality": "provisional",
        "quality_note": (
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
            "(NASA-JPL and ISRO), not by our team. Regions are ranked by rate_cm_per_100d (LOS)."
        ),
        "ranking_metric": "rate_cm_per_100d",
        "n_regions": len(entries),
        "n_reliable": len(reliable),
        "n_indicative": len(indicative),
        "regions": entries,
        "reliable": reliable,
        "indicative": indicative,
    }

    out_path = ROOT / "data" / "global" / "atlas.json"
    out_path.write_text(json.dumps(atlas, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path} ({len(entries)} regions: {len(reliable)} reliable, {len(indicative)} indicative)")
    for e in entries:
        print(
            f"  #{e['rank']:2d} {e['id']:16s} | {e['rate_cm_per_100d']:6.1f} cm/100d | "
            f"max={e['max_cm_los']:5.1f} | p2={str(e['p2_cm']):>5s} | vf={str(e['valid_fraction']):>5s} | "
            f"conf={e['confidence']}"
        )


if __name__ == "__main__":
    main()
