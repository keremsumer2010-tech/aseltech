"""Backup fetcher (PC3): find provisional GUNW pairs for a site/path/frame, download one at a time
to raw/ (git-ignored), cut to the site bbox into analysis/out/subset/<site>/<t1>_<t2>.npz, delete the raw file.
PC2's pipeline/subset/<site>/ npz files take precedence when present (cumulative.py prefers them).

Credentials: ~/.netrc or ~/_netrc written by the human (never read or printed here).
Usage: python analysis/fetch_subset.py central_valley 34 020
"""
import subprocess
import sys
import time
from pathlib import Path

import asf_search as asf
import numpy as np
from shapely.geometry import box

sys.path.insert(0, str(Path(__file__).parent))
from gunw_io import BBOX, subset  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main(site, path, frame, ref_height_m=None):
    b = box(*BBOX[site])
    res = asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith=b.wkt,
                     start="2026-06-17", end="2026-12-31", maxResults=500)
    todo = {}
    for p in res:
        n = p.properties["fileID"]
        if p.properties.get("pathNumber") != int(path) or f"_{int(path):03d}_A_{frame}_" not in n and f"_{int(path):03d}_D_{frame}_" not in n:
            continue
        if "_P05023_" not in n:
            continue
        key = n.split("_SH_")[1][:8] + "_" + n.split("_SH_")[1][34:42]
        todo[key] = max(todo.get(key, ""), n)  # keep highest product counter (J_00x)
    out_dir = ROOT / "analysis" / "out" / "subset" / site
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = ROOT / "raw"
    raw.mkdir(exist_ok=True)
    netrc = Path.home() / ("_netrc" if (Path.home() / "_netrc").exists() else ".netrc")
    for key in sorted(todo):
        n = todo[key]
        t1, t2 = key.split("_")
        dst = out_dir / f"{t1[:4]}-{t1[4:6]}-{t1[6:]}_{t2[:4]}-{t2[4:6]}-{t2[6:]}.npz"
        if dst.exists():
            print("skip", dst.name, flush=True)
            continue
        url = f"https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GUNW_PROVISIONAL_V1/{n}/{n}.h5"
        h5 = raw / f"{n}.h5"
        t0 = time.time()
        rc = subprocess.run(["curl", "-sS", "-L", "--fail", "--netrc-file", str(netrc), "-c", str(raw / "cj.txt"),
                             "-b", str(raw / "cj.txt"), "-o", str(h5), url]).returncode
        if rc != 0:
            print("DOWNLOAD FAILED", n, rc, flush=True)
            h5.unlink(missing_ok=True)
            continue
        mb = h5.stat().st_size / 1e6
        o = subset(h5, site, ref_height_m=ref_height_m)
        np.savez_compressed(dst, **o)
        h5.unlink()
        print(f"{dst.name} {o['unw'].shape} q={o['quality']} lam={o['wavelength']:.5f} "
              f"{mb:.0f}MB in {time.time()-t0:.0f}s -> {dst.stat().st_size/1e6:.1f}MB", flush=True)
    (raw / "cj.txt").unlink(missing_ok=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else None)
