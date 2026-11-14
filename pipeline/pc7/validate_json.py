#!/usr/bin/env python3
"""Offline strict JSON and quality-field audit for data/**/*.json."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def reject_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant {value}")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_constant=reject_constant)


def non_finite_paths(value: Any, prefix: str = "$" ) -> list[str]:
    found: list[str] = []
    if isinstance(value, float) and not math.isfinite(value):
        found.append(prefix)
    elif isinstance(value, dict):
        for key, child in value.items():
            found.extend(non_finite_paths(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(non_finite_paths(child, f"{prefix}[{index}]"))
    return found


def has_quality(value: Any) -> bool:
    if isinstance(value, dict):
        quality = value.get("quality")
        if isinstance(quality, str) and quality.strip():
            return True
        # Catalog entries carry quality per layer record, by contract.
        if isinstance(value.get("layers"), list):
            return all(
                isinstance(layer, dict)
                and isinstance(layer.get("quality"), str)
                and bool(layer["quality"].strip())
                for layer in value["layers"]
            )
        return False
    if isinstance(value, list):
        return bool(value) and all(
            isinstance(item, dict)
            and isinstance(item.get("quality"), str)
            and bool(item["quality"].strip())
            for item in value
        )
    return False


def sibling_meta_quality(path: Path) -> bool:
    meta_path = path.parent / "meta.json"
    if path.name == "meta.json" or not meta_path.is_file():
        return False
    try:
        meta = load_json(meta_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        return False
    quality = meta.get("quality") if isinstance(meta, dict) else None
    return isinstance(quality, str) and bool(quality.strip())


def main() -> int:
    paths = sorted(DATA.rglob("*.json"))
    parse_errors: list[str] = []
    non_finite: list[str] = []
    missing_quality: list[str] = []
    inherited_quality: list[str] = []

    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        try:
            value = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            parse_errors.append(f"{rel}: {exc}")
            continue

        bad_values = non_finite_paths(value)
        non_finite.extend(f"{rel}{where[1:]}" for where in bad_values)

        if not has_quality(value):
            if sibling_meta_quality(path):
                inherited_quality.append(rel)
            else:
                missing_quality.append(rel)

    print(f"JSON files: {len(paths)}")
    print(f"Parse errors / non-standard constants: {len(parse_errors)}")
    for item in parse_errors:
        print(f"INVALID: {item}")
    print(f"Non-finite numeric values: {len(non_finite)}")
    for item in non_finite:
        print(f"NON_FINITE: {item}")
    print(f"Missing quality field: {len(missing_quality)}")
    for item in missing_quality:
        print(f"MISSING_QUALITY: {item}")
    print(f"Quality inherited from sibling meta.json: {len(inherited_quality)}")
    for item in inherited_quality:
        print(f"META_QUALITY: {item}")

    return 1 if parse_errors or non_finite or missing_quality else 0


if __name__ == "__main__":
    raise SystemExit(main())
