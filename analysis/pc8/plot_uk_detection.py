"""Generate docs/story/media/pc8_uk_detection.png from PC3's data/uk_clay/detection.json
and analysis/out/uk_clay_pair_stats.json (PC8, Task 1 — 15:35).

Does NOT write to data/uk_clay/ or analysis/out/.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    det = json.loads((ROOT / "data" / "uk_clay" / "detection.json").read_text(encoding="utf-8"))
    pstats = json.loads((ROOT / "analysis" / "out" / "uk_clay_pair_stats.json").read_text(encoding="utf-8"))

    pairs = pstats["pairs"]
    pair_labels = [f"{p['pair'][0][5:]}\n→{p['pair'][1][5:]}" for p in pairs]
    p2 = np.array([p["p2_p50_p98_cm"][0] for p in pairs], dtype=float)
    p50 = np.array([p["p2_p50_p98_cm"][1] for p in pairs], dtype=float)
    p98 = np.array([p["p2_p50_p98_cm"][2] for p in pairs], dtype=float)
    block_std = np.array(det["per_pair_block_std_cm"], dtype=float)

    chain_sigma = float(det["chain_sigma_cm"])         # 1.21 cm
    det_thr = float(det["detection_threshold_cm"])     # 3.62 cm
    frac_1p5 = float(det["fraction_blocks_within_1p5cm"]) * 100.0  # 97.7%
    q_p2, q_p50, q_p98 = det["after_quadratic_block_p2_p50_p98_cm"]  # [-1.47, 0.19, 1.26]

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.titlesize": 10.5,
        "axes.labelsize": 9.5,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.8), dpi=160, gridspec_kw={"width_ratios": [1.12, 1.0]})
    fig.patch.set_facecolor("#ffffff")

    # --- Panel A: Per-pair atmospheric scatter (p2-p98 & block std) across 9 pairs ---
    x = np.arange(len(pairs))
    ax1.set_facecolor("#fafafa")
    ax1.axhspan(-chain_sigma, chain_sigma, color="#cbd5e1", alpha=0.45,
                label=f"Chain 1σ noise band (±{chain_sigma:.2f} cm)")
    ax1.axhline(0.0, color="#475569", lw=0.9, ls="--")

    # p2 to p98 vertical range bars per pair
    ax1.vlines(x, p2, p98, color="#64748b", lw=2.2, alpha=0.8, label="Per-pair scene spread (p2 to p98)")
    # ±1 block std around p50
    ax1.errorbar(
        x, p50, yerr=block_std, fmt="o", color="#1e3a8a", ecolor="#1d4ed8",
        elinewidth=4.0, capsize=3, markersize=5.5,
        label="Per-pair median ± 1 km block std (0.31–0.47 cm)"
    )

    ax1.set_xticks(x)
    ax1.set_xticklabels(pair_labels, fontsize=8)
    ax1.set_ylim(-3.9, 3.9)
    ax1.set_ylabel("Line-of-sight (LOS) displacement per pair (cm)")
    ax1.set_title("A. Per-pair atmospheric scatter over London (21 Jun–19 Oct 2026)", fontweight="bold", loc="left")
    ax1.grid(True, axis="y", linestyle=":", alpha=0.6)
    ax1.legend(loc="upper right", fontsize=8, frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0")

    # --- Panel B: Signal amplitude vs single-season noise & multi-year stacking ---
    ax2.set_facecolor("#fafafa")
    three_yr_rate = det_thr / 3.0
    categories = [
        "London Clay\nseasonal shrink-swell\n(expected: 0.5–2.0 cm)",
        "Holme Fen peat\nongoing loss\n(1.0–2.0 cm/yr)",
        "London 1 km blocks\n98% observed spread\n(|disp| ≤ 1.5 cm)",
        "1-season chain σ\n(9 pairs, 120 d:\n1.21 cm)",
        "1-season 3σ\ndetection limit\n(3.62 cm)",
        f"3-year NISAR\n3σ rate limit\n({three_yr_rate:.2f} cm/yr est.)",
    ]
    y_pos = np.arange(len(categories))
    lows = np.array([0.5, 1.0, 0.0, 0.0, 0.0, 0.0])
    highs = np.array([2.0, 2.0, 1.50, chain_sigma, det_thr, three_yr_rate])
    colors = ["#0284c7", "#0d9488", "#64748b", "#f59e0b", "#dc2626", "#16a34a"]

    for i in range(len(categories)):
        ax2.barh(
            y_pos[i], highs[i] - lows[i], left=lows[i], height=0.52,
            color=colors[i], alpha=0.88, edgecolor="#1e293b", linewidth=0.7
        )
        val_txt = (
            f"{lows[i]:.1f}–{highs[i]:.1f} cm"
            if lows[i] > 0
            else f"{highs[i]:.2f} cm" + ("/yr (est.)" if i == 5 else "")
        )
        ax2.text(highs[i] + 0.08, y_pos[i], val_txt, va="center", ha="left", fontsize=8.5, fontweight="bold", color="#0f172a")

    ax2.axvline(det_thr, color="#dc2626", lw=1.3, ls="--", label=f"1-season 3σ threshold ({det_thr:.2f} cm)")
    ax2.axvline(three_yr_rate, color="#16a34a", lw=1.3, ls=":", label=f"3-year stacked 3σ limit ({three_yr_rate:.2f} cm/yr est.)")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(categories, fontsize=8.2)
    ax2.invert_yaxis()
    ax2.set_xlim(0, 6.8)
    ax2.set_xlabel("Displacement / detection threshold magnitude (cm or cm/yr)")
    ax2.set_title("B. UK ground motion vs. detection limits", fontweight="bold", loc="left")
    ax2.grid(True, axis="x", linestyle=":", alpha=0.6)
    ax2.legend(loc="center right", fontsize=7.5, frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0")

    fig.suptitle(
        "Greater London (Track 101, 9 Provisional GUNW Pairs): Why 1-Season Clay Motion Is Below Detection (3σ = 3.6 cm)",
        fontsize=11.0, fontweight="bold", y=0.98
    )
    fig.text(
        0.5, 0.012,
        f"Data: NASA-ISRO NISAR L2 GUNW (provisional CRID P05023, 21 Jun–19 Oct 2026) via ASF DAAC; Holme Fen rate from UKCEH/Defra WP2.\n"
        f"97.7% of 1 km London blocks lie within ±1.5 cm (p2={q_p2:.2f} cm, p50=+{q_p50:.2f} cm, p98=+{q_p98:.2f} cm; n_detected=0). Analysis: Team Taykut.",
        fontsize=7.6, color="#334155", ha="center"
    )
    plt.tight_layout(rect=[0.0, 0.055, 1.0, 0.94])

    out_path = ROOT / "docs" / "story" / "media" / "pc8_uk_detection.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    print(f"Saved {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
