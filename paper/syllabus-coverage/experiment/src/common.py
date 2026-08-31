"""Shared data loading, paths, and constants for the coverage-audit experiment.

All metrics treat the GAP (uncovered) class as the positive class, because the
method's load-bearing claim is recall on the gap list (manuscript Sec. 6.5).
"""
from __future__ import annotations

import csv
import os
from dataclasses import dataclass

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")

# Pinned encoder (record the resolved revision in env.lock at run time).
DEFAULT_MODEL = "sentence-transformers/LaBSE"
ALT_MODELS = ["sentence-transformers/paraphrase-multilingual-mpnet-base-v2"]

SEED = 20260626

for d in (RESULTS, FIGURES):
    os.makedirs(d, exist_ok=True)


@dataclass
class Clause:
    clause_id: str
    source: str
    framework: str
    text_en: str


@dataclass
class Outcome:
    outcome_id: str
    curriculum_id: str
    text_en: str
    text_uk: str


def load_clauses(path: str | None = None) -> list[Clause]:
    path = path or os.path.join(DATA, "clauses.csv")
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(Clause(r["clause_id"], r["source"], r["framework"], r["text_en"]))
    return out


def load_outcomes(path: str | None = None) -> list[Outcome]:
    path = path or os.path.join(DATA, "outcomes.csv")
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(Outcome(r["outcome_id"], r["curriculum_id"],
                               r["text_en"], r.get("text_uk", "")))
    return out


def load_gold(path: str | None = None) -> dict[str, int]:
    """Return {clause_id: covered(0/1)} from an adjudicated gold file.

    Raises FileNotFoundError if the gold file is missing -- metrics cannot be
    computed without human labels, and we deliberately do not fabricate them.
    """
    path = path or os.path.join(DATA, "gold_adjudicated.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Gold file not found: {path}\n"
            "Coverage metrics require human-adjudicated labels. Have two annotators "
            "fill copies of gold_template.csv per data/annotation_guideline.md, run "
            "the kappa check, adjudicate, and save gold_adjudicated.csv."
        )
    gold = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["clause_id"].strip():
                gold[r["clause_id"]] = int(r["covered"])
    return gold


def gold_gap_vector(clause_ids: list[str], gold: dict[str, int]) -> np.ndarray:
    """gap = 1 when the clause is uncovered (the positive class)."""
    return np.array([1 - gold[cid] for cid in clause_ids], dtype=int)
