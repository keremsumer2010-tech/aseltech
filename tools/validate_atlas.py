"""Validate global atlas summaries against the PC1 quality standard.

Run from the repository root with ``python tools/validate_atlas.py``. The
validator is offline and read-only; it reports missing evidence without
inventing replacement coordinates or confidence values.
"""
from __future__ import annotations

import datetime as dt
import json
import math
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ATLAS_PATH = ROOT / "data/global/atlas.json"
BBOX_SPAN_DEG = 0.5
BBOX_TOL_DEG = 0.005
# Accept values rounded to one decimal place while still catching larger drift.
RATE_TOL_CM_PER_100D = 0.051
REFERENCE_RANGE_RATIO_MAX = 0.30


class ValidationError(ValueError):
    pass


def _reject_constant(value: str) -> None:
    raise ValidationError(f"non-standard JSON numeric constant {value}")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream, parse_constant=_reject_constant)


def _walk_nonfinite_or_empty(value: Any, prefix: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, float) and not math.isfinite(value):
        found.append(f"{prefix}: non-finite number")
    elif isinstance(value, str) and not value.strip():
        found.append(f"{prefix}: empty string")
    elif isinstance(value, dict):
        for key, item in value.items():
            found.extend(_walk_nonfinite_or_empty(item, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_walk_nonfinite_or_empty(item, f"{prefix}[{index}]"))
    return found


def _period_days(period: Any) -> int:
    if not isinstance(period, list) or len(period) != 2:
        raise ValidationError("period must contain [start_date, end_date]")
    try:
        start, end = (dt.date.fromisoformat(str(part)) for part in period)
    except ValueError as exc:
        raise ValidationError(f"period contains invalid ISO date: {period!r}") from exc
    days = (end - start).days
    if days <= 0:
        raise ValidationError(f"period dates are not strictly increasing: {period!r}")
    return days


def _finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _bbox_findings(city: str, bbox: Any) -> list[str]:
    if not isinstance(bbox, list) or len(bbox) != 4 or not all(_finite_number(v) for v in bbox):
        return [f"{city}: bbox missing/invalid; expected [west,south,east,north]"]
    west, south, east, north = (float(v) for v in bbox)
    if east <= west or north <= south:
        return [f"{city}: bbox coordinates are not ordered"]
    width, height = east - west, north - south
    findings = []
    if abs(width - BBOX_SPAN_DEG) > BBOX_TOL_DEG:
        findings.append(f"{city}: bbox longitude span {width:.4f} degrees, expected 0.5000 +/- {BBOX_TOL_DEG:.3f}")
    if abs(height - BBOX_SPAN_DEG) > BBOX_TOL_DEG:
        findings.append(f"{city}: bbox latitude span {height:.4f} degrees, expected 0.5000 +/- {BBOX_TOL_DEG:.3f}")
    return findings


def _reference_checks(city: str, summary: dict[str, Any], meta: dict[str, Any], atlas_region: dict[str, Any]) -> list[str]:
    explicit = next((obj["reference_outside_basin"] for obj in (summary, meta, atlas_region)
                     if isinstance(obj, dict) and "reference_outside_basin" in obj), None)
    if isinstance(explicit, bool):
        if explicit:
            return []
        return [f"{city}: reference_outside_basin is explicitly false"]

    headline = summary.get("max_subsidence_cm")
    ref_range = summary.get("ref_range_cm")
    if not _finite_number(ref_range):
        interval = summary.get("max_subsidence_range_cm", summary.get("range_cm"))
        if isinstance(interval, list) and len(interval) == 2 and all(_finite_number(v) for v in interval):
            ref_range = abs(float(interval[1]) - float(interval[0]))
    n_references = summary.get("n_references")
    if _finite_number(headline) and abs(float(headline)) > 0 and _finite_number(ref_range):
        ratio = float(ref_range) / abs(float(headline))
        if _finite_number(n_references) and int(n_references) >= 3 and ratio < REFERENCE_RANGE_RATIO_MAX:
            return [f"{city}: reference stability proxy passes ({int(n_references)} alternatives; range/headline={ratio:.1%}), but geographic/geologic basin exclusion is not explicit"]
        return [f"{city}: reference basin exclusion not verified (reference alternatives={n_references!r}, range/headline={ratio:.1%}; required >=3 and <30% proxy)"]
    return [f"{city}: reference basin exclusion not verifiable; explicit reference_outside_basin and usable ref_range_cm are absent"]


def _confidence_checks(city: str, obj: dict[str, Any], label: str) -> list[str]:
    findings = []
    confidence = obj.get("confidence")
    valid_fraction = obj.get("valid_fraction")
    if not isinstance(confidence, str) or confidence not in {"high", "medium", "low"}:
        findings.append(f"{city}: {label}.confidence missing/invalid")
    if not _finite_number(valid_fraction) or not 0.0 <= float(valid_fraction) <= 1.0:
        findings.append(f"{city}: {label}.valid_fraction missing or outside [0,1]")
    elif confidence == "high" and float(valid_fraction) < 0.40:
        findings.append(f"{city}: {label}.confidence=high conflicts with valid_fraction={float(valid_fraction):.3f} (<0.40)")
    return findings


def _check_summary(city: str, directory: Path, atlas_region: dict[str, Any]) -> tuple[list[str], dict[str, Any] | None]:
    findings: list[str] = []
    summary_path, meta_path, points_path = directory / "summary.json", directory / "meta.json", directory / "points.json"
    summary = meta = None
    for path in (summary_path, meta_path, points_path):
        if not path.is_file():
            findings.append(f"{city}: required file missing: {path.relative_to(ROOT).as_posix()}")
    if not summary_path.is_file():
        return findings, None
    try:
        summary = load_json(summary_path)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        return findings + [f"{city}: invalid summary.json: {exc}"], None
    if not isinstance(summary, dict):
        return findings + [f"{city}: summary.json root must be an object"], None
    findings.extend(f"{city}: summary.json {issue}" for issue in _walk_nonfinite_or_empty(summary))

    if meta_path.is_file():
        try:
            meta = load_json(meta_path)
            findings.extend(f"{city}: meta.json {issue}" for issue in _walk_nonfinite_or_empty(meta))
        except (OSError, json.JSONDecodeError, ValidationError) as exc:
            findings.append(f"{city}: invalid meta.json: {exc}")
            meta = {}
    else:
        meta = {}
    if isinstance(meta, dict) and isinstance(meta.get("dates"), list) and len(meta["dates"]) >= 2:
        try:
            _period_days([meta["dates"][0], meta["dates"][-1]])
        except ValidationError as exc:
            findings.append(f"{city}: meta.json dates {exc}")
        if summary.get("period") != [meta["dates"][0], meta["dates"][-1]]:
            findings.append(f"{city}: summary period disagrees with meta.json first/last dates")
    if points_path.is_file():
        try:
            points = load_json(points_path)
            findings.extend(f"{city}: points.json {issue}" for issue in _walk_nonfinite_or_empty(points))
            if isinstance(points, list) and isinstance(meta, dict) and isinstance(meta.get("dates"), list):
                expected_dates = meta["dates"]
                for index, point in enumerate(points):
                    if not isinstance(point, dict):
                        findings.append(f"{city}: points.json entry {index} is not an object")
                        continue
                    dates = point.get("dates")
                    values = point.get("disp_cm")
                    if dates != expected_dates:
                        findings.append(f"{city}: points.json entry {index} dates disagree with meta.json")
                    if isinstance(values, list) and isinstance(dates, list) and len(values) != len(dates):
                        findings.append(f"{city}: points.json entry {index} disp_cm length differs from dates")
        except (OSError, json.JSONDecodeError, ValidationError) as exc:
            findings.append(f"{city}: invalid points.json: {exc}")
    known_files = {p.resolve() for p in (summary_path, meta_path, points_path)}
    for extra_path in directory.rglob("*.json"):
        if extra_path.resolve() in known_files:
            continue
        try:
            extra = load_json(extra_path)
            findings.extend(f"{city}: {extra_path.relative_to(directory).as_posix()} {issue}"
                            for issue in _walk_nonfinite_or_empty(extra))
        except (OSError, json.JSONDecodeError, ValidationError) as exc:
            findings.append(f"{city}: invalid {extra_path.relative_to(directory).as_posix()}: {exc}")

    for key in ("max_subsidence_cm", "period", "rate_cm_per_100d", "p2_cm", "confidence", "valid_fraction", "ref_range_cm", "reference_point", "quality"):
        if key not in summary or summary[key] is None or summary[key] == "":
            findings.append(f"{city}: summary.json missing required field {key}")
    reference_point = summary.get("reference_point")
    if not isinstance(reference_point, dict) or not all(_finite_number(reference_point.get(k)) for k in ("lon", "lat")):
        findings.append(f"{city}: reference_point must contain finite lon and lat")
    elif not (-180 <= float(reference_point["lon"]) <= 180 and -90 <= float(reference_point["lat"]) <= 90):
        findings.append(f"{city}: reference_point coordinates outside lon/lat limits")
    bbox = summary.get("bbox", meta.get("bbox"))
    findings.extend(_bbox_findings(city, bbox))

    try:
        days = _period_days(summary.get("period"))
        headline = summary.get("max_subsidence_cm")
        stored_rate = summary.get("rate_cm_per_100d")
        if not _finite_number(headline):
            findings.append(f"{city}: max_subsidence_cm is not finite numeric")
        elif not _finite_number(stored_rate):
            findings.append(f"{city}: rate_cm_per_100d is missing or non-numeric")
        else:
            expected = float(headline) * 100.0 / days
            if abs(float(stored_rate) - expected) > RATE_TOL_CM_PER_100D:
                findings.append(f"{city}: rate_cm_per_100d {float(stored_rate):.4f} disagrees with headline/days×100 {expected:.4f}")
        if _finite_number(headline) and _finite_number(atlas_region.get("rate_cm_per_100d")):
            expected = float(headline) * 100.0 / days
            atlas_rate = float(atlas_region["rate_cm_per_100d"])
            if abs(atlas_rate - expected) > RATE_TOL_CM_PER_100D:
                findings.append(f"{city}: atlas rate_cm_per_100d {atlas_rate:.4f} disagrees with summary headline/dates {expected:.4f}")
    except ValidationError as exc:
        findings.append(f"{city}: {exc}")

    findings.extend(_confidence_checks(city, summary, "summary"))
    findings.extend(_reference_checks(city, summary, meta, atlas_region))
    if isinstance(meta, dict) and meta.get("quality") and summary.get("quality") != meta.get("quality"):
        findings.append(f"{city}: summary quality disagrees with meta.json quality")

    # Check atlas values against the underlying city summary where both exist.
    pairs = (("max_cm_los", "max_subsidence_cm"), ("rate_cm_per_100d", "rate_cm_per_100d"),
             ("p2_cm", "p2_cm"), ("confidence", "confidence"), ("valid_fraction", "valid_fraction"),
             ("ref_range_cm", "ref_range_cm"), ("period", "period"))
    for atlas_key, summary_key in pairs:
        if atlas_key not in atlas_region:
            findings.append(f"{city}: atlas region missing {atlas_key}")
        elif summary_key in summary and summary[summary_key] is not None:
            left, right = atlas_region[atlas_key], summary[summary_key]
            if _finite_number(left) and _finite_number(right):
                if abs(float(left) - float(right)) > (RATE_TOL_CM_PER_100D if atlas_key == "rate_cm_per_100d" else 1e-6):
                    findings.append(f"{city}: atlas.{atlas_key}={left!r} disagrees with summary.{summary_key}={right!r}")
            elif left != right:
                findings.append(f"{city}: atlas.{atlas_key}={left!r} disagrees with summary.{summary_key}={right!r}")
    findings.extend(_confidence_checks(city, atlas_region, "atlas"))
    return findings, summary


def validate() -> tuple[list[str], int, int]:
    issues: list[str] = []
    try:
        atlas = load_json(ATLAS_PATH)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        return [f"atlas.json invalid: {exc}"], 0, 1
    if not isinstance(atlas, dict) or not isinstance(atlas.get("regions"), list):
        return ["atlas.json must contain a regions array"], 0, 1
    issues.extend(f"atlas.json {issue}" for issue in _walk_nonfinite_or_empty(atlas))

    regions = atlas["regions"]
    by_id: dict[str, dict[str, Any]] = {}
    for region in regions:
        if not isinstance(region, dict):
            issues.append("atlas.json regions contains a non-object entry")
            continue
        city = str(region.get("id") or region.get("name") or "unknown")
        if not region.get("id"):
            issues.append(f"{city}: atlas region missing id")
        by_id[city] = region

    classification_ids: dict[str, set[str]] = {"reliable": set(), "indicative": set()}
    for bucket in ("reliable", "indicative"):
        entries = atlas.get(bucket)
        if not isinstance(entries, list):
            issues.append(f"atlas.json {bucket} must be an array")
            continue
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict) or not entry.get("id"):
                issues.append(f"atlas.json {bucket}[{index}] missing id/object")
                continue
            city = str(entry["id"])
            classification_ids[bucket].add(city)
            if city not in by_id:
                issues.append(f"atlas.json {bucket} contains {city}, absent from regions")
                continue
            for field in ("rate_cm_per_100d", "p2_cm", "confidence", "valid_fraction", "ref_range_cm", "period"):
                if field not in entry or entry[field] is None:
                    issues.append(f"atlas.json {bucket}[{city}] missing/empty {field}")
            findings = _confidence_checks(city, entry, f"atlas.{bucket}")
            issues.extend(findings)
            expected_confidence = by_id[city].get("confidence")
            actual_confidence = entry.get("confidence")
            if actual_confidence != expected_confidence:
                issues.append(f"atlas.json {bucket}[{city}] confidence disagrees with regions")
            if bucket == "indicative" and actual_confidence != "low":
                issues.append(f"atlas.json indicative entry {city} is not confidence=low")
            if bucket == "reliable" and actual_confidence == "low":
                issues.append(f"atlas.json reliable entry {city} is confidence=low")
    overlap = classification_ids["reliable"] & classification_ids["indicative"]
    if overlap:
        issues.append(f"atlas.json reliable/indicative lists overlap: {sorted(overlap)}")
    listed_ids = classification_ids["reliable"] | classification_ids["indicative"]
    region_ids = set(by_id)
    if listed_ids != region_ids:
        issues.append(f"atlas.json reliable/indicative coverage differs from regions; missing={sorted(region_ids-listed_ids)}, extra={sorted(listed_ids-region_ids)}")

    city_dirs: dict[str, Path] = {}
    for city, region in by_id.items():
        rel = Path(str(region.get("path", f"data/global/{city}/")))
        directory = (ROOT / rel).resolve()
        if ROOT.resolve() not in directory.parents and directory != ROOT.resolve():
            issues.append(f"{city}: atlas path escapes repository")
            continue
        city_dirs[city] = directory
    global_root = ROOT / "data/global"
    if global_root.is_dir():
        for directory in global_root.iterdir():
            if directory.is_dir():
                city_dirs.setdefault(directory.name, directory)

    summaries: dict[str, dict[str, Any]] = {}
    for city, directory in sorted(city_dirs.items()):
        region = by_id.get(city, {})
        if city not in by_id and (directory / "summary.json").is_file():
            issues.append(f"{city}: city data folder has summary.json but no atlas.json region entry")
        city_issues, summary = _check_summary(city, directory, region)
        issues.extend(city_issues)
        if summary is not None:
            summaries[city] = summary

    for city, region in by_id.items():
        for field in ("rate_cm_per_100d", "p2_cm", "confidence", "valid_fraction", "ref_range_cm", "period"):
            if field not in region or region[field] is None:
                issues.append(f"{city}: atlas region missing/empty {field}")

    rates: list[tuple[str, float]] = []
    derived_rates: list[tuple[str, float]] = []
    for city, region in by_id.items():
        rate = region.get("rate_cm_per_100d")
        if _finite_number(rate):
            rates.append((city, float(rate)))
        summary = summaries.get(city)
        if summary and _finite_number(summary.get("max_subsidence_cm")):
            try:
                days = _period_days(summary.get("period"))
                derived_rates.append((city, float(summary["max_subsidence_cm"]) * 100.0 / days))
            except ValidationError:
                pass
    actual_order = [str(r.get("id", "unknown")) for r in regions if isinstance(r, dict)]
    if len(rates) == len(regions):
        expected_order = [name for name, _ in sorted(rates, key=lambda item: item[1])]
        if actual_order != expected_order:
            issues.append("atlas.json regions are not sorted by ascending rate_cm_per_100d")
    elif len(derived_rates) == len(regions):
        expected_order = [name for name, _ in sorted(derived_rates, key=lambda item: item[1])]
        if actual_order != expected_order:
            issues.append("atlas.json order disagrees with rates derived from city summaries")
        else:
            issues.append("atlas.json order matches summary-derived rates, but stored rate_cm_per_100d fields are missing")
    else:
        issues.append("atlas.json ranking cannot be validated: stored and summary-derived rate_cm_per_100d values are incomplete")
    return issues, len(city_dirs), len(regions)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    issues, city_count, atlas_count = validate()
    print(f"Atlas regions: {atlas_count}; city folders checked: {city_count}")
    if not issues:
        print("PASS: atlas contract checks are clean")
        return 0
    warning_markers = ("not verifiable", "not verified", "proxy passes")
    info_markers = ("order matches summary-derived rates",)
    warnings = [issue for issue in issues if any(marker in issue for marker in warning_markers)]
    infos = [issue for issue in issues if any(marker in issue for marker in info_markers)]
    errors = [issue for issue in issues if issue not in warnings and issue not in infos]
    for issue in issues:
        print(f"- {issue}")
    print(f"Findings: {len(issues)}; errors: {len(errors)}; warnings: {len(warnings)}; info: {len(infos)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
