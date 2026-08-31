"""Statistical helpers: bootstrap CI, McNemar's test, Cohen's kappa.

Also runnable as a CLI for the annotation kappa check:
    python src/stats.py --kappa data/gold_or.csv data/gold_a2.csv
"""
from __future__ import annotations

import csv
import sys

import numpy as np

from common import SEED


def bootstrap_ci(gold_gap, pred_gap, metric_fn, n: int = 10000, seed: int = SEED):
    """Percentile 95% CI of a metric by resampling clauses with replacement."""
    rng = np.random.default_rng(seed)
    gold_gap = np.asarray(gold_gap)
    pred_gap = np.asarray(pred_gap)
    m = len(gold_gap)
    point = metric_fn(gold_gap, pred_gap)
    vals = []
    for _ in range(n):
        idx = rng.integers(0, m, m)
        v = metric_fn(gold_gap[idx], pred_gap[idx])
        if not np.isnan(v):
            vals.append(v)
    lo, hi = np.percentile(vals, [2.5, 97.5]) if vals else (float("nan"), float("nan"))
    return float(point), float(lo), float(hi)


def mcnemar(correct_a: np.ndarray, correct_b: np.ndarray):
    """Paired test on per-clause correctness of two methods.

    Returns (b, c, p) where b = A right & B wrong, c = A wrong & B right.
    Exact binomial p (two-sided) on the discordant pairs -- right for small n.
    """
    from scipy.stats import binomtest

    a = np.asarray(correct_a).astype(bool)
    b_arr = np.asarray(correct_b).astype(bool)
    b = int(np.sum(a & ~b_arr))
    c = int(np.sum(~a & b_arr))
    n = b + c
    p = 1.0 if n == 0 else binomtest(min(b, c), n, 0.5).pvalue
    return b, c, float(p)


def cohen_kappa(labels_a, labels_b) -> float:
    from sklearn.metrics import cohen_kappa_score
    return float(cohen_kappa_score(labels_a, labels_b))


def _read_covered(path: str) -> dict[str, int]:
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cid = r["clause_id"].strip()
            if cid and r.get("covered", "").strip() != "":
                out[cid] = int(r["covered"])
    return out


def _kappa_cli(p1: str, p2: str) -> None:
    a, b = _read_covered(p1), _read_covered(p2)
    keys = sorted(set(a) & set(b))
    if not keys:
        print("No overlapping labelled clause_ids between the two files.")
        return
    la = [a[k] for k in keys]
    lb = [b[k] for k in keys]
    k = cohen_kappa(la, lb)
    disagree = [k_ for k_ in keys if a[k_] != b[k_]]
    print(f"Clauses compared : {len(keys)}")
    print(f"Disagreements    : {len(disagree)}  {disagree}")
    print(f"Cohen's kappa    : {k:.3f}")
    print("Gate: kappa >= 0.6 -> adjudicate; < 0.6 -> revise guideline and re-label.")


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--kappa":
        _kappa_cli(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
