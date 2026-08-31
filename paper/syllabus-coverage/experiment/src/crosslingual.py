"""Cross-lingual check (manuscript Sec. 8.6, RQ4).

Encode outcomes in Ukrainian, keep clauses in English, re-match against the same
English gold. Compare EN vs UA gap metrics and the per-clause score delta, to
bound the 'no translation needed' promise on real text.
"""
from __future__ import annotations

import numpy as np

from embed import encode
from match import sim_matrix, best_match


def en_vs_uk(clauses, outcomes, encoder=None, model_name=None):
    """Return dict with EN and UA best-match score vectors over the same clauses.

    clauses: list[Clause]; outcomes: list[Outcome] (must have text_uk filled).
    """
    kw = {"encoder": encoder} if encoder is not None else {}
    if model_name:
        kw["model_name"] = model_name

    C = encode([c.text_en for c in clauses], **kw)
    L_en = encode([o.text_en for o in outcomes], **kw)
    L_uk = encode([o.text_uk for o in outcomes], **kw)

    s_en, j_en = best_match(sim_matrix(C, L_en))
    s_uk, j_uk = best_match(sim_matrix(C, L_uk))
    return {
        "clause_ids": [c.clause_id for c in clauses],
        "s_en": s_en, "s_uk": s_uk,
        "jstar_en": j_en, "jstar_uk": j_uk,
        "delta": s_uk - s_en,
    }
