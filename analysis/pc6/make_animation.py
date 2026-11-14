#!/usr/bin/env python3
"""Render 1080p MP4 and GIF subsidence animations purely from local NISAR PNGs and vectors."""

from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = REPO_ROOT / "data"
RISK_ROOT = REPO_ROOT / "risk"
MEDIA_ROOT = REPO_ROOT / "docs" / "story" / "media"

SITE_CONFIGS = {
    "central_valley": {
        "out_prefix": "cv_subsidence",
        "title": "San Joaquin Valley, CA — NISAR Cumulative LOS Subsidence",
        "subtitle": "NISAR L2 GUNW Track 34 Ascending · Frame 20 · Ref 2026-06-28",
        "infra_geojson": RISK_ROOT / "central_valley_infra.geojson",
        "highlight_ids": ["p01", "p02", "p03", "p04", "p06", "p11"],
        "palette": ["#ff5c57", "#ff8c42", "#fbbf24", "#f472b6", "#38bdf8", "#94a3b8"],
        "tick_step": 0.2,
        "extra_note": "OSM canals, rail, and highways",
    },
    "karapinar": {
        "out_prefix": "kp_subsidence",
        "title": "Karapinar Basin, Turkey — NISAR Cumulative LOS Subsidence",
        "subtitle": "NISAR L2 GUNW Track 7 Descending · Frame 69 · Ref 2026-06-26",
        "infra_geojson": RISK_ROOT / "karapinar_infra.geojson",
        "sinkholes_geojson": DATA_ROOT / "karapinar" / "sinkholes.geojson",
        "highlight_ids": ["p01", "p02", "p03", "p06", "p08"],
        "palette": ["#ff5c57", "#ff8c42", "#fbbf24", "#38bdf8", "#94a3b8"],
        "tick_step": 0.1,
        "extra_note": "OSM infrastructure · Sinkholes: Tapur & Bozyigit (2015)",
    },
}


def load_site_bundle(site: str) -> dict:
    site_dir = DATA_ROOT / site
    with (site_dir / "meta.json").open(encoding="utf-8") as fh:
        meta = json.load(fh)
    with (site_dir / "points.json").open(encoding="utf-8") as fh:
        points = json.load(fh)
    with (site_dir / "summary.json").open(encoding="utf-8") as fh:
        summary = json.load(fh)

    cfg = SITE_CONFIGS[site]
    infra_features = []
    if cfg["infra_geojson"].exists():
        with cfg["infra_geojson"].open(encoding="utf-8") as fh:
            infra_features = json.load(fh).get("features", [])

    sinkhole_coords: list[tuple[float, float]] = []
    sh_path = cfg.get("sinkholes_geojson")
    if sh_path and sh_path.exists():
        with sh_path.open(encoding="utf-8") as fh:
            for feat in json.load(fh).get("features", []):
                coords = feat.get("geometry", {}).get("coordinates")
                if coords and len(coords) >= 2:
                    sinkhole_coords.append((float(coords[0]), float(coords[1])))

    return {
        "site": site,
        "cfg": cfg,
        "meta": meta,
        "points": points,
        "summary": summary,
        "infra": infra_features,
        "sinkholes": sinkhole_coords,
        "disp_dir": site_dir / "disp",
    }


def _group_infra_lines(features: list[dict]) -> dict[str, list[np.ndarray]]:
    groups: dict[str, list[np.ndarray]] = {"water": [], "rail": [], "road": []}
    for feat in features:
        geom = feat.get("geometry", {})
        if geom.get("type") != "LineString":
            continue
        coords = np.asarray(geom.get("coordinates", []), dtype=float)
        if coords.ndim != 2 or len(coords) < 2:
            continue
        ftype = str(feat.get("properties", {}).get("type", "")).lower()
        if ftype in {"canal", "ditch", "drain", "river", "stream", "aqueduct"}:
            groups["water"].append(coords)
        elif "rail" in ftype:
            groups["rail"].append(coords)
        else:
            groups["road"].append(coords)
    return groups


def _format_lon_label(val: float, _pos=None) -> str:
    hemi = "E" if val >= 0 else "W"
    return f"{abs(val):.1f}\u00b0{hemi}"


def _format_lat_label(val: float, _pos=None) -> str:
    hemi = "N" if val >= 0 else "S"
    return f"{abs(val):.1f}\u00b0{hemi}"


def render_epoch_frame(
    bundle: dict,
    infra_groups: dict[str, list[np.ndarray]],
    epoch_idx: int,
    out_png: Path,
) -> None:
    meta = bundle["meta"]
    cfg = bundle["cfg"]
    points = bundle["points"]
    dates = meta["dates"]
    cur_date = dates[epoch_idx]
    disp_path = bundle["disp_dir"] / f"{cur_date}.png"
    with Image.open(disp_path) as im:
        disp_rgba = np.asarray(im.convert("RGBA"))

    w_min, s_min, e_max, n_max = [float(v) for v in meta["bbox"]]
    mean_lat = 0.5 * (s_min + n_max)
    vmin = float(meta.get("vmin", -6.0))
    vmax = float(meta.get("vmax", 6.0))

    d0 = datetime.strptime(dates[0], "%Y-%m-%d")
    d_cur = datetime.strptime(cur_date, "%Y-%m-%d")
    days_elapsed = (d_cur - d0).days

    pt_by_id = {p["id"]: p for p in points}
    selected_pts = [pt_by_id[pid] for pid in cfg["highlight_ids"] if pid in pt_by_id]
    p01 = selected_pts[0] if selected_pts else points[0]
    p01_val = float(p01["disp_cm"][epoch_idx])

    bg = "#080d14"
    panel_bg = "#0f1722"
    border_col = "#243247"
    text_main = "#f1f5f9"
    text_muted = "#94a3b8"

    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=bg)

    # Top-left title + subtitle (bounded safely left of right badges)
    fig.text(
        0.032,
        0.955,
        cfg["title"],
        color=text_main,
        fontsize=18.5,
        fontweight="bold",
        family="DejaVu Sans",
        va="top",
    )
    fig.text(
        0.032,
        0.916,
        cfg["subtitle"],
        color=text_muted,
        fontsize=10.5,
        family="DejaVu Sans",
        va="top",
    )

    # Top-right Provisional pill badge + Epoch counter pill cleanly separated above right chart
    fig.text(
        0.968,
        0.956,
        "NASA-ISRO NISAR \u00b7 PROVISIONAL",
        color="#fef3c7",
        fontsize=10,
        fontweight="bold",
        family="DejaVu Sans",
        ha="right",
        va="top",
        bbox=dict(
            boxstyle="round,pad=0.35",
            facecolor="#78350f",
            edgecolor="#f59e0b",
            linewidth=1.1,
        ),
    )
    fig.text(
        0.968,
        0.897,
        f"EPOCH {epoch_idx + 1}/{len(dates)}:  {cur_date}  (Day +{days_elapsed}  ·  Peak {p01['id'].upper()}: {p01_val:+.2f} cm)",
        color="#f8fafc",
        fontsize=11.0,
        fontweight="bold",
        family="DejaVu Sans Mono",
        ha="right",
        va="top",
        bbox=dict(
            boxstyle="round,pad=0.32",
            facecolor="#162235",
            edgecolor="#38bdf8",
            linewidth=0.95,
        ),
    )

    # Left axis: Map
    ax_map = fig.add_axes([0.046, 0.145, 0.488, 0.715], facecolor=panel_bg)
    ax_map.set_xlim(w_min, e_max)
    ax_map.set_ylim(s_min, n_max)
    ax_map.set_aspect(1.0 / math.cos(math.radians(mean_lat)))

    tick_step = float(cfg["tick_step"])
    ax_map.xaxis.set_major_locator(MultipleLocator(tick_step))
    ax_map.yaxis.set_major_locator(MultipleLocator(tick_step))
    ax_map.xaxis.set_major_formatter(plt.FuncFormatter(_format_lon_label))
    ax_map.yaxis.set_major_formatter(plt.FuncFormatter(_format_lat_label))
    ax_map.tick_params(colors=text_muted, labelsize=9)
    ax_map.grid(True, color="#1e293b", linestyle="--", linewidth=0.7, zorder=1)

    for arr in infra_groups["road"]:
        ax_map.plot(arr[:, 0], arr[:, 1], color="#64748b", linewidth=0.55, alpha=0.35, zorder=2)
    for arr in infra_groups["rail"]:
        ax_map.plot(arr[:, 0], arr[:, 1], color="#fbbf24", linewidth=0.75, alpha=0.40, zorder=3)
    for arr in infra_groups["water"]:
        ax_map.plot(arr[:, 0], arr[:, 1], color="#38bdf8", linewidth=0.85, alpha=0.45, zorder=4)

    ax_map.imshow(
        disp_rgba,
        extent=[w_min, e_max, s_min, n_max],
        origin="upper",
        interpolation="nearest",
        zorder=5,
    )

    if bundle["sinkholes"]:
        sh_arr = np.asarray(bundle["sinkholes"], dtype=float)
        ax_map.scatter(
            sh_arr[:, 0],
            sh_arr[:, 1],
            s=36,
            marker="D",
            facecolors="none",
            edgecolors="#f8fafc",
            linewidths=0.95,
            alpha=0.9,
            zorder=7,
        )

    ref_pt = meta.get("reference_point", {})
    if "lon" in ref_pt and "lat" in ref_pt:
        ax_map.scatter(
            [ref_pt["lon"]],
            [ref_pt["lat"]],
            s=115,
            marker="*",
            color="#f8fafc",
            edgecolors="#090d14",
            linewidths=0.8,
            zorder=8,
        )
        ax_map.text(
            ref_pt["lon"],
            ref_pt["lat"] + (n_max - s_min) * 0.018,
            "REF",
            color="#f8fafc",
            fontsize=8,
            fontweight="bold",
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.14", facecolor="#080d14", edgecolor="#475569", alpha=0.82),
            zorder=9,
        )

    for idx, pt in enumerate(selected_pts):
        col = cfg["palette"][idx % len(cfg["palette"])]
        ax_map.scatter(
            [pt["lon"]],
            [pt["lat"]],
            s=52,
            color=col,
            edgecolors="#080d14",
            linewidths=1.0,
            zorder=9,
        )
        offset_y = (n_max - s_min) * (0.018 if idx % 2 == 0 else -0.025)
        ax_map.text(
            pt["lon"],
            pt["lat"] + offset_y,
            pt["id"].upper(),
            color=col,
            fontsize=8,
            fontweight="bold",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round,pad=0.14", facecolor="#080d14", edgecolor=col, alpha=0.86, linewidth=0.7),
            zorder=10,
        )

    for spine in ax_map.spines.values():
        spine.set_color(border_col)
        spine.set_linewidth(1.1)

    legend_handles = [
        Line2D([0], [0], color="#38bdf8", lw=1.6, label="Canals / waterways"),
        Line2D([0], [0], color="#fbbf24", lw=1.4, label="Rail corridors"),
        Line2D([0], [0], color="#64748b", lw=1.2, label="Major roads"),
        Line2D([0], [0], marker="*", color="none", markerfacecolor="#f8fafc", markersize=9, label="Reference window"),
    ]
    if bundle["sinkholes"]:
        legend_handles.append(
            Line2D([0], [0], marker="D", color="none", markeredgecolor="#f8fafc", markersize=6, label="Sinkholes (29)")
        )
    leg = ax_map.legend(
        handles=legend_handles,
        loc="lower left",
        fontsize=8.2,
        frameon=True,
        facecolor="#080d14",
        edgecolor="#334155",
        labelcolor="#e2e8f0",
        ncol=2,
    )
    leg.set_zorder(11)

    # Colorbar separated clearly from right chart ylabel
    cax = fig.add_axes([0.550, 0.21, 0.014, 0.58])
    sm = ScalarMappable(norm=Normalize(vmin=vmin, vmax=vmax), cmap=plt.get_cmap("RdBu"))
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cax)
    cbar.set_label("LOS (cm)  [- subsidence]", color="#cbd5e1", fontsize=9.2, labelpad=7)
    cbar.ax.tick_params(colors=text_muted, labelsize=8.8)
    cbar.outline.set_edgecolor(border_col)

    # Right axis: Cumulative time-series progression (clear gap left of x=0.67)
    ax_ts = fig.add_axes([0.668, 0.295, 0.300, 0.505], facecolor=panel_bg)
    x_days = np.array([(datetime.strptime(d, "%Y-%m-%d") - d0).days for d in dates], dtype=float)

    ax_ts.axhline(0.0, color="#475569", linestyle="--", linewidth=0.9, zorder=1)
    ax_ts.axvline(days_elapsed, color="#f8fafc", linestyle=":", linewidth=1.1, alpha=0.65, zorder=2)

    all_vals = [v for p in selected_pts for v in p["disp_cm"]]
    y_min = min(-2.0, math.floor(min(all_vals) - 0.8))
    y_max = max(1.5, math.ceil(max(all_vals) + 0.8))

    for idx, pt in enumerate(selected_pts):
        col = cfg["palette"][idx % len(cfg["palette"])]
        vals = np.asarray(pt["disp_cm"], dtype=float)
        ax_ts.plot(x_days, vals, color=col, linewidth=0.9, alpha=0.18, zorder=3)
        ax_ts.plot(
            x_days[: epoch_idx + 1],
            vals[: epoch_idx + 1],
            color=col,
            linewidth=2.2,
            zorder=4,
            label=f"{pt['id'].upper()}: {pt['name'][:20]} ({vals[epoch_idx]:+.2f} cm)",
        )
        ax_ts.scatter(x_days[: epoch_idx + 1], vals[: epoch_idx + 1], s=18, color=col, alpha=0.8, zorder=5)
        ax_ts.scatter(
            [x_days[epoch_idx]],
            [vals[epoch_idx]],
            s=62,
            color=col,
            edgecolors="#f8fafc",
            linewidths=1.2,
            zorder=6,
        )

    ax_ts.set_xlim(-4, x_days[-1] + 5)
    ax_ts.set_ylim(y_min, y_max)
    ax_ts.set_title("Tracked Sample Points — Cumulative LOS (cm)", color=text_main, fontsize=11.0, fontweight="bold", pad=10)
    ax_ts.set_xlabel(f"Days since {dates[0]}", color=text_muted, fontsize=9.2)
    ax_ts.set_ylabel("LOS displacement (cm)", color=text_muted, fontsize=9.2)
    ax_ts.set_xticks(x_days)
    ax_ts.set_xticklabels([f"{int(dx)}d" for dx in x_days], fontsize=8.0)
    ax_ts.tick_params(colors=text_muted, labelsize=8.8)
    ax_ts.grid(True, color="#1e293b", linestyle="--", linewidth=0.65, zorder=0)
    for spine in ax_ts.spines.values():
        spine.set_color(border_col)
        spine.set_linewidth(1.1)

    ts_leg = ax_ts.legend(
        loc="lower left",
        fontsize=8.0,
        frameon=True,
        facecolor="#080d14",
        edgecolor="#334155",
        labelcolor="#e2e8f0",
    )
    ts_leg.set_zorder(10)

    # Bottom-right Epoch Timeline Strip
    ax_tl = fig.add_axes([0.668, 0.145, 0.300, 0.080], facecolor=panel_bg)
    ax_tl.set_xlim(-0.5, len(dates) - 0.5)
    ax_tl.set_ylim(0, 1)
    ax_tl.set_xticks([])
    ax_tl.set_yticks([])
    for spine in ax_tl.spines.values():
        spine.set_color(border_col)
        spine.set_linewidth(1.0)

    xs = np.arange(len(dates))
    ax_tl.plot([0, len(dates) - 1], [0.58, 0.58], color="#334155", linewidth=3.0, zorder=1)
    if epoch_idx > 0:
        ax_tl.plot([0, epoch_idx], [0.58, 0.58], color="#ff5c57", linewidth=3.5, zorder=2)
    for i, d_str in enumerate(dates):
        done = i <= epoch_idx
        active = i == epoch_idx
        c = "#ff5c57" if active else ("#f8fafc" if done else "#475569")
        sz = 88 if active else 38
        ax_tl.scatter([xs[i]], [0.58], s=sz, color=c, edgecolors="#080d14", linewidths=1.0, zorder=3)
        ax_tl.text(
            xs[i],
            0.22,
            d_str[5:],
            color="#f8fafc" if active else "#94a3b8",
            fontsize=7.3,
            fontweight="bold" if active else "normal",
            ha="center",
            va="center",
            family="DejaVu Sans Mono",
        )

    # Footer
    fig.text(
        0.032,
        0.048,
        f"Source: {meta.get('source', 'NASA-ISRO NISAR L2 GUNW')}  |  {cfg['extra_note']}",
        color="#cbd5e1",
        fontsize=8.8,
        family="DejaVu Sans",
    )
    fig.text(
        0.032,
        0.022,
        meta.get(
            "quality_note",
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.",
        ),
        color="#fbbf24",
        fontsize=8.8,
        fontweight="bold",
        family="DejaVu Sans",
    )

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=120, facecolor=bg)
    plt.close(fig)


def build_site_media(site: str) -> dict:
    bundle = load_site_bundle(site)
    infra_groups = _group_infra_lines(bundle["infra"])
    dates = bundle["meta"]["dates"]
    prefix = bundle["cfg"]["out_prefix"]

    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    mp4_path = MEDIA_ROOT / f"{prefix}.mp4"
    gif_path = MEDIA_ROOT / f"{prefix}.gif"

    with tempfile.TemporaryDirectory(prefix=f"nisar_anim_{site}_") as tmp:
        tmp_dir = Path(tmp)
        epoch_pngs: list[Path] = []
        for idx, d_str in enumerate(dates):
            ep_png = tmp_dir / f"epoch_{idx:02d}_{d_str}.png"
            render_epoch_frame(bundle, infra_groups, idx, ep_png)
            epoch_pngs.append(ep_png)

        pil_epochs = [Image.open(p).convert("RGB") for p in epoch_pngs]
        gif_frames = [im.quantize(colors=256, method=Image.Quantize.MEDIANCUT) for im in pil_epochs]
        durations = [900] * (len(gif_frames) - 1) + [2400]
        gif_frames[0].save(
            gif_path,
            save_all=True,
            append_images=gif_frames[1:],
            duration=durations,
            loop=0,
            optimize=True,
        )

        # Pipe raw RGB24 frames directly to ffmpeg stdin for fast 1080p encoding
        ffmpeg_bin = shutil.which("ffmpeg")
        if ffmpeg_bin:
            w, h = pil_epochs[0].size
            fps = 24
            hold_frames = 22
            fade_frames = 6
            final_hold = 54
            cmd = [
                ffmpeg_bin,
                "-y",
                "-f",
                "rawvideo",
                "-vcodec",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-s",
                f"{w}x{h}",
                "-r",
                str(fps),
                "-i",
                "pipe:0",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "20",
                "-movflags",
                "+faststart",
                str(mp4_path),
            ]
            stderr_path = tmp_dir / "ffmpeg_err.log"
            with stderr_path.open("wb") as err_fh:
                proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=err_fh)
                assert proc.stdin is not None
                for idx, img in enumerate(pil_epochs):
                    raw_bytes = img.tobytes()
                    cnt = final_hold if idx == len(pil_epochs) - 1 else hold_frames
                    for _ in range(cnt):
                        proc.stdin.write(raw_bytes)
                    if idx < len(pil_epochs) - 1:
                        nxt = pil_epochs[idx + 1]
                        for step in range(1, fade_frames + 1):
                            alpha = step / (fade_frames + 1)
                            proc.stdin.write(Image.blend(img, nxt, alpha).tobytes())
                proc.stdin.close()
                ret = proc.wait()
            if ret != 0:
                err = stderr_path.read_text(encoding="utf-8", errors="replace")
                raise RuntimeError(f"ffmpeg failed ({ret}): {err}")

        for im in pil_epochs:
            im.close()

    return {
        "site": site,
        "frames": len(dates),
        "gif": str(gif_path),
        "gif_mb": round(gif_path.stat().st_size / (1024 * 1024), 2),
        "mp4": str(mp4_path) if mp4_path.exists() else None,
        "mp4_mb": round(mp4_path.stat().st_size / (1024 * 1024), 2) if mp4_path.exists() else None,
    }


def main() -> int:
    for site in ("central_valley", "karapinar"):
        info = build_site_media(site)
        print(
            f"[OK] {site}: {info['frames']} epochs | "
            f"GIF={info['gif_mb']} MB | MP4={info['mp4_mb']} MB"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
