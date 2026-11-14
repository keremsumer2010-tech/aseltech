"""Automatic time-series QC for atlas headline points (PC1).

For every region in data/global/atlas.json, look at the headline point's cumulative series
(points.json, kind == "most_subsiding") and flag two failure modes that a single summary
number hides:

  phase_cycle_jump      one step whose size is within ±CYCLE_TOL of a full L-band phase cycle
                        (lambda/2 = 12.1 cm LOS). Typical of an unwrapping error.
  single_date_outlier   two consecutive steps of opposite sign, each larger than SPIKE_CM, that
                        largely cancel: one acquisition is off (atmosphere, unwrapping), the
                        surrounding dates agree.

Output: data/global/qc_flags.json  {id: {"flags": [...], "steps_cm": [...], "detail": "...",
         "headline_without_flagged_steps_cm": x}}.
build_atlas.py reads this file: a flagged region becomes confidence "low" (indicative only)
with the QC reason in its note, until the owner re-processes it.
Usage: python tools/atlas_qc.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAVELENGTH_CM = 24.196          # NISAR L-band, c / 1.239 GHz
CYCLE_CM = WAVELENGTH_CM / 2    # one 2*pi cycle of interferometric phase in LOS displacement
CYCLE_TOL = 2.0
SPIKE_CM = 5.0
CANCEL_RATIO = 0.4


def headline_series(base: Path):
    pf = base / "points.json"
    if not pf.exists():
        return None
    pts = json.loads(pf.read_text(encoding="utf-8"))
    pts = pts.get("points", pts) if isinstance(pts, dict) else pts
    head = [p for p in pts if p.get("kind") == "most_subsiding"] or pts[:1]
    return head[0] if head else None


def check(series):
    d = series.get("disp_cm") or []
    steps = [round(d[i] - d[i - 1], 2) for i in range(1, len(d))]
    flags, detail, drop = [], [], set()
    for i, s in enumerate(steps):
        if abs(abs(s) - CYCLE_CM) <= CYCLE_TOL:
            flags.append("phase_cycle_jump")
            detail.append(f"step {i + 1} ({series['dates'][i]}→{series['dates'][i + 1]}) = {s:+.2f} cm ≈ one phase cycle ({CYCLE_CM:.1f} cm)")
            drop.add(i)
    for i in range(1, len(steps)):
        a, b = steps[i - 1], steps[i]
        if abs(a) > SPIKE_CM and abs(b) > SPIKE_CM and a * b < 0 and abs(a + b) < CANCEL_RATIO * max(abs(a), abs(b)):
            flags.append("single_date_outlier")
            detail.append(f"date {series['dates'][i]}: {a:+.2f} then {b:+.2f} cm (one acquisition off)")
            drop.update({i - 1, i})
    kept = round(sum(s for j, s in enumerate(steps) if j not in drop), 2)
    return sorted(set(flags)), steps, "; ".join(detail), kept


def main():
    # Regions: everything already in the atlas plus any data/global/<id>/ folder with a points.json,
    # so a city is checked before build_atlas.py adds it.
    regions = {}
    ap = ROOT / "data/global/atlas.json"
    if ap.exists():
        for r in json.loads(ap.read_text(encoding="utf-8")).get("regions", []):
            regions[r["id"]] = ROOT / (r.get("path") or f"data/global/{r['id']}/")
    for d in sorted((ROOT / "data/global").iterdir()):
        if d.is_dir() and (d / "points.json").exists():
            regions.setdefault(d.name, d)
    out = {}
    for rid, base in regions.items():
        r = {"id": rid}
        s = headline_series(base)
        if not s:
            continue
        flags, steps, detail, kept = check(s)
        if flags:
            out[r["id"]] = {"flags": flags, "steps_cm": steps, "detail": detail,
                            "headline_point": [s.get("lon"), s.get("lat")],
                            "headline_without_flagged_steps_cm": kept}
    man_path = ROOT / "data/global/qc_manual.json"
    if man_path.exists():
        for rid, m in json.loads(man_path.read_text(encoding="utf-8")).get("flags", {}).items():
            cur = out.setdefault(rid, {"flags": [], "detail": "", "headline_without_flagged_steps_cm": None})
            cur["flags"] = sorted(set(cur["flags"]) | set(m["flags"]))
            cur["detail"] = "; ".join(x for x in (cur["detail"], m["detail"]) if x)
            cur["sources"] = m.get("sources", [])
    path = ROOT / "data/global/qc_flags.json"
    path.write_text(json.dumps({"method": __doc__.split("Output:")[0].strip(), "cycle_cm": round(CYCLE_CM, 2),
                                "flags": out}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}: {len(out)} flagged -> {', '.join(out) or 'none'}")


if __name__ == "__main__":
    main()
