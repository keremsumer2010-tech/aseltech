"""Operational Bulletin Generator — NISAR Pulse Bulletin (PC8, ATLAS_PLANI.md).

Generates single-page printable HTML bulletins (`docs/bulletins/<region>.html`) and
an index (`docs/bulletins/index.html`) for all regions listed in `data/global/atlas.json`
(Central Valley, Karapinar, Konya Plain, Delta, and all global atlas cities).

Usage:
  python tools/bulletin.py                 # build bulletins for all regions in atlas.json
  python tools/bulletin.py --region delta  # build a single region
"""
from __future__ import annotations

import argparse
from datetime import date
import html
import json
import statistics
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ATLAS_PATH = ROOT / "data" / "global" / "atlas.json"
OUT_DIR = ROOT / "docs" / "bulletins"

CALIBRATION_NOTICE = (
    "NISAR data are provisional. Calibration and validation are carried out by the "
    "NISAR project (NASA-JPL and ISRO), not by our team."
)


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _esc(val: Any) -> str:
    return html.escape(str(val), quote=True)


def _format_last_pair(points_data: Any) -> dict[str, Any]:
    if not isinstance(points_data, list) or not points_data:
        return {"available": False}
    p0 = points_data[0]
    dates = p0.get("dates") or []
    disp = p0.get("disp_cm") or []
    if len(dates) < 2 or len(disp) < 2:
        return {"available": False}
    last_val = disp[-1]
    prev_val = disp[-2]
    if last_val is None or prev_val is None:
        return {"available": False}
    step_cm = float(last_val) - float(prev_val)
    return {
        "available": True,
        "point_id": p0.get("id", "p01"),
        "point_name": p0.get("name", "Peak point"),
        "pair_start": dates[-2],
        "pair_end": dates[-1],
        "step_cm_los": round(step_cm, 2),
        "total_cm_los": round(float(last_val), 2),
    }


def _compute_rate_100d_and_confidence(
    region: dict[str, Any],
    summary: dict[str, Any],
    meta: dict[str, Any],
) -> tuple[float | None, str, str]:
    """Return (rate_cm_per_100d, confidence_level, display_label)."""
    period = summary.get("period") or region.get("period") or []
    days: int | None = None
    if isinstance(period, list) and len(period) >= 2 and period[0] and period[1]:
        try:
            d0 = date.fromisoformat(str(period[0]))
            d1 = date.fromisoformat(str(period[1]))
            days = max(1, (d1 - d0).days)
        except ValueError:
            days = None

    max_los = summary.get("max_subsidence_cm", region.get("max_cm_los"))
    rate_100d = region.get("rate_cm_per_100d") or summary.get("rate_cm_per_100d")
    if rate_100d is not None:
        rate_val: float | None = round(float(rate_100d), 2)
    elif max_los is not None and days is not None:
        rate_val = round((float(max_los) / days) * 100.0, 2)
    else:
        rate_val = None

    explicit_conf = region.get("confidence") or summary.get("confidence")
    if isinstance(explicit_conf, str) and explicit_conf.lower() in {"high", "medium", "low"}:
        conf = explicit_conf.lower()
    else:
        conf = "high"
        coverage = region.get("coverage", "ok")
        n_pairs = summary.get("n_pairs", region.get("n_pairs"))
        vfrac = summary.get("valid_pixel_fraction")
        if vfrac is None:
            vfrac = meta.get("valid_pixel_fraction")
        ref_range = summary.get("range_cm") or summary.get("max_subsidence_range_cm")

        if coverage != "ok":
            conf = "low"
        elif vfrac is not None and float(vfrac) < 0.25:
            conf = "low"
        elif max_los is not None and abs(float(max_los)) < 3.0:
            conf = "low"
        elif isinstance(n_pairs, int) and n_pairs < 3:
            conf = "medium"
        elif vfrac is not None and float(vfrac) < 0.60:
            conf = "medium"

        if conf != "low" and max_los is not None and isinstance(ref_range, list) and len(ref_range) == 2:
            spread = abs(float(ref_range[1]) - float(ref_range[0]))
            if abs(float(max_los)) > 0 and spread > 0.5 * abs(float(max_los)):
                conf = "medium"

    label = "LOW (indicative only)" if conf == "low" else conf.upper()
    return rate_val, conf, label


def _top_segments(region_dir: Path, limit: int = 5) -> tuple[str, str, list[dict[str, Any]]]:
    """Read O2 `assets_prob.json` if available, else fall back to `assets.json`."""
    prob = _read_json(region_dir / "assets_prob.json")
    if isinstance(prob, dict) and prob.get("features"):
        rows = []
        for f in prob["features"]:
            pr = f.get("properties", {})
            p_beta = pr.get("p_beta_exceed") or {}
            ci90 = pr.get("ci90") or {}
            diff_ci = ci90.get("max_differential_cm")
            p500 = p_beta.get("1/500")
            p1000 = p_beta.get("1/1000")
            rows.append({
                "name": pr.get("name") or pr.get("type") or "Unnamed corridor",
                "type": pr.get("type", ""),
                "max_diff_cm": pr.get("max_differential_cm"),
                "diff_ci90": diff_ci,
                "beta_max": pr.get("beta_max"),
                "p_diff_gt_10cm": pr.get("p_diff_gt_10cm"),
                "p_beta_500": p500,
                "p_beta_1000": p1000,
            })
        rows.sort(
            key=lambda r: (
                float(r.get("p_diff_gt_10cm") or 0.0),
                float(r.get("p_beta_1000") or 0.0),
                float(r.get("p_beta_500") or 0.0),
                float(r.get("max_diff_cm") or 0.0),
                float(r.get("beta_max") or 0.0),
            ),
            reverse=True,
        )
        return "o2", "O2 probabilistic infrastructure risk (assets_prob.json)", rows[:limit]

    assets = _read_json(region_dir / "assets.json")
    if isinstance(assets, dict) and assets.get("features"):
        rows = []
        for f in assets["features"]:
            pr = f.get("properties", {})
            rows.append({
                "name": pr.get("name") or pr.get("type") or "Unnamed corridor",
                "type": pr.get("type", ""),
                "length_km": pr.get("length_km"),
                "gradient_mm_per_km": pr.get("gradient_mm_per_km"),
                "max_cm": pr.get("max_cm"),
                "nearest_sinkhole_m": pr.get("nearest_sinkhole_m"),
                "risk": pr.get("risk", ""),
            })
        rows.sort(key=lambda r: float(r.get("gradient_mm_per_km") or 0.0), reverse=True)
        return "o1_assets", "Infrastructure tilt ranking (assets.json)", rows[:limit]

    return "none", "none", []


def _gnss_summary(region_dir: Path) -> dict[str, Any]:
    val = _read_json(region_dir / "validation.json")
    if not isinstance(val, list) or not val:
        return {"available": False}
    rmses = [float(s["rmse_cm"]) for s in val if s.get("rmse_cm") is not None]
    corrs = [float(s["corr"]) for s in val if s.get("corr") is not None]
    return {
        "available": True,
        "n_stations": len(val),
        "median_rmse_cm": round(statistics.median(rmses), 2) if rmses else None,
        "median_corr": round(statistics.median(corrs), 2) if corrs else None,
        "stations": [s.get("station", "") for s in val[:6]],
    }


def render_region_bulletin(region: dict[str, Any], out_dir: Path = OUT_DIR) -> Path | None:
    rid = region["id"]
    if region.get("coverage") == "none":
        return None
    rel_data = (region.get("path") or f"data/global/{rid}/").rstrip("/")
    region_dir = ROOT / rel_data
    summary = _read_json(region_dir / "summary.json") or {}
    meta = _read_json(region_dir / "meta.json") or {}
    points = _read_json(region_dir / "points.json")
    exposure = _read_json(region_dir / "exposure.json")
    area_stats = _read_json(region_dir / "area_stats.json")

    name = region.get("name") or rid
    country = region.get("country") or ""
    title_loc = f"{name} ({country})" if country else name
    period = summary.get("period") or region.get("period") or ["N/A", "N/A"]
    last_date = period[1] if len(period) >= 2 else "N/A"
    start_date = period[0] if len(period) >= 1 else "N/A"

    quality = (summary.get("quality") or region.get("quality") or "provisional").upper()
    qnote = summary.get("quality_note") or CALIBRATION_NOTICE
    max_los = summary.get("max_subsidence_cm", region.get("max_cm_los"))
    max_vert = summary.get("max_subsidence_vertical_cm_estimate", region.get("max_cm_vertical_est"))
    ref_range = summary.get("range_cm") or summary.get("max_subsidence_range_cm")
    rate_yr = summary.get("rate_cm_per_yr_estimate", region.get("rate_cm_per_yr_estimate"))
    rate_100d, conf_level, conf_label = _compute_rate_100d_and_confidence(region, summary, meta)
    n_pairs = summary.get("n_pairs", region.get("n_pairs", "N/A"))
    inc_deg = summary.get("incidence_deg_at_max", "N/A")

    last_pair = _format_last_pair(points)
    seg_kind, seg_source, top_segs = _top_segments(region_dir, limit=5)
    gnss = _gnss_summary(region_dir)

    disp_png_rel = f"../../{rel_data}/disp/{last_date}.png"
    has_disp_png = (region_dir / "disp" / f"{last_date}.png").exists()

    # Build HTML fragments
    if last_pair["available"]:
        last_pair_html = (
            f"<strong>{last_pair['step_cm_los']:+.2f} cm LOS</strong> "
            f"({ _esc(last_pair['pair_start']) } to { _esc(last_pair['pair_end']) } at "
            f"{ _esc(last_pair['point_id']) }: { _esc(last_pair['point_name']) }; "
            f"cumulative at point: {last_pair['total_cm_los']:+.2f} cm)"
        )
    else:
        last_pair_html = "Latest consecutive pair step not itemized in regional points file."

    range_str = (
        f"[{ref_range[0]:+.1f}, {ref_range[1]:+.1f}] cm LOS"
        if isinstance(ref_range, list) and len(ref_range) == 2
        else "single reference window"
    )

    if top_segs and seg_kind == "o2":
        seg_rows = []
        for idx, s in enumerate(top_segs, 1):
            mdiff = f"{s['max_diff_cm']:.2f} cm" if s.get("max_diff_cm") is not None else "-"
            ci = s.get("diff_ci90")
            ci_str = f" [{ci[0]:.1f}, {ci[1]:.1f}]" if isinstance(ci, list) and len(ci) == 2 else ""
            beta_val = f"{s['beta_max']:.2e}" if s.get("beta_max") is not None else "-"
            p10 = f"{s['p_diff_gt_10cm']:.1%}" if s.get("p_diff_gt_10cm") is not None else "-"
            p1000 = f"{s['p_beta_1000']:.1%}" if s.get("p_beta_1000") is not None else "-"
            p500 = f"{s['p_beta_500']:.1%}" if s.get("p_beta_500") is not None else "-"
            seg_rows.append(
                f"<tr><td>{idx}</td><td>{_esc(s['name'])}</td><td>{_esc(s['type'])}</td>"
                f"<td class='num'>{mdiff}{ci_str}</td><td class='num'>{beta_val}</td>"
                f"<td class='num'>{p10}</td><td class='num'>{p1000} / {p500}</td></tr>"
            )
        seg_section = (
            f"<p class='sub'>Source: {_esc(seg_source)}</p>"
            "<table><thead><tr><th>#</th><th>Segment</th><th>Type</th>"
            "<th class='num'>Max Diff (90% CI)</th><th class='num'>Beta Max</th>"
            "<th class='num'>P(Diff &gt; 10 cm)</th><th class='num'>P(Beta &gt; 1/1000 | 1/500)</th></tr></thead>"
            f"<tbody>{''.join(seg_rows)}</tbody></table>"
        )
    elif top_segs:
        seg_rows = []
        for idx, s in enumerate(top_segs, 1):
            extra = (
                f"{s['nearest_sinkhole_m']:.0f} m to sinkhole"
                if s.get("nearest_sinkhole_m") is not None
                else str(s.get("risk", ""))
            )
            grad = f"{s['gradient_mm_per_km']:.2f}" if s.get("gradient_mm_per_km") is not None else "-"
            mcm = f"{s['max_cm']:.2f}" if s.get("max_cm") is not None else "-"
            lkm = f"{s['length_km']:.2f}" if s.get("length_km") is not None else "-"
            seg_rows.append(
                f"<tr><td>{idx}</td><td>{_esc(s['name'])}</td><td>{_esc(s['type'])}</td>"
                f"<td class='num'>{lkm}</td><td class='num'>{grad}</td><td class='num'>{mcm}</td><td>{_esc(extra)}</td></tr>"
            )
        seg_section = (
            f"<p class='sub'>Source: {_esc(seg_source)}</p>"
            "<table><thead><tr><th>#</th><th>Segment</th><th>Type</th>"
            "<th class='num'>Length (km)</th><th class='num'>Tilt (mm/km)</th>"
            "<th class='num'>Max LOS (cm)</th><th>Risk / Flag</th></tr></thead>"
            f"<tbody>{''.join(seg_rows)}</tbody></table>"
        )
    else:
        seg_section = "<p class='muted'>Infrastructure corridor ranking (OSM canal/road overlay) has not been computed for this regional subset yet.</p>"

    if gnss["available"]:
        gnss_html = (
            f"<p><strong>{gnss['n_stations']} continuous GNSS stations</strong> compared: "
            f"median time-series RMSE <strong>{gnss['median_rmse_cm']:.2f} cm</strong>, "
            f"median correlation <strong>r = {gnss['median_corr']:.2f}</strong> "
            f"(sample stations: {_esc(', '.join(gnss['stations']))}).</p>"
        )
    else:
        gnss_html = "<p class='muted'>Continuous GNSS time-series validation was not bundled for this regional subset.</p>"

    exp_html = ""
    if isinstance(exposure, dict):
        pop = exposure.get("population", {})
        p2 = pop.get("population_subsidence_gt_2cm_los_estimate")
        p5 = pop.get("population_subsidence_gt_5cm_los_estimate")
        if p2 is not None:
            exp_html = (
                f"<li><strong>Population Exposure (WorldPop 100 m, 2020 estimate):</strong> "
                f"~{p2:,} residents on &gt;2 cm LOS subsiding pixels (~{p5:,} on &gt;5 cm LOS).</li>"
            )
    area_html = ""
    if isinstance(area_stats, dict):
        a2 = area_stats.get("area_subsiding_gt_2cm_los_km2") or area_stats.get("gt_2cm_los_km2")
        a5 = area_stats.get("area_subsiding_gt_5cm_los_km2") or area_stats.get("gt_5cm_los_km2")
        if a2 is not None:
            area_html = f"<li><strong>Subsiding Footprint:</strong> {a2} km&sup2; (&gt;2 cm LOS), {a5} km&sup2; (&gt;5 cm LOS).</li>"

    img_block = (
        f"<figure class='map'><img src='{_esc(disp_png_rel)}' alt='Cumulative LOS displacement map for {_esc(title_loc)} ending {_esc(last_date)}'>"
        f"<figcaption>Cumulative LOS displacement ({_esc(start_date)} to {_esc(last_date)}, {n_pairs} NISAR L2 GUNW pairs).</figcaption></figure>"
        if has_disp_png
        else "<p class='muted'>Cumulative displacement PNG preview not present in repository subset.</p>"
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NISAR Pulse Bulletin — {_esc(title_loc)} — {_esc(last_date)}</title>
<style>
  :root {{ --ink:#0f172a; --muted:#475569; --line:#cbd5e1; --bg:#ffffff; --panel:#f8fafc; --accent:#1d4ed8; --warn:#b45309; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:24px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; color:var(--ink); background:#f1f5f9; line-height:1.45; }}
  .sheet {{ max-width:920px; margin:0 auto; background:var(--bg); border:1px solid var(--line); border-radius:10px; padding:24px 28px; box-shadow:0 4px 16px rgba(15,23,42,.06); }}
  .topbar {{ display:flex; justify-content:space-between; align-items:flex-start; gap:12px; border-bottom:2px solid var(--ink); padding-bottom:12px; margin-bottom:14px; }}
  h1 {{ font-size:1.35rem; margin:0 0 4px 0; }}
  .meta {{ font-size:.86rem; color:var(--muted); }}
  .badge {{ display:inline-block; padding:3px 9px; border-radius:999px; font-size:.75rem; font-weight:700; letter-spacing:.04em; background:#fef3c7; color:#92400e; border:1px solid #f59e0b; }}
  .conf-high {{ background:#dcfce7; color:#166534; border-color:#22c55e; }}
  .conf-medium {{ background:#fef3c7; color:#92400e; border-color:#f59e0b; }}
  .conf-low {{ background:#fee2e2; color:#991b1b; border-color:#ef4444; }}
  .kpi .subval {{ font-size:.76rem; color:var(--muted); margin-top:2px; font-weight:400; }}
  .actions {{ display:flex; gap:8px; align-items:center; }}
  .btn {{ font-size:.82rem; padding:6px 12px; border-radius:6px; border:1px solid var(--line); background:var(--panel); color:var(--ink); text-decoration:none; cursor:pointer; }}
  .btn-primary {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
  .grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:12px 0 16px; }}
  .kpi {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:10px 12px; }}
  .kpi .lbl {{ font-size:.74rem; color:var(--muted); text-transform:uppercase; letter-spacing:.03em; }}
  .kpi .val {{ font-size:1.18rem; font-weight:700; margin-top:2px; }}
  .two {{ display:grid; grid-template-columns:1.15fr .85fr; gap:18px; align-items:start; }}
  h2 {{ font-size:1.0rem; margin:14px 0 6px; border-bottom:1px solid var(--line); padding-bottom:3px; }}
  .sub {{ font-size:.8rem; color:var(--muted); margin:0 0 6px; }}
  .muted {{ font-size:.86rem; color:var(--muted); }}
  table {{ width:100%; border-collapse:collapse; font-size:.82rem; margin-top:4px; }}
  th, td {{ border-bottom:1px solid #e2e8f0; padding:6px 6px; text-align:left; }}
  th {{ background:var(--panel); font-weight:600; }}
  .num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .map {{ margin:0; background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:8px; }}
  .map img {{ width:100%; height:auto; display:block; border-radius:4px; }}
  .map figcaption {{ font-size:.76rem; color:var(--muted); margin-top:6px; }}
  .notice {{ margin-top:14px; padding:10px 12px; background:#fffbeb; border-left:4px solid var(--warn); font-size:.82rem; }}
  ul {{ margin:6px 0 0 18px; padding:0; font-size:.86rem; }}
  @media (max-width:760px) {{ .grid {{ grid-template-columns:repeat(2,1fr); }} .two {{ grid-template-columns:1fr; }} }}
  @media print {{
    body {{ background:#fff; padding:0; }}
    .sheet {{ border:none; box-shadow:none; padding:10px; max-width:100%; }}
    .actions {{ display:none; }}
  }}
</style>
</head>
<body>
<div class="sheet">
  <div class="topbar">
    <div>
      <h1>NISAR Pulse Bulletin &mdash; {_esc(title_loc)} &mdash; {_esc(last_date)}</h1>
      <div class="meta">Observation window: {_esc(start_date)} to {_esc(last_date)} ({_esc(n_pairs)} pairs) &middot; Atlas Rank #{_esc(region.get('rank', '-'))} &middot; Coverage: {_esc(region.get('coverage', 'ok'))}</div>
    </div>
    <div class="actions">
      <span class="badge conf-{_esc(conf_level)}">CONFIDENCE: {_esc(conf_label)}</span>
      <span class="badge">{_esc(quality)}</span>
      <a class="btn" href="index.html">All Bulletins</a>
      <button class="btn btn-primary" onclick="window.print()">Print / PDF</button>
    </div>
  </div>

  <div class="grid">
    <div class="kpi"><div class="lbl">Peak Cumulative (LOS)</div><div class="val">{_esc(max_los)} cm</div></div>
    <div class="kpi"><div class="lbl">Vertical Est. ({_esc(inc_deg)}&deg;)</div><div class="val">{_esc(max_vert)} cm</div></div>
    <div class="kpi"><div class="lbl">3-Ref Sensitivity</div><div class="val" style="font-size:0.98rem;">{_esc(range_str)}</div></div>
    <div class="kpi"><div class="lbl">Rate (cm / 100 days)</div><div class="val">{_esc(rate_100d if rate_100d is not None else 'N/A')} cm/100d</div><div class="subval">Annualized est.: {_esc(rate_yr)} cm/yr</div></div>
  </div>

  <div class="two">
    <div>
      <h2>Latest Pair &amp; Cumulative Summary</h2>
      <ul>
        <li><strong>Latest Consecutive Pair Step:</strong> {last_pair_html}</li>
        {area_html}
        {exp_html}
      </ul>

      <h2>Top 5 At-Risk Infrastructure Segments</h2>
      {seg_section}

      <h2>GNSS Comparison &amp; Calibration Status</h2>
      {gnss_html}
    </div>
    <div>
      <h2>Cumulative Displacement Map</h2>
      {img_block}
    </div>
  </div>

  <div class="notice">
    <strong>Calibration &amp; Quality Notice ({_esc(quality)}):</strong> {_esc(qnote)}<br>
    <strong>Sources:</strong> NASA-ISRO NISAR L2 GUNW (CRID P05023 via ASF DAAC); Nevada Geodetic Laboratory GNSS; OpenStreetMap (ODbL); WorldPop 100 m (CC BY 4.0) / USDA CDL 30 m / ESA WorldCover 10 m where noted.
  </div>
</div>
</body>
</html>
"""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{rid}.html"
    out_file.write_text(page, encoding="utf-8")
    return out_file


def render_index(regions: list[dict[str, Any]], generated: list[tuple[dict[str, Any], Path]], out_dir: Path = OUT_DIR) -> Path:
    enriched: list[tuple[float, dict[str, Any], Path, float | None, str, str]] = []
    for reg, path in generated:
        rel_data = (reg.get("path") or f"data/global/{reg['id']}/").rstrip("/")
        rdir = ROOT / rel_data
        summary = _read_json(rdir / "summary.json") or {}
        meta = _read_json(rdir / "meta.json") or {}
        rate_100d, conf_level, conf_label = _compute_rate_100d_and_confidence(reg, summary, meta)
        sort_key = abs(rate_100d) if rate_100d is not None else 0.0
        enriched.append((sort_key, reg, path, rate_100d, conf_level, conf_label))

    enriched.sort(key=lambda item: item[0], reverse=True)

    rows = []
    for idx, (_, reg, path, rate_100d, conf_level, conf_label) in enumerate(enriched, 1):
        period = reg.get("period") or ["", ""]
        end_d = period[1] if len(period) >= 2 else ""
        rate_str = f"{rate_100d:+.2f} cm/100d" if rate_100d is not None else "N/A"
        rows.append(
            f"<tr><td>#{idx}</td>"
            f"<td><a href='{_esc(path.name)}'><strong>{_esc(reg.get('name', reg['id']))}</strong></a></td>"
            f"<td>{_esc(reg.get('country', ''))}</td>"
            f"<td class='num'><strong>{_esc(rate_str)}</strong></td>"
            f"<td class='num'>{_esc(reg.get('max_cm_los', ''))} cm</td>"
            f"<td class='num'>{_esc(reg.get('max_cm_vertical_est', ''))} cm</td>"
            f"<td>{_esc(end_d)}</td>"
            f"<td><span class='pill conf-{_esc(conf_level)}'>{_esc(conf_label)}</span></td>"
            f"<td>{_esc(reg.get('quality', 'provisional'))}</td></tr>"
        )

    idx_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NISAR Pulse Bulletins — 2026 Operational Index</title>
<style>
  body {{ margin:0; padding:24px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; color:#0f172a; background:#f8fafc; }}
  .wrap {{ max-width:1020px; margin:0 auto; background:#fff; border:1px solid #cbd5e1; border-radius:10px; padding:24px 28px; }}
  h1 {{ margin:0 0 6px; font-size:1.4rem; }}
  p {{ color:#475569; font-size:.92rem; }}
  table {{ width:100%; border-collapse:collapse; margin-top:16px; font-size:.88rem; }}
  th, td {{ padding:9px 10px; border-bottom:1px solid #e2e8f0; text-align:left; }}
  th {{ background:#f1f5f9; }}
  .num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .pill {{ display:inline-block; padding:2px 8px; border-radius:999px; font-size:.74rem; font-weight:700; border:1px solid #cbd5e1; }}
  .conf-high {{ background:#dcfce7; color:#166534; border-color:#22c55e; }}
  .conf-medium {{ background:#fef3c7; color:#92400e; border-color:#f59e0b; }}
  .conf-low {{ background:#fee2e2; color:#991b1b; border-color:#ef4444; }}
  a {{ color:#1d4ed8; text-decoration:none; }}
  a:hover {{ text-decoration:underline; }}
  .notice {{ margin-top:18px; padding:10px 12px; background:#fffbeb; border-left:4px solid #b45309; font-size:.82rem; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>NISAR Pulse Operational Bulletins</h1>
  <p>Single-page, printable subsidence bulletins automatically generated from <code>data/global/atlas.json</code> and regional contract outputs ({len(generated)} active regions, ranked by period-independent <code>rate_cm_per_100d</code>).</p>
  <table>
    <thead><tr><th>Rank</th><th>Region</th><th>Country</th><th class="num">Rate (cm/100d)</th><th class="num">Max LOS</th><th class="num">Vertical Est.</th><th>Latest Date</th><th>Confidence</th><th>Quality</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <div class="notice"><strong>Calibration Notice:</strong> {_esc(CALIBRATION_NOTICE)}</div>
</div>
</body>
</html>
"""
    idx_path = out_dir / "index.html"
    idx_path.write_text(idx_html, encoding="utf-8")
    return idx_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate NISAR Pulse HTML bulletins from atlas.json.")
    ap.add_argument("--region", help="Optional single region id (default: all regions in atlas.json)")
    args = ap.parse_args()

    atlas = _read_json(ATLAS_PATH) or {}
    regions = atlas.get("regions", [])
    if args.region:
        regions = [r for r in regions if r.get("id") == args.region]
        if not regions:
            raise SystemExit(f"Region '{args.region}' not found in {ATLAS_PATH}")

    generated: list[tuple[dict[str, Any], Path]] = []
    for reg in regions:
        out = render_region_bulletin(reg, OUT_DIR)
        if out is not None:
            generated.append((reg, out))
            print(f"Generated {out.relative_to(ROOT)}")

    if not args.region:
        idx = render_index(regions, generated, OUT_DIR)
        print(f"Generated {idx.relative_to(ROOT)} ({len(generated)} bulletins)")


if __name__ == "__main__":
    main()
