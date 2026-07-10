# Automated NIS2/ISO 27001 Curriculum Compliance Auditing Using Sentence Embeddings: A Cross-Lingual Method and Worked Example

**Oleksiy Rykhalskyy**
Private Higher Educational Institution "European University", Kyiv, Ukraine
ORCID: https://orcid.org/0009-0000-6892-9420 · Email: alexey.rykhalskiy@e-u.edu.ua

*Citation style: numbered by order of appearance (author name + bracketed reference number). Main text: English; bilingual abstract (English + Ukrainian) below.*

---

## Abstract

The NIS2 Directive makes demonstrable cybersecurity training a legal obligation, yet auditing whether a training curriculum covers the required regulatory clauses is still manual, subjective, and bound to one language. This paper presents a sentence-embedding method that audits a curriculum against the clauses of NIS2 and ISO/IEC 27001 and reports the uncovered requirements as its primary result. Clause units from the standard and learning-outcome units from the curriculum are embedded into a shared multilingual space with a language-agnostic encoder, matched by cosine similarity, and separated by a threshold. The audit verdict is modelled as a partial function whose undefined region — the clauses no learning outcome addresses — is returned as a ranked gap list rather than hidden inside an aggregate coverage score. This explicit-gap design is the contribution: it gives a curriculum owner an actionable list of missing topics and gives an auditor a reproducible, cross-lingual screen that needs no prior translation. A worked example over a slice of ISO/IEC 27001:2022 Annex A.5 and NIS2 Article 21(2), run through an actual LaBSE encoder, locates three coverage gaps that a coverage percentage alone would conceal — one of them an incident-management clause that a keyword scan would wrongly mark covered — and a threshold-sensitivity analysis keeps the residual judgement explicit and with the human expert. The method is positioned as a triage screen whose load-bearing claim is recall on the gap list, not precision on matches. Limitations and an empirical evaluation are identified as future work.

**Keywords:** sentence embeddings; compliance auditing; NIS2 Directive; ISO/IEC 27001; semantic textual similarity; cybersecurity training; partial functions.

## Анотація

Директива NIS2 робить документально підтверджене навчання з кібербезпеки правовим обов'язком, проте перевірка того, чи покриває навчальна програма потрібні нормативні положення, залишається ручною, суб'єктивною та прив'язаною до однієї мови. У статті запропоновано метод на основі речникових вкладень (sentence embeddings), який зіставляє навчальну програму з положеннями NIS2 та ISO/IEC 27001 і подає непокриті вимоги як основний результат. Одиниці положень стандарту та одиниці результатів навчання програми відображаються у спільний багатомовний простір за допомогою мовнонезалежного кодувальника, зіставляються за косинусною подібністю та розділяються пороговим значенням. Рішення аудиту змодельовано як часткову функцію, область невизначеності якої — положення, що їх не охоплює жоден результат навчання — повертається як впорядкований перелік прогалин, а не приховується в агрегованому показнику покриття. Саме цей підхід явного виявлення прогалин є внеском роботи: він дає власникові програми дієвий перелік відсутніх тем, а аудиторові — відтворюваний міжмовний інструмент попередньої перевірки без потреби у попередньому перекладі. Наведений приклад на фрагменті ISO/IEC 27001:2022 (додаток A.5) та статті 21(2) NIS2, пропущений через справжній кодувальник LaBSE, виявляє три прогалини покриття, які відсоток покриття приховав би, — серед них положення про управління інцидентами, яке пошук за ключовими словами помилково позначив би покритим, — а аналіз чутливості до порогу залишає остаточне рішення за експертом. Метод позиціоновано як інструмент попереднього сортування, ключове твердження якого — повнота виявлення прогалин, а не точність зіставлень.

**Ключові слова:** речникові вкладення; аудит відповідності; Директива NIS2; ISO/IEC 27001; семантична подібність тексту; навчання з кібербезпеки; часткові функції.

---

## 1. Introduction

The NIS2 Directive [28] moved cybersecurity training from good practice to legal obligation. Since the transposition deadline of 17 October 2024, essential and important entities across eighteen sectors must show that their staff receive cybersecurity training aligned with the risk-management measures of Article 21. Failure carries fines of up to €10 million or 2% of global turnover, and personal liability for senior management. A training programme that merely exists is no longer enough; an organisation now has to demonstrate that its curriculum actually covers the competence areas the regulation expects.

Demonstrating coverage is harder than it sounds. A curriculum is written in the language of pedagogy — learning outcomes, modules, assessment criteria. A standard such as ISO/IEC 27001:2022 or the NIS2 measures is written in the language of control objectives and legal obligation. Auditing one against the other means reading both, deciding which learning outcome satisfies which clause, and recording where nothing does. Done by hand, this work is slow, depends on the individual auditor's interpretation, and rarely produces a record that a second auditor would reproduce. In Ukraine the task carries an extra difficulty, because curricula are frequently authored in Ukrainian while the reference standards circulate in English.

Recent natural language processing offers tools that look promising for this problem, yet none of them solves it directly. One body of work checks legal contracts — most prominently data processing agreements — against the GDPR, treating compliance as sentence-level classification (Amaral Cejas et al. [1]). A second body of work answers questions about regulatory text through retrieval-augmented generation, returning a passage and a generated explanation (Gokhan et al. [2]). Neither produces what an auditor of a training programme needs: a clause-by-clause statement of which regulatory requirements the curriculum covers and, more importantly, which it leaves uncovered.

This paper argues that a lightweight sentence-embedding pipeline can produce exactly that statement. Clause texts from the standard and learning-outcome texts from the curriculum are each mapped into a shared semantic vector space; cosine similarity then proposes matches, and a threshold separates covered clauses from uncovered ones. The approach reuses the text-comparison method that Skliarenko et al. [3] applied to unstructured legal documents, and it draws its competence taxonomy from the cybersecurity training study of Arsenovych et al. [4].

The contribution we place at the centre is not the matching itself but its inverse. Most compliance tools report what they found; ours is designed to report what is missing. We call this an *explicit-gap* design: every clause that receives no curricular match above the threshold is surfaced as a first-class output, rather than being absorbed into an aggregate score or a silent default. A single percentage of "coverage" hides the one uncovered requirement that an auditor most needs to see. By making the undefined region of the matching function visible, the method turns a coverage audit into an actionable gap list. The framing extends an earlier treatment of narrowed domains of definition as a route to software correctness (Rykhalskyy [5]), here applied to regulatory coverage rather than program semantics. This also keeps the tool honest about its own limits, because a clause the embeddings cannot match is shown, not guessed.

The remainder of the paper is organised as follows. Section 2 reviews four converging research threads, locates the gap, and connects the explicit-gap design to software-correctness practice. Section 3 states the problem and its relevance. Sections 4 and 5 define the goal, tasks, object, and subject. Section 6 details the method. Section 7 states the novelty, Section 8 demonstrates the pipeline on a worked NIS2 and ISO 27001 example, and Section 9 concludes with limitations and future work.

## 2. Related Works

Four research threads bear on automated curriculum compliance auditing: sentence-embedding methods, NLP-based compliance checking, retrieval-augmented generation over regulation, and domain-specific models for cybersecurity. Each contributes a component, and together they leave one problem open.

### 2.1 Sentence embeddings and semantic textual similarity

The technical foundation of our method is the sentence embedding — a fixed-length vector whose geometry reflects meaning. Reimers and Gurevych [6] introduced Sentence-BERT, a siamese network that makes pairwise semantic comparison tractable by allowing cosine similarity over precomputed vectors. Gao et al. [7] improved embedding quality with SimCSE, a contrastive objective later refined from two further perspectives by Xu et al. [8]. For multilingual settings, Feng et al. [9] trained LaBSE across 109 languages, producing a shared space in which a Ukrainian sentence and its English counterpart land close together. The Massive Text Embedding Benchmark of Muennighoff et al. [10] and the multi-functional M3-Embedding model of Chen et al. [11] give practitioners a basis for choosing among the now-large family of encoders. The systematic review by Guder et al. [12] surveys this evolution and confirms semantic textual similarity as a mature, well-characterised task. Skliarenko et al. [3] applied precisely this class of models to the comparison of unstructured legal texts, and reported how a failure at one pipeline stage propagates downstream — a caution we carry into our own design.

### 2.2 NLP-based compliance checking

The work closest to ours treats compliance as a text-matching problem. Amaral Cejas et al. [1] built an NLP system that checks data processing agreements against the GDPR, combining classifiers with cosine-similarity matching between agreement sentences and regulatory requirements. Their pipeline embeds each sentence and tests it against the rule set, the same mechanism we adopt. The requirements engineering community has since pushed toward generative models. Hassani et al. [13] argued that compliance analysis should move from classification toward end-to-end strategies able to explain and justify their verdicts, and a companion study explored regulation analysis with large language models more broadly (Hassani [14]). Zhu et al. [15] introduced LegiLM, a legal language model fine-tuned for data-compliance judgements, while Hassani et al. [16] tested LLM classification of requirement-related provisions in food-safety regulation. More recently, Li et al. [17] reframed financial compliance checking as code generation. These systems are powerful, yet all of them target legal or contractual text and return a judgement rather than a coverage map of a training curriculum.

### 2.3 Retrieval-augmented generation over regulation

A parallel thread treats regulation as a knowledge base to be queried. Gokhan et al. [2] released RIRAG together with the ObliQA dataset and an obligation-aware evaluation metric, framing the task as regulatory information retrieval and answer generation. Aushev et al. [18] tuned retrieval for regulatory question answering in RAGulator, and Zheng et al. [19] applied the same architecture to civil-aviation airworthiness regulations, which change often and so reward an updatable retrieval layer. Retrieval-augmented generation suits a user who asks a specific question and wants a grounded answer. It is a poor fit for the auditor who must verify that every clause of a standard is addressed, because question answering optimises recall for a single query rather than exhaustive coverage of a requirement set. Our explicit-gap design inverts that priority.

### 2.4 Domain-specific models and control mapping

A final thread adapts language technology to the cybersecurity domain itself. Aghaei et al. [20] trained SecureBERT on a large cybersecurity corpus, and its successor (Aghaei et al. [21]) extended the model for threat-intelligence tasks; such encoders could replace a general-purpose model in our embedding stage when domain vocabulary dominates. On the mapping side, Nautiyal and Rashid [22] proposed a framework for assessing an organisation's workforce knowledge against a standardised cybersecurity reference, which is conceptually adjacent to curriculum auditing though it stops short of an automated text-similarity method. Sargolzaei Javan [23] built a machine-readable semantic model linking security mechanisms to ISO/IEC 27001:2022 controls, demonstrating the value of explicit control-to-evidence mappings. Semantic alignment of heterogeneous models has also been explored for decision-support architectures using an ontology-based approach (Rykhalskyy [24]); the present work pursues semantic matching in a different setting, regulatory clause text, with sentence embeddings rather than ontologies. The training context that motivates our work is established by Arsenovych et al. [4], who studied digital-technology-supported cybersecurity training and supply the competence categories against which coverage is meaningful; the formal information-security-management framing comes from Lakhno et al. [25].

### 2.5 The gap

One adjacent field deserves explicit mention, because it already reports gaps as a first-class output. Requirements-engineering research on information-retrieval-based traceability recovers links between requirements and the artefacts that satisfy them, and a traceability matrix's empty rows — requirements with no satisfying artefact — are exactly an uncovered-requirement report. Antoniol et al. [26] established the IR formulation, and the systematic mapping of Borg et al. [27] surveys a decade of such methods. Our work is not the first to treat uncovered requirements as a deliverable; its contribution is to carry that stance into *cross-lingual auditing of a training curriculum against regulatory clauses*, where the satisfying artefacts are learning outcomes, the requirements are NIS2 and ISO 27001 clauses, and the two sides are typically written in different languages.

### 2.6 Partial functions and explicit absence in correctness

A further perspective, from software correctness rather than language technology, shapes how this paper reports its result. A partial function is defined on only part of its domain; the inputs it does not map are left explicitly undefined rather than forced to a default value. Meyer's design-by-contract turns this into engineering practice, because a precondition narrows a routine's domain so that out-of-contract inputs are surfaced instead of silently mishandled (Meyer [29]). Denotational semantics gives the same notion a formal reading, modelling computations that need not return a value as partial functions (Winskel [30]). Functional languages encode it as a type, where an optional value makes "no result" a visible, checked outcome rather than a null that fails downstream. Rykhalskyy argued that such a narrowed, explicit domain of definition improves the correctness of the surrounding system (Rykhalskyy [5]). We carry that discipline into compliance auditing: the audit verdict is a partial function whose undefined region — the uncovered clauses — is returned as the deliverable, not hidden inside a total coverage score. Requirements-traceability research already treats unmatched requirements as an output [26, 27], and the partial-function reading explains why that choice is principled rather than merely convenient.

Taken together, the literature supplies every ingredient yet assembles none of them for this purpose. Embedding methods give the comparison engine. Compliance-checking work shows that sentence-level matching against a requirement set is viable, but only for contracts. Retrieval-augmented systems handle regulatory text, but optimise for answering questions, not for proving coverage. Traceability research surfaces uncovered requirements, but within a single language and for software artefacts, not cross-lingual curriculum-versus-regulation auditing. Domain models and mapping frameworks address cybersecurity knowledge, yet none audits a training curriculum against NIS2 and ISO 27001 clause by clause, across languages, while surfacing the uncovered requirements as the primary result. The software-correctness view contributes no component but a reporting discipline — treat the unmatched remainder as a partial function's undefined region and return it, rather than fold it into a score. That intersection — cross-lingual coverage auditing with an explicit-gap output — is the contribution of this paper.

## 3. Problem Statement (актуальність)

Article 21 of the NIS2 Directive [28] obliges essential and important entities to provide cybersecurity training and to keep it aligned with their risk-management measures. The obligation is now enforceable: since 17 October 2024 a supervisory authority may ask an organisation to demonstrate that its training actually covers the required competence areas, and it may impose fines of up to €10 million or 2% of global turnover where it does not. Demonstrating coverage, not merely running a course, has become the compliance test.

The demonstration is difficult for three reasons. First, the two documents speak different languages of intent. A standard states control objectives and legal obligations, while a curriculum states learning outcomes and assessment criteria, so a human auditor must bridge the two by interpretation. Second, the work does not reproduce. Two auditors reading the same syllabus against the same standard often disagree on which outcome satisfies which clause, and neither leaves a record a third party could replay. Third, in the Ukrainian setting the curriculum is frequently written in Ukrainian while ISO/IEC 27001 and the NIS2 measures circulate in English, which forces a manual translation step that adds cost and a further source of error.

The volume makes manual auditing worse, not merely slow. ISO/IEC 27001:2022 Annex A alone lists ninety-three controls, and NIS2 Article 21(2) adds ten measure families; a training programme may carry dozens of learning outcomes. Checking every clause against every outcome by hand is quadratic in effort and rarely completed exhaustively, so the requirement most likely to be missed is precisely the one no outcome addresses — the gap the auditor cannot see because nothing prompts attention to it. Existing automated tools do not close this gap. They audit contracts rather than curricula, or they answer questions rather than prove coverage, as Section 2 set out. The relevance of this work is the absence of a reproducible, language-neutral method that tells an auditor which regulatory requirements a curriculum leaves uncovered.

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

## 5. Object and Subject of Research

### 5.1 Object of research

The object of research is the process of auditing a cybersecurity training curriculum for compliance with regulatory requirements — that is, the activity of establishing which clauses of a standard the curriculum covers and which it leaves unaddressed.

### 5.2 Subject of research

The subject of research is a language-agnostic sentence-embedding method for measuring the semantic coverage of NIS2 and ISO/IEC 27001 clauses by curriculum content, with particular attention to the explicit identification of uncovered clauses as the undefined region of a partial verdict function.

## 6. Methods

The method audits a curriculum against a standard in five stages: clause segmentation, outcome segmentation, embedding, similarity matching, and gap extraction. The design goal is not a single coverage score but an explicit list of the requirements the curriculum fails to address. We therefore formalise the audit as a *partial* verdict function whose undefined region is the audit's main product.

### 6.1 Inputs as text-unit sets

Let the standard be decomposed into a finite set of clause units
$$ S = \{c_1, c_2, \dots, c_m\}, $$
where each $c_i$ is the smallest self-contained requirement statement — one ISO control or one NIS2 measure. Let the curriculum be decomposed into a set of learning-outcome units
$$ L = \{l_1, l_2, \dots, l_n\}, $$
where each $l_j$ is one learning outcome or module description. Segmentation granularity matters: a clause that bundles several obligations is split so that partial coverage is detectable rather than hidden inside one coarse unit. To keep this step reproducible rather than subjective, we apply one rule: split at every coordinating conjunction or enumerated sub-item that introduces a separate obligation, so that each resulting unit carries a single verb–object obligation. The same rule is applied to learning outcomes. This rule is mechanical and auditable, which matters because an unspecified manual split would reintroduce the very subjectivity the method aims to remove.

### 6.2 Embedding into a shared semantic space

A single encoder $\varphi : \text{Text} \rightarrow \mathbb{R}^{d}$ maps both clause units and outcome units into one $d$-dimensional space. We use LaBSE (Feng et al. [9]) — in its `sentence-transformers` implementation, with mean pooling and L2-normalised output so that cosine equals the dot product — so that a Ukrainian learning outcome and an English clause are comparable without prior translation, which removes a translation step that would otherwise inject its own errors. Pinning the encoder version and the normalisation is what makes the scores reproducible; a second auditor running the same model on the same units obtains the same numbers. LaBSE is a baseline choice, selected for its 109-language coverage rather than a benchmark win; a stronger multilingual encoder from MTEB [10] or M3-Embedding [11] could be substituted without changing the pipeline. Each unit is encoded once and cached, following the precomputation strategy that makes pairwise comparison scalable (Reimers and Gurevych [6]).

### 6.3 Similarity and the per-clause match

Semantic proximity between a clause and an outcome is the cosine of their embedding vectors,
$$ \operatorname{sim}(c_i, l_j) = \frac{\varphi(c_i) \cdot \varphi(l_j)}{\lVert \varphi(c_i) \rVert \, \lVert \varphi(l_j) \rVert}. $$
For each clause we keep only its best-matching outcome and that outcome's score:
$$ s_i = \max_{1 \le j \le n} \operatorname{sim}(c_i, l_j), \qquad j_i^{\ast} = \arg\max_{1 \le j \le n} \operatorname{sim}(c_i, l_j). $$
The pair $(s_i, j_i^{\ast})$ is the evidence the auditor inspects: the strength of the best match and the outcome that produced it. One caveat is structural rather than incidental. Cosine similarity is symmetric and measures topical relatedness, whereas the relation the audit truly cares about — does an outcome *satisfy* a clause — is directional and closer to entailment; natural-language-inference research formalises this directional relation and shows that symmetric similarity does not capture it (Bowman et al. [31]). We use similarity as a tractable proxy and treat its output as a screen, not a verdict; a directional entailment or cross-encoder stage (Section 9.2) is the natural way to tighten the proxy, and we keep the explicit-gap output so that any residual mismatch surfaces for review rather than hiding in a score.

### 6.4 The coverage decision as a partial function

A threshold $\tau \in [0,1]$ separates covered clauses from uncovered ones. We define the audit verdict as a partial function $v$ over the clause set:
$$ v(c_i) = \begin{cases} l_{j_i^{\ast}}, & s_i \ge \tau \\ \text{undefined}, & s_i < \tau. \end{cases} $$
The covered set and the gap set follow directly:
$$ \mathrm{Cov}_\tau = \{\, c_i \in S : s_i \ge \tau \,\}, \qquad G_\tau = S \setminus \mathrm{Cov}_\tau = \{\, c_i \in S : s_i < \tau \,\}. $$
The aggregate coverage ratio is reported for context,
$$ \rho_\tau = \frac{\lvert \mathrm{Cov}_\tau \rvert}{\lvert S \rvert}, $$
but $\rho_\tau$ is explicitly the secondary output. The primary output is $G_\tau$, the set of clauses on which $v$ is undefined. Treating the gap as the domain complement of a partial function — rather than as a failure branch folded into a score — is what we mean by an explicit-gap design. The construction follows the principle that a narrowed domain of definition, made explicit, improves the correctness of the surrounding system (Rykhalskyy [5]): here the undefined region is not an error to suppress but the audit's deliverable. A clause the encoder cannot match is shown to the auditor, never silently defaulted. The threshold is not fixed silently either: $\tau$ should be calibrated on a small labelled development set to target a chosen *false-coverage rate*, since absolute LaBSE cosine magnitudes vary with text length and language pairing and so cannot be assumed from one setting to another.

### 6.5 Gap report and auditor review

The pipeline emits a coverage matrix of scores $s_i$, the covered pairs $(c_i, l_{j_i^{\ast}})$ ranked by confidence, and the gap list $G_\tau$ ranked by how far each clause falls below $\tau$. Because cosine proximity signals topical relatedness rather than proven requirement satisfaction, every covered pair is offered for human confirmation, not asserted as compliance. The method is positioned as a triage screen that concentrates expert attention on the gap list and on borderline matches near $\tau$, where Skliarenko et al. [3] showed that spurious similarity is most likely. In a compliance setting the asymmetry of risk matters: the dangerous error is a false *covered* verdict — a clause reported as addressed when it is not, on which an organisation then relies and is later sanctioned — whereas a false *gap* merely costs review time. Raising $\tau$ therefore trades reviewer effort for legal safety, and the operationally critical quantity is the false-coverage rate rather than overall accuracy. This recall-first stance follows screening-automation practice, where a human-in-the-loop triage tool is tuned for high recall and judged by what it wrongly lets through rather than by overall accuracy (O'Mara-Eves et al. [32]).

## 7. Novelty of Results

The novelty of the work lies in three results that together distinguish it from the methods reviewed in Section 2.

The first and central result is the **explicit-gap design**. Prior compliance-checking systems report what they match — a coverage score, a classification, or a generated answer — and absorb the unmatched remainder into an aggregate or a default branch. We instead model the audit verdict as a partial function whose undefined region is computed and returned as the primary output. The set of uncovered clauses $G_\tau$ is a first-class artefact, ranked and presented to the auditor, rather than a residue inferred from a percentage. Reporting uncovered requirements is itself established practice in requirements-traceability research [26, 27]; what is new here is bringing that gap-as-deliverable stance to compliance auditing of a training curriculum against regulatory clauses, where prior compliance-checking and question-answering systems instead return a coverage score, a classification, or a generated answer.

The second result is **language-neutral auditing without a translation stage**. By embedding clauses and learning outcomes into the shared LaBSE space, a Ukrainian curriculum is audited directly against an English standard. The cross-lingual property is not specific to one encoder, since massively multilingual sentence embeddings have been shown to align translations across many languages in a shared space (Artetxe & Schwenk [33]). This removes the manual translation step that earlier compliance pipelines assume, and with it a documented source of propagated error (Skliarenko et al. [3]). The contract-checking work of Amaral Cejas et al. [1] and the regulatory question-answering systems of Gokhan et al. [2] and Zheng et al. [19] operate monolingually; cross-lingual coverage auditing is new in this setting.

The third result is **reproducibility with the residual judgement kept explicit**. The method fixes no threshold silently. With the encoder version and normalisation pinned (Section 6.2), it reports the coverage matrix, the gap list, and a threshold-sensitivity analysis, so a second auditor replaying the pipeline obtains the same scores and sees the same consequence of any threshold choice. The worked example in Section 8 is itself produced by an actual LaBSE run rather than stipulated, which is what lets this reproducibility claim be checked rather than merely asserted. This contrasts with manual auditing, where Section 3 noted that two experts rarely agree or leave a replayable record. The pipeline does not replace expert judgement; it makes the point at which judgement enters visible and auditable.

## 8. Worked Example

To show the pipeline end to end we audit a short cybersecurity-awareness syllabus against a slice of two standards: the organisational controls of ISO/IEC 27001:2022 Annex A.5 and the risk-management measures of NIS2 Article 21(2). The slice is small enough to inspect by hand, which lets the reader verify every match and every gap.

### 8.1 The clause set and the curriculum

Six clause units form the standard slice $S$:

| Clause | Source | Requirement (abbreviated) |
|--------|--------|---------------------------|
| $c_1$ | ISO A.5.1 | Information security policy defined and communicated |
| $c_2$ | ISO A.5.7 | Threat intelligence collected and analysed |
| $c_3$ | ISO A.5.24 | Incident management planned and prepared |
| $c_4$ | NIS2 21(2)(d) | Supply-chain security addressed |
| $c_5$ | NIS2 21(2)(g) | Basic cyber hygiene and training provided |
| $c_6$ | NIS2 21(2)(j) | Multi-factor authentication used |

Five learning outcomes form the curriculum $L$:

| Outcome | Learning outcome (abbreviated) |
|---------|--------------------------------|
| $l_1$ | Explain the organisation's information security policy and staff duties |
| $l_2$ | Recognise phishing and report incidents to the service desk |
| $l_3$ | Apply strong passwords and multi-factor authentication |
| $l_4$ | Follow good cyber-hygiene habits in daily work |
| $l_5$ | Describe how personal data is backed up |

### 8.2 Coverage matrix

Best-match scores $s_i$ from an actual LaBSE run (`sentence-transformers/LaBSE`, L2-normalised) at an illustrative threshold $\tau = 0.45$:

| Clause | Best outcome $j_i^{\ast}$ | $s_i$ | $s_i \ge \tau$ | Verdict |
|--------|---------------------------|-------|----------------|---------|
| $c_1$ A.5.1 policy | $l_1$ | 0.65 | yes | covered |
| $c_2$ A.5.7 threat intel | $l_2$ | 0.28 | no | **gap** |
| $c_3$ A.5.24 incident mgmt | $l_2$ | 0.34 | no | **gap** |
| $c_4$ NIS2 supply chain | $l_1$ | 0.24 | no | **gap** |
| $c_5$ NIS2 hygiene & training | $l_4$ | 0.50 | yes | covered |
| $c_6$ NIS2 MFA | $l_3$ | 0.62 | yes | covered |

The threshold is set at $0.45$ rather than the round $0.60$ one might assume, because real LaBSE cosines for short clause–outcome pairs are lower than for full sentences: here the three intended matches land at $0.50$–$0.65$ and the clear non-matches at $0.24$–$0.34$, so the natural separation sits near $0.45$. This is itself a reminder that $\tau$ must be calibrated to the encoder and text length, not fixed by intuition. Coverage ratio $\rho_{0.45} = 3/6 = 0.50$. The gap set is
$$ G_{0.45} = \{\, c_2 \text{ (threat intelligence)},\; c_3 \text{ (incident management)},\; c_4 \text{ (supply-chain security)} \,\}. $$

### 8.3 Reading the result

A covered clause behaves as expected. Clause $c_6$ (multi-factor authentication) matches outcome $l_3$ at 0.62, among the highest scores in the matrix, because both texts name the same control directly. The verdict function returns $v(c_6) = l_3$, and an auditor confirms the match in seconds.

The three gaps are the point of the exercise. The syllabus never addresses threat intelligence ($c_2$, best 0.28) or supply-chain security ($c_4$, best 0.24); no outcome comes near either clause. The third gap is the instructive one. Clause $c_3$ (incident management) finds its best match in outcome $l_2$, "recognise phishing and report incidents to the service desk," yet scores only 0.34 — below $\tau$. The two texts share the surface token *incident*, so a keyword scan would mark the clause covered, but LaBSE correctly separates a staff duty to *report* an incident from the organisational duty to *plan and prepare* incident management. The explicit-gap output catches exactly the requirement that a lexical check would conceal. A coverage percentage of 50% on its own would not tell an auditor *which* requirements failed; the gap list names all three, so the curriculum owner knows precisely which modules must be added before the programme can claim alignment with Article 21. This is the practical payoff of treating $G_\tau$, not $\rho_\tau$, as the primary result.

### 8.4 Threshold sensitivity

The gap set depends on $\tau$, so the audit reports its sensitivity rather than fixing one value silently. Moving the threshold across the two borderline clauses — $c_3$ (incident management, $s_3 = 0.34$) at the low end and $c_5$ (hygiene, $s_5 = 0.50$) at the high end — shows the trade-off:

| $\tau$ | Covered | Gap set | Risk |
|--------|---------|---------|------|
| 0.30 | $c_1,c_5,c_6$ + $c_3$ | $\{c_2,c_4\}$ | $c_3$ admitted on a weak 0.34 match — false assurance |
| 0.45 | $c_1,c_5,c_6$ | $\{c_2,c_3,c_4\}$ | balanced |
| 0.55 | $c_1,c_6$ | $\{c_2,c_3,c_4,c_5\}$ | $c_5$ now flagged — conservative, more manual review |

A lower threshold hides real gaps behind weak matches; a higher one floods the auditor with borderline clauses. The method does not choose $\tau$ for the user. It exposes the consequence of the choice, which keeps the audit reproducible and the residual judgement with the human expert.

### 8.5 False matches and their containment

Cosine proximity can in principle reward topical overlap that is not true coverage. To test this, we encoded a decoy outcome, "control physical access to the server room," against clause $c_6$ (multi-factor authentication): both concern *access control*, yet a building-access lesson does not satisfy an MFA requirement. LaBSE scored the pair at only 0.15 — far below any reasonable $\tau$ — so in this slice the encoder separated the two adjacent controls cleanly rather than producing the feared false match. That is reassuring but not a guarantee: cosine remains a topical-similarity signal, and the explicit-gap design contains the failure mode in two ways regardless. First, every covered pair is surfaced with its score and its source outcome for human confirmation, so a plausible-but-wrong match is visible rather than asserted. Second, the load-bearing claim of the method is recall on the gap list — catching missing requirements — not precision on matches, so a conservative auditor can raise $\tau$ and let borderline matches fall into the gap list for review. This is the same propagation-of-error caution that Skliarenko et al. [3] documented when a single pipeline stage produced spurious similarity.

### 8.6 Cross-lingual spot check

The cross-lingual claim is the method's most distinctive practical promise, so we tested it directly by re-encoding three outcomes in Ukrainian and matching them against the English clauses:

| Ukrainian outcome (gloss) | English clause | $s_i$ |
|---------------------------|----------------|-------|
| "Explain the organisation's security policy and staff duties" | $c_1$ A.5.1 policy | 0.66 |
| "Apply strong passwords and multi-factor authentication" | $c_6$ NIS2 MFA | 0.55 |
| "Follow cyber-hygiene habits in daily work" | $c_5$ NIS2 hygiene | 0.36 |

Two of the three Ukrainian outcomes match their English clause above $\tau = 0.45$, at scores close to the English originals (0.66 against 0.65 for the policy clause; 0.55 against 0.62 for MFA), confirming that translation-free auditing is feasible. The hygiene pair, however, falls to 0.36 — below the threshold and well under the English outcome's 0.50 — which shows that cross-lingual scores can sit lower than monolingual ones. A conservative margin on $\tau$, or a domain- and language-calibrated threshold, is therefore advisable when curriculum and standard are in different languages.

## 9. Conclusion

This paper presented a sentence-embedding method for auditing cybersecurity training curricula against the clauses of NIS2 and ISO/IEC 27001. The method embeds clause and learning-outcome texts into a shared multilingual space, matches them by cosine similarity, and models the audit verdict as a partial function whose undefined region — the uncovered clauses — is returned as the primary result. A worked example over a slice of ISO/IEC 27001:2022 Annex A.5 and NIS2 Article 21(2), run through an actual LaBSE encoder, showed the pipeline locating three coverage gaps that an aggregate score would have concealed — including an incident-management clause that a keyword scan would have wrongly marked covered — and a cross-lingual spot check confirmed Ukrainian outcomes matching English clauses without translation.

The contribution is the explicit-gap design. By reporting what a curriculum fails to cover, rather than only what it covers, the method gives a curriculum owner an actionable list and gives an auditor a reproducible, language-neutral screen. The approach reuses the text-comparison method of Skliarenko et al. [3], draws its competence framing from Arsenovych et al. [4], and sits within the formal information-security-management context of Lakhno et al. [25]; its partial-function treatment of the undefined region extends earlier work on narrowed domains of definition (Rykhalskyy [5]).

### 9.1 Limitations

Three limitations bound the claims. Cosine similarity signals topical relatedness, not proven requirement satisfaction, so a high score can reward overlap that does not amount to compliance; the method is therefore a triage screen, not a verdict. The gap set depends on the threshold $\tau$, and although the pipeline exposes this dependence and we calibrate it to the encoder rather than assuming a round value, choosing $\tau$ remains an expert decision without a principled optimum. The worked example, though now produced by a real LaBSE run rather than stipulated, still exercises a small synthetic slice rather than a labelled corpus, so precision and recall on the gap list — the method's load-bearing metric — are demonstrated as feasible but not yet quantified at scale.

### 9.2 Future work

Three directions follow from these limits. An empirical study on a labelled curriculum-and-standard dataset would quantify gap-recall and calibrate $\tau$. A domain-specific encoder such as SecureBERT 2.0 (Aghaei et al. [21]) could replace the general LaBSE model where cybersecurity vocabulary dominates, and its cross-lingual coverage would need evaluation. Finally, an LLM re-ranking stage could review borderline matches near $\tau$ and supply the explanation that requirements-engineering researchers have argued compliance tools should provide (Hassani et al. [13]), turning the screen into an explained audit while keeping the explicit-gap output at its core.

---

## Declarations

**Data Availability.** No new datasets were generated. The worked example in Section 8 uses publicly available clause text from ISO/IEC 27001:2022 Annex A and NIS2 Article 21(2) together with a synthetic illustrative syllabus reproduced in full in the paper. The reported similarity scores are produced by an actual run of the `sentence-transformers/LaBSE` encoder (L2-normalised embeddings, cosine similarity) over the clause and outcome texts as printed; the short encoding script that reproduces every figure in Section 8 is available from the author on request.

**Funding.** This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

**Conflict of Interest.** The author declares no conflict of interest.

**Ethics Statement.** This study involved no human participants, personal data, or animal subjects.

**Author Contributions (CRediT).** Oleksiy Rykhalskyy: Conceptualization, Methodology, Formal analysis, Writing – original draft, Writing – review & editing.

**AI Usage Disclosure.** The author used an AI assistant to support the literature search, citation verification, and editing of this manuscript. All sources were verified against their original publications, and the author takes full responsibility for the content.

---

## References

*Scopus quartile (SJR, latest available) is shown immediately after the reference number where the source is a Scopus-indexed journal or book series. SCImago does not assign quartiles to conference proceedings or to non-indexed venues, so these and arXiv preprints carry no quartile.*

[1]Q1 Amaral Cejas, O., Azeem, M. I., Abualhaija, S., & Briand, L. C. (2023). NLP-based automated compliance checking of data processing agreements against GDPR. *IEEE Transactions on Software Engineering, 49*(9), 4282–4303. https://doi.org/10.1109/TSE.2023.3288901

[2] Gokhan, T., Wang, K., Gurevych, I., & Briscoe, T. (2024). *RIRAG: Regulatory information retrieval and answer generation.* https://arxiv.org/abs/2409.05677

[3] Skliarenko, O., Pashko, A., Lytvynenko, L., & Kolodinska, Y. (2025). Deep learning models for solving the problem of comparing unstructured textual information. *Bulletin of Taras Shevchenko National University of Kyiv. Physics and Mathematics, 80*(1), 157–163. https://doi.org/10.17721/1812-5409.2025/1.21

[4]Q4 Arsenovych, L., Nikolaievsky, O., Skliarenko, O., Lytvynenko, L., & Kydriavskyi, I. (2024). Organization of training with the use of digital technologies for ensuring cybersecurity in the educational space. *WSEAS Transactions on Computer Research, 12,* 524–536. https://doi.org/10.37394/232018.2024.12.51

[5] Rykhalskyy, O. Yu. (2025). Narrowing of domains of definition as a path to improving software correctness [Звуження областей визначення як шлях до підвищення коректності програмного забезпечення]. *Measuring and Computing Devices in Technological Processes, 1*(81), 362–372. https://doi.org/10.31891/2219-9365-2025-81-46

[6] Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP-IJCNLP 2019)* (pp. 3982–3992). Association for Computational Linguistics. https://doi.org/10.18653/v1/D19-1410

[7] Gao, T., Yao, X., & Chen, D. (2021). SimCSE: Simple contrastive learning of sentence embeddings. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP 2021)* (pp. 6894–6910). Association for Computational Linguistics. https://doi.org/10.18653/v1/2021.emnlp-main.552

[8] Xu, J., Shao, W., Chen, L., & Liu, L. (2023). SimCSE++: Improving contrastive learning for sentence embeddings from two perspectives. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)* (pp. 12028–12040). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.emnlp-main.737

[9] Feng, F., Yang, Y., Cer, D., Arivazhagan, N., & Wang, W. (2022). Language-agnostic BERT sentence embedding. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL 2022)* (pp. 878–891). Association for Computational Linguistics. https://doi.org/10.18653/v1/2022.acl-long.62

[10] Muennighoff, N., Tazi, N., Magne, L., & Reimers, N. (2023). MTEB: Massive Text Embedding Benchmark. In *Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2023)* (pp. 2014–2037). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.eacl-main.148

[11] Chen, J., Xiao, S., Zhang, P., Luo, K., Lian, D., & Liu, Z. (2024). M3-Embedding: Multi-linguality, multi-functionality, multi-granularity text embeddings through self-knowledge distillation. In *Findings of the Association for Computational Linguistics: ACL 2024* (pp. 2318–2335). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.findings-acl.137

[12]Q2 Guder, L., Aires, J. P., da Silva, H. U., Meneguzzi, F., & Griebler, D. (2026). Sentence representations for semantic textual similarity: A systematic review. *Computer Speech & Language, 100,* 101970. https://doi.org/10.1016/j.csl.2026.101970

[13] Hassani, S., Sabetzadeh, M., Amyot, D., & Liao, J. (2024). Rethinking legal compliance automation: Opportunities with large language models. In *2024 IEEE 32nd International Requirements Engineering Conference (RE)* (pp. 432–440). IEEE. https://arxiv.org/abs/2404.14356

[14] Hassani, S. (2024). *Enhancing legal compliance and regulation analysis with large language models.* https://arxiv.org/abs/2404.17522

[15] Zhu, L., Yang, L., Li, C., Hu, S., Liu, L., & Yin, B. (2024). *LegiLM: A fine-tuned legal language model for data compliance.* https://arxiv.org/abs/2409.13721

[16] Hassani, S., Sabetzadeh, M., & Amyot, D. (2025). *An empirical study on LLM-based classification of requirements-related provisions in food-safety regulations.* https://arxiv.org/abs/2501.14683

[17] Li, S., Chen, J., Yao, R., Hu, X., Zhou, P., Qiu, W., Zhang, S., Dong, C., Li, Z., Xie, Q., & Yuan, Z. (2025). *Compliance-to-Code: Enhancing financial compliance checking via code generation.* https://arxiv.org/abs/2505.19804

[18] Aushev, I., Kratkov, E., Nikolaev, E., Glinskii, A., Krikunov, V., Panchenko, A., Konovalov, V., & Belikova, J. (2025). RAGulator: Effective RAG for regulatory question answering. In *Proceedings of the 1st Regulatory NLP Workshop (RegNLP 2025)* (pp. 114–120). Association for Computational Linguistics.

[19]Q2 Zheng, T., Shen, S., & Zeng, C. (2025). A retrieval-augmented generation method for question answering on airworthiness regulations. *Electronics, 14*(16), 3314. https://doi.org/10.3390/electronics14163314

[20]Q4 Aghaei, E., Niu, X., Shadid, W., & Al-Shaer, E. (2023). SecureBERT: A domain-specific language model for cybersecurity. In *Security and Privacy in Communication Networks (SecureComm 2022)* (LNICST Vol. 462, pp. 39–56). Springer. https://doi.org/10.1007/978-3-031-25538-0_3

[21] Aghaei, E., Jain, S., Arun, P., & Sambamoorthy, A. (2025). *SecureBERT 2.0: Advanced language model for cybersecurity intelligence.* https://arxiv.org/abs/2510.00240

[22]Q1 Nautiyal, L., & Rashid, A. (2024). A framework for mapping organisational workforce knowledge profile in cyber security. *Computers & Security, 145,* 103925. https://doi.org/10.1016/j.cose.2024.103925

[23] Sargolzaei Javan, M. (2025). *A semantic model for audit of cloud engines based on ISO/IEC TR 3445:2022.* https://arxiv.org/abs/2510.09690

[24] Rykhalskyy, O. Yu. (2025). Architecture of an intelligent decision-support system based on semantic matching of models [Архітектура інтелектуальної системи підтримки рішень на основі семантичного узгодження моделей]. *Information Technologies and Society, 2/2025.* https://doi.org/10.32689/maup.it.2025.2.24

[25]Q4 Lakhno, V. A., Kasatkin, D. Y., Skliarenko, O. V., & Kolodinska, Y. O. (2022). Modeling and optimization of discrete evolutionary systems of information security management in a random environment. In *Machine Learning and Autonomous Systems* (Smart Innovation, Systems and Technologies, Vol. 269, pp. 9–22). Springer. https://doi.org/10.1007/978-981-16-7996-4_2

[26]Q1 Antoniol, G., Canfora, G., Casazza, G., De Lucia, A., & Merlo, E. (2002). Recovering traceability links between code and documentation. *IEEE Transactions on Software Engineering, 28*(10), 970–983. https://doi.org/10.1109/TSE.2002.1041053

[27]Q1 Borg, M., Runeson, P., & Ardö, A. (2014). Recovering from a decade: A systematic mapping of information retrieval approaches to software traceability. *Empirical Software Engineering, 19*(6), 1565–1616. https://doi.org/10.1007/s10664-013-9255-y

<!-- EDITORIAL NOTE: References [28]-[33] were added during revision and are appended here in
insertion order, not yet renumbered. Because the citation style is "numbered by order of
appearance" and the forthcoming Section 8 (Experimental Evaluation) will introduce/move further
citations, run a single global renumber-by-appearance pass only once the manuscript structure is
frozen. Quartiles for indexed journals are added per SCImago (latest available, 2024): [29] Computer
Q2, [32] Systematic Reviews Q1, [33] TACL Q1. [28] (EU legislation), [30] (monograph), and [31]
(conference proceedings) carry no quartile. Re-verify these on scimagojr.com before submission. -->

[28] Directive (EU) 2022/2555 of the European Parliament and of the Council of 14 December 2022 on measures for a high common level of cybersecurity across the Union, amending Regulation (EU) No 910/2014 and Directive (EU) 2018/1972, and repealing Directive (EU) 2016/1148 (NIS2 Directive). *Official Journal of the European Union, L 333,* 80–152. http://data.europa.eu/eli/dir/2022/2555/oj

[29]Q2 Meyer, B. (1992). Applying "Design by Contract". *Computer, 25*(10), 40–51. https://doi.org/10.1109/2.161279

[30] Winskel, G. (1993). *The Formal Semantics of Programming Languages: An Introduction.* MIT Press.

[31] Bowman, S. R., Angeli, G., Potts, C., & Manning, C. D. (2015). A large annotated corpus for learning natural language inference. In *Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing (EMNLP 2015)* (pp. 632–642). Association for Computational Linguistics. https://doi.org/10.18653/v1/D15-1075

[32]Q1 O'Mara-Eves, A., Thomas, J., McNaught, J., Miwa, M., & Ananiadou, S. (2015). Using text mining for study identification in systematic reviews: A systematic review of current approaches. *Systematic Reviews, 4,* 5. https://doi.org/10.1186/2046-4053-4-5

[33]Q1 Artetxe, M., & Schwenk, H. (2019). Massively multilingual sentence embeddings for zero-shot cross-lingual transfer and beyond. *Transactions of the Association for Computational Linguistics, 7,* 597–610. https://doi.org/10.1162/tacl_a_00288
