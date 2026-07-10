"""Lexical baselines: the 'keyword scan' the method claims to beat.

Each returns a per-clause best-match score s_i in [0, 1], directly comparable to
the LaBSE cosine so the same threshold sweep and metrics apply (manuscript Sec. 8.3,
the c_3 'shares the word incident' trap).
"""
from __future__ import annotations

import numpy as np


def _minmax(x: np.ndarray) -> np.ndarray:
    lo, hi = float(np.min(x)), float(np.max(x))
    return (x - lo) / (hi - lo) if hi > lo else np.zeros_like(x)


def tfidf_match(clause_texts: list[str], outcome_texts: list[str]) -> np.ndarray:
    """Best TF-IDF cosine of each clause against the outcome set."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)
    X = vec.fit_transform(clause_texts + outcome_texts)
    C = X[: len(clause_texts)]
    L = X[len(clause_texts):]
    sim = cosine_similarity(C, L)
    return sim.max(axis=1)


def bm25_match(clause_texts: list[str], outcome_texts: list[str]) -> np.ndarray:
    """Best BM25 score of each clause (as query) over outcomes, min-max scaled."""
    from rank_bm25 import BM25Okapi

    def tok(s: str) -> list[str]:
        return [w for w in s.lower().replace("/", " ").split() if w.isalpha()]

    bm25 = BM25Okapi([tok(o) for o in outcome_texts])
    best = np.array([bm25.get_scores(tok(c)).max() for c in clause_texts])
    return _minmax(best)
