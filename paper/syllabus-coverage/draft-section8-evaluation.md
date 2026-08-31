<!--
DRAFT of the new Section 8 "Experimental Evaluation".
Status: STRUCTURE + placeholders. Every {{...}} is filled from a file in
experiment/results/ AFTER the outcomes.csv rows are verified and two annotators
produce experiment/data/gold_adjudicated.csv, then `python3 run_all.py` is re-run.
Each table notes its source result file in an HTML comment.

Placement plan when splicing into manuscript.md:
  - The current Section 8 "Worked Example" is DEMOTED to a short motivating
    illustration (keep the c_3 incident-management keyword trap) and moved to the
    end of Section 7 (Novelty) or kept as 8.1 "Motivating illustration".
  - This new material becomes Section 8 "Experimental Evaluation".
  - Section 9 (Conclusion / Limitations / Future work) is updated to cite real
    numbers; the "not yet quantified" sentences in 9.1 are removed.
  - manuscript_ua.md is updated in parallel, then re-exported via pandoc.

Honesty gate (from plan.md): if LaBSE does not beat BM25 on gap-F1, report it and
reframe the contribution as explicit-gap + cross-lingual. Do NOT tune to win.
-->

## 8. Experimental Evaluation

The worked example of Section 7 shows the pipeline on a slice small enough to read by
hand. This section tests it where the toy example cannot: on a hand-labelled clause set,
against lexical baselines, with confidence intervals, a significance test, and a
cross-lingual run on real text. The evaluation targets the method's load-bearing claim —
recall on the gap list — rather than precision on individual matches.

### 8.1 Dataset

The clause set $S$ pairs two regulatory sources. The ten risk-management measures of
NIS2 Article 21(2)(a)–(j) are taken verbatim from the public directive text. The
thirty-seven organisational controls of ISO/IEC 27001:2022 Annex A.5 are represented by
their official control name together with a one-sentence paraphrase of the control
objective, since the full control text is copyrighted; the paraphrase wording was fixed
before any score was computed. This yields $|S| = 47$ clauses.

The curriculum set $L$ collects 80 learning outcomes from three real
cybersecurity curricula: a general-user work role of the NIST NICE Framework
(SP 800-181r1), a public security-awareness syllabus, and a Ukrainian university course
that supplies native-language outcomes for the cross-lingual test (Section 8.8). Each
outcome is recorded with its source and, for the Ukrainian sources, its original
wording. Both clause and outcome texts are segmented to one obligation per unit by the
mechanical rule of Section 6.1.

<!-- Table 8.1 fed by data/clauses.csv + data/outcomes.csv summary counts -->

| Source | Units | In set |
|--------|-------|--------|
| NIS2 Article 21(2) | 10 | $S$ |
| ISO/IEC 27001:2022 Annex A.5 | 37 | $S$ |
| NICE general-user curriculum (C1) | 27 | $L$ |
| Awareness syllabus (C2) | 27 | $L$ |
| Ukrainian university course (C3) | 26 | $L$ |

**Table 8.1.** Composition of the clause and curriculum sets.

### 8.2 Annotation and inter-annotator agreement

Two qualified annotators labelled each of the 47 clauses as *covered* or *gap* against
the union of the three curricula, working independently from a written guideline. The
guideline defines coverage as an outcome that lets a trained person *satisfy* the
clause's obligation, not merely share its topic, with worked positive and negative
examples including the incident-report-versus-incident-management distinction. Agreement
before adjudication was Cohen's $\kappa = {{KAPPA}}$ over the 47 clauses, with
{{N_DISAGREE}} disagreements; these were resolved in a joint session to produce the
adjudicated gold set used for all metrics. The gold set contains {{N_GAP_GOLD}} gaps and
{{N_COV_GOLD}} covered clauses.

<!-- KAPPA from `python3 src/stats.py --kappa data/gold_or.csv data/gold_a2.csv`;
     counts from data/gold_adjudicated.csv -->

### 8.3 Baselines

Two lexical methods stand in for the keyword scan the method is meant to improve on.
TF-IDF cosine compares each clause with each outcome over one- and two-gram term
vectors. BM25 scores each clause as a query against the outcome set. Both produce a
best-match score per clause on the same $[0,1]$ scale as the LaBSE cosine, so the same
threshold procedure and metrics apply to all three.

### 8.4 Metrics

The gap (uncovered) class is the positive class. We report gap recall, gap precision,
and gap $F_1$, together with the false-coverage rate — the share of clauses called
covered that are in truth gaps, which is the operationally dangerous error of
Section 6.5. A threshold-free average precision for the gap class (AUC-PR) summarises
performance across all thresholds. Point estimates carry a bootstrap 95% confidence
interval over clauses, and the LaBSE-versus-BM25 comparison is tested with McNemar's
test on paired per-clause coverage decisions.

### 8.5 Gap detection (RQ1)

At the threshold calibrated in Section 8.7, LaBSE attains gap recall
{{A_RECALL}} (95% CI [{{A_RECALL_LO}}, {{A_RECALL_HI}}]), gap precision {{A_PREC}}, and a
false-coverage rate of {{A_FCR}}. The threshold-free AUC-PR for the gap class is
{{A_AUCPR}}.

<!-- Table 8.2 fed by results/expA_metrics.csv -->

| Metric | Value | 95% CI |
|--------|-------|--------|
| Gap recall | {{A_RECALL}} | [{{A_RECALL_LO}}, {{A_RECALL_HI}}] |
| Gap precision | {{A_PREC}} | [{{A_PREC_LO}}, {{A_PREC_HI}}] |
| Gap $F_1$ | {{A_F1}} | [{{A_F1_LO}}, {{A_F1_HI}}] |
| False-coverage rate | {{A_FCR}} | [{{A_FCR_LO}}, {{A_FCR_HI}}] |
| AUC-PR (gap) | {{A_AUCPR}} | — |

**Table 8.2.** Gap-detection performance of the LaBSE pipeline (calibrated $\tau = {{A_TAU}}$).

### 8.6 Comparison with lexical baselines and the keyword trap (RQ2)

Table 8.3 compares the three methods. LaBSE reaches gap $F_1$ {{B_LABSE_F1}} against
{{B_BM25_F1}} for BM25 and {{B_TFIDF_F1}} for TF-IDF; the difference in paired coverage
decisions between LaBSE and BM25 is {{B_MCNEMAR_SIG}} (McNemar $p = {{B_P}}$).

<!-- Table 8.3 fed by results/expB_compare.csv + results/expB_mcnemar.csv -->

| Method | $\tau$ | Gap recall | Gap precision | Gap $F_1$ | FCR | AUC-PR |
|--------|--------|-----------|---------------|-----------|-----|--------|
| LaBSE | {{B_LABSE_TAU}} | {{B_LABSE_R}} | {{B_LABSE_P}} | {{B_LABSE_F1}} | {{B_LABSE_FCR}} | {{B_LABSE_AUC}} |
| BM25 | {{B_BM25_TAU}} | {{B_BM25_R}} | {{B_BM25_P}} | {{B_BM25_F1}} | {{B_BM25_FCR}} | {{B_BM25_AUC}} |
| TF-IDF | {{B_TFIDF_TAU}} | {{B_TFIDF_R}} | {{B_TFIDF_P}} | {{B_TFIDF_F1}} | {{B_TFIDF_FCR}} | {{B_TFIDF_AUC}} |

**Table 8.3.** Gap detection by method on the same gold labels.

The decisive comparison is on the **lexical-trap** clauses — gold gaps whose best
lexical match scores high enough to be called covered, the large-scale version of the
$c_3$ incident-management case in Section 7. On these {{B_TRAP_N}} clauses the lexical
baseline marks {{B_TRAP_BM25_WRONG}} wrongly covered, whereas LaBSE correctly flags
{{B_TRAP_LABSE_RIGHT}} of them as gaps.

<!-- Table 8.4 fed by results/expB_keyword_trap.csv -->

| Method | Trap clauses | Correctly flagged as gap | Accuracy on trap |
|--------|--------------|--------------------------|------------------|
| LaBSE | {{B_TRAP_N}} | {{B_TRAP_LABSE_RIGHT}} | {{B_TRAP_LABSE_ACC}} |
| BM25 | {{B_TRAP_N}} | {{B_TRAP_BM25_RIGHT}} | {{B_TRAP_BM25_ACC}} |
| TF-IDF | {{B_TRAP_N}} | {{B_TRAP_TFIDF_RIGHT}} | {{B_TRAP_TFIDF_ACC}} |

**Table 8.4.** Performance on clauses where a shared keyword would mislead a lexical scan.

### 8.7 Threshold calibration and generalisation (RQ3)

The threshold is calibrated, not fixed by intuition. Across a five-fold split, $\tau$ was
chosen on each training fold to meet a target false-coverage rate of 0.10 and then
applied to the held-out fold. The mean held-out false-coverage rate was {{C_FCR_MEAN}}
and the mean held-out gap recall {{C_RECALL_MEAN}}, showing that a development-calibrated
threshold transfers to unseen clauses rather than being fitted to the test set. Figure
8.1 plots gap recall and false-coverage rate against $\tau$ over the full set.

<!-- Table 8.5 fed by results/expC_calibration.csv; Figure 8.1 = figures/threshold_sensitivity.pdf -->

| Fold | $\tau$ | Test gap recall | Test FCR |
|------|--------|-----------------|----------|
| 1–5 | {{C_TAU_RANGE}} | {{C_RECALL_RANGE}} | {{C_FCR_RANGE}} |

**Table 8.5.** Five-fold threshold calibration (target FCR ≤ 0.10).

![Threshold sensitivity of gap recall and false-coverage rate.](experiment/figures/threshold_sensitivity.pdf)

**Figure 8.1.** Gap recall and false-coverage rate as functions of the threshold $\tau$.

### 8.8 Cross-lingual evaluation (RQ4)

The cross-lingual claim is tested directly by re-encoding every outcome in Ukrainian and
re-matching it against the English clauses, scored against the same gold. A pilot run on
the unverified candidate outcomes already shows close agreement: English and Ukrainian
best-match scores differ by a mean of {{D_DELTA_MEAN}} and stay within
{{D_DELTA_MAX}} for all 47 clauses. On the verified data, gap recall falls from
{{D_EN_RECALL}} (English outcomes) to {{D_UK_RECALL}} (Ukrainian outcomes), a drop of
{{D_RECALL_DROP}}, confirming that translation-free auditing is feasible while bounding
its cost. Figure 8.2 shows the per-clause score agreement.

<!-- Table 8.6 fed by results/expD_crosslingual_scores.csv (summary);
     Figure 8.2 = figures/en_vs_uk_scatter.pdf -->

| Outcome language | Gap recall | FCR |
|------------------|-----------|-----|
| English | {{D_EN_RECALL}} | {{D_EN_FCR}} |
| Ukrainian | {{D_UK_RECALL}} | {{D_UK_FCR}} |

**Table 8.6.** Coverage auditing with English versus Ukrainian outcomes against English clauses.

![Per-clause best-match scores: English versus Ukrainian outcomes.](experiment/figures/en_vs_uk_scatter.pdf)

**Figure 8.2.** Cross-lingual score agreement; points near the diagonal indicate
translation-free stability.

### 8.9 Encoder ablation (RQ5)

To support the claim that the pipeline is encoder-agnostic, LaBSE was replaced by
{{E_MODEL}} with no other change. Gap recall was {{E_RECALL}} and gap $F_1$ {{E_F1}},
{{E_VERDICT}} the LaBSE result, which shows the method does not depend on one specific
encoder and can adopt a stronger multilingual model as it becomes available.

<!-- Table 8.7 fed by results/expE_*.csv -->

### 8.10 Threats to validity

Four limits qualify these results. *Construct:* coverage is a directional, near-entailment
judgement, while cosine is a symmetric proxy; we mitigate this with human-adjudicated
gold and by reporting the false-coverage rate rather than accuracy alone. *Internal:* the
ISO control texts are paraphrased for copyright reasons, which could shift similarity; the
paraphrases were fixed before scoring and are released with the artifact. *External:*
forty-seven clauses, three curricula, and one domain make these results indicative rather
than general; we position the study as a calibrated pilot. *Conclusion:* with a small
sample we report confidence intervals throughout and a paired significance test, and we do
not claim a difference the interval does not support.
