"""Download ONE provisional GUNW of a track/frame, extract LOS geometry on the site grid, delete the raw file.

Output: analysis/out/<site>_geometry.npz  (x, y, epsg, los_e, los_n, los_u, incidence)
LOS unit vector points from the ground to the sensor (GUNW spec D-102272, metadata/radarGrid/losUnitVectorX/Y).
Geometry changes negligibly between repeat passes of the same track/frame, so one granule is enough.
Usage: python analysis/fetch_geometry.py central_valley 34 020 100
"""
import subprocess
import sys
from pathlib import Path

import asf_search as asf
import numpy as np
from shapely.geometry import box

sys.path.insert(0, str(Path(__file__).parent))
from gunw_io import BBOX, dates_from_name, los_only, quality_for  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main(site, path, frame, ref_height_m=None):
    res = asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith=box(*BBOX[site]).wkt,
                     start="2026-06-17", end="2026-12-31", maxResults=500)
    names = sorted(p.properties["fileID"] for p in res
                   if p.properties.get("pathNumber") == int(path) and f"_{frame}_" in p.properties["fileID"][24:36]
                   and "_P05023_" in p.properties["fileID"]
                   and quality_for(*dates_from_name(p.properties["fileID"]), "P05023") == "provisional")
    if not names:
        raise SystemExit("no granule found")
    n = names[0]
    raw = ROOT / "raw"
    raw.mkdir(exist_ok=True)
    h5 = raw / f"{n}.h5"
    netrc = Path.home() / ("_netrc" if (Path.home() / "_netrc").exists() else ".netrc")
    url = f"https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GUNW_PROVISIONAL_V1/{n}/{n}.h5"
    rc = subprocess.run(["curl", "-sS", "-L", "--fail", "--netrc-file", str(netrc), "-c", str(raw / "cj.txt"),
                         "-b", str(raw / "cj.txt"), "-o", str(h5), url]).returncode
    (raw / "cj.txt").unlink(missing_ok=True)
    if rc:
        h5.unlink(missing_ok=True)
        raise SystemExit(f"download failed rc={rc}")
    try:
        g = los_only(h5, site, ref_height_m)
    finally:
        h5.unlink(missing_ok=True)
    dst = ROOT / "analysis" / "out" / f"{site}_geometry.npz"
    # float16 keeps the file far below the 20 MB repo limit (K-12); unit vectors need ~3 decimals only
    g = {k: (v.astype(np.float16) if k in ("los_e", "los_n", "los_u", "incidence") else v) for k, v in g.items()}
    np.savez_compressed(dst, granule=n, **g)
    print(dst.name, n, "los_e", np.nanmedian(g["los_e"]), "los_n", np.nanmedian(g["los_n"]),
          "los_u", np.nanmedian(g["los_u"]), "inc", np.nanmedian(g["incidence"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else None)
