"""Kept for compatibility: the home-page summary has one producer, pipeline/pc10/build_home_summary.py
(called automatically by build_atlas.py). This wrapper just runs it.
Usage: python tools/build_home_summary.py
"""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent.parent / "pipeline" / "pc10" / "build_home_summary.py"), run_name="__main__")
