# Plan: Minimal Empirical Experiment to Raise the Paper to Q3/Q4

This plan turns the current proof-of-concept (a 6×5 toy slice) into a small but
**real, reproducible empirical study** with a baseline comparison, standard
metrics, statistical validity, and a genuine cross-lingual test. It is written to
be executed directly: data schemas, file layout, function specs, metric formulas,
and the manuscript edits that follow are all spelled out.

The target is the level of the journals already in our reference list
(WSEAS Q4, Electronics Q2, Ukrainian Cat. B / Scopus Q3–Q4): real data + one
honest baseline + standard metrics + a reproducibility artifact. We do **not**
need SOTA, a large corpus, or model training.

---

## 0. The single sentence the paper must be able to say after this

> On a hand-labelled set of ~50 regulatory clauses against ~80 learning outcomes
> from three real cybersecurity curricula, the LaBSE gap detector achieved
> gap-recall of X.XX (95% CI […]) at a false-coverage rate of Y.YY, significantly
> better than a BM25 lexical baseline (McNemar p < 0.05), and lost only Z points
> of recall when the curriculum was supplied in Ukrainian instead of English.

Every number in that sentence is an output of the experiments below.

---

## 1. Research questions and hypotheses

| ID | Question | Hypothesis | Decided by |
|----|----------|------------|------------|
| RQ1 | Does the embedding method find uncovered clauses reliably? | H1: gap-recall ≥ 0.80 | Exp. A |
| RQ2 | Is it better than a lexical baseline, especially on the "shares a keyword but isn't covered" case? | H2: LaBSE > BM25 on gap-F1, McNemar significant | Exp. B |
| RQ3 | Can τ be calibrated to a target false-coverage rate and hold on unseen data? | H3: dev-calibrated τ keeps test FCR within target ± small margin | Exp. C |
| RQ4 | Does translation-free cross-lingual auditing work on real text? | H4: UA-vs-EN gap-recall drop ≤ 0.10 | Exp. D |
| RQ5 | (optional) Does a stronger multilingual encoder help? | H5: paraphrase-multilingual-mpnet ≈ or > LaBSE | Exp. E |

**Success criteria for "Q3/Q4-ready":** RQ1–RQ4 answered with numbers, CIs, and a
significance test for RQ2. RQ5 is a nice-to-have ablation, not a gate.

---

## 2. Data set construction

Target size (minimal but credible):
- **Clauses (S): ~50.** NIS2 Article 21(2) measures (a)–(j) = 10 + ISO/IEC 27001:2022
  Annex A.5 *Organizational controls* = 37. Total **47**. (Expandable to A.6/A.8 later.)
- **Outcomes (L): ~80**, drawn from **3 real curricula** (~25–30 outcomes each).

### 2.1 Clause side `data/clauses.csv`

Schema:
```
clause_id, source, framework, text_en, copyright_note
c01, "NIS2 21(2)(a)", NIS2, "policies on risk analysis and information system security", public
c11, "ISO A.5.1", ISO27001, "information security policy defined, approved and communicated", title+paraphrase
...
```
Rules:
- **NIS2 21(2)(a)–(j):** EU legal text is public — quote the measure verbatim.
- **ISO/IEC 27001:2022 Annex A.5:** full control text is copyrighted. Use the
  **official control name + a one-line paraphrase of the control objective** (fair
  use, cited). Record `copyright_note=title+paraphrase`. This is defensible and
  keeps us legal; note it explicitly in the Data Availability statement.
- One obligation per row; apply the §6.1 split rule and record any split.

### 2.2 Curriculum side `data/outcomes.csv`

Schema:
```
outcome_id, curriculum_id, text_en, text_uk, source_url, lang_original
o01, C1, "explain the organisation's information security policy and staff duties", "<UA>", <url>, en
```
Three real curricula, public sources (pick the three most accessible at run time):
- **C1 — NIST NICE Framework (SP 800-181r1)** Task/Knowledge/Skill statements for a
  security-awareness / general-user work role. Structured, free, ideal.
- **C2 — A public university cybersecurity-awareness syllabus** with stated learning
  outcomes (e.g. an open courseware / ENISA / SANS awareness outline). Prefer one
  with an explicit "learning outcomes" list.
- **C3 — A real Ukrainian university cybersecurity course** (силабус / освітня
  програма, public PDF). This supplies **native Ukrainian** outcomes for RQ4 —
  better than machine-translating C1/C2.

Provenance (URL + access date) is recorded per outcome for reproducibility.

### 2.3 Ground-truth labels `data/gold.csv`

For every (clause, curriculum) we need the truth of "is this clause covered by some
outcome, and which one?".

Schema (one row per clause, per annotator):
```
clause_id, annotator, covered, covering_outcome_ids, note
c11, A1, 1, "o01", "policy explicitly taught"
c02, A1, 0, "", "no threat-intel content anywhere"
```
- `covered ∈ {0,1}`; `covering_outcome_ids` = semicolon list (may be empty).
- Labelled against the **union of all three curricula** (the realistic audit
  question: does *the programme* cover the clause).

### 2.4 Annotation protocol (this is the scientific backbone — do it properly)

1. **Two annotators.** A1 = the author (Doctor of Science). A2 = a second qualified
   reader (colleague / co-supervisor). Independent, no discussion during round 1.
2. **Written guideline** (`data/annotation_guideline.md`): "covered" = an outcome
   would let a graduate *perform/satisfy* the clause's obligation, not merely
   mention the topic. Include 3 worked positive and 3 worked negative examples,
   including the *incident-report vs incident-management* distinction.
3. **Inter-annotator agreement:** compute **Cohen's κ** on the binary `covered`
   labels over all 47 clauses. Report it. (κ ≥ 0.6 is acceptable; below that, the
   guideline is revised and re-run.)
4. **Adjudication:** disagreements resolved in a joint session → `data/gold_adjudicated.csv`
   is the single source of truth for all metrics.
5. The κ value and adjudication count go into the paper. This is what converts the
   study from "the author decided" to "a measured, replicable label set."

---

## 3. Pipeline implementation

Stack: Python 3.11, `sentence-transformers`, `scikit-learn`, `rank-bm25`,
`numpy`, `scipy`, `matplotlib`, `pandas`. CPU is fine (~130 short texts).

### 3.1 Directory layout
```
progress/4-eu2627/experiment/
  data/
    clauses.csv
    outcomes.csv
    gold.csv
    gold_adjudicated.csv
    annotation_guideline.md
  src/
    embed.py          # encode + cache vectors
    match.py          # cosine matrix, best-match per clause (s_i, j*)
    baselines.py      # TF-IDF cosine, BM25
    metrics.py        # gap P/R/F1, FCR, accuracy, formulas in §4
    calibrate.py      # threshold sweep + dev/test calibration (§Exp C)
    stats.py          # bootstrap CI, McNemar, Cohen's kappa
    crosslingual.py   # EN vs UA re-encode and compare (§Exp D)
    plots.py          # PR curve, threshold-sensitivity, score histograms
  run_all.py          # orchestrates A–E, writes results/ + figures/
  results/            # *.csv tables produced by the run
  figures/            # *.pdf/*.png for the manuscript
  requirements.txt
  README.md           # exact commands to reproduce every number
  env.lock            # model name+revision, package versions, seed
```

### 3.2 Module specs (function-level)

`embed.py`
- `load_encoder(name, revision) -> SentenceTransformer` — pin model **and revision
  hash**; write both to `env.lock`.
- `encode(texts, encoder) -> np.ndarray` — mean pooling, **L2-normalise**, cache to
  `results/emb_<hash>.npy` keyed by sha1(text+model+revision).

`match.py`
- `sim_matrix(C, L) -> np.ndarray[m,n]` — cosine = dot product (already normalised).
- `best_match(simM) -> (s: np.ndarray[m], jstar: np.ndarray[m])` — implements
  the §6.3 \(s_i, j_i^\*\).
- `verdict(s, tau) -> covered_mask` — implements the §6.4 partial function.

`baselines.py`
- `tfidf_match(C, L)` — sklearn `TfidfVectorizer` (1–2-grams), cosine, best per clause.
- `bm25_match(C, L)` — `rank_bm25.BM25Okapi`, treat each clause as the query over the
  outcome "documents", best score per clause. Min-max scale to [0,1] for a comparable τ.
- These are the "keyword scan" the paper keeps claiming to beat — now we measure it.

`metrics.py` — see §4 for formulas.

`stats.py`
- `bootstrap_ci(y_true, y_pred, metric_fn, n=10000, seed) -> (point, lo, hi)` —
  resample clauses, 95% percentile CI.
- `mcnemar(correct_A, correct_B) -> (stat, p)` — paired per-clause coverage decisions.
- `cohen_kappa(a1, a2) -> float`.

---

## 4. Metrics (exact definitions)

The method's **load-bearing claim is recall on the gap list**, so the *gap*
(uncovered) class is the positive class.

Let, per clause, gold ∈ {covered, gap} and pred ∈ {covered, gap} at threshold τ.

- **Gap recall** (the headline): \( R_{gap} = \dfrac{\#(\text{gold gap} \wedge \text{pred gap})}{\#(\text{gold gap})} \) — fraction of truly-missing requirements the system flags.
- **Gap precision:** \( P_{gap} = \dfrac{\#(\text{gold gap} \wedge \text{pred gap})}{\#(\text{pred gap})} \).
- **Gap F1:** harmonic mean of the two (primary single-number for RQ2).
- **False-coverage rate (the dangerous error):**
  \( \text{FCR} = \dfrac{\#(\text{pred covered} \wedge \text{gold gap})}{\#(\text{pred covered})} \)
  — of everything the tool calls "covered", how much is wrongly reassured. This is the
  quantity §6.5 calls operationally critical; report it everywhere.
- **Coverage-decision accuracy** (context only): overall fraction correct.
- **Threshold-free:** **PR curve and AUC-PR for the gap class**, sweeping τ ∈ [0,1].
  This removes the "you cherry-picked τ" objection.

All point metrics get a **bootstrap 95% CI**. RQ2 also gets **McNemar** on paired
coverage decisions (LaBSE vs BM25 on the same clauses).

---

## 5. Experiments

### Exp A — Gap detection (RQ1)
Run LaBSE pipeline over the 47 clauses vs 80 outcomes. At the dev-calibrated τ (Exp C),
report gap recall / precision / F1 / FCR with CIs, plus the full PR curve.
Output: `results/expA_metrics.csv`, `figures/pr_curve.pdf`.

### Exp B — Baseline comparison (RQ2)
Same gold, same τ-calibration procedure, for **BM25** and **TF-IDF**. Compare AUC-PR
(gap class) and gap-F1 across the three methods; McNemar LaBSE-vs-BM25 on coverage
decisions. **Targeted sub-analysis:** isolate the clauses that *share a surface
keyword with a non-covering outcome* (the §8.3 `c_3` phenomenon) and report per-method
accuracy on just that subset — this is where embeddings should visibly win and is the
single most persuasive table in the paper.
Output: `results/expB_compare.csv`, `results/expB_keyword_trap.csv`,
`figures/pr_curves_all.pdf`.

### Exp C — Threshold calibration & generalisation (RQ3)
- Split clauses **5-fold** (or leave-one-curriculum-out). On each train fold pick
  τ\* that hits a **target FCR (e.g. ≤ 0.10)**; evaluate on the held-out fold.
- Report mean test FCR and gap-recall across folds vs the target. Demonstrates τ is
  *calibrated*, not fitted to the test set — kills the strongest reviewer objection.
Output: `results/expC_calibration.csv`, `figures/threshold_sensitivity.pdf`.

### Exp D — Cross-lingual (RQ4) — the distinctive claim
- Take **C3 (native Ukrainian outcomes)** and, for C1/C2, a professionally/manually
  checked Ukrainian translation. Re-encode outcomes in Ukrainian, keep clauses in
  English, re-run matching against the **same English gold**.
- Report EN vs UA: gap-recall, gap-F1, FCR, and the **per-clause score delta**
  distribution (mean/SD, how many pairs cross τ). Confirms or bounds the "no
  translation needed" promise on real text, not one toy triple.
Output: `results/expD_crosslingual.csv`, `figures/en_vs_uk_scatter.pdf`.

### Exp E — Encoder ablation (RQ5, optional)
Swap LaBSE for `paraphrase-multilingual-mpnet-base-v2` (and optionally a
multilingual-e5). Re-run Exp A+D. Shows the pipeline is encoder-agnostic and whether
a stronger model helps — supports the §6.2 "drop-in replacement" claim with evidence.
Output: `results/expE_encoders.csv`.

---

## 6. Reproducibility artifact

- `requirements.txt` pinned; `env.lock` records model **revision hash**, package
  versions, OS, and the RNG seed.
- `run_all.py` regenerates **every table and figure** from raw CSVs with one command;
  `README.md` lists the command.
- Release `data/` (clauses, outcomes, gold_adjudicated, guideline) + `src/` as a
  zenodo/OSF/GitHub deposit; cite the DOI in Data Availability. **A public,
  labelled mini-dataset is itself a citable contribution** and meaningfully helps a
  Q3/Q4 acceptance.

---

## 7. Threats to validity (write this section honestly in the paper)

- **Construct:** "coverage" is a directional/entailment judgement; cosine is a proxy.
  Mitigated by human-adjudicated gold + reporting FCR, not just accuracy.
- **Internal:** ISO text is paraphrased for copyright → paraphrase wording could
  inflate/deflate similarity. Mitigate: paraphrase from the official *objective*, fix
  wording before seeing scores, document in the artifact.
- **External:** ~50 clauses, 3 curricula, one domain → results are indicative, not
  general. State the scope plainly; position as a calibrated pilot.
- **Conclusion:** small n → always report CIs and a paired significance test; never
  claim a difference the CI doesn't support.
- **Annotation:** subjectivity → reported via Cohen's κ + adjudication.

---

## 8. Manuscript changes that follow

1. **New Section 8 "Experimental Evaluation"** (replaces the toy worked example as the
   centre of gravity), with subsections: Dataset & sources, Annotation & κ, Baselines,
   Metrics, Results (Exp A/B), Threshold calibration (Exp C), Cross-lingual (Exp D),
   Encoder ablation (Exp E), Threats to validity.
2. **Demote current §8 worked example** to a short §7-style *motivating illustration*
   (keep the `c_3` incident-management trap — it now also appears, measured, in Exp B).
3. **Abstract / Анотація:** replace "Limitations and an empirical evaluation are
   identified as future work" with the actual headline numbers.
4. **§7 Novelty:** keep explicit-gap framing but back claim 1 with gap-recall numbers
   and claim 2 with the cross-lingual result.
5. **§9.1 Limitations:** drop "demonstrated as feasible but not yet quantified";
   replace with the measured-but-small-sample framing.
6. **Add 3–4 references:** a metrics/eval methodology cite, Cohen's kappa, BM25
   (Robertson & Zaragoza), NIST NICE SP 800-181 as a data source.

---

## 9. Execution order & effort

| Phase | Task | Output | Rough effort |
|-------|------|--------|--------------|
| 1 | Build clauses.csv (NIS2 + ISO A.5) | 47 clauses | 0.5 day |
| 2 | Collect 3 curricula → outcomes.csv (+UA) | ~80 outcomes | 1 day |
| 3 | Write guideline, dual-annotate, κ, adjudicate | gold_adjudicated.csv | 1–1.5 days |
| 4 | Implement src/ (embed, match, baselines, metrics, stats) | code | 1 day |
| 5 | Run Exp A–D (+E), generate tables/figures | results/, figures/ | 0.5 day |
| 6 | Rewrite §8, update abstract/novelty/limits | manuscript | 1 day |
| 7 | Package artifact + DOI, Data Availability | deposit | 0.5 day |

Total ≈ 6–7 focused days. Critical path = Phases 2–3 (real data + honest labels);
everything else is mechanical once those exist.

---

## 10. Go/no-go gates

- After Phase 3: if **κ < 0.5**, stop and fix the guideline — bad labels invalidate
  everything downstream.
- After Phase 5: if **LaBSE does not beat BM25** on gap-F1, that is still a publishable
  (and more honest) result — reframe the contribution as "explicit-gap reporting +
  cross-lingual" rather than "embeddings beat lexical", and report the negative finding.
  Do **not** tune until the embedding wins.
