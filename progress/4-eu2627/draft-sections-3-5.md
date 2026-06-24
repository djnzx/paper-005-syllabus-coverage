# Draft — Sections 3 (Problem Statement), 4 (Goal & Tasks), 5 (Object & Subject)

*Connective sections between Related Works and Methods. Headline contribution: explicit-gap design.*

---

## 3. Problem Statement (актуальність)

Article 21 of the NIS2 Directive obliges essential and important entities to provide cybersecurity training and to keep it aligned with their risk-management measures. The obligation is now enforceable: since 17 October 2024 a supervisory authority may ask an organisation to demonstrate that its training actually covers the required competence areas, and it may impose fines of up to €10 million or 2% of global turnover where it does not. Demonstrating coverage, not merely running a course, has become the compliance test.

The demonstration is difficult for three reasons. First, the two documents speak different languages of intent. A standard states control objectives and legal obligations, while a curriculum states learning outcomes and assessment criteria, so a human auditor must bridge the two by interpretation. Second, the work does not reproduce. Two auditors reading the same syllabus against the same standard often disagree on which outcome satisfies which clause, and neither leaves a record a third party could replay. Third, in the Ukrainian setting the curriculum is frequently written in Ukrainian while ISO/IEC 27001 and the NIS2 measures circulate in English, which forces a manual translation step that adds cost and a further source of error.

The volume makes manual auditing worse, not merely slow. ISO/IEC 27001:2022 Annex A alone lists ninety-three controls, and NIS2 Article 21(2) adds ten measure families; a training programme may carry dozens of learning outcomes. Checking every clause against every outcome by hand is quadratic in effort and rarely completed exhaustively, so the requirement most likely to be missed is precisely the one no outcome addresses — the gap the auditor cannot see because nothing prompts attention to it. Existing automated tools do not close this gap. They audit contracts rather than curricula, or they answer questions rather than prove coverage, as Section 2 set out. The relevance of this work is the absence of a reproducible, language-neutral method that tells an auditor which regulatory requirements a curriculum leaves uncovered.

---

## 4. Goal and Tasks

### 4.1 Goal (Мета)

The goal of the study is to develop a reproducible, language-neutral method that audits a cybersecurity training curriculum against the clauses of NIS2 and ISO/IEC 27001 and reports the uncovered requirements as its primary result.

### 4.2 Tasks (Завдання)

The goal decomposes into five tasks:

1. Formalise a regulatory standard and a training curriculum as comparable sets of text units, at a granularity that makes partial coverage detectable.
2. Define a coverage decision as a partial verdict function over the clause set, whose undefined region is the set of uncovered clauses.
3. Design an embedding-based pipeline that computes this function across languages using a shared semantic space.
4. Specify a gap report and a threshold-sensitivity analysis that keep the residual judgement with the human auditor.
5. Demonstrate the pipeline on a worked NIS2 and ISO/IEC 27001 example and discuss its failure modes.

---

## 5. Object and Subject of Research

### 5.1 Object of research

The object of research is the process of auditing a cybersecurity training curriculum for compliance with regulatory requirements — that is, the activity of establishing which clauses of a standard the curriculum covers and which it leaves unaddressed.

### 5.2 Subject of research

The subject of research is a language-agnostic sentence-embedding method for measuring the semantic coverage of NIS2 and ISO/IEC 27001 clauses by curriculum content, with particular attention to the explicit identification of uncovered clauses as the undefined region of a partial verdict function.
