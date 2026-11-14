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
    "cangzhou": ("Cangzhou", "China"),
    "delhi": ("Delhi", "India"),
    "eloy": ("Eloy", "USA"),
    "quetta": ("Quetta", "Pakistan"),
    "xian": ("Xi'an", "China"),
    "pekalongan": ("Pekalongan", "Indonesia"),
    "can_tho": ("Can Tho", "Vietnam"),
}


def _load_most_subsiding_series(ddir: Path) -> list[tuple[date, float]]:
    pf = ddir / "points.json"
    if not pf.exists():
        return []
    try:
        raw = json.loads(pf.read_text(encoding="utf-8"))
        arr = raw if isinstance(raw, list) else raw.get("points", [])
        pt = next((x for x in arr if x.get("kind") == "most_subsiding"), None)
        if not pt:
            return []
        if "dates" in pt and "disp_cm" in pt:
            pairs = [(date.fromisoformat(d), float(v)) for d, v in zip(pt["dates"], pt["disp_cm"]) if v is not None]
        elif "series" in pt:
            pairs = [(date.fromisoformat(x["date"]), float(x.get("disp_cm", x.get("cum_cm")))) for x in pt["series"]]
        else:
            return []
        pairs.sort(key=lambda x: x[0])
        return pairs
    except Exception:
        return []


def _interp_at(series: list[tuple[date, float]], target: date) -> float | None:
    if not series or target < series[0][0] or target > series[-1][0]:
        return None
    for d, v in series:
        if d == target:
            return v
    for i in range(len(series) - 1):
        d0, v0 = series[i]
        d1, v1 = series[i + 1]
        if d0 <= target <= d1:
            span = (d1 - d0).days
            if span <= 0:
                return v0
            w = (target - d0).days / span
            return v0 + w * (v1 - v0)
    return None


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


def _load_aux_maps() -> tuple[dict, dict, dict, dict]:
    det_map: dict[str, dict] = {}
    det_f = ROOT / "data" / "global" / "detectability.json"
    if det_f.exists():
        for c in json.loads(det_f.read_text(encoding="utf-8")).get("cities", []):
            det_map[c["id"]] = c

    rob_map: dict[str, dict] = {}
    rob_f = ROOT / "data" / "global" / "robustness.json"
    if rob_f.exists():
        for c in json.loads(rob_f.read_text(encoding="utf-8")).get("cities", []):
            rob_map[c["id"]] = c

    exp_map: dict[str, dict] = {}
    exp_f = ROOT / "data" / "global" / "exposure_atlas.json"
    if exp_f.exists():
        for c in json.loads(exp_f.read_text(encoding="utf-8")).get("cities", []):
            exp_map[c["id"]] = c

    op_map: dict[str, dict] = {}
    op_f = ROOT / "data" / "global" / "opera_check.json"
    if op_f.exists():
        op_data = json.loads(op_f.read_text(encoding="utf-8"))
        if isinstance(op_data, list):
            for c in op_data:
                if "id" in c:
                    op_map[c["id"]] = c

    return det_map, rob_map, exp_map, op_map


def _load_entry(
    site_id: str,
    name: str,
    country: str,
    ddir: Path,
    rel_path: str,
    aux: tuple[dict, dict, dict, dict] | None = None,
) -> dict | None:
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

    det_map, rob_map, exp_map, op_map = aux or ({}, {}, {}, {})
    det_row = det_map.get(site_id)
    rob_row = rob_map.get(site_id)
    exp_row = exp_map.get(site_id)
    op_row = op_map.get(site_id)

    detectable = det_row.get("detectable") if det_row else None
    rob_spread = rob_row.get("spread_cm") if rob_row else None
    people_exposed = exp_row.get("people_lt_minus2cm") if exp_row else None
    opera_check = (
        {k: op_row.get(k) for k in ("r", "rmse_cm", "rmse_cm_per_100d", "slope", "n") if k in op_row}
        if op_row
        else None
    )

    # ATLAS_FINAL §2: detectable=false or robustness_spread > |value|/2 -> low confidence
    if detectable is False:
        conf = "low"
    if rob_spread is not None and abs(max_cm) > 0 and float(rob_spread) > abs(max_cm) / 2.0:
        conf = "low"

    # ATLAS v2: uncertainty fields (sigma_cm_median, rate_ci_cm_per_100d)
    sigma_med = None
    unc_f = ddir / "uncertainty" / "meta.json"
    if unc_f.exists():
        try:
            sigma_med = json.loads(unc_f.read_text(encoding="utf-8")).get("median_sigma_cm")
        except Exception:
            pass
    if sigma_med is None and det_row:
        sigma_med = det_row.get("sigma_median_cm")
    if sigma_med is not None:
        sigma_med = round(float(sigma_med), 3)

    rate_ci = None
    if rob_row and rob_row.get("min_rate_cm_per_100d") is not None and rob_row.get("max_rate_cm_per_100d") is not None:
        lo_r = round(float(rob_row["min_rate_cm_per_100d"]), 1)
        hi_r = round(float(rob_row["max_rate_cm_per_100d"]), 1)
        rate_ci = sorted([lo_r, hi_r])
    elif sigma_med is not None:
        half_ci = 2.0 * sigma_med / days * 100.0
        rate_ci = sorted([round(float(rate_100d) - half_ci, 1), round(float(rate_100d) + half_ci, 1)])

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
        "detectable": detectable,
        "robustness_spread": rob_spread,
        "people_exposed": people_exposed,
        "opera_check": opera_check,
        "sigma_cm_median": sigma_med,
        "rate_ci_cm_per_100d": rate_ci,
        "confidence": conf,
        "indicative_only": conf == "low",
        "coverage": "ok",
        "path": rel_path,
        "note": (val_note.get("note", "") if val_note else ""),
        "_series_dir": str(ddir),
    }


def _update_changelog(out_dir: Path, prev_atlas: dict | None, new_atlas: dict) -> None:
    from datetime import datetime, timezone

    cl_path = out_dir / "atlas_changelog.json"
    if cl_path.exists():
        try:
            cl = json.loads(cl_path.read_text(encoding="utf-8"))
        except Exception:
            cl = {"entries": []}
    else:
        cl = {
            "title": "NISAR Pulse Global Atlas Changelog",
            "entries": [
                {
                    "timestamp": "2026-11-14T23:05:00Z",
                    "note": "Initial historical corrections (off-basin re-referencing and phase-cycle QC)",
                    "added": [],
                    "removed": [],
                    "value_changes": [
                        {"id": "tehran", "old_cm": -3.5, "new_cm": -7.4, "reason": "Recomputed with off-basin reference (PC11)"},
                        {"id": "semarang", "old_cm": -12.1, "new_cm": -6.2, "reason": "2026-09-29->2026-10-11 phase-cycle jump removed; peak moved to northern coast"},
                    ],
                    "confidence_changes": [],
                    "qc_flag_changes": [],
                }
            ],
        }

    if prev_atlas:
        old_by_id = {r["id"]: r for r in prev_atlas.get("regions", [])}
        new_by_id = {r["id"]: r for r in new_atlas.get("regions", [])}
        added = sorted(set(new_by_id) - set(old_by_id))
        removed = sorted(set(old_by_id) - set(new_by_id))
        val_changes = []
        conf_changes = []
        qc_changes = []
        for sid in sorted(set(old_by_id) & set(new_by_id)):
            o, n = old_by_id[sid], new_by_id[sid]
            if abs(float(n["max_cm_los"]) - float(o["max_cm_los"])) > 0.5:
                val_changes.append({"id": sid, "old_cm": o["max_cm_los"], "new_cm": n["max_cm_los"], "reason": "Summary updated"})
            if n.get("confidence") != o.get("confidence"):
                conf_changes.append({"id": sid, "old": o.get("confidence"), "new": n.get("confidence"), "reason": n.get("note", "")[:120]})
            if n.get("qc_flags") != o.get("qc_flags"):
                qc_changes.append({"id": sid, "old": o.get("qc_flags"), "new": n.get("qc_flags")})

        if added or removed or val_changes or conf_changes or qc_changes:
            cl["entries"].append({
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "n_regions": new_atlas["n_regions"],
                "added": added,
                "removed": removed,
                "value_changes": val_changes,
                "confidence_changes": conf_changes,
                "qc_flag_changes": qc_changes,
            })

    cl_path.write_text(json.dumps(cl, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    aux = _load_aux_maps()
    entries: list[dict] = []

    for sid, name, country, ddir in CORE_REGIONS:
        e = _load_entry(sid, name, country, ddir, f"data/{sid}/", aux=aux)
        if e:
            entries.append(e)

    global_dir = ROOT / "data" / "global"
    if global_dir.exists():
        for sub in sorted(global_dir.iterdir()):
            if not sub.is_dir():
                continue
            sid = sub.name
            name, country = GLOBAL_META.get(sid, (sid.replace("_", " ").title(), ""))
            e = _load_entry(sid, name, country, sub, f"data/global/{sid}/", aux=aux)
            if e:
                entries.append(e)

    # ATLAS v2: common time window across all regions with most_subsiding series
    series_map = {e["id"]: _load_most_subsiding_series(Path(e.pop("_series_dir"))) for e in entries}
    non_empty = [s for s in series_map.values() if s]
    common_window = None
    common_days = None
    if non_empty:
        c_start = max(s[0][0] for s in non_empty)
        c_end = min(s[-1][0] for s in non_empty)
        if c_end > c_start:
            common_window = [c_start.isoformat(), c_end.isoformat()]
            common_days = (c_end - c_start).days
            for e in entries:
                ser = series_map.get(e["id"], [])
                v0 = _interp_at(ser, c_start) if ser else None
                v1 = _interp_at(ser, c_end) if ser else None
                if v0 is not None and v1 is not None:
                    e["rate_cm_per_100d_common"] = round((v1 - v0) / common_days * 100.0, 1)
                else:
                    e["rate_cm_per_100d_common"] = None

    # Time-series QC (PC1, tools/atlas_qc.py): a headline built on a one-cycle phase jump or a single
    # bad acquisition is not a measurement we can defend -> low confidence, reason in the note.
    import subprocess, sys
    subprocess.run([sys.executable, str(ROOT / "tools" / "atlas_qc.py")], check=False)   # refresh flags first
    qc_path = ROOT / "data" / "global" / "qc_flags.json"
    qc_flags = json.loads(qc_path.read_text(encoding="utf-8")).get("flags", {}) if qc_path.exists() else {}
    for e in entries:
        q = qc_flags.get(e["id"])
        if q:
            e["confidence"] = "low"
            e["indicative_only"] = True
            e["qc_flags"] = q["flags"]
            kept = q.get("headline_without_flagged_steps_cm")
            reason = "QC: " + q["detail"] + (f" Without the flagged step(s) the headline point shows {kept} cm." if kept is not None else "") + " Under revision."
            e["note"] = (e.get("note", "") + " " + reason).strip()

    # Rank reliable regions first, then indicative ones; inside each group by rate_cm_per_100d_common
    # (fallback to rate_cm_per_100d if unavailable).
    entries.sort(key=lambda r: (
        r["confidence"] == "low",
        r["rate_cm_per_100d_common"] if r.get("rate_cm_per_100d_common") is not None else r["rate_cm_per_100d"],
        r["max_cm_los"],
    ))
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
        "status": "Generated by PC10 pipeline/pc10/build_atlas.py (KALITE STANDARDI §1-§4 + ATLAS v2)",
        "quality": "provisional",
        "quality_note": (
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
            "(NASA-JPL and ISRO), not by our team. Regions are ranked by rate_cm_per_100d_common (LOS) "
            "over the intersecting window."
        ),
        "ranking_metric": "rate_cm_per_100d_common" if common_window else "rate_cm_per_100d",
        "common_window": common_window,
        "common_window_days": common_days,
        "n_regions": len(entries),
        "n_reliable": len(reliable),
        "n_indicative": len(indicative),
        "regions": entries,
        "reliable": reliable,
        "indicative": indicative,
    }

    out_path = ROOT / "data" / "global" / "atlas.json"
    prev_atlas = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else None
    _update_changelog(out_path.parent, prev_atlas, atlas)
    out_path.write_text(json.dumps(atlas, indent=2, ensure_ascii=False), encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools" / "atlas_exports.py"), str(out_path)], check=False)
    print(f"Wrote {out_path} ({len(entries)} regions: {len(reliable)} reliable, {len(indicative)} indicative, common={common_window})")
    for e in entries:
        print(
            f"  #{e['rank']:2d} {e['id']:16s} | c={str(e.get('rate_cm_per_100d_common')):>5s} ({e['rate_cm_per_100d']:6.1f}) cm/100d | "
            f"max={e['max_cm_los']:5.1f} | sig={str(e.get('sigma_cm_median')):>5s} | conf={e['confidence']}"
        )


if __name__ == "__main__":
    main()
