"""Permanent vs. seasonal subsidence decomposition and InSAR uncertainty budget (PC5).

Modules:
    decompose: Vectorized per-pixel linear trend + annual sinusoid least-squares fit.
    error_budget: Empirical per-pair noise, chain propagation, ionosphere bounds, and GNSS summary.
    point_quality: Per-point linear regression quality and phase-unwrapping jump diagnostics.
"""

from .error_budget import (
    compute_error_budget,
    ionosphere_stats_cm,
    phase_to_los_cm,
    propagate_chain_std,
    summarize_gnss_validation,
)
from .point_quality import analyze_point_series, analyze_points_file

__all__ = [
    "analyze_point_series",
    "analyze_points_file",
    "compute_error_budget",
    "ionosphere_stats_cm",
    "phase_to_los_cm",
    "propagate_chain_std",
    "summarize_gnss_validation",
]

try:
    from .decompose import (
        REASON_CODES,
        DecompResult,
        dates_to_years,
        decompose,
        summarize_decomposition,
    )

    __all__.extend([
        "REASON_CODES",
        "DecompResult",
        "dates_to_years",
        "decompose",
        "summarize_decomposition",
    ])
except ImportError:
    pass
