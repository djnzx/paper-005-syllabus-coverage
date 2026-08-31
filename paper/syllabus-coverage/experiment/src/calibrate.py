"""Threshold calibration (manuscript Sec. 6.4-6.5, RQ3).

tau is never fixed silently. We pick tau on a development fold to hit a target
false-coverage rate (FCR), then evaluate on a held-out fold, so the reported tau
is calibrated rather than fitted to the test set.
"""
from __future__ import annotations

import numpy as np

from metrics import gap_metrics
from common import SEED


def sweep(gold_gap: np.ndarray, s: np.ndarray, grid=None):
    """Return list of (tau, metrics-dict) across a threshold grid."""
    grid = np.linspace(0.0, 1.0, 101) if grid is None else grid
    rows = []
    for tau in grid:
        pred_gap = (s < tau).astype(int)
        rows.append((float(tau), gap_metrics(gold_gap, pred_gap)))
    return rows


def tau_for_target_fcr(gold_gap: np.ndarray, s: np.ndarray,
                       target_fcr: float = 0.10, grid=None) -> float:
    """Smallest tau whose FCR <= target (least reviewer burden meeting the safety bar).

    Lower tau marks fewer gaps -> higher FCR; raising tau lowers FCR. We pick the
    smallest tau achieving the target so we do not over-flag.
    """
    grid = np.linspace(0.0, 1.0, 101) if grid is None else grid
    feasible = []
    for tau in grid:
        pred_gap = (s < tau).astype(int)
        fcr = gap_metrics(gold_gap, pred_gap)["false_coverage_rate"]
        if not np.isnan(fcr) and fcr <= target_fcr:
            feasible.append(tau)
    return float(min(feasible)) if feasible else 1.0


def kfold_calibration(gold_gap: np.ndarray, s: np.ndarray, k: int = 5,
                      target_fcr: float = 0.10, seed: int = SEED):
    """Calibrate tau on train folds, evaluate on the held-out fold.

    Returns per-fold (tau*, test metrics) so we can report that a dev-calibrated
    tau generalises (RQ3). With ~47 clauses, k=5 keeps folds non-trivial.
    """
    rng = np.random.default_rng(seed)
    m = len(gold_gap)
    idx = rng.permutation(m)
    folds = np.array_split(idx, k)
    results = []
    for i in range(k):
        test = folds[i]
        train = np.concatenate([folds[j] for j in range(k) if j != i])
        tau = tau_for_target_fcr(gold_gap[train], s[train], target_fcr)
        pred_gap = (s[test] < tau).astype(int)
        results.append((float(tau), gap_metrics(gold_gap[test], pred_gap)))
    return results
