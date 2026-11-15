"""Validate data/global/atlas.json against data/global/atlas.schema.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "data" / "global" / "atlas.json"
SCHEMA_PATH = ROOT / "data" / "global" / "atlas.schema.json"


def _check_type(val, expected) -> bool:
    type_map = {
        "string": lambda v: isinstance(v, str),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        "boolean": lambda v: isinstance(v, bool),
        "array": lambda v: isinstance(v, list),
        "object": lambda v: isinstance(v, dict),
        "null": lambda v: v is None,
    }
    allowed = expected if isinstance(expected, list) else [expected]
    return any(type_map[t](val) for t in allowed)


def test_atlas_matches_schema() -> None:
    atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    # Optional jsonschema validation if available
    try:
        import jsonschema  # type: ignore

        jsonschema.validate(instance=atlas, schema=schema)
    except ImportError:
        pass

    # Built-in strict structural validation (always runs)
    for req in schema["required"]:
        assert req in atlas, f"Missing top-level required key: {req}"
    for key, spec in schema["properties"].items():
        if key in atlas and "type" in spec:
            assert _check_type(atlas[key], spec["type"]), f"Top-level {key} type mismatch"

    assert atlas["n_regions"] == len(atlas["regions"])
    assert atlas["n_reliable"] == len(atlas["reliable"])
    assert atlas["n_indicative"] == len(atlas["indicative"])
    assert atlas["n_reliable"] + atlas["n_indicative"] == atlas["n_regions"]
    assert "NISAR data are provisional." in atlas["quality_note"]

    reg_schema = schema["definitions"]["region"]
    seen_ids = set()
    for idx, reg in enumerate(atlas["regions"]):
        for req in reg_schema["required"]:
            assert req in reg, f"Region[{idx}] ({reg.get('id')}) missing required key: {req}"
        assert reg["id"] not in seen_ids, f"Duplicate region id: {reg['id']}"
        seen_ids.add(reg["id"])
        for key, spec in reg_schema["properties"].items():
            if key not in reg:
                continue
            val = reg[key]
            assert _check_type(val, spec["type"]), f"{reg['id']}.{key} type mismatch: {type(val)}"
            if val is not None and "enum" in spec:
                assert val in spec["enum"], f"{reg['id']}.{key}={val} not in {spec['enum']}"
            if val is not None and "pattern" in spec and isinstance(val, str):
                assert re.match(spec["pattern"], val), f"{reg['id']}.{key}={val} failed pattern"
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                if "minimum" in spec:
                    assert val >= spec["minimum"], f"{reg['id']}.{key}={val} < {spec['minimum']}"
                if "maximum" in spec:
                    assert val <= spec["maximum"], f"{reg['id']}.{key}={val} > {spec['maximum']}"
