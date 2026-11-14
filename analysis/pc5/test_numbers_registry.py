"""Unit tests for analysis.pc5.numbers_registry."""
from __future__ import annotations

import json
from pathlib import Path

from analysis.pc5.numbers_registry import (
    build_canonical_entries,
    scan_documents,
    write_registry_outputs,
)


def test_canonical_entries_nonempty_and_sourced() -> None:
    entries = build_canonical_entries()
    assert len(entries) >= 15
    ids = {e["id"] for e in entries}
    assert "cv_max_los_cm" in ids
    assert "kp_max_los_cm" in ids
    for e in entries:
        assert e["verdict"] in {"approved", "preliminary", "rejected"}
        assert e["source_file"]
        assert e["source_key"]


def test_scan_and_write_outputs(tmp_path: Path) -> None:
    entries = build_canonical_entries()
    discrepancies = scan_documents(entries)
    j_out = tmp_path / "numbers_registry.json"
    m_out = tmp_path / "numbers_registry.md"
    payload = write_registry_outputs(entries, discrepancies, json_out=j_out, md_out=m_out)

    assert j_out.exists() and m_out.exists()
    parsed = json.loads(j_out.read_text(encoding="utf-8"))
    assert parsed["summary"]["total"] == len(entries)
    cv_entry = next(e for e in parsed["entries"] if e["id"] == "cv_max_los_cm")
    assert len(cv_entry["used_in"]) >= 1
    assert "Numbers Registry" in m_out.read_text(encoding="utf-8")
