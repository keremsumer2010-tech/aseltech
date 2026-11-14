#!/usr/bin/env python3
"""Automated 20-strategy x 2-basin test harness for game/model.js (Tulare & Konya)."""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
MODEL_JS_PATH = REPO_ROOT / "game" / "model.js"
CV_DIR = REPO_ROOT / "data" / "central_valley"
KP_DIR = REPO_ROOT / "data" / "karapinar"

MONTH_NAMES = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]

# Exact benchmark table from docs/qa/PC7.md (pipeline/pc7/game_strategy_test.js run in Node.js)
PC7_NODE_BENCHMARKS = {
    "D0": (0.08, 0.00, 452.1),
    "D50": (6.05, 6.03, 849.9),
    "D100": (28.87, 28.84, 1308.9),
    "D150": (51.68, 51.66, 1748.5),
    "W100": (0.04, 0.00, 1748.1),
    "BN100": (17.62, 17.60, 1529.8),
    "D100-F30": (15.18, 15.15, 898.6),
    "W0-F30": (0.24, 0.00, 572.1),
    "W150-F30": (0.41, 0.39, 1292.4),
    "BN50-F30": (0.09, 0.00, 739.8),
}

# 20 diverse water-management policy strategies (name, y1, y2, pump_pct, surf_mode_or_pct, fallow_pct)
STRATEGIES_20 = [
    ("S01-D0", "Dry", "Dry", 0, "cap", 0),
    ("S02-D50", "Dry", "Dry", 50, "cap", 0),
    ("S03-D100", "Dry", "Dry", 100, "cap", 0),
    ("S04-D150", "Dry", "Dry", 150, "cap", 0),
    ("S05-W100", "Wet", "Wet", 100, "cap", 0),
    ("S06-BN100", "Below Normal", "Below Normal", 100, "cap", 0),
    ("S07-D100-F30", "Dry", "Dry", 100, "cap", 30),
    ("S08-W0-F30", "Wet", "Wet", 0, "cap", 30),
    ("S09-W150-F30", "Wet", "Wet", 150, "cap", 30),
    ("S10-BN50-F30", "Below Normal", "Below Normal", 50, "cap", 30),
    ("S11-C0-F50", "Critical", "Critical", 0, "cap", 50),
    ("S12-C150", "Critical", "Critical", 150, "cap", 0),
    ("S13-C100-F25", "Critical", "Critical", 100, "cap", 25),
    ("S14-AN75", "Above Normal", "Above Normal", 75, "cap", 0),
    ("S15-BN-SGMA", "Below Normal", "Below Normal", 40, "cap", 25),
    ("S16-BN-OverPump", "Below Normal", "Below Normal", 145, 20, 0),
    ("S17-WetToCrit120", "Wet", "Critical", 120, "cap", 10),
    ("S18-CritToWet60", "Critical", "Wet", 60, "cap", 20),
    ("S19-DryToAN90-F15", "Dry", "Above Normal", 90, "cap", 15),
    ("S20-CritToBN-NoSurf", "Critical", "Below Normal", 80, 0, 0),
]


def _extract_js_literal(source: str, anchor: str) -> Any:
    """Parse a pure JS object/array literal cleanly from game/model.js into Python data."""
    idx = source.find(anchor)
    if idx < 0:
        raise ValueError(f"Anchor not found in model.js: {anchor}")
    start = idx + len(anchor) - 1
    open_ch = source[start]
    close_ch = "}" if open_ch == "{" else "]"

    depth = 0
    in_quote: str | None = None
    escaped = False
    end = -1
    i = start
    while i < len(source):
        ch = source[i]
        if in_quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_quote:
                in_quote = None
        else:
            if ch in ("'", '"'):
                in_quote = ch
            elif ch == "/" and i + 1 < len(source) and source[i + 1] == "/":
                nl = source.find("\n", i)
                i = len(source) - 1 if nl < 0 else nl
            elif ch == "/" and i + 1 < len(source) and source[i + 1] == "*":
                ce = source.find("*/", i + 2)
                i = len(source) - 1 if ce < 0 else ce + 1
            elif ch == open_ch:
                depth += 1
            elif ch == close_ch:
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        i += 1
    if end < 0:
        raise ValueError(f"Unclosed literal for anchor: {anchor}")

    raw = source[start:end]
    # Convert JS object/array literal -> valid JSON
    out: list[str] = []
    i = 0
    n = len(raw)
    while i < n:
        ch = raw[i]
        if ch in ("'", '"'):
            q = ch
            buf = ['"']
            i += 1
            while i < n:
                c = raw[i]
                if c == "\\":
                    nxt = raw[i + 1] if i + 1 < n else ""
                    if nxt == "'":
                        buf.append("'")
                    elif nxt == '"':
                        buf.append('\\"')
                    else:
                        buf.append("\\" + nxt)
                    i += 2
                    continue
                if c == q:
                    break
                if c == '"' and q == "'":
                    buf.append('\\"')
                else:
                    buf.append(c)
                i += 1
            buf.append('"')
            out.append("".join(buf))
            i += 1
        elif ch == "/" and i + 1 < n and raw[i + 1] == "/":
            nl = raw.find("\n", i)
            i = n if nl < 0 else nl
        elif ch == "/" and i + 1 < n and raw[i + 1] == "*":
            ce = raw.find("*/", i + 2)
            i = n if ce < 0 else ce + 2
        elif ch.isalpha() or ch == "_":
            j = i + 1
            while j < n and (raw[j].isalnum() or raw[j] == "_"):
                j += 1
            ident = raw[i:j]
            k = j
            while k < n and raw[k] in " \t":
                k += 1
            if k < n and raw[k] == ":":
                out.append(f'"{ident}"')
            else:
                out.append(ident)
            i = j
        elif ch in ("}", "]"):
            # Strip trailing comma if present
            back = len(out) - 1
            while back >= 0 and out[back].strip() == "":
                back -= 1
            if back >= 0 and out[back] == ",":
                out[back] = ""
            out.append(ch)
            i += 1
        else:
            out.append(ch)
            i += 1

    cleaned = "".join(out)
    # Substitute identifier references inside BASINS if parsing BASINS separately
    return json.loads(cleaned)


def load_model_spec() -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    """Read live CONFIG, DEFAULT_DISTRICTS, and KONYA_DISTRICTS from game/model.js."""
    src = MODEL_JS_PATH.read_text(encoding="utf-8")
    config = _extract_js_literal(src, "const CONFIG = {")
    tulare_districts = _extract_js_literal(src, "const DEFAULT_DISTRICTS = [")
    konya_districts = _extract_js_literal(src, "const KONYA_DISTRICTS = [")
    return config, {"tulare": tulare_districts, "konya": konya_districts}


class ValleyModelPy:
    """Exact Python mirror of game/model.js loaded directly from game/model.js constants."""

    def __init__(self) -> None:
        self.config, self.basin_districts = load_model_spec()
        self.basins = {
            "tulare": {
                "id": "tulare",
                "name": "Tulare Basin, California (USA)",
                "incidenceDegDefault": 39.1,
                "targetMeasuredLosCm": -7.8,
                "targetMeasuredVertCm": -10.1,
                "districts": self.basin_districts["tulare"],
            },
            "konya": {
                "id": "konya",
                "name": "Konya Closed Basin / Karapinar, Turkiye",
                "incidenceDegDefault": 41.9,
                "targetMeasuredLosCm": -5.9,
                "targetMeasuredVertCm": -8.0,
                "districts": self.basin_districts["konya"],
            },
        }

    def get_water_year_spec(self, wy_id: str) -> dict[str, Any]:
        for wy in self.config["waterYearTypes"]:
            if wy["id"] == wy_id:
                return wy
        return self.config["waterYearTypes"][2]

    @staticmethod
    def vertical_to_los(vertical_cm: float, incidence_deg: float) -> float:
        return vertical_cm * math.cos(math.radians(incidence_deg))

    @staticmethod
    def los_to_vertical(los_cm: float, incidence_deg: float) -> float:
        return los_cm / math.cos(math.radians(incidence_deg))

    def compute_calibrated_demand_multiplier(self, target_vert_cm: float, basin_id: str) -> float:
        basin = self.basins[basin_id]
        p01 = basin["districts"][0]
        phys = self.config["physics"]
        sy = phys["specificYield"]["value"]
        ske = phys["elasticSpecificStorage"]["value"]
        skv = phys["inelasticSpecificStorage"]["value"]
        b0 = p01["clayThicknessM"]

        pw = self.config["seasonalWeights"]["pumping"]
        rw = self.config["seasonalWeights"]["recharge"]
        pump_sum = pw[9] + pw[10] + pw[11] + 0.45 * pw[0] + 0.07 * pw[8]
        rech_sum = rw[9] + rw[10] + rw[11] + 0.45 * rw[0] + 0.07 * rw[8]

        initial_buffer = max(0.0, p01["initialHeadM"] - p01["preconsolidationHeadM"])
        needed_comp_m = abs(target_vert_cm) / 100.0
        if needed_comp_m / b0 <= ske * initial_buffer:
            required_dh_abs = needed_comp_m / (b0 * ske)
        else:
            required_dh_abs = initial_buffer + (needed_comp_m / b0 - ske * initial_buffer) / skv

        cal_scen = self.config["calibration"]["scenario"]
        cal_wy = self.get_water_year_spec(cal_scen["waterYearType"])
        rech_col = (
            phys["baselineAnnualRechargeM"]["value"]
            * cal_wy["rechargeMult"]
            * (0.65 + 0.35 * (cal_scen["surfaceAllocPct"] / 100.0))
            * rech_sum
        )
        needed_pump_col = sy * required_dh_abs + rech_col
        raw_pump_col = phys["baselineAnnualDemandM"]["value"] * p01["pumpingIntensity"] * pump_sum
        return needed_pump_col / raw_pump_col

    def hydrate_districts(self, basin_id: str, points_json: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
        districts = copy.deepcopy(self.basins[basin_id]["districts"])
        if points_json:
            by_id = {p["id"]: p for p in points_json}
            for d in districts:
                m = by_id.get(d["id"])
                if m:
                    d["pointName"] = m.get("name", d["pointName"])
                    d["lon"] = m.get("lon", d["lon"])
                    d["lat"] = m.get("lat", d["lat"])
                    if m.get("dates"):
                        d["nisarDates"] = m["dates"]
                    if m.get("disp_cm"):
                        d["nisarSeriesCm"] = m["disp_cm"]
                        d["nisarLosCm"] = m["disp_cm"][-1]
        return districts

    def create_state(
        self,
        basin_id: str = "tulare",
        year1_wy: str = "Below Normal",
        year2_wy: str = "Below Normal",
        summary_data: dict[str, Any] | None = None,
        points_data: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        basin = self.basins[basin_id]
        s = summary_data or {}
        target_vert = s.get("max_subsidence_vertical_cm_estimate", basin["targetMeasuredVertCm"])
        target_los = s.get("max_subsidence_cm", basin["targetMeasuredLosCm"])
        inc_deg = s.get("incidence_deg_at_max", basin["incidenceDegDefault"])
        cal_factor = self.compute_calibrated_demand_multiplier(target_vert, basin_id)
        wy1_spec = self.get_water_year_spec(year1_wy)

        districts = []
        for d in self.hydrate_districts(basin_id, points_data):
            d_copy = copy.deepcopy(d)
            d_copy.update(
                {
                    "headM": float(d["initialHeadM"]),
                    "preconsolidationHeadM": float(d["preconsolidationHeadM"]),
                    "elasticCm": 0.0,
                    "inelasticCm": 0.0,
                    "totalCm": 0.0,
                    "dryWells": 0,
                    "canalCapacityLossPct": 0.0,
                    "sinkholeRiskIndicator": False,
                    "currentGradientMmKm": d["baseGradientMmKm"] * 0.15,
                    "cumulativeRevenueMUsd": 0.0,
                    "controls": {
                        "pumpingPct": 100.0,
                        "surfaceAllocPct": float(wy1_spec["maxSurfacePct"]),
                        "fallowPct": 0.0,
                    },
                    "history": [],
                }
            )
            districts.append(d_copy)

        return {
            "basinId": basin_id,
            "monthStep": 0,
            "totalMonths": int(self.config["totalMonths"]),
            "finished": False,
            "calibrationFactor": cal_factor,
            "incidenceDeg": float(inc_deg),
            "measuredTargetLosCm": float(target_los),
            "measuredTargetVertCm": float(target_vert),
            "year1WaterYear": year1_wy,
            "year2WaterYear": year2_wy,
            "currentWaterYear": year1_wy,
            "sinkholeRiskActive": False,
            "districts": districts,
            "valleyHistory": [],
        }

    def set_all_controls(
        self,
        state: dict[str, Any],
        pumping_pct: float,
        surface_alloc_pct: float,
        fallow_pct: float,
    ) -> None:
        wy_spec = self.get_water_year_spec(state["currentWaterYear"])
        for d in state["districts"]:
            d["controls"]["pumpingPct"] = max(0.0, min(150.0, float(pumping_pct)))
            d["controls"]["surfaceAllocPct"] = max(0.0, min(float(wy_spec["maxSurfacePct"]), float(surface_alloc_pct)))
            d["controls"]["fallowPct"] = max(0.0, min(50.0, float(fallow_pct)))

    def step_month(self, state: dict[str, Any], frac: float = 1.0) -> None:
        if state["finished"] or state["monthStep"] >= state["totalMonths"]:
            state["finished"] = True
            return

        m_idx = state["monthStep"]
        wy_month_idx = m_idx % 12
        wy_number = 1 if m_idx < 12 else 2
        state["currentWaterYear"] = state["year1WaterYear"] if wy_number == 1 else state["year2WaterYear"]
        wy_spec = self.get_water_year_spec(state["currentWaterYear"])

        phys = self.config["physics"]
        sy = phys["specificYield"]["value"]
        ske = phys["elasticSpecificStorage"]["value"]
        skv = phys["inelasticSpecificStorage"]["value"]
        base_demand = phys["baselineAnnualDemandM"]["value"]
        base_recharge = phys["baselineAnnualRechargeM"]["value"]

        pump_weight = self.config["seasonalWeights"]["pumping"][wy_month_idx] * frac
        rech_weight = self.config["seasonalWeights"]["recharge"][wy_month_idx] * frac

        for d in state["districts"]:
            if d["controls"]["surfaceAllocPct"] > wy_spec["maxSurfacePct"]:
                d["controls"]["surfaceAllocPct"] = float(wy_spec["maxSurfacePct"])

            active_crop = 1.0 - d["controls"]["fallowPct"] / 100.0
            pump_factor = (d["controls"]["pumpingPct"] / 100.0) * active_crop
            surf_factor = min(wy_spec["maxSurfacePct"], d["controls"]["surfaceAllocPct"]) / 100.0

            recharge_m = base_recharge * wy_spec["rechargeMult"] * (0.65 + 0.35 * surf_factor) * rech_weight
            withdrawal_m = base_demand * d["pumpingIntensity"] * state["calibrationFactor"] * pump_factor * pump_weight

            delta_h = (recharge_m - withdrawal_m) / sy
            prev_head = d["headM"]
            next_head = prev_head + delta_h
            prev_pc = d["preconsolidationHeadM"]

            d_elast = 0.0
            d_inelast = 0.0
            if next_head >= prev_pc:
                d_elast = ske * d["clayThicknessM"] * delta_h * 100.0
            else:
                if prev_head > prev_pc:
                    d_elast = ske * d["clayThicknessM"] * (prev_pc - prev_head) * 100.0
                    d_inelast = skv * d["clayThicknessM"] * (next_head - prev_pc) * 100.0
                else:
                    d_inelast = skv * d["clayThicknessM"] * delta_h * 100.0
                d["preconsolidationHeadM"] = next_head

            d["headM"] = next_head
            d["elasticCm"] = min(2.0, d["elasticCm"] + d_elast)
            d["inelasticCm"] = min(0.0, d["inelasticCm"] + d_inelast)
            d["totalCm"] = d["elasticCm"] + d["inelasticCm"]

            depth_to_water = -d["headM"]
            d["dryWells"] = sum(1 for dep in d["wellDepthsM"] if depth_to_water >= dep)

            amp = max(0.0, abs(d["totalCm"]) / max(1.5, abs(self.los_to_vertical(d["nisarLosCm"], state["incidenceDeg"]))))
            d["currentGradientMmKm"] = round(d["baseGradientMmKm"] * min(2.5, amp), 2)
            if d["currentGradientMmKm"] > self.config["thresholds"]["canalHighGradientMmKm"] and abs(d["totalCm"]) > 2.0:
                excess = min(1.0, (abs(d["totalCm"]) - 2.0) / 28.0)
                d["canalCapacityLossPct"] = round(min(60.0, excess * 60.0), 1)
            else:
                d["canalCapacityLossPct"] = max(d["canalCapacityLossPct"], 0.0)

            if state["basinId"] == "konya" and d.get("sinkholesWithin5km", 0) > 0:
                if (
                    d["headM"] <= d["preconsolidationHeadM"] + 0.05
                    and abs(d["totalCm"]) >= self.config["thresholds"]["sinkholeAlertCm"]
                ):
                    d["sinkholeRiskIndicator"] = True
                    state["sinkholeRiskActive"] = True

            water_supply = min(1.15, 0.58 * (d["controls"]["pumpingPct"] / 100.0) + 0.42 * surf_factor + 0.15 * rech_weight * 8)
            crop_mult = max(0.25, water_supply) * active_crop
            gross_year_rev = (d["revenuePerIrrigatedHa"] * (d["irrigatedAreaKHa"] * 1000.0)) / 1e6
            energy_pen = 0.04 * (d["controls"]["pumpingPct"] / 100.0) * (depth_to_water / 50.0) * gross_year_rev * pump_weight
            d["cumulativeRevenueMUsd"] += gross_year_rev * pump_weight * crop_mult - energy_pen

        worst = min(state["districts"], key=lambda x: x["totalCm"])
        total_rev = sum(d["cumulativeRevenueMUsd"] for d in state["districts"])
        state["valleyHistory"].append(
            {
                "monthStep": m_idx + 1,
                "worstDistrictId": worst["id"],
                "worstTotalCm": round(worst["totalCm"], 2),
                "worstInelasticCm": round(worst["inelasticCm"], 2),
                "worstElasticCm": round(worst["elasticCm"], 2),
                "totalDryWells": sum(d["dryWells"] for d in state["districts"]),
                "maxCanalLossPct": round(max(d["canalCapacityLossPct"] for d in state["districts"]), 1),
                "totalRevenueMUsd": round(total_rev, 1),
            }
        )
        state["monthStep"] += 1
        if state["monthStep"] >= state["totalMonths"]:
            state["finished"] = True

    def run_calibration_check(self, basin_id: str, summary_data: dict[str, Any] | None) -> dict[str, Any]:
        cal_wy = self.config["calibration"]["scenario"]["waterYearType"]
        sim = self.create_state(basin_id=basin_id, year1_wy=cal_wy, year2_wy=cal_wy, summary_data=summary_data)
        self.set_all_controls(
            sim,
            self.config["calibration"]["scenario"]["pumpingPct"],
            self.config["calibration"]["scenario"]["surfaceAllocPct"],
            self.config["calibration"]["scenario"]["fallowPct"],
        )
        for idx, frac in [(8, 0.07), (9, 1.0), (10, 1.0), (11, 1.0), (0, 0.45)]:
            sim["monthStep"] = idx
            sim["finished"] = False
            self.step_month(sim, frac)
        p01 = sim["districts"][0]
        sim_vert = round(p01["totalCm"], 2)
        measured_vert = sim["measuredTargetVertCm"]
        err_pct = round(abs((sim_vert - measured_vert) / measured_vert) * 100.0, 2)
        return {
            "basinId": basin_id,
            "k": round(sim["calibrationFactor"], 3),
            "simVertCm": sim_vert,
            "measuredVertCm": measured_vert,
            "simLosCm": round(self.vertical_to_los(p01["totalCm"], sim["incidenceDeg"]), 2),
            "measuredLosCm": sim["measuredTargetLosCm"],
            "errorPct": err_pct,
        }


def run_20_strategies(verbose: bool = True) -> dict[str, Any]:
    """Run all 20 strategies on both Tulare and Konya (40 simulations total) + parity checks."""
    model = ValleyModelPy()
    cv_sum = json.loads((CV_DIR / "summary.json").read_text(encoding="utf-8"))
    cv_pts = json.loads((CV_DIR / "points.json").read_text(encoding="utf-8"))
    kp_sum = json.loads((KP_DIR / "summary.json").read_text(encoding="utf-8"))
    kp_pts = json.loads((KP_DIR / "points.json").read_text(encoding="utf-8"))

    cal_tulare = model.run_calibration_check("tulare", cv_sum)
    cal_konya = model.run_calibration_check("konya", kp_sum)
    assert cal_tulare["errorPct"] <= 0.1, f"Tulare calibration drift: {cal_tulare}"
    assert cal_konya["errorPct"] <= 0.1, f"Konya calibration drift: {cal_konya}"

    results: list[dict[str, Any]] = []
    for basin_id, sum_data, pts_data in [
        ("tulare", cv_sum, cv_pts),
        ("konya", kp_sum, kp_pts),
    ]:
        for name, wy1, wy2, pump_pct, surf_spec, fallow_pct in STRATEGIES_20:
            st = model.create_state(
                basin_id=basin_id,
                year1_wy=wy1,
                year2_wy=wy2,
                summary_data=sum_data,
                points_data=pts_data,
            )
            surf_pct = model.get_water_year_spec(wy1)["maxSurfacePct"] if surf_spec == "cap" else surf_spec
            model.set_all_controls(st, pump_pct, surf_pct, fallow_pct)
            for _ in range(24):
                model.step_month(st)

            assert len(st["valleyHistory"]) == 24 and st["finished"]
            final = st["valleyHistory"][-1]
            tot_abs = abs(final["worstTotalCm"])
            perm_abs = abs(final["worstInelasticCm"])
            elast_cm = final["worstElasticCm"]
            rev = final["totalRevenueMUsd"]

            for val in (tot_abs, perm_abs, rev):
                assert math.isfinite(val) and val >= 0.0, f"Invalid number in {basin_id}/{name}: {final}"
            assert final["worstInelasticCm"] <= 0.0 and elast_cm <= 2.0 + 1e-9, f"Bounds violated: {final}"
            assert abs((elast_cm + final["worstInelasticCm"]) - final["worstTotalCm"]) <= 0.03, (
                f"Compaction sum identity failed in {basin_id}/{name}: {final}"
            )
            assert perm_abs <= tot_abs + max(0.0, elast_cm) + 0.05, (
                f"Permanent exceeds total+elastic heave in {basin_id}/{name}: {final}"
            )

            results.append(
                {
                    "basin": basin_id,
                    "strategy": name,
                    "wy": f"{wy1}/{wy2}" if wy1 != wy2 else wy1,
                    "pumpPct": pump_pct,
                    "fallowPct": fallow_pct,
                    "totalCm": tot_abs,
                    "permCm": perm_abs,
                    "revenueM": rev,
                    "dryWells": final["totalDryWells"],
                    "maxCanalLossPct": final["maxCanalLossPct"],
                    "sinkholeRisk": st["sinkholeRiskActive"],
                }
            )

    # Assert exact parity with PC7 Node.js run on Tulare (top 10 strategies match PC7 scenarios)
    pc7_keys = list(PC7_NODE_BENCHMARKS.keys())
    tulare_top10 = [r for r in results if r["basin"] == "tulare"][:10]
    for r, pc7_name in zip(tulare_top10, pc7_keys):
        exp_tot, exp_perm, exp_rev = PC7_NODE_BENCHMARKS[pc7_name]
        assert abs(r["totalCm"] - exp_tot) <= 0.02, f"Parity mismatch {pc7_name}: {r['totalCm']} vs {exp_tot}"
        assert abs(r["permCm"] - exp_perm) <= 0.02, f"Perm mismatch {pc7_name}: {r['permCm']} vs {exp_perm}"
        assert abs(r["revenueM"] - exp_rev) <= 0.2, f"Rev mismatch {pc7_name}: {r['revenueM']} vs {exp_rev}"

    # Monotonic pumping check (0% -> 50% -> 100% -> 150% under Dry) on BOTH basins
    for basin_id in ("tulare", "konya"):
        dry_4 = [r["totalCm"] for r in results if r["basin"] == basin_id][:4]
        assert all(dry_4[i] <= dry_4[i + 1] for i in range(3)), f"Non-monotonic in {basin_id}: {dry_4}"

    # Konya sinkhole indicator check: active on Dry/Crit high pump, inactive on S01-D0 / S08-W0-F30
    konya_map = {r["strategy"]: r for r in results if r["basin"] == "konya"}
    assert konya_map["S03-D100"]["sinkholeRisk"] is True
    assert konya_map["S12-C150"]["sinkholeRisk"] is True
    assert konya_map["S01-D0"]["sinkholeRisk"] is False
    assert konya_map["S08-W0-F30"]["sinkholeRisk"] is False

    if verbose:
        print(f"Calibration Tulare: {cal_tulare}")
        print(f"Calibration Konya : {cal_konya}")
        print(f"Evaluated {len(results)} 24-month runs (20 strategies x 2 basins): ALL CHECKS PASS\n")
        print("| Strategy | WY (Y1/Y2) | Pump | Fallow | Tulare Tot/Perm (cm) | Tulare Rev ($M) | Konya Tot/Perm (cm) | Konya Obruk Ind. |")
        print("|---|---|---:|---:|---:|---:|---:|:---:|")
        tul = [r for r in results if r["basin"] == "tulare"]
        kon = [r for r in results if r["basin"] == "konya"]
        for rt, rk in zip(tul, kon):
            print(
                f"| `{rt['strategy']}` | {rt['wy']} | {rt['pumpPct']}% | {rt['fallowPct']}% | "
                f"{rt['totalCm']:.2f} / {rt['permCm']:.2f} | {rt['revenueM']:.1f} | "
                f"{rk['totalCm']:.2f} / {rk['permCm']:.2f} | {'Elevated' if rk['sinkholeRisk'] else 'Safe'} |"
            )

    return {"cal_tulare": cal_tulare, "cal_konya": cal_konya, "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run 20 policy strategies against Valley Under Pressure model.")
    parser.add_argument("--self-test", action="store_true", help="Run full verification assertions and exit 0 on pass.")
    args = parser.parse_args()
    out = run_20_strategies(verbose=True)
    if args.self_test:
        print(f"\nSELF-TEST PASSED: {len(out['results'])} runs clean, 0 NaN/Infinity, PC7 Node parity verified.")


if __name__ == "__main__":
    main()
