"""Plot Semarang before and after unwrapping error fix.

Outputs:
- docs/story/media/pc10_semarang_qc.png

Compares:
- Pre-fix time series with cycle slip (-11.18 cm step -> -12.05 cm total) on 2026-10-11
- Clean 7-pair series ending at -6.20 cm on 2026-09-29
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

ROOT = Path(__file__).resolve().parents[2]

BEFORE_PATH = ROOT / "data" / "global" / "semarang" / "qc_before.json"
AFTER_PATH = ROOT / "data" / "global" / "semarang" / "points.json"
OUT_PATH = ROOT / "docs" / "story" / "media" / "pc10_semarang_qc.png"


def main() -> None:
    before = json.loads(BEFORE_PATH.read_text(encoding="utf-8"))
    pts = json.loads(AFTER_PATH.read_text(encoding="utf-8"))
    after = pts[0]

    b_dates = before["dates"]
    b_disp = before["disp_cm"]

    a_dates = after["dates"]
    a_disp = after["disp_cm"]

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#fafbfc")

    # Plot before (dashed blue with orange/red highlight on jump)
    ax.plot(
        range(len(b_dates)),
        b_disp,
        label="Before QC: contaminated by phase cycle slip (−12.1 cm)",
        color="#2b6cb0",
        linestyle="--",
        linewidth=2.0,
        marker="o",
        markersize=5,
        alpha=0.85,
    )

    # Plot after (solid red/crimson)
    ax.plot(
        range(len(a_dates)),
        a_disp,
        label="After QC: verified subsidence series (−6.2 cm)",
        color="#c53030",
        linestyle="-",
        linewidth=2.4,
        marker="s",
        markersize=6,
    )

    # Highlight the cycle slip jump on before series
    # From index 7 (2026-09-29: -0.87) to index 8 (2026-10-11: -12.05)
    ax.annotate(
        "Phase cycle jump\n(Δ ≈ 11.2 cm, ~1 L-band cycle)",
        xy=(8, -12.05),
        xytext=(5.3, -13.5),
        arrowprops=dict(facecolor="#d69e2e", edgecolor="#b7791f", width=1.5, headwidth=7, shrink=0.08),
        fontsize=9,
        fontweight="bold",
        color="#975a16",
        bbox=dict(boxstyle="round,pad=0.3", fc="#fefcbf", ec="#d69e2e", alpha=0.9),
    )

    # Highlight genuine after trend
    ax.annotate(
        "Physically consistent\ncoastal subsidence (−6.2 cm)",
        xy=(7, -6.20),
        xytext=(4.2, -4.5),
        arrowprops=dict(facecolor="#c53030", edgecolor="#9b2c2c", width=1.5, headwidth=7, shrink=0.08),
        fontsize=9,
        fontweight="bold",
        color="#742a2a",
        bbox=dict(boxstyle="round,pad=0.3", fc="#fed7d7", ec="#feb2b2", alpha=0.9),
    )

    ax.set_xticks(range(len(b_dates)))
    ax.set_xticklabels(b_dates, rotation=35, ha="right", fontsize=8.5)
    ax.set_ylabel("Cumulative LOS Displacement (cm)", fontsize=10, fontweight="bold")
    ax.set_title("Semarang Quality Control: Phase Unwrap Cycle Jump Removal", fontsize=12, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e0")
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.set_ylim(-15, 2)

    ax.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e0", fontsize=9)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"Saved Semarang QC figure: {OUT_PATH}")


if __name__ == "__main__":
    main()
