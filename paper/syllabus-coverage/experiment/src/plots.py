"""Figures for the manuscript. Saved as PDF (vector) into figures/."""
from __future__ import annotations

import os

import numpy as np

from common import FIGURES


def _ensure():
    import matplotlib
    matplotlib.use("Agg")


def _save(fname):
    """Save the current figure as both PDF (vector, for LaTeX/PDF builds) and
    PNG (raster, for DOCX builds, which embed PNG far better than PDF).
    Returns the PDF path; the PNG sits beside it with the same stem."""
    import matplotlib.pyplot as plt

    base = os.path.join(FIGURES, os.path.splitext(fname)[0])
    pdf_path = base + ".pdf"
    for ext in (".pdf", ".png"):
        plt.savefig(base + ext, dpi=200, bbox_inches="tight")
    plt.close()
    return pdf_path


def pr_curves(curves: dict[str, tuple[np.ndarray, np.ndarray]], fname="pr_curves.pdf"):
    """curves: {method_label: (gold_gap, gap_score)}."""
    _ensure()
    import matplotlib.pyplot as plt
    from sklearn.metrics import precision_recall_curve, average_precision_score

    plt.figure(figsize=(5, 4))
    for label, (gold_gap, gap_score) in curves.items():
        if len(set(gold_gap.tolist())) < 2:
            continue
        p, r, _ = precision_recall_curve(gold_gap, gap_score)
        ap = average_precision_score(gold_gap, gap_score)
        plt.plot(r, p, label=f"{label} (AP={ap:.2f})")
    plt.xlabel("Gap recall")
    plt.ylabel("Gap precision")
    plt.title("Gap-detection precision-recall")
    plt.legend(loc="lower left", fontsize=8)
    plt.tight_layout()
    return _save(fname)


def threshold_sensitivity(sweep_rows, fname="threshold_sensitivity.pdf"):
    """sweep_rows: list of (tau, metrics-dict) from calibrate.sweep."""
    _ensure()
    import matplotlib.pyplot as plt

    tau = [t for t, _ in sweep_rows]
    recall = [m["gap_recall"] for _, m in sweep_rows]
    fcr = [m["false_coverage_rate"] for _, m in sweep_rows]
    plt.figure(figsize=(5, 4))
    plt.plot(tau, recall, label="gap recall")
    plt.plot(tau, fcr, label="false-coverage rate")
    plt.xlabel(r"threshold $\tau$")
    plt.ylabel("rate")
    plt.title("Threshold sensitivity")
    plt.legend(fontsize=8)
    plt.tight_layout()
    return _save(fname)


def en_uk_scatter(s_en, s_uk, tau=None, fname="en_vs_uk_scatter.pdf"):
    _ensure()
    import matplotlib.pyplot as plt

    plt.figure(figsize=(4.5, 4.5))
    plt.scatter(s_en, s_uk, s=18)
    lim = [0, 1]
    plt.plot(lim, lim, "--", linewidth=0.8, color="grey")
    if tau is not None:
        plt.axhline(tau, linewidth=0.6, color="red")
        plt.axvline(tau, linewidth=0.6, color="red")
    plt.xlabel("best score (English outcomes)")
    plt.ylabel("best score (Ukrainian outcomes)")
    plt.title("Cross-lingual score agreement")
    plt.xlim(lim)
    plt.ylim(lim)
    plt.tight_layout()
    return _save(fname)
