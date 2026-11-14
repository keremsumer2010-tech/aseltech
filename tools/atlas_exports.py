"""Write open-data copies of the atlas next to atlas.json: atlas.geojson and atlas.csv.

Usage: python tools/atlas_exports.py [path/to/atlas.json]
Run at deploy time by .github/workflows/pages.yml so the downloads always match atlas.json.
"""
import csv
import json
import sys
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else "data/global/atlas.json")
atlas = json.loads(src.read_text(encoding="utf-8"))
regions = atlas.get("regions", [])

features = []
for r in regions:
    if not isinstance(r.get("lon"), (int, float)) or not isinstance(r.get("lat"), (int, float)):
        continue
    props = {k: v for k, v in r.items() if k not in ("lon", "lat")}
    features.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]}, "properties": props})

meta = {k: atlas[k] for k in ("title", "quality", "quality_note", "ranking_metric") if k in atlas}
(src.parent / "atlas.geojson").write_text(
    json.dumps({"type": "FeatureCollection", "metadata": meta, "features": features}, ensure_ascii=False, indent=1),
    encoding="utf-8")

cols = ["rank", "id", "name", "country", "lon", "lat", "rate_cm_per_100d", "max_cm_los", "max_cm_vertical_est",
        "p2_cm", "days", "n_pairs", "confidence", "indicative_only", "quality", "valid_fraction", "path", "note"]
with open(src.parent / "atlas.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(cols + ["period_start", "period_end"])
    for r in regions:
        per = r.get("period") or [None, None]
        w.writerow([r.get(c, "") for c in cols] + list(per[:2]))

print(f"atlas exports: {len(features)} features -> {src.parent / 'atlas.geojson'}, {src.parent / 'atlas.csv'}")
