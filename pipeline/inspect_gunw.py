"""Inspect a NISAR L2 GUNW HDF5 file and generate docs/gunw_structure.md."""

from __future__ import annotations

import argparse
from pathlib import Path

import h5py
import numpy as np

C_LIGHT_M_S = 299792458.0


def _decode_val(val) -> str:
    if isinstance(val, (bytes, np.bytes_)):
        return val.decode("utf-8", errors="replace")
    if isinstance(val, np.ndarray):
        if val.ndim == 0:
            return _decode_val(val.item())
        return f"array(shape={val.shape}, dtype={val.dtype})"
    return str(val)


def _ds_info(ds: h5py.Dataset) -> dict:
    units = _decode_val(ds.attrs["units"]) if "units" in ds.attrs else "-"
    fill = _decode_val(ds.attrs["_FillValue"]) if "_FillValue" in ds.attrs else "-"
    desc = _decode_val(ds.attrs["description"]) if "description" in ds.attrs else ""
    return {
        "shape": ds.shape,
        "dtype": str(ds.dtype),
        "units": units,
        "fill": fill,
        "desc": desc,
    }


def inspect_to_markdown(h5_path: Path) -> str:
    lines: list[str] = []
    with h5py.File(h5_path, "r") as h5:
        ident = h5["/science/LSAR/identification"]
        ident_keys = [
            "compositeReleaseId",
            "productVersion",
            "productSpecificationVersion",
            "processingType",
            "processingDateTime",
            "trackNumber",
            "frameNumber",
            "orbitPassDirection",
            "lookDirection",
            "referenceAbsoluteOrbitNumber",
            "secondaryAbsoluteOrbitNumber",
            "referenceZeroDopplerStartTime",
            "referenceZeroDopplerEndTime",
            "secondaryZeroDopplerStartTime",
            "secondaryZeroDopplerEndTime",
            "listOfFrequencies",
            "isGeocoded",
            "isFullFrame",
            "isUrgentObservation",
            "productDoi",
            "boundingPolygon",
        ]
        ident_vals: dict[str, str] = {}
        for k in ident_keys:
            if k in ident:
                ident_vals[k] = _decode_val(ident[k][()])

        freq_a = h5["/science/LSAR/GUNW/grids/frequencyA"]
        center_freq = float(freq_a["centerFrequency"][()])
        wavelength = C_LIGHT_M_S / center_freq

        hh = freq_a["unwrappedInterferogram/HH"]
        proj_ds = hh["projection"]
        epsg = proj_ds.attrs.get("epsg_code", proj_ds[()])
        x_coords = hh["xCoordinates"][:]
        y_coords = hh["yCoordinates"][:]
        x_sp = float(hh["xCoordinateSpacing"][()])
        y_sp = float(hh["yCoordinateSpacing"][()])

        unw_ds = hh["unwrappedPhase"]
        coh_ds = hh["coherenceMagnitude"]
        conn_ds = hh["connectedComponents"]
        iono_ds = hh["ionospherePhaseScreen"]
        iono_unc_ds = hh["ionospherePhaseScreenUncertainty"]

        unw_sample = unw_ds[::8, ::8]
        coh_sample = coh_ds[::8, ::8]
        unw_min = float(np.nanmin(unw_sample))
        unw_max = float(np.nanmax(unw_sample))
        coh_mean = float(np.nanmean(coh_sample))

        rg = h5["/science/LSAR/GUNW/metadata/radarGrid"]
        height_key = "heightAboveEllipsoid" if "heightAboveEllipsoid" in rg else "heights"
        rg_heights = rg[height_key][:]
        rg_x = rg["xCoordinates"][:]
        rg_y = rg["yCoordinates"][:]
        rg_epsg = _decode_val(rg["projection"].attrs.get("epsg_code", rg["projection"][()])) if "projection" in rg else str(epsg)

        pi = h5["/science/LSAR/GUNW/metadata/processingInformation/parameters"]

        lines.append("# NISAR L2 GUNW HDF5 Structure (`docs/gunw_structure.md`)")
        lines.append("")
        lines.append(f"Inspected granule: `{h5_path.name}`")
        lines.append("")
        lines.append("## 1. Identification & Quality / Version Attributes (`/science/LSAR/identification/`)")
        lines.append("")
        lines.append("| Attribute / Dataset | Value |")
        lines.append("|---|---|")
        for k, v in ident_vals.items():
            v_clean = v.replace("\n", " ")
            if len(v_clean) > 120:
                v_clean = v_clean[:117] + "..."
            lines.append(f"| `{k}` | `{v_clean}` |")
        lines.append("")

        lines.append("## 2. Processing & Calibration Flags (`/science/LSAR/GUNW/metadata/processingInformation/parameters/`)")
        lines.append("")
        lines.append("| Parameter Path | Value |")
        lines.append("|---|---|")
        param_paths = [
            "geocoding/azimuthIonosphericCorrectionApplied",
            "geocoding/rangeIonosphericCorrectionApplied",
            "geocoding/hydrostaticTroposphericCorrectionApplied",
            "geocoding/wetTroposphericCorrectionApplied",
            "unwrappedInterferogram/frequencyA/ellipsoidalFlatteningApplied",
            "unwrappedInterferogram/frequencyA/topographicFlatteningApplied",
            "unwrappedInterferogram/frequencyA/numberOfAzimuthLooks",
            "unwrappedInterferogram/frequencyA/numberOfRangeLooks",
            "reference/rfiMitigationApplied",
            "secondary/rfiMitigationApplied",
        ]
        for pp in param_paths:
            if pp in pi:
                lines.append(f"| `{pp}` | `{_decode_val(pi[pp][()])}` |")
        lines.append("")

        lines.append("## 3. Frequency & Wavelength (`/science/LSAR/GUNW/grids/frequencyA/`)")
        lines.append("")
        lines.append(f"- `centerFrequency`: `{center_freq:.1f} Hz` ({center_freq / 1e6:.3f} MHz)")
        lines.append(f"- **Computed wavelength**: `lambda = 299792458.0 / centerFrequency = {wavelength:.8f} m`")
        lines.append("- **Rule (`VERI_SOZLESMESI.md` §2):** Never hardcode `0.2384 m`; always read `centerFrequency` per file.")
        if "listOfPolarizations" in freq_a:
            pols = [p.decode("utf-8") if isinstance(p, (bytes, np.bytes_)) else str(p) for p in freq_a["listOfPolarizations"][:]]
            lines.append(f"- `listOfPolarizations`: `{pols}`")
        lines.append("")

        lines.append("## 4. Unwrapped Interferogram Grids (`/science/LSAR/GUNW/grids/frequencyA/unwrappedInterferogram/HH/`)")
        lines.append("")
        lines.append("| Dataset | Path (under `frequencyA/unwrappedInterferogram/HH/`) | Shape | Dtype | Units | `_FillValue` | Notes |")
        lines.append("|---|---|---|---|---|---|---|")
        grid_items = [
            ("unwrappedPhase", unw_ds, f"8x sample range: [{unw_min:.2f}, {unw_max:.2f}] rad (attrs min={unw_ds.attrs.get('min_value', 'N/A'):.2f}, max={unw_ds.attrs.get('max_value', 'N/A'):.2f})"),
            ("coherenceMagnitude", coh_ds, f"8x sample mean: {coh_mean:.3f} (attrs mean={coh_ds.attrs.get('mean_value', 'N/A'):.3f})"),
            ("connectedComponents", conn_ds, "0 = disconnected/unreliable, 65535 = fill (mask to NaN)"),
            ("ionospherePhaseScreen", iono_ds, f"attrs min={iono_ds.attrs.get('min_value', 'N/A'):.2f}, max={iono_ds.attrs.get('max_value', 'N/A'):.2f}"),
            ("ionospherePhaseScreenUncertainty", iono_unc_ds, "Uncertainty of ionospheric screen"),
            ("xCoordinates", hh["xCoordinates"], f"UTM Easting ascending: {x_coords[0]:.1f} -> {x_coords[-1]:.1f} m"),
            ("yCoordinates", hh["yCoordinates"], f"UTM Northing descending: {y_coords[0]:.1f} -> {y_coords[-1]:.1f} m"),
        ]
        for name, ds, note in grid_items:
            info = _ds_info(ds)
            lines.append(
                f"| `{name}` | `{name}` | `{info['shape']}` | `{info['dtype']}` | `{info['units']}` | `{info['fill']}` | {note} |"
            )

        mask_ds = freq_a["unwrappedInterferogram/mask"]
        minfo = _ds_info(mask_ds)
        lines.append(
            f"| `mask` | `../mask` | `{minfo['shape']}` | `{minfo['dtype']}` | `{minfo['units']}` | `{minfo['fill']}` | Water/subswath valid bitmask |"
        )
        lines.append("")
        lines.append(f"- **Projection (`projection`):** EPSG `{_decode_val(epsg)}` (UTM Zone 11N, WGS84)")
        lines.append(f"- **Grid spacing:** `xCoordinateSpacing = {x_sp} m`, `yCoordinateSpacing = {y_sp} m`")
        lines.append("")

        lines.append("## 5. Radar Geometry & Atmospheric Metadata Cubes (`/science/LSAR/GUNW/metadata/radarGrid/`)")
        lines.append("")
        lines.append(
            f"- Cube coordinates: `{height_key}` shape `{rg_heights.shape}` (`{float(rg_heights[0]):.0f} m` to `{float(rg_heights[-1]):.0f} m`, index `1` = `0 m`), "
            f"`yCoordinates` shape `{rg_y.shape}` (`{rg_y[0]:.0f} -> {rg_y[-1]:.0f}` descending), "
            f"`xCoordinates` shape `{rg_x.shape}` (`{rg_x[0]:.0f} -> {rg_x[-1]:.0f}` ascending), `epsg = {rg_epsg}`."
        )
        lines.append("- Use `heightAboveEllipsoid == 0 m` slice (index 1) and bilinearly interpolate onto the 80 m grid `(yCoordinates, xCoordinates)`.")
        lines.append("")
        lines.append("| Cube Dataset | Path | Shape | Dtype | Units | Description |")
        lines.append("|---|---|---|---|---|---|")
        for cname in [
            "incidenceAngle",
            "elevationAngle",
            "losUnitVectorX",
            "losUnitVectorY",
            "alongTrackUnitVectorX",
            "alongTrackUnitVectorY",
            "parallelBaseline",
            "perpendicularBaseline",
            "wetTroposphericPhaseScreen",
            "hydrostaticTroposphericPhaseScreen",
            "slantRangeSolidEarthTidesPhase",
        ]:
            if cname in rg:
                cinfo = _ds_info(rg[cname])
                desc = cinfo["desc"].replace("\n", " ")
                if len(desc) > 90:
                    desc = desc[:87] + "..."
                lines.append(
                    f"| `{cname}` | `/science/LSAR/GUNW/metadata/radarGrid/{cname}` | `{cinfo['shape']}` | `{cinfo['dtype']}` | `{cinfo['units']}` | {desc} |"
                )
        lines.append("")

        lines.append("## 6. Full HDF5 Group Tree (Summary)")
        lines.append("")
        lines.append("```text")
        def _walk(name: str, obj):
            depth = name.count("/")
            indent = "  " * depth
            leaf = name.split("/")[-1]
            if isinstance(obj, h5py.Group):
                lines.append(f"{indent}{leaf}/")
            elif isinstance(obj, h5py.Dataset):
                units = _decode_val(obj.attrs["units"]) if "units" in obj.attrs else ""
                u_str = f" [{units}]" if units else ""
                lines.append(f"{indent}{leaf}: {obj.shape} {obj.dtype}{u_str}")

        h5.visititems(_walk)
        lines.append("```")
        lines.append("")

        lines.append("## 7. PC2 Subset Output Contract (`pipeline/subset/<site>/<t1>_<t2>.npz`)")
        lines.append("")
        lines.append("Produced by `pipeline/subset.py` via `np.savez_compressed` (<= 20 MB per file):")
        lines.append("")
        lines.append("| Key | Shape | Dtype | Units / Encoding |")
        lines.append("|---|---|---|---|")
        lines.append("| `unw` | `(ny, nx)` | `float32` | `radians` (`NaN` where `connectedComponents == 0` or `65535` or invalid) |")
        lines.append("| `coh` | `(ny, nx)` | `uint8` | `0..255` linear map of `[0.0, 1.0]` (`coh_float = coh.astype(np.float32) / 255.0`) |")
        lines.append("| `x` | `(nx,)` | `float64` | UTM Easting (`m`, ascending) |")
        lines.append("| `y` | `(ny,)` | `float64` | UTM Northing (`m`, descending) |")
        lines.append("| `epsg` | `()` | `int32` | EPSG code (e.g. `32611` for Central Valley) |")
        lines.append("| `wavelength` | `()` | `float64` | `m` (`299792458.0 / centerFrequency`) |")
        lines.append("| `incidence` | `(ny, nx)` | `float32` | `degrees` (bilinearly interpolated from `metadata/radarGrid/incidenceAngle` at `heightAboveEllipsoid == 0 m`) |")
        lines.append("| `quality` | `()` | `str` | `\"provisional\"` or `\"beta-precal\"` |")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("h5_path", type=Path)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "docs" / "gunw_structure.md",
    )
    args = parser.parse_args()
    md = inspect_to_markdown(args.h5_path)
    args.out.write_text(md, encoding="utf-8")
    print(f"Wrote {args.out} ({len(md.splitlines())} lines)")


if __name__ == "__main__":
    main()
