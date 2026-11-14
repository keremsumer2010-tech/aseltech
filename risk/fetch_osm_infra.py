#!/usr/bin/env python3
"""Fetch OpenStreetMap infrastructure lines (canals, major highways, railways) via Overpass API
for Central Valley and Karapinar bounding boxes.

License of output data: © OpenStreetMap contributors, ODbL.
Owner: PC6
"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

ROOT_DIR = Path(__file__).resolve().parent

CV_QUERY = """[out:json][timeout:90];
(
  way["waterway"="canal"](35.6,-120.2,36.6,-119.0);
  way["highway"~"^(motorway|trunk)$"](35.6,-120.2,36.6,-119.0);
  way["railway"="rail"](35.6,-120.2,36.6,-119.0);
);
out body geom;"""

KARAPINAR_QUERY = """[out:json][timeout:90];
(
  way["waterway"~"^(canal|drain|ditch)$"](37.6,33.3,37.9,33.8);
  way["highway"~"^(motorway|trunk|primary|secondary)$"](37.6,33.3,37.9,33.8);
  way["railway"="rail"](37.6,33.3,37.9,33.8);
);
out body geom;"""


def query_overpass(ql: str, timeout: int = 120) -> dict:
    payload = urllib.parse.urlencode({"data": ql}).encode("utf-8")
    last_err: Exception | None = None
    for endpoint in OVERPASS_ENDPOINTS:
        for attempt in range(2):
            try:
                print(f"Querying {endpoint} (attempt {attempt + 1}) ...")
                req = urllib.request.Request(
                    endpoint,
                    data=payload,
                    headers={"User-Agent": "aseltech-nisar-pulse/1.0 (NASA Space Apps 2026)"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                if "elements" in data:
                    return data
                last_err = RuntimeError(f"Unexpected response from {endpoint}: keys={list(data.keys())}")
            except Exception as exc:
                last_err = exc
                print(f"  Error on {endpoint}: {exc}")
                time.sleep(2)
    raise RuntimeError(f"All Overpass endpoints failed: {last_err}")


def classify_type(tags: dict[str, str]) -> str:
    if "waterway" in tags:
        ww = tags["waterway"]
        return "canal" if ww == "canal" else ww
    if "highway" in tags:
        hw = tags["highway"]
        if hw in ("motorway", "trunk", "primary", "secondary"):
            return hw
        return "highway"
    if tags.get("railway") == "rail":
        return "rail"
    return "other"


def ways_to_geojson(data: dict) -> dict:
    features = []
    seen_ids: set[int] = set()
    for elem in data.get("elements", []):
        if elem.get("type") != "way":
            continue
        osm_id = int(elem["id"])
        if osm_id in seen_ids:
            continue
        geom = elem.get("geometry") or []
        if len(geom) < 2:
            continue
        seen_ids.add(osm_id)
        coords = [[round(float(pt["lon"]), 5), round(float(pt["lat"]), 5)] for pt in geom]
        tags = elem.get("tags") or {}
        name = (tags.get("name") or tags.get("ref") or "").strip()
        infra_type = classify_type(tags)
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": coords},
                "properties": {
                    "name": name,
                    "type": infra_type,
                    "osm_id": osm_id,
                },
            }
        )
    return {
        "type": "FeatureCollection",
        "license": "© OpenStreetMap contributors, ODbL",
        "features": features,
    }


def summarize_geojson(path: Path, gj: dict) -> None:
    feats = gj["features"]
    counts = Counter(f["properties"]["type"] for f in feats)
    named_canals = sorted(
        {
            f["properties"]["name"]
            for f in feats
            if f["properties"]["type"] in ("canal", "drain", "ditch") and f["properties"]["name"]
        }
    )
    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"Saved {path.name}: {len(feats)} features, {size_mb:.3f} MB")
    print(f"  Counts by type: {dict(counts)}")
    print(f"  Named waterways ({len(named_canals)}): {named_canals[:15]}")


def main() -> None:
    cv_raw = query_overpass(CV_QUERY)
    cv_gj = ways_to_geojson(cv_raw)
    cv_path = ROOT_DIR / "central_valley_infra.geojson"
    cv_path.write_text(json.dumps(cv_gj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summarize_geojson(cv_path, cv_gj)

    kp_raw = query_overpass(KARAPINAR_QUERY)
    kp_gj = ways_to_geojson(kp_raw)
    kp_path = ROOT_DIR / "karapinar_infra.geojson"
    kp_path.write_text(json.dumps(kp_gj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summarize_geojson(kp_path, kp_gj)


if __name__ == "__main__":
    main()
