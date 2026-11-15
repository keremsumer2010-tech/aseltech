from __future__ import annotations

import numpy as np
import pytest
from pyproj import Transformer

from pipeline.pc7.run_atlas_city import choose_reference_window


def _pair(path, x, y, epsg, invalid: tuple[tuple[int, int], ...] = ()) -> None:
    unw = np.ones((7, 7), dtype=np.float32)
    coh = np.full((7, 7), 255, dtype=np.uint8)
    for row, col in invalid:
        coh[row, col] = 0
    np.savez_compressed(path, x=x, y=y, epsg=np.int32(epsg), unw=unw, coh=coh)


def test_reference_window_accepts_one_masked_pixel(tmp_path) -> None:
    epsg = 32650
    anchor = (116.31, 40.10)
    forward = Transformer.from_crs(4326, f"EPSG:{epsg}", always_xy=True)
    center_x, center_y = forward.transform(*anchor)
    x = center_x + (np.arange(7) - 3) * 80.0
    y = center_y + (np.arange(7) - 3) * 80.0
    first, second = tmp_path / "first.npz", tmp_path / "second.npz"
    _pair(first, x, y, epsg)
    _pair(second, x, y, epsg, invalid=((0, 0),))

    row, col, coherence, *_ = choose_reference_window([first, second], anchor)

    assert (row, col) == (3, 3)
    assert coherence > 0.98


def test_reference_window_rejects_two_masked_pixels(tmp_path) -> None:
    epsg = 32650
    anchor = (116.31, 40.10)
    forward = Transformer.from_crs(4326, f"EPSG:{epsg}", always_xy=True)
    center_x, center_y = forward.transform(*anchor)
    x = center_x + (np.arange(7) - 3) * 80.0
    y = center_y + (np.arange(7) - 3) * 80.0
    first, second = tmp_path / "first.npz", tmp_path / "second.npz"
    _pair(first, x, y, epsg)
    _pair(second, x, y, epsg, invalid=((0, 0), (0, 1)))

    with pytest.raises(ValueError, match="no common-valid 7x7"):
        choose_reference_window([first, second], anchor)
