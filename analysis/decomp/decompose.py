"""Permanent vs recoverable subsidence: per-pixel trend + annual sinusoid (tasks/PC5.md, Task 1).

Model (t in decimal years, e.g. 2026.5):
    d(t) = a + v*(t - t0) + A*sin(2*pi*t) + B*cos(2*pi*t)
  v           permanent (secular) rate, cm/yr  -> inelastic, mostly non-recoverable compaction
  C=sqrt(A^2+B^2)  seasonal amplitude, cm      -> elastic, recoverable part (half of peak-to-peak)
  phase       month of the seasonal LOW (deepest point of the annual cycle)
Fit: weighted least squares per pixel, NaN = weight 0. Vectorised: the 4x4 normal equations of every
pixel are built with one einsum and solved with one batched np.linalg.solve (no Python loop over pixels).
Uncertainties: sigma^2 = RSS/(n-4), cov = sigma^2 (G^T G)^-1 (assumes independent, equal-variance
epochs; cumulative InSAR epochs are NOT independent, so standard errors are optimistic -> report as such).
Pixels with < MIN_POINTS valid epochs or a valid span < MIN_SPAN_YR are NaN with a reason code.

Owner note: written by PC3 on Mehmet's instruction (2026-11-14 14:11 TR), path owned by PC5.
"""
from __future__ import annotations

from datetime import date

import numpy as np

MIN_POINTS = 8
MIN_SPAN_YR = 0.75  # 9 months: shorter spans cannot separate trend from the annual term
REASON = {0: "ok", 1: "fewer than 8 valid epochs", 2: "valid span shorter than 9 months", 3: "singular fit"}


def decimal_year(d) -> float:
    """'2026-07-01' or datetime.date -> 2026.4959 (day-of-year based)."""
    if isinstance(d, str):
        d = date.fromisoformat(d)
    start = date(d.year, 1, 1)
    days = (date(d.year + 1, 1, 1) - start).days
    return d.year + (d - start).days / days


def fit(t_years, data, t0=None):
    """Fit the model to data of shape (T, ...) (e.g. (T, H, W) cumulative cm stack).

    Returns dict of arrays shaped like data.shape[1:]:
      v_cm_per_yr, amp_cm, low_month (1-12), a_cm, v_se, amp_se, r2, n_valid, reason (int, see REASON)
    """
    t = np.asarray(t_years, dtype=np.float64)
    D = np.asarray(data, dtype=np.float64)
    T = t.size
    if D.shape[0] != T:
        raise ValueError("time axis length mismatch")
    shp = D.shape[1:]
    Y = D.reshape(T, -1)                                    # (T, P)
    W = np.isfinite(Y)
    Yz = np.where(W, Y, 0.0)
    t0 = float(np.mean(t)) if t0 is None else float(t0)
    G = np.stack([np.ones(T), t - t0, np.sin(2 * np.pi * t), np.cos(2 * np.pi * t)], axis=1)  # (T, 4)

    Wf = W.astype(np.float64)
    N = np.einsum("tp,ti,tj->pij", Wf, G, G)               # (P, 4, 4)
    rhs = np.einsum("tp,ti,tp->pi", Wf, G, Yz)              # (P, 4)
    n = W.sum(axis=0)
    tt = np.where(W, t[:, None], np.nan)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # all-NaN pixels -> span NaN -> 0 below
        span = np.nanmax(tt, axis=0) - np.nanmin(tt, axis=0)
    span = np.nan_to_num(span, nan=0.0)

    reason = np.zeros(Y.shape[1], np.int8)
    reason[n < MIN_POINTS] = 1
    reason[(reason == 0) & (span < MIN_SPAN_YR)] = 2
    ok = reason == 0
    cond = np.full(Y.shape[1], np.inf)
    if ok.any():
        cond[ok] = np.linalg.cond(N[ok])
    reason[ok & ~(cond < 1e10)] = 3
    ok = reason == 0

    coef = np.full((Y.shape[1], 4), np.nan)
    cov = np.full((Y.shape[1], 4, 4), np.nan)
    r2 = np.full(Y.shape[1], np.nan)
    if ok.any():
        Ninv = np.linalg.inv(N[ok])
        c = np.einsum("pij,pj->pi", Ninv, rhs[ok])
        coef[ok] = c
        resid = np.where(W[:, ok], Y[:, ok] - G @ c.T, 0.0)
        rss = (resid ** 2).sum(axis=0)
        mean = Yz[:, ok].sum(axis=0) / n[ok]
        tss = (np.where(W[:, ok], Y[:, ok] - mean, 0.0) ** 2).sum(axis=0)
        dof = np.maximum(n[ok] - 4, 1)
        s2 = rss / dof
        cov[ok] = Ninv * s2[:, None, None]
        with np.errstate(divide="ignore", invalid="ignore"):
            r2[ok] = np.where(tss > 0, 1 - rss / tss, np.nan)

    a, v, A, B = coef.T
    amp = np.hypot(A, B)
    with np.errstate(divide="ignore", invalid="ignore"):
        # var(amp) by linear error propagation of sqrt(A^2+B^2)
        amp_var = (A ** 2 * cov[:, 2, 2] + B ** 2 * cov[:, 3, 3] + 2 * A * B * cov[:, 2, 3]) / amp ** 2
    # A sin(x) + B cos(x) = C cos(x - phi), phi = atan2(A, B): max at t = phi/2pi, low half a year later
    t_low = (np.arctan2(A, B) / (2 * np.pi) + 0.5) % 1.0
    low_month = np.where(np.isfinite(t_low), np.floor(t_low * 12) + 1, np.nan)

    def r(x):
        return np.asarray(x, dtype=np.float32).reshape(shp)

    return {
        "a_cm": r(a), "v_cm_per_yr": r(v), "amp_cm": r(amp), "low_month": r(low_month),
        "v_se": r(np.sqrt(cov[:, 1, 1])), "amp_se": r(np.sqrt(amp_var)), "r2": r(r2),
        "n_valid": n.reshape(shp).astype(np.int16), "reason": reason.reshape(shp), "t0": t0,
    }
