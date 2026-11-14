"""Offline unit tests for pipeline.nisarpulse."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pipeline.nisarpulse.__main__ import parse_cli_args
from pipeline.nisarpulse.catalog import upsert_catalog
from pipeline.nisarpulse.search import build_chain, classify_quality, parse_bbox


class TestNisarPulse(unittest.TestCase):
    def test_parse_bbox_valid(self) -> None:
        self.assertEqual(
            parse_bbox("-121.85, 37.95, -121.45, 38.20"),
            (-121.85, 37.95, -121.45, 38.20),
        )

    def test_parse_bbox_invalid(self) -> None:
        with self.assertRaises(ValueError):
            parse_bbox("-120.0,36.0,-121.0,37.0")
        with self.assertRaises(ValueError):
            parse_bbox("1,2,3")

    def test_classify_quality(self) -> None:
        self.assertEqual(classify_quality("2026-06-17", "2026-06-29", "P05023"), "provisional")
        self.assertEqual(classify_quality("2026-06-10", "2026-06-22", "P05023"), "beta-precal")
        self.assertEqual(classify_quality("2026-06-26", "2026-07-08", "X05010"), "beta-precal")

    def test_build_chain_and_gap_detection(self) -> None:
        rows = [
            {"date1": "2025-12-28", "date2": "2026-01-09", "quality": "beta-precal", "size_mb": 2200.0},
            {"date1": "2026-06-26", "date2": "2026-07-08", "quality": "provisional", "size_mb": 2100.0},
            {"date1": "2026-07-08", "date2": "2026-07-20", "quality": "provisional", "size_mb": 2150.0},
        ]
        chain_prov, gaps_prov = build_chain(rows, quality_mode="provisional")
        self.assertEqual(len(chain_prov), 2)
        self.assertEqual(gaps_prov, [])

        chain_mix, gaps_mix = build_chain(rows, quality_mode="mixed")
        self.assertEqual(len(chain_mix), 3)
        self.assertEqual(gaps_mix, [("2026-01-09", "2026-06-26")])

    def test_upsert_catalog_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cat = Path(tmp) / "catalog.json"
            meta = {"quality": "provisional", "dates": ["2026-06-17", "2026-06-29"]}
            upsert_catalog(cat, "delta", (-121.85, 37.95, -121.45, 38.2), meta, title="Delta")
            upsert_catalog(cat, "delta", (-121.85, 37.95, -121.45, 38.2), meta, title="Delta v2")
            data = json.loads(cat.read_text(encoding="utf-8"))
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["title"], "Delta v2")
            self.assertEqual(data[0]["layers"][0]["dates"], ["2026-06-17", "2026-06-29"])

    def test_cli_parser_dry_run(self) -> None:
        args = parse_cli_args(
            [
                "run",
                "--name",
                "delta",
                "--bbox",
                "-121.85,37.95,-121.45,38.20",
                "--start",
                "2026-06-17",
                "--end",
                "2026-10-15",
                "--dry-run",
                "--resume",
            ]
        )
        self.assertTrue(args.dry_run)
        self.assertTrue(args.resume)
        self.assertEqual(args.quality, "provisional")


if __name__ == "__main__":
    unittest.main()
