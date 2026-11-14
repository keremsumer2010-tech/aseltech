"""Search ASF for provisional NISAR GCOV granules over the Fens."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BBOX = (-0.3, 52.4, 0.4, 52.9)  # west, south, east, north
CUTOFF = "2026-06-17"
CRID = "P05023"  # provisional class defined by rules/VERI_SOZLESMESI.md
PATH_NUMBER = 52
FRAME_NUMBER = 61
API = "https://api.daac.asf.alaska.edu/services/search/param"
OUTPUT = Path(__file__).resolve().with_name("fens_gcov_catalog.json")


def bbox_wkt() -> str:
    west, south, east, north = BBOX
    return (
        f"POLYGON(({west} {south}, {east} {south}, {east} {north}, "
        f"{west} {north}, {west} {south}))"
    )


def h5_size_bytes(properties: dict) -> int | None:
    files = properties.get("bytes")
    if not isinstance(files, dict):
        return None
    h5_name = properties.get("fileName")
    item = files.get(h5_name) if h5_name else None
    if not isinstance(item, dict):
        item = next(
            (value for name, value in files.items()
             if name.lower().endswith(".h5") and isinstance(value, dict)),
            None,
        )
    return item.get("bytes") if isinstance(item, dict) else None


def search() -> dict:
    params = {
        "platform": "NISAR",
        "processingLevel": "GCOV",
        "start": f"{CUTOFF}T00:00:00Z",
        "intersectsWith": bbox_wkt(),
        "output": "geojson",
    }
    request = Request(
        f"{API}?{urlencode(params)}",
        headers={"User-Agent": "PC7-Fens-GCOV/1.0"},
    )
    with urlopen(request, timeout=120) as response:
        result = json.load(response)

    features = result.get("features", [])
    products = []
    for feature in features:
        p = feature.get("properties", {})
        start = p.get("startTime", "")
        polarizations = p.get("mainBandPolarization", [])
        if (
            p.get("processingLevel") != "GCOV"
            or p.get("crid") != CRID
            or start[:10] < CUTOFF
            or not {"HH", "HV"}.issubset(set(polarizations))
        ):
            continue
        products.append({
            "date": start[:10],
            "start_time": start,
            "granule": p.get("fileID"),
            "crid": p.get("crid"),
            "path": p.get("pathNumber"),
            "frame": p.get("frameNumber"),
            "direction": p.get("flightDirection"),
            "polarizations": polarizations,
            "size_bytes": h5_size_bytes(p),
            "url": p.get("url"),
        })

    products.sort(key=lambda row: (row["date"], row["granule"] or ""))
    selected = [
        row for row in products
        if row["path"] == PATH_NUMBER and row["frame"] == FRAME_NUMBER
    ]
    if not selected:
        raise RuntimeError(
            f"No P05023 GCOV products found for path={PATH_NUMBER}, frame={FRAME_NUMBER}"
        )
    dates = [row["date"] for row in selected]
    if len(dates) != len(set(dates)):
        raise RuntimeError("Selected path/frame contains duplicate acquisition dates")
    if any(not row["url"] or not row["granule"] for row in selected):
        raise RuntimeError("ASF result is missing a product URL or granule identifier")

    return {
        "queried_at_utc": datetime.now(timezone.utc).isoformat(),
        "query": {
            "url": API,
            "platform": "NISAR",
            "processing_level": "GCOV",
            "bbox_west_south_east_north": list(BBOX),
            "start_date": CUTOFF,
            "quality_crid": CRID,
        },
        "result_count": len(features),
        "provisional_product_count": len(products),
        "selected_series": {
            "path": PATH_NUMBER,
            "frame": FRAME_NUMBER,
            "products": selected,
        },
        "all_provisional_products": products,
    }


def main() -> None:
    catalog = search()
    OUTPUT.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    products = catalog["selected_series"]["products"]
    print(
        f"ASF results={catalog['result_count']}; "
        f"P05023 GCOV={catalog['provisional_product_count']}; "
        f"selected path {PATH_NUMBER}/frame {FRAME_NUMBER}={len(products)}"
    )
    print("dates=" + ",".join(row["date"] for row in products))
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()