"""Offline synthetic-stack unit tests for NISAR Pulse pixel-level QC."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from pipeline.nisarpulse.__main__ import parse_cli_args
from pipeline.nisarpulse.qc import L_BAND_CYCLE_CM, qc_stack, write_qc_report


class TestNisarPulseQC(unittest.TestCase):
    def test_cycle_jump_correction_by_connected_component(self) -> None:
        dates = ["2026-07-01", "2026-07-13", "2026-07-25", "2026-08-06"]
        shape = (20, 20)
        cc = np.ones(shape, dtype=np.int32)
        cc[10:, :] = 2  # bottom half is connected component 2

        p0 = np.full(shape, -0.5, dtype=np.float32)
        p1 = np.full(shape, -0.5, dtype=np.float32)
        p1[10:, :] += L_BAND_CYCLE_CM  # 1-cycle (+12.1 cm) jump in component 2
        p2 = np.full(shape, -0.5, dtype=np.float32)

        fixed, out_dates, report = qc_stack([p0, p1, p2], dates, [cc, cc, cc])
        self.assertEqual(out_dates, dates)
        self.assertEqual(len(report["corrected_pairs"]), 1)
        self.assertEqual(report["corrected_pairs"][0]["component"], 2)
        self.assertEqual(report["corrected_pairs"][0]["k"], 1)
        self.assertAlmostEqual(float(np.mean(fixed[1][:10, :])), -0.5, places=4)
        self.assertAlmostEqual(float(np.mean(fixed[1][10:, :])), -0.5, places=4)
        self.assertGreater(report["affected_pixel_pct"], 45.0)

    def test_opposite_sign_single_date_outlier_dropped(self) -> None:
        dates = ["2026-07-01", "2026-07-13", "2026-07-25", "2026-08-06"]
        shape = (20, 20)
        p0 = np.full(shape, -0.5, dtype=np.float32)
        p1 = np.full(shape, -0.5, dtype=np.float32)
        p2 = np.full(shape, -0.5, dtype=np.float32)
        # Corrupt 2026-07-13 across 60% of pixels: -8.0 cm then +7.5 cm
        p0[:12, :] = -8.0
        p1[:12, :] = 7.5

        fixed, out_dates, report = qc_stack([p0, p1, p2], dates)
        self.assertEqual(out_dates, ["2026-07-01", "2026-07-25", "2026-08-06"])
        self.assertEqual(len(fixed), 2)
        self.assertEqual(len(report["dropped_dates"]), 1)
        self.assertEqual(report["dropped_dates"][0]["date"], "2026-07-13")
        self.assertAlmostEqual(float(np.mean(fixed[0][:12, :])), -0.5, places=4)

    def test_small_local_spike_not_dropped(self) -> None:
        dates = ["2026-07-01", "2026-07-13", "2026-07-25"]
        shape = (20, 20)
        p0 = np.full(shape, -0.5, dtype=np.float32)
        p1 = np.full(shape, -0.5, dtype=np.float32)
        # Only 10% of pixels have opposite-sign >5 cm spike -> keep date
        p0[:2, :] = -8.0
        p1[:2, :] = 7.5

        fixed, out_dates, report = qc_stack([p0, p1], dates)
        self.assertEqual(out_dates, dates)
        self.assertEqual(len(fixed), 2)
        self.assertEqual(report["dropped_dates"], [])

    def test_write_qc_report_and_cli_flags(self) -> None:
        args_default = parse_cli_args(["run", "--name", "test", "--center", "57.07,30.28", "--start", "2026-06-17", "--end", "2026-10-31", "--dry-run"])
        self.assertTrue(args_default.qc)
        args_no_qc = parse_cli_args(["run", "--name", "test", "--center", "57.07,30.28", "--start", "2026-06-17", "--end", "2026-10-31", "--dry-run", "--no-qc"])
        self.assertFalse(args_no_qc.qc)

        with tempfile.TemporaryDirectory() as tmp:
            p = write_qc_report(Path(tmp), {"qc_enabled": True, "corrected_pairs": [], "dropped_dates": [], "affected_pixel_pct": 0.0})
            payload = json.loads(p.read_text(encoding="utf-8"))
            self.assertEqual(payload["quality"], "provisional")
            self.assertTrue(payload["qc_enabled"])


if __name__ == "__main__":
    unittest.main()
