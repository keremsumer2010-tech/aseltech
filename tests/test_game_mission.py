"""Simulator mission balance (PC1): over-pumping must fail, a balanced plan must reach A/B.
Runs game/test_mission.js with Node; skipped when Node is not installed."""
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_mission_balance():
    r = subprocess.run(["node", str(ROOT / "game" / "test_mission.js")], capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
