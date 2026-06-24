# Chapter Plan — Automated NIS2/ISO 27001 Curriculum Compliance Auditing Using Sentence Embeddings

**Paper type:** Conceptual / methodological paper with one worked illustrative example.
**Object of research:** the process of auditing a cybersecurity training curriculum for compliance with regulatory requirements.
**Subject of research:** a language-agnostic sentence-embedding method for measuring semantic coverage of NIS2 / ISO 27001 clauses by curriculum content.
**Target length:** ~6,500–7,500 words (12–15 pages). **Target venue:** WSEAS Trans. Computer Research (eu8 venue) or KNU Bulletin (eu7 venue).

---

## [INSIGHT: thesis_statement]
A lightweight, language-agnostic sentence-embedding pipeline can measure — automatically, reproducibly, and clause-by-clause — how well a cybersecurity training curriculum covers the semantic requirements of NIS2 and ISO/IEC 27001, yielding an auditable coverage-gap report without the cost and subjectivity of manual review or the opacity and resource demand of large generative models.

## [INSIGHT: research_gap]
Existing NLP-compliance work audits legal contracts (GDPR/DPAs — eu-cite #8) or answers regulatory questions via RAG (#14–16). None measures clause-level coverage of a *training curriculum* against cybersecurity standards. eu7 supplies the comparison method, eu8 the competency baseline, eu9 the formal ISMS framing — the synthesis is unaddressed.

## [INSIGHT: contribution_claim] — (to refine in your own words)
Three candidate contributions; confirm/rewrite which one is primary:
1. A reproducible, language-neutral coverage metric (not a black-box score) for curriculum-vs-standard auditing.
2. A pipeline design that makes the *partial / undefined* region explicit — clauses with no curricular match are surfaced, not hidden.
3. A worked NIS2 + ISO 27001 example demonstrating feasibility on a real syllabus.

---

## Chapter-by-chapter plan

| # | Section | Core argument | Key evidence / citations | Words |
|---|---------|---------------|--------------------------|-------|
| 1 | Introduction | NIS2 enforcement (Oct 2024) makes training-compliance demonstrable a legal duty; manual curriculum auditing is slow, subjective, language-bound | NIS2 timeline; eu8 (training context) | 700 |
| 2 | Related works | Three threads converge but leave a gap | A: SBERT/LaBSE/MTEB (#1–5); B: GDPR-DPA & legal LLM checking (#8–13); C: RAG (#14–16); D: SecureBERT, mapping (#17–20); eu7, eu9 | 1300 |
| 3 | Problem statement (актуальність) | Demonstrating curriculum coverage of NIS2/ISO clauses cannot scale manually and must be cross-lingual & auditable | eu8, NIS2 fines clause | 500 |
| 4 | Goal & Tasks | Goal: a reproducible embedding-based coverage-audit method. Tasks: formalize clauses+curriculum as text units; define coverage metric; design pipeline; demonstrate | — | 350 |
| 5 | Object / Subject | (as defined above) | — | 200 |
| 6 | Methods | Pipeline: segment standard into clause units → segment curriculum into learning-outcome units → embed both (LaBSE for cross-lingual) → cosine-similarity matching with threshold τ → coverage matrix → gap report. Explicitly mark uncovered clauses | #1 (SBERT), #3 (LaBSE), #4 (MTEB for model choice), eu7 (comparison precedent); formula for coverage score in LaTeX | 1500 |
| 7 | Novelty | First clause-level, language-neutral, transparent coverage auditor for cyber-training; surfaces gaps rather than producing one opaque score | contrast with #8 (contract-level), #14–16 (QA, not coverage) | 400 |
| 8 | Body / worked example | Apply to a sample syllabus vs a slice of ISO 27001 Annex A + NIS2 Art. 21 measures; show coverage matrix, a covered clause, an uncovered clause, threshold sensitivity; discuss false matches (eu7's documented failure mode) | eu7 (pipeline-failure discussion), eu8 (competency categories) | 1500 |
| 9 | Conclusion + limitations + future work | Method is feasible & auditable; limitations = threshold tuning, embedding bias, no semantic reasoning; future = LLM-assisted re-ranking, multilingual eval | #13 (code-gen direction), #18 (SecureBERT 2.0) | 500 |
| 16 | References | 3 anchors + 20 modern | — | — |

---

## Argument stress test (Step 3)

- **Weakest point:** cosine similarity ≠ true semantic compliance; a high score can be a topical match without requirement satisfaction. → Defence: position the tool as a *triage/coverage screen*, not a verdict; uncovered-clause detection (recall on gaps) is the load-bearing claim, not precision on matches.
- **Reverse-the-argument:** "Why not just use an LLM (Cluster B/C)?" → Defence: cost, reproducibility, language-neutrality (Ukrainian/English curricula), and transparency — embedding similarity is inspectable; an LLM verdict is not. Cite #9's own call for explanation as the open problem.
- **Reviewer "no real dataset":** acknowledged as conceptual paper; the worked example demonstrates feasibility; empirical evaluation is named future work.

---

## Open decisions before drafting
1. **Embedding model for the example:** LaBSE (cross-lingual, matches the Ukrainian/English bilingual context) vs SBERT all-mpnet (English-only, higher STS scores). Recommend **LaBSE** — the cross-lingual angle is a genuine differentiator from Cluster B.
2. **Which standard slice for the example:** ISO 27001:2022 Annex A theme (e.g. A.5 organizational) + NIS2 Art. 21(2) measures — small, citable, reproducible.
3. Primary contribution claim (pick from the three above).