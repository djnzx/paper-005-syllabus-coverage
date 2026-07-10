# Coverage-Audit Experiment

Reproducible empirical evaluation for the paper *Automated NIS2/ISO 27001 Curriculum
Compliance Auditing Using Sentence Embeddings*. It measures the method's load-bearing
claim — **recall on the gap list** — on a hand-labelled clause set, against lexical
baselines, with confidence intervals, a significance test, and a cross-lingual check.

## What is here

```
data/
  clauses.csv             47 clauses: NIS2 21(2) (verbatim) + ISO 27001 A.5 (title+paraphrase)
  outcomes.csv            50 learning outcomes from 3 curricula (EN+UA) -- VERIFY before use
  annotation_guideline.md labelling protocol (two annotators, Cohen's kappa, adjudication)
  gold_template.csv       empty label sheet (47 clauses) -- copy per annotator
  gold_adjudicated.csv    <- you create this; the ONLY file metrics read
src/                      embed, match, baselines, metrics, stats, calibrate, crosslingual, plots
run_all.py                one-command runner (Exp A-E)
results/  figures/        generated outputs
```

## Reproduce

```bash
cd experiment
python3 -m pip install -r requirements.txt
python3 run_all.py                 # add --alt-encoder for the Exp E ablation
```

Without `gold_adjudicated.csv` the run still writes `results/predictions.csv` and the
cross-lingual scores (it encodes everything with a real LaBSE run). Full gap metrics
appear once the gold file exists — **labels are never fabricated**.

## Before the numbers count — human steps (per the plan)

1. **Verify `outcomes.csv`.** Replace each `VERIFY` row with real learning-outcome text
   from an actual cited curriculum (NIST NICE SP 800-181r1; a public awareness syllabus;
   a real Ukrainian university course) and record its `source_ref`/URL.
2. **Label.** Two annotators each copy `gold_template.csv` -> `gold_or.csv`, `gold_a2.csv`
   and fill `covered` independently, following `annotation_guideline.md`.
3. **Agreement gate.** `python3 src/stats.py --kappa data/gold_or.csv data/gold_a2.csv`.
   If kappa < 0.6, sharpen the guideline and re-label.
4. **Adjudicate** disagreements -> `data/gold_adjudicated.csv`.
5. `python3 run_all.py` -> tables in `results/`, figures in `figures/`.

## Outputs -> manuscript

| File | Feeds |
|------|-------|
| `expA_metrics.csv` | RQ1 headline gap recall/precision/F1/FCR + 95% CI |
| `expB_compare.csv`, `expB_mcnemar.csv`, `expB_keyword_trap.csv` | RQ2 baseline comparison + the c_3 lexical-trap result |
| `expC_calibration.csv`, `figures/threshold_sensitivity.pdf` | RQ3 tau calibration generalises |
| `expD_crosslingual_scores.csv`, `figures/en_vs_uk_scatter.pdf` | RQ4 translation-free auditing |
| `expE_*.csv` | RQ5 encoder ablation |
| `figures/pr_curves.pdf` | gap-detection PR curves (all methods) |
| `env.lock` | pinned model revision + library versions |

## Honesty gates (from the plan)

- κ < 0.5 after labelling → fix the guideline before proceeding.
- If LaBSE does not beat BM25 → report it and reframe the contribution as
  explicit-gap + cross-lingual. **Do not tune until the embedding wins.**
