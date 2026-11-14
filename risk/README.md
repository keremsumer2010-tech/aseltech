# Infrastructure Lines (OpenStreetMap)

Linear infrastructure layers for differential subsidence risk analysis along canals, highways, and railways.

- **License:** © OpenStreetMap contributors, ODbL (`https://www.openstreetmap.org/copyright`)
- **Source API:** OpenStreetMap Overpass API (`https://overpass-api.de/api/interpreter`)
- **Query date:** `2026-11-14`
- **Owner:** PC6 (`risk/fetch_osm_infra.py`)

---

## 1. Central Valley (`risk/central_valley_infra.geojson`)

- **Bounding box (`[w, s, e, n]`):** `[-120.2, 35.6, -119.0, 36.6]`
- **File size:** `1.066 MB` (< 20 MB limit)
- **Feature properties:** `name`, `type`, `osm_id` (LineString geometries, coordinates rounded to 5 decimal places)
- **Total features:** `3,238`
  - `canal`: `1,662` (69 distinct named waterways, including **California Aqueduct**, **California Aqueduct Coastal Branch - Phase 1/2**, and **Friant-Kern Canal**; note: Delta-Mendota Canal terminates north of `36.6°N`, outside the project bbox)
  - `rail`: `656`
  - `motorway`: `591`
  - `trunk`: `329`

### Overpass QL Query

```overpass
[out:json][timeout:90];
(
  way["waterway"="canal"](35.6,-120.2,36.6,-119.0);
  way["highway"~"^(motorway|trunk)$"](35.6,-120.2,36.6,-119.0);
  way["railway"="rail"](35.6,-120.2,36.6,-119.0);
);
out body geom;
```

---

## 2. Karapınar (`risk/karapinar_infra.geojson`)

- **Bounding box (`[w, s, e, n]`):** `[33.3, 37.6, 33.8, 37.9]`
- **File size:** `0.040 MB`
- **Total features:** `64`
  - `secondary`: `45` (including `Karapınar Caddesi`, `Konya Caddesi`, `İnönü Caddesi`, `42-11`, `42-27`, `42-28`, `42-42`)
  - `trunk`: `19` (including `Adana - Konya Yolu`, `Konya - Adana Yolu`, `42-28`)
  - `waterway` / `rail`: `0` mapped inside this closed-basin bounding box in OSM

### Overpass QL Query

```overpass
[out:json][timeout:90];
(
  way["waterway"~"^(canal|drain|ditch)$"](37.6,33.3,37.9,33.8);
  way["highway"~"^(motorway|trunk|primary|secondary)$"](37.6,33.3,37.9,33.8);
  way["railway"="rail"](37.6,33.3,37.9,33.8);
);
out body geom;
```
