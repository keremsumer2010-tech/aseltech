"""Build data/catalog.json from the files that actually exist (site + explorer read it).

Every layer: id, title, kind, file, quality (read from the file itself) and, for map layers, what the explorer
needs: png pattern ({date} placeholder), dates, bbox, legend (vmin, vmax, colormap, units).
Kinds: raster_series (one PNG per date), raster (one PNG), geojson, points, table, summary.
New regions appear automatically when their data/<site>/meta.json exists (add a title in TITLES).
Usage: python analysis/build_catalog.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE = ("NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
        "(NASA-JPL and ISRO), not by our team.")
TITLES = {  # display order = order here; unknown sites are appended with their folder name
    "central_valley": "Central Valley, California — summer 2026",
    "central_valley_fullyear": "Central Valley, California — full year (Nov 2025 – Oct 2026)",
    "karapinar": "Karapınar, Türkiye — track 7",
    "karapinar_p172": "Karapınar, Türkiye — track 172 (second orbit)",
    "konya_plain": "Konya Plain, Türkiye",
    "delta": "Sacramento–San Joaquin Delta, California",
    "uk_clay": "London clay, UK (result: below detection)",
    "uk": "The Fens, UK — radar through cloud",
    "fens": "The Fens, UK — crop radar signal",
}


def load(f):
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return None


def q(d, default=None):
    return d.get("quality", default) if isinstance(d, dict) else default


def rel(p):
    return p.relative_to(ROOT).as_posix()


def site_entry(site, folder):
    meta = load(folder / "meta.json") or {}
    summ = load(folder / "summary.json") or {}
    L = []
    if meta.get("dates") and (folder / "disp").is_dir():
        L.append({"id": "motion", "title": "Ground motion (cm, line of sight)", "kind": "raster_series",
                  "file": rel(folder / "meta.json"), "png": rel(folder / "disp") + "/{date}.png", "dates": meta["dates"],
                  "bbox": meta["bbox"], "legend": {"vmin": meta["vmin"], "vmax": meta["vmax"], "cmap": "RdBu",
                                                    "units": "cm", "low": "sinking", "high": "rising"},
                  "quality": q(meta)})
    if meta.get("date") and (folder / f"radar_{meta['date']}.png").exists() and meta.get("bbox"):
        L.append({"id": "radarimg", "title": f"NISAR radar image, {meta['date']} (quick-look)", "kind": "raster",
                  "file": rel(folder / "meta.json"), "png": rel(folder / f"radar_{meta['date']}.png"), "bbox": meta["bbox"],
                  "legend": None, "quality": q(meta)})
    um = load(folder / "uncertainty" / "meta.json")
    if um:
        L.append({"id": "uncertainty", "title": "Measurement uncertainty (1σ, cm)", "kind": "raster",
                  "file": rel(folder / "uncertainty" / "meta.json"), "png": rel(folder / "uncertainty" / "sigma_cm.png"),
                  "bbox": um["bbox"], "legend": {"vmin": um["vmin"], "vmax": um["vmax"], "cmap": "viridis", "units": "cm",
                                                 "low": "more certain", "high": "less certain"}, "quality": q(um)})
    gm = load(folder / "gcov" / "meta.json")
    if gm:
        L.append({"id": "radar", "title": "Radar brightness, HV (dB)", "kind": "raster_series",
                  "file": rel(folder / "gcov" / "meta.json"), "png": rel(folder / "gcov") + "/{date}.png", "dates": gm["dates"],
                  "bbox": gm["bbox"], "legend": {"vmin": gm["vmin"], "vmax": gm["vmax"], "cmap": "viridis", "units": "dB",
                                                 "low": "bare or dry", "high": "dense crops"}, "quality": q(gm)})
    dc = load(folder / "decomp.json")
    if dc and dc.get("status") == "ok":
        for key, title, cmap, lo, hi in (("permanent_cm_per_yr", "Permanent trend (cm/yr)", "RdBu", "sinking", "rising"),
                                         ("seasonal_amp_cm", "Seasonal swing (cm)", "magma", "small", "large")):
            d = dc[key]
            L.append({"id": key.split("_")[0], "title": title, "kind": "raster", "file": rel(folder / "decomp.json"),
                      "png": rel(folder / d["png"]), "bbox": dc["bbox"],
                      "legend": {"vmin": d["vmin"], "vmax": d["vmax"], "cmap": cmap, "units": title.split("(")[1][:-1],
                                 "low": lo, "high": hi}, "quality": q(dc)})
    for fn, lid, title, kind in (("assets.json", "risk", "Infrastructure risk (canals, roads, rail)", "geojson"),
                                 ("sinkholes.geojson", "sinkholes", "Documented sinkholes", "geojson"),
                                 ("points.json", "points", "Point time series", "points"),
                                 ("grid.json", "grid", "Clickable ~1–2 km grid", "table"),
                                 ("summary.json", "summary", "Headline numbers", "summary"),
                                 ("area_stats.json", "area", "Area sinking more than 2 / 5 cm", "table"),
                                 ("validation.json", "validation", "GPS comparison", "validation"),
                                 ("vertical.json", "vertical", "Vertical and east–west motion (two orbits)", "summary"),
                                 ("drivers.json", "drivers", "Soil moisture and irrigation drivers", "table"),
                                 ("detection.json", "detection", "Signal vs noise test", "summary"),
                                 ("crops.json", "crops", "Field radar time series (HH, HV)", "table")):
        f = folder / fn
        if f.exists():
            d = load(f)
            L.append({"id": lid, "title": title, "kind": kind, "file": rel(f),
                      "quality": q(d) or q(meta) or q(summ)})
    if not L:
        return None
    head = summ or meta or load(folder / "crops.json") or {}
    e = {"site": site, "title": TITLES.get(site, site.replace("_", " ")), "quality": q(head) or q(meta),
         "quality_note": head.get("quality_note", NOTE) if isinstance(head, dict) else NOTE,
         "path": rel(folder) + "/", "bbox": meta.get("bbox") or head.get("bbox"), "layers": L}
    if summ.get("period"):
        e["period"] = summ["period"]
    elif meta.get("dates"):
        e["period"] = [meta["dates"][0], meta["dates"][-1]]
    elif meta.get("date"):
        e["date"] = meta["date"]
    elif isinstance(head, dict) and head.get("dates"):
        e["period"] = [head["dates"][0], head["dates"][-1]]
    return e


def main():
    sites = [p.name for p in sorted((ROOT / "data").iterdir()) if p.is_dir()]
    order = [s for s in TITLES if s in sites] + [s for s in sites if s not in TITLES]
    out = [e for s in order if (e := site_entry(s, ROOT / "data" / s))]
    (ROOT / "data" / "catalog.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for e in out:
        print(f"{e['site']:24s} {str(e['quality']):12s} {[l['id'] for l in e['layers']]}")


if __name__ == "__main__":
    main()
