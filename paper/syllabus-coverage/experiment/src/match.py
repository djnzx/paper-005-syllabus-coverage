"""Similarity, per-clause best match, and the partial-function verdict.

Implements manuscript Sec. 6.3-6.4:
  sim(c_i, l_j) = cosine,  s_i = max_j sim,  j*_i = argmax_j sim,
  v(c_i) = l_{j*}  if s_i >= tau   else  undefined (a gap).
"""
from __future__ import annotations

import numpy as np


def sim_matrix(C: np.ndarray, L: np.ndarray) -> np.ndarray:
    """Cosine similarity; inputs are already L2-normalised, so dot product."""
    return C @ L.T


def best_match(sim: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (s_i, j*_i): best score and best outcome index per clause."""
    jstar = np.argmax(sim, axis=1)
    s = sim[np.arange(sim.shape[0]), jstar]
    return s, jstar


def covered_mask(s: np.ndarray, tau: float) -> np.ndarray:
    """True where the clause is covered (s_i >= tau)."""
    return s >= tau


def pred_gap_vector(s: np.ndarray, tau: float) -> np.ndarray:
    """gap prediction = 1 when s_i < tau (the positive class)."""
    return (s < tau).astype(int)
