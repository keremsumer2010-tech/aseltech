"""Run the Aquifer Run system and engine checks when Node.js is available."""

import shutil
import subprocess
from pathlib import Path

import pytest


NODE = shutil.which("node")
ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(NODE is None, reason="Node.js is not installed")
def test_run_systems():
    subprocess.run([NODE, "web/run/test_systems.js"], cwd=ROOT, check=True)


@pytest.mark.skipif(NODE is None, reason="Node.js is not installed")
def test_run_engine():
    subprocess.run([NODE, "web/run/test_engine.js"], cwd=ROOT, check=True)
