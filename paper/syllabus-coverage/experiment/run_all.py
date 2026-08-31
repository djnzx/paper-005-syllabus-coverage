"""One-command runner for the coverage-audit experiment (Exp A-E).

    python run_all.py                 # LaBSE, all available experiments
    python run_all.py --alt-encoder   # also run the encoder ablation (Exp E)

Behaviour:
  * Always: encode clauses+outcomes, compute LaBSE / TF-IDF / BM25 best-match
    scores, write predictions.csv and cross-lingual scores, draw the figures that
    do not need gold. This works the moment data exists.
  * If data/gold_adjudicated.csv is present: also run Exp A (gap metrics + CIs),
    Exp B (baseline comparison + McNemar + lexical-trap subset) and Exp C
    (threshold calibration). Metrics are NEVER computed without human gold.

Outputs: results/*.csv, figures/*.pdf, and env.lock (model revision + versions).
"""
from __future__ import annotations

import csv
import os
import platform
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import common  # noqa: E402
from common import (load_clauses, load_outcomes, load_gold, gold_gap_vector,  # noqa: E402
                    RESULTS, DEFAULT_MODEL, ALT_MODELS, SEED)
from embed import encode, load_encoder  # noqa: E402
from match import sim_matrix, best_match  # noqa: E402
import baselines  # noqa: E402
from metrics import gap_metrics, auc_pr_gap  # noqa: E402
from stats import bootstrap_ci, mcnemar  # noqa: E402
import calibrate  # noqa: E402
import crosslingual  # noqa: E402
import plots  # noqa: E402

ILLUSTRATIVE_TAU = 0.45  # for the no-gold prediction dump only (manuscript Sec. 8.2)
TARGET_FCR = 0.10


def _write_csv(name, header, rows):
    path = os.path.join(RESULTS, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote {os.path.relpath(path)}")
    return path


def write_env_lock(revision):
    import sklearn
    import scipy
    lines = [
        f"model={DEFAULT_MODEL}",
        f"model_revision={revision}",
        f"seed={SEED}",
        f"python={platform.python_version()}",
        f"platform={platform.platform()}",
        f"numpy={np.__version__}",
        f"scipy={scipy.__version__}",
        f"scikit_learn={sklearn.__version__}",
    ]
    try:
        import sentence_transformers as st
        lines.append(f"sentence_transformers={st.__version__}")
    except Exception:
        pass
    with open(os.path.join(common.ROOT, "env.lock"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("  wrote env.lock")


def predictions(clauses, outcomes, scores):
    cids = [c.clause_id for c in clauses]
    s = scores["LaBSE"][0]
    jstar = scores["LaBSE"][1]
    rows = []
    for i, c in enumerate(clauses):
        oj = outcomes[jstar[i]]
        rows.append([c.clause_id, c.source, f"{s[i]:.3f}",
                     "covered" if s[i] >= ILLUSTRATIVE_TAU else "GAP",
                     oj.outcome_id, oj.text_en[:60]])
    _write_csv("predictions.csv",
               ["clause_id", "source", "labse_best_score",
                f"verdict@tau={ILLUSTRATIVE_TAU}", "best_outcome", "best_outcome_text"],
               rows)


def exp_A(cids, gold_gap, scores):
    print("Exp A - gap detection (LaBSE)")
    s = scores["LaBSE"][0]
    tau = calibrate.tau_for_target_fcr(gold_gap, s, TARGET_FCR)
    pred = (s < tau).astype(int)
    m = gap_metrics(gold_gap, pred)
    rows = []
    for key in ("gap_recall", "gap_precision", "gap_f1", "false_coverage_rate", "accuracy"):
        pt, lo, hi = bootstrap_ci(gold_gap, pred,
                                  lambda g, p, k=key: gap_metrics(g, p)[k])
        rows.append([key, f"{pt:.3f}", f"{lo:.3f}", f"{hi:.3f}"])
    rows.append(["auc_pr_gap", f"{auc_pr_gap(gold_gap, 1 - s):.3f}", "", ""])
    rows.append(["tau_calibrated", f"{tau:.3f}", "", ""])
    _write_csv("expA_metrics.csv", ["metric", "point", "ci_lo", "ci_hi"], rows)
    return tau


def exp_B(cids, gold_gap, scores, tau_labse):
    print("Exp B - baseline comparison + lexical-trap subset")
    rows = [["method", "tau", "gap_recall", "gap_precision", "gap_f1",
             "false_coverage_rate", "auc_pr_gap"]]
    preds = {}
    for name, (s, _) in scores.items():
        tau = (tau_labse if name == "LaBSE"
               else calibrate.tau_for_target_fcr(gold_gap, s, TARGET_FCR))
        pred = (s < tau).astype(int)
        preds[name] = pred
        m = gap_metrics(gold_gap, pred)
        rows.append([name, f"{tau:.3f}", f"{m['gap_recall']:.3f}",
                     f"{m['gap_precision']:.3f}", f"{m['gap_f1']:.3f}",
                     f"{m['false_coverage_rate']:.3f}",
                     f"{auc_pr_gap(gold_gap, 1 - s):.3f}"])
    _write_csv("expB_compare.csv", rows[0], rows[1:])

    # McNemar: LaBSE vs BM25 on per-clause coverage-decision correctness.
    if "BM25" in preds:
        corr_l = (preds["LaBSE"] == gold_gap)
        corr_b = (preds["BM25"] == gold_gap)
        b, c, p = mcnemar(corr_l, corr_b)
        _write_csv("expB_mcnemar.csv",
                   ["comparison", "labse_right_bm25_wrong", "bm25_right_labse_wrong", "p_value"],
                   [["LaBSE_vs_BM25", b, c, f"{p:.4f}"]])

    # Lexical-trap subset: gold gaps that the lexical baseline would call covered.
    s_tfidf = scores["TF-IDF"][0]
    tau_tfidf = calibrate.tau_for_target_fcr(gold_gap, s_tfidf, TARGET_FCR)
    trap = (gold_gap == 1) & (s_tfidf >= tau_tfidf)
    rows = [["method", "trap_clauses", "correctly_flagged_gap", "accuracy_on_trap"]]
    n_trap = int(np.sum(trap))
    for name, pred in preds.items():
        correct = int(np.sum(pred[trap] == 1))
        acc = correct / n_trap if n_trap else float("nan")
        rows.append([name, n_trap, correct, f"{acc:.3f}" if n_trap else "n/a"])
    _write_csv("expB_keyword_trap.csv", rows[0], rows[1:])


def exp_C(cids, gold_gap, scores):
    print("Exp C - threshold calibration (5-fold)")
    s = scores["LaBSE"][0]
    folds = calibrate.kfold_calibration(gold_gap, s, k=5, target_fcr=TARGET_FCR)
    rows = [["fold", "tau", "test_gap_recall", "test_fcr", "test_accuracy"]]
    for i, (tau, m) in enumerate(folds):
        rows.append([i, f"{tau:.3f}", f"{m['gap_recall']:.3f}",
                     f"{m['false_coverage_rate']:.3f}", f"{m['accuracy']:.3f}"])
    _write_csv("expC_calibration.csv", rows[0], rows[1:])
    plots.threshold_sensitivity(calibrate.sweep(gold_gap, s))


def exp_D(clauses, outcomes, gold_gap, tau, encoder):
    print("Exp D - cross-lingual (EN vs UA outcomes)")
    if any(not o.text_uk.strip() for o in outcomes):
        print("  skipped: some outcomes lack text_uk")
        return
    cl = crosslingual.en_vs_uk(clauses, outcomes, encoder=encoder)
    rows = [["clause_id", "s_en", "s_uk", "delta"]]
    for cid, se, su, d in zip(cl["clause_ids"], cl["s_en"], cl["s_uk"], cl["delta"]):
        rows.append([cid, f"{se:.3f}", f"{su:.3f}", f"{d:+.3f}"])
    _write_csv("expD_crosslingual_scores.csv", rows[0], rows[1:])
    # The scatter needs only the EN/UA scores, not gold, so draw it always
    # (tau is drawn as a guide line only when a calibrated value exists).
    plots.en_uk_scatter(cl["s_en"], cl["s_uk"], tau)
    if gold_gap is not None and tau is not None:
        for lang, s in (("EN", cl["s_en"]), ("UA", cl["s_uk"])):
            m = gap_metrics(gold_gap, (s < tau).astype(int))
            print(f"  {lang}: gap_recall={m['gap_recall']:.3f} "
                  f"fcr={m['false_coverage_rate']:.3f} (tau={tau:.3f})")


def compute_scores(clauses, outcomes, encoder):
    ct = [c.text_en for c in clauses]
    ot = [o.text_en for o in outcomes]
    C = encode(ct, encoder=encoder)
    L = encode(ot, encoder=encoder)
    s_labse, j_labse = best_match(sim_matrix(C, L))
    s_tfidf = baselines.tfidf_match(ct, ot)
    s_bm25 = baselines.bm25_match(ct, ot)
    n = len(outcomes)
    return {
        "LaBSE": (s_labse, j_labse),
        "TF-IDF": (s_tfidf, np.zeros(len(clauses), int)),
        "BM25": (s_bm25, np.zeros(len(clauses), int)),
    }


def main():
    clauses = load_clauses()
    outcomes = load_outcomes()
    print(f"Loaded {len(clauses)} clauses, {len(outcomes)} outcomes")

    encoder = load_encoder(DEFAULT_MODEL)
    write_env_lock(encoder[1])

    scores = compute_scores(clauses, outcomes, encoder)
    predictions(clauses, outcomes, scores)

    cids = [c.clause_id for c in clauses]
    try:
        gold = load_gold()
        gold_gap = gold_gap_vector(cids, gold)
        n_gap = int(gold_gap.sum())
        print(f"Gold present: {n_gap} gaps / {len(cids)} clauses")
        tau = exp_A(cids, gold_gap, scores)
        exp_B(cids, gold_gap, scores, tau)
        exp_C(cids, gold_gap, scores)
        plots.pr_curves({name: (gold_gap, 1 - s) for name, (s, _) in scores.items()})
        exp_D(clauses, outcomes, gold_gap, tau, encoder)
    except FileNotFoundError as e:
        print("\n[metrics skipped] " + str(e).split("\n")[0])
        print("Predictions and cross-lingual scores were still written.")
        exp_D(clauses, outcomes, None, None, encoder)

    if "--alt-encoder" in sys.argv:
        for alt in ALT_MODELS:
            print(f"Exp E - encoder ablation: {alt}")
            enc = load_encoder(alt)
            sc = compute_scores(clauses, outcomes, enc)
            try:
                gold_gap = gold_gap_vector(cids, load_gold())
                s = sc["LaBSE"][0]
                tau = calibrate.tau_for_target_fcr(gold_gap, s, TARGET_FCR)
                m = gap_metrics(gold_gap, (s < tau).astype(int))
                _write_csv(f"expE_{alt.split('/')[-1]}.csv",
                           ["metric", "value"],
                           [["gap_recall", f"{m['gap_recall']:.3f}"],
                            ["gap_f1", f"{m['gap_f1']:.3f}"],
                            ["false_coverage_rate", f"{m['false_coverage_rate']:.3f}"],
                            ["auc_pr_gap", f"{auc_pr_gap(gold_gap, 1 - s):.3f}"]])
            except FileNotFoundError:
                print("  metrics skipped (no gold)")

    print("\nDone. See results/ and figures/.")


if __name__ == "__main__":
    main()
