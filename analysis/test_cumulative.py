import numpy as np

from cumulative import chain, to_latlon_grid
from gunw_io import quality_for


def _mk(tmp_path, d1, d2, q="provisional"):
    p = tmp_path / f"{d1}_{d2}.npz"
    np.savez_compressed(p, unw=np.zeros((2, 2), np.float32), date1=d1, date2=d2, quality=q)
    return p


def test_chain_stops_at_gap_and_skips_beta(tmp_path):
    files = [_mk(tmp_path, "2026-06-16", "2026-06-28", "beta-precal"),
             _mk(tmp_path, "2026-06-28", "2026-07-10"),
             _mk(tmp_path, "2026-07-10", "2026-07-22"),
             _mk(tmp_path, "2026-08-15", "2026-08-27")]
    used, notes = chain(sorted(files))
    assert [u[0] for u in used] == ["2026-06-28", "2026-07-10"]
    assert any("beta-precal" in n for n in notes)
    assert any("gap 2026-07-22 -> 2026-08-15" in n for n in notes)


def test_quality_rule():
    assert quality_for("2026-06-16", "2026-06-28", "P05023") == "beta-precal"
    assert quality_for("2026-06-28", "2026-07-10", "P05023") == "provisional"
    assert quality_for("2026-06-28", "2026-07-10", "P04000") == "beta-precal"


def test_latlon_resample_is_north_up():
    # UTM 11N grid, value = row index; north (small row) must land at top of output
    x = np.arange(240000, 250000, 80.0)
    y = np.arange(3960000, 3950000, -80.0)
    arr = np.tile(np.arange(len(y), dtype=np.float32)[:, None], (1, len(x)))
    from pyproj import Transformer
    lon0, lat0 = Transformer.from_crs(32611, 4326, always_xy=True).transform(245000, 3955000)
    g = to_latlon_grid(arr, x, y, 32611, (lon0 - 0.02, lat0 - 0.02, lon0 + 0.02, lat0 + 0.02))
    col = g[:, g.shape[1] // 2]
    col = col[np.isfinite(col)]
    assert col[0] < col[-1]


def test_chain_mixed_mode_accepts_beta(tmp_path):
    files = [_mk(tmp_path, "2026-06-04", "2026-06-16", "beta-precal"),
             _mk(tmp_path, "2026-06-16", "2026-06-28", "beta-precal"),
             _mk(tmp_path, "2026-06-28", "2026-07-10")]
    used, _ = chain(sorted(files), ("provisional", "beta-precal"))
    assert [u[0] for u in used] == ["2026-06-04", "2026-06-16", "2026-06-28"]
    used, _ = chain(sorted(files))
    assert [u[0] for u in used] == ["2026-06-28"]
