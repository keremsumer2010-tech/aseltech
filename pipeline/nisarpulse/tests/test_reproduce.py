"""Offline unit tests for `python -m pipeline.nisarpulse reproduce <id>`."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pipeline.nisarpulse.__main__ import parse_cli_args
from pipeline.nisarpulse.reproduce import (
    find_cached_subsets,
    find_region_dir,
    parse_granule_pair,
    reproduce_region,
)


class TestReproduce(unittest.TestCase):
    def test_parse_granule_pair(self) -> None:
        gran = "NISAR_L2_PR_GUNW_023_078_D_070_024_2000_SH_20260619T145232_20260619T145307_20260701T145231_20260701T145306_P05023_N_F_J_001"
        self.assertEqual(parse_granule_pair(gran), ("2026-06-19", "2026-07-01"))

    def test_reproduce_dry_run_on_synthetic_region(self) -> None:
        gran1 = "NISAR_L2_PR_GUNW_023_078_D_070_024_2000_SH_20260619T145232_20260619T145307_20260701T145231_20260701T145306_P05023_N_F_J_001"
        gran2 = "NISAR_L2_PR_GUNW_024_078_D_070_025_2000_SH_20260701T145231_20260701T145306_20260713T145231_20260713T145306_P05023_N_F_J_001"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reg_dir = root / "data" / "global" / "demo_city"
            reg_dir.mkdir(parents=True)
            (reg_dir / "meta.json").write_text(
                json.dumps({"site": "demo_city", "bbox": [1.0, 2.0, 1.5, 2.5], "granules": [gran1, gran2]}),
                encoding="utf-8",
            )
            (reg_dir / "summary.json").write_text(
                json.dumps({"max_subsidence_cm": -4.2, "quality": "provisional"}),
                encoding="utf-8",
            )
            sub_dir = root / "pipeline" / "subset" / "demo_city"
            sub_dir.mkdir(parents=True)
            (sub_dir / "2026-06-19_2026-07-01.npz").write_bytes(b"stub")

            self.assertEqual(find_region_dir("demo_city", root=root), reg_dir)
            found, missing = find_cached_subsets("demo_city", [gran1, gran2], root=root)
            self.assertEqual(len(found), 1)
            self.assertEqual(missing, [gran2])

            res = reproduce_region("demo_city", dry_run=False, root=root)
            self.assertEqual(res["mode"], "dry-run")
            self.assertEqual(res["cached"], 1)
            self.assertEqual(res["missing"], [gran2])

    def test_cli_reproduce_flags(self) -> None:
        args = parse_cli_args(["reproduce", "mashhad", "--dry-run", "--no-qc"])
        self.assertEqual(args.command, "reproduce")
        self.assertEqual(args.region, "mashhad")
        self.assertTrue(args.dry_run)
        self.assertFalse(args.qc)


if __name__ == "__main__":
    unittest.main()
