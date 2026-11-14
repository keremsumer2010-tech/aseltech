"""NISAR GUNW unwrapped phase -> line-of-sight (LOS) displacement in cm.

Owner: PC3. We use NISAR products as released by the NISAR project (NASA-JPL / ISRO);
we do NOT calibrate or correct them.

SIGN CONVENTION (verified 2026-11-14, see status/PC3.md):
  * ISCE3 forms the interferogram as reference * conj(secondary):
    https://github.com/isce-framework/isce3/blob/develop/cxx/isce3/signal/Crossmul.cpp
    ("ifgramUpsampled[...] = refSlcUpsampled[...]* std::conj(secSlcUpsampled[...])")
  * MintPy reads NISAR GUNW `unwrappedPhase` with no sign flip
    (https://github.com/insarlab/MintPy/blob/main/src/mintpy/prep_nisar.py) and converts with
    phase2range = -1 * WAVELENGTH / (4*pi)
    (https://github.com/insarlab/MintPy/blob/main/src/mintpy/ifgram_inversion.py),
    WAVELENGTH = c / centerFrequency read from the GUNW file.
  * MintPy FAQ: in metres, "positive value represents motion toward the satellite
    (uplift for pure vertical motion)" (https://github.com/insarlab/MintPy/blob/main/docs/FAQs.md).
  * NISAR ATBD notebook (https://github.com/nisar-solid/ATBD, methods/coseismic): negative LOS
    = moving away from the radar = subsidence for vertical motion.
  => disp_LOS = -lambda/(4*pi) * unwrapped_phase ; NEGATIVE = away from satellite = SUBSIDENCE.
  The GUNW product spec (JPL D-102272 Rev E) does not state the sign explicitly; we also check it
  empirically: known Central Valley subsidence bowls must come out negative.

Corrections: per https://nisar-docs.asf.alaska.edu/gunw the ionosphere phase screen and the
troposphere / solid-earth-tide layers are shipped in the product but NOT applied to
unwrappedPhase. We do not apply them either (first-pass, documented in meta.json notes).
"""
from __future__ import annotations

import numpy as np

C_LIGHT = 299_792_458.0  # m/s


def wavelength_from_frequency(center_frequency_hz: float) -> float:
    """lambda = c / f. Never hardcode lambda (rules/VERI_SOZLESMESI.md section 2)."""
    return C_LIGHT / float(center_frequency_hz)


def phase_to_cm(unw, wavelength_m: float):
    """Unwrapped phase [rad] -> LOS displacement [cm]. Negative = away from satellite (subsidence)."""
    unw = np.asarray(unw, dtype=np.float64)
    return (-wavelength_m / (4.0 * np.pi) * unw * 100.0).astype(np.float32)


def coh_to_float(coh):
    """Coherence stored as uint8 0-255 (data contract 4.1) -> float 0-1. Floats pass through."""
    coh = np.asarray(coh)
    if np.issubdtype(coh.dtype, np.integer):
        return coh.astype(np.float32) / 255.0
    return coh.astype(np.float32)


def mask_coherence(arr, coh, thr: float = 0.3):
    """Set pixels with coherence < thr (or NaN coherence) to NaN."""
    out = np.array(arr, dtype=np.float32, copy=True)
    c = coh_to_float(coh)
    out[~(c >= thr)] = np.nan
    return out


def mask_components(arr, conncomp):
    """connectedComponents == 0 means unreliable unwrapping (docs/qa/PC1.md) -> NaN."""
    out = np.array(arr, dtype=np.float32, copy=True)
    out[np.asarray(conncomp) == 0] = np.nan
    return out


def reference(arr, ref_rc, radius: int = 3):
    """Subtract the NaN-median of a (2r+1)x(2r+1) window centred at ref_rc=(row, col).

    Raises ValueError if the window has no valid pixel (a sum over pairs with a missing
    reference would be meaningless).
    """
    r, c = int(ref_rc[0]), int(ref_rc[1])
    a = np.asarray(arr, dtype=np.float32)
    win = a[max(r - radius, 0): r + radius + 1, max(c - radius, 0): c + radius + 1]
    if not np.isfinite(win).any():
        raise ValueError(f"reference window at {ref_rc} has no valid pixels")
    return (a - np.nanmedian(win)).astype(np.float32)


def los_to_vertical(cm, incidence_deg):
    """Approximation assuming purely vertical motion: d_vert = d_los / cos(incidence)."""
    return (np.asarray(cm, dtype=np.float32) / np.cos(np.deg2rad(incidence_deg))).astype(np.float32)


def remove_islands(arr, min_px: int = 200):
    """NaN out valid regions (8-connected) smaller than min_px. Small isolated patches surrounded by
    masked pixels are where unwrapping cycle errors (+-2pi = lambda/2) survive the coherence mask."""
    from scipy.ndimage import label
    a = np.array(arr, dtype=np.float32, copy=True)
    lab, n = label(np.isfinite(a), structure=np.ones((3, 3), bool))
    if n == 0:
        return a
    sizes = np.bincount(lab.ravel())
    small = sizes < min_px
    small[0] = False
    a[small[lab]] = np.nan
    return a


def cycle_outliers(arr, thr_cm: float, block: int = 9):
    """NaN pixels deviating more than thr_cm from the NaN-median of their block x block tile.

    Use thr_cm = lambda/4 in cm (half an unwrapping cycle): a pixel that jumped by a full 2*pi
    (lambda/2) relative to its 720 m neighbourhood is an unwrapping error, not ground motion
    in a 12-24 day pair.
    """
    a = np.array(arr, dtype=np.float32, copy=True)
    H, W = a.shape
    Hp, Wp = -(-H // block) * block, -(-W // block) * block
    pad = np.full((Hp, Wp), np.nan, np.float32)
    pad[:H, :W] = a
    tiles = pad.reshape(Hp // block, block, Wp // block, block)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        med = np.nanmedian(tiles, axis=(1, 3))
    full = np.repeat(np.repeat(med, block, 0), block, 1)[:H, :W]
    a[np.abs(a - full) > thr_cm] = np.nan
    return a


def deramp(arr, order: int = 1, step: int = 4):
    """Remove a best-fit plane (order=1) or quadratic surface (order=2) fitted to finite pixels.

    Standard InSAR step for long-wavelength residuals (orbit/atmosphere), as MintPy's `deramp`
    (https://github.com/insarlab/MintPy/blob/main/src/mintpy/objects/ramp.py). It can also remove part of a
    genuine scene-wide signal; callers must document its use. Fitting uses every `step`-th pixel for speed.
    """
    a = np.asarray(arr, dtype=np.float32)
    H, W = a.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    yy /= H
    xx /= W
    cols = [np.ones_like(xx), xx, yy] + ([xx * xx, yy * yy, xx * yy] if order == 2 else [])
    G = np.stack([c.ravel() for c in cols], axis=1)
    sub = np.zeros((H, W), bool)
    sub[::step, ::step] = True
    ok = (np.isfinite(a) & sub).ravel()
    if ok.sum() < G.shape[1] * 10:
        raise ValueError("too few valid pixels to fit a ramp")
    coef, *_ = np.linalg.lstsq(G[ok], a.ravel()[ok].astype(np.float64), rcond=None)
    return (a - (G @ coef).reshape(H, W)).astype(np.float32)


def choose_reference(coh, valid=None, radius: int = 3, stride: int = 5, exclude=None):
    """Pick the (row, col) whose (2r+1)^2 window is fully valid and has the highest mean coherence.

    coh: coherence (uint8 or float); valid: optional bool mask (e.g. finite in ALL pairs);
    exclude: optional bool mask of pixels not allowed as centre (e.g. known subsidence area).
    Deterministic; returns (row, col, mean_coh).
    """
    c = coh_to_float(coh)
    ok = np.isfinite(c) if valid is None else (np.asarray(valid, bool) & np.isfinite(c))
    best = (-1.0, None)
    H, W = c.shape
    for r in range(radius, H - radius, stride):
        for q in range(radius, W - radius, stride):
            if exclude is not None and exclude[r, q]:
                continue
            sl = (slice(r - radius, r + radius + 1), slice(q - radius, q + radius + 1))
            if not ok[sl].all():
                continue
            m = float(c[sl].mean())
            if m > best[0]:
                best = (m, (r, q))
    if best[1] is None:
        raise ValueError("no fully valid reference window found")
    return best[1][0], best[1][1], best[0]


def pair_to_cm(unw, coh, wavelength_m, ref_rc, thr=0.3, radius=3, conncomp=None):
    """Full per-pair chain: phase -> cm -> masks -> referenced. Same ref_rc for every pair."""
    cm = phase_to_cm(unw, wavelength_m)
    if conncomp is not None:
        cm = mask_components(cm, conncomp)
    cm = mask_coherence(cm, coh, thr)
    return reference(cm, ref_rc, radius)
