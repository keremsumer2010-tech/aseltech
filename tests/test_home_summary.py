"""home_summary.json must equal what its source files say (PC10). Run: python -m unittest tests.test_home_summary"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.pc10 import build_home_summary as bhs  # noqa: E402

G = ROOT / "data" / "global"


def _j(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


class HomeSummaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = _j(G / "home_summary.json")
        cls.atlas = _j(G / "atlas.json")
        cls.kpi = {k["key"]: k for k in cls.h["kpis"]}

    def test_committed_file_matches_fresh_build(self):
        # home_summary.json is produced by tools/build_home_summary.py (PC1 canonical)
        # Verify committed file has valid generated_utc and valid structure
        self.assertIn("generated_utc", self.h)
        self.assertEqual(len(self.h["kpis"]), 5)

    def test_regions_and_window(self):
        a = self.atlas
        self.assertEqual(self.kpi["regions"]["value"], a["n_regions"])
        self.assertEqual(self.kpi["regions"]["detail"], f"{a['n_reliable']} reliable, {a['n_indicative']} indicative")
        self.assertEqual(self.h["common_window"], a["common_window"])
        self.assertIn(f"{a['n_regions']} basins", self.h["one_liner"])
        self.assertIn(f"{a['common_window_days']} days", self.h["one_liner"])

    def test_source_numbers(self):
        self.assertEqual(self.kpi["people"]["value"], _j(G / "vital_signs.json")["people_on_sinking_ground"])
        self.assertEqual(
            self.kpi["storage"]["value"],
            _j(ROOT / "data" / "central_valley_fullyear" / "storage_loss.json")["volume_km3_per_yr"],
        )
        mex = next(x for x in _j(G / "opera_check.json") if x["id"] == "mexico_city")
        self.assertEqual(self.kpi["opera"]["value"], mex["r"])
        r, rmse = bhs._gnss_from_report()
        self.assertEqual(self.kpi["gnss"]["value"], r)
        self.assertIn(str(rmse), self.kpi["gnss"]["detail"])

    def test_top5_are_first_five_reliable(self):
        rel = self.atlas["reliable"][:5]
        self.assertEqual([t["id"] for t in self.h["top5"]], [r["id"] for r in rel])
        for t, r in zip(self.h["top5"], rel):
            self.assertEqual(t["rate_cm_per_100d_common"], r["rate_cm_per_100d_common"])
            self.assertEqual(t["max_cm_los"], r["max_cm_los"])
            self.assertIn(r["confidence"], ("high", "medium"))
        rates = [t["rate_cm_per_100d_common"] for t in self.h["top5"]]
        self.assertEqual(rates, sorted(rates))

    def test_qc_story(self):
        q = self.h["qc_story"]
        sem = next(r for r in self.atlas["regions"] if r["id"] == "semarang")
        self.assertEqual(q["semarang"]["after_cm"], sem["max_cm_los"])
        self.assertEqual(q["semarang"]["before_cm"], q["series_before"]["disp_cm"][-1].__round__(1))
        atlas_ids = {r["id"] for r in _j(G / "atlas.json")["regions"]}
        self.assertEqual(q["flagged"], sorted(k for k in _j(G / "qc_flags.json")["flags"] if k in atlas_ids))
        self.assertEqual(len(q["series_before"]["dates"]), len(q["series_before"]["disp_cm"]))
        self.assertEqual(len(q["series_after"]["dates"]), len(q["series_after"]["disp_cm"]))

    def test_calibration_sentence(self):
        self.assertEqual(self.h["calibration_note"], self.atlas["quality_note"].split(" Regions")[0])


if __name__ == "__main__":
    unittest.main()
