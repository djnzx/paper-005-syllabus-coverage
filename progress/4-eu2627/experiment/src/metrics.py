"""Evaluation metrics. GAP (uncovered) is the positive class (manuscript Sec. 6.5).

  gap recall    = TP / (TP + FN)   -- fraction of true gaps flagged (the headline)
  gap precision = TP / (TP + FP)
  gap F1        = harmonic mean
  false-coverage rate (FCR) = (gold gap & pred covered) / (pred covered)
        -- of everything called 'covered', how much is wrongly reassured (the
           dangerous error). Undefined (nan) if nothing is predicted covered.
  accuracy      = overall coverage-decision accuracy (context only)
  AUC-PR        = threshold-free average precision for the gap class over a score sweep
"""
from __future__ import annotations

import numpy as np


def _counts(gold_gap: np.ndarray, pred_gap: np.ndarray):
    tp = int(np.sum((gold_gap == 1) & (pred_gap == 1)))
    fp = int(np.sum((gold_gap == 0) & (pred_gap == 1)))
    fn = int(np.sum((gold_gap == 1) & (pred_gap == 0)))
    tn = int(np.sum((gold_gap == 0) & (pred_gap == 0)))
    return tp, fp, fn, tn


def gap_metrics(gold_gap: np.ndarray, pred_gap: np.ndarray) -> dict:
    tp, fp, fn, tn = _counts(gold_gap, pred_gap)
    recall = tp / (tp + fn) if (tp + fn) else float("nan")
    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    f1 = (2 * precision * recall / (precision + recall)
          if precision and recall and not np.isnan(precision) and not np.isnan(recall)
          else float("nan"))
    pred_covered = fn + tn  # gold gap & pred covered (fn) + gold cov & pred covered (tn)
    fcr = fn / pred_covered if pred_covered else float("nan")
    accuracy = (tp + tn) / len(gold_gap)
    return {
        "gap_recall": recall, "gap_precision": precision, "gap_f1": f1,
        "false_coverage_rate": fcr, "accuracy": accuracy,
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
    }


def auc_pr_gap(gold_gap: np.ndarray, gap_score: np.ndarray) -> float:
    """Average precision for the gap class.

    A clause is 'more gap' as its match score is lower, so the gap score is
    (1 - s_i): higher means more likely a gap.
    """
    from sklearn.metrics import average_precision_score

    if len(set(gold_gap.tolist())) < 2:
        return float("nan")
    return float(average_precision_score(gold_gap, gap_score))
