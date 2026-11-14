"""Sunday one-command run (Q08): full-year chain (beta-precal + provisional) -> cumulative -> decomposition.

Rules: beta and provisional never share a provisional product (K-3). This run is labelled `mixed` and writes ONLY
to separate places:
  data/<site>_fullyear/{meta,points,summary}.json, disp/*.png, decomp.json, decomp_permanent.png, decomp_seasonal.png
  analysis/out/<site>_fullyear_cum.npz, <site>_fullyear_cum_stack.npz, <site>_fullyear_pair_stats.json
Inputs: pipeline/subset/<site>/ (provisional) + pipeline/subset/<site>_beta/ (PC2, Q07); analysis/out/subset/...
backups are used where PC2's file lacks the ionosphere screen.
Usage: python analysis/run_fullyear.py central_valley [--ref-radius 3]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(site="central_valley", *extra):
    py = sys.executable
    subprocess.run([py, str(ROOT / "analysis" / "cumulative.py"), site, "--mixed", *extra], check=True)
    stack = ROOT / "analysis" / "out" / f"{site}_fullyear_cum_stack.npz"
    subprocess.run([py, str(ROOT / "analysis" / "decomp" / "run_decomp.py"), site, "--stack", str(stack),
                    "--out", str(ROOT / "data" / f"{site}_fullyear"), "--quality", "mixed"], check=True)


if __name__ == "__main__":
    main(*(sys.argv[1:] or ["central_valley"]))
