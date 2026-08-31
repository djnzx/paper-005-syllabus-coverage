# Draft — Sections 6 (Methods) and 8 (Worked Example)

*Headline contribution: explicit-gap design. Embedding model: LaBSE. Example slice: ISO/IEC 27001:2022 Annex A.5 + NIS2 Article 21(2).*

---

## 6. Methods

The method audits a curriculum against a standard in five stages: clause segmentation, outcome segmentation, embedding, similarity matching, and gap extraction. The design goal is not a single coverage score but an explicit list of the requirements the curriculum fails to address. We therefore formalise the audit as a *partial* verdict function whose undefined region is the audit's main product.

### 6.1 Inputs as text-unit sets

Let the standard be decomposed into a finite set of clause units
$$ S = \{c_1, c_2, \dots, c_m\}, $$
where each $c_i$ is the smallest self-contained requirement statement — one ISO control or one NIS2 measure. Let the curriculum be decomposed into a set of learning-outcome units
$$ L = \{l_1, l_2, \dots, l_n\}, $$
where each $l_j$ is one learning outcome or module description. Segmentation granularity matters: a clause that bundles several obligations is split so that partial coverage is detectable rather than hidden inside one coarse unit.

### 6.2 Embedding into a shared semantic space

A single encoder $\varphi : \text{Text} \rightarrow \mathbb{R}^{d}$ maps both clause units and outcome units into one $d$-dimensional space. We use LaBSE (Feng et al., 2022) so that a Ukrainian learning outcome and an English clause are comparable without prior translation, which removes a translation step that would otherwise inject its own errors. Each unit is encoded once and cached, following the precomputation strategy that makes pairwise comparison scalable (Reimers & Gurevych, 2019).

### 6.3 Similarity and the per-clause match

Semantic proximity between a clause and an outcome is the cosine of their embedding vectors,
$$ \operatorname{sim}(c_i, l_j) = \frac{\varphi(c_i) \cdot \varphi(l_j)}{\lVert \varphi(c_i) \rVert \, \lVert \varphi(l_j) \rVert}. $$
For each clause we keep only its best-matching outcome and that outcome's score:
$$ s_i = \max_{1 \le j \le n} \operatorname{sim}(c_i, l_j), \qquad j_i^{\ast} = \arg\max_{1 \le j \le n} \operatorname{sim}(c_i, l_j). $$
The pair $(s_i, j_i^{\ast})$ is the evidence the auditor inspects: the strength of the best match and the outcome that produced it.

### 6.4 The coverage decision as a partial function

A threshold $\tau \in [0,1]$ separates covered clauses from uncovered ones. We define the audit verdict as a partial function $v$ over the clause set:
$$ v(c_i) = \begin{cases} l_{j_i^{\ast}}, & s_i \ge \tau \\ \text{undefined}, & s_i < \tau. \end{cases} $$
The covered set and the gap set follow directly:
$$ \mathrm{Cov}_\tau = \{\, c_i \in S : s_i \ge \tau \,\}, \qquad G_\tau = S \setminus \mathrm{Cov}_\tau = \{\, c_i \in S : s_i < \tau \,\}. $$
The aggregate coverage ratio is reported for context,
$$ \rho_\tau = \frac{\lvert \mathrm{Cov}_\tau \rvert}{\lvert S \rvert}, $$
but $\rho_\tau$ is explicitly the secondary output. The primary output is $G_\tau$, the set of clauses on which $v$ is undefined. Treating the gap as the domain complement of a partial function — rather than as a failure branch folded into a score — is what we mean by an explicit-gap design. The construction follows the principle that a narrowed domain of definition, made explicit, improves the correctness of the surrounding system (Rykhalskyy, 2025a): here the undefined region is not an error to suppress but the audit's deliverable. A clause the encoder cannot match is shown to the auditor, never silently defaulted.

### 6.5 Gap report and auditor review

The pipeline emits a coverage matrix of scores $s_i$, the covered pairs $(c_i, l_{j_i^{\ast}})$ ranked by confidence, and the gap list $G_\tau$ ranked by how far each clause falls below $\tau$. Because cosine proximity signals topical relatedness rather than proven requirement satisfaction, every covered pair is offered for human confirmation, not asserted as compliance. The method is positioned as a triage screen that concentrates expert attention on the gap list and on borderline matches near $\tau$, where Skliarenko et al. (2025) showed that spurious similarity is most likely.

---

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

Best-match scores $s_i$ at an illustrative threshold $\tau = 0.60$ (values are representative of LaBSE cosine ranges for this kind of short-text pair):

| Clause | Best outcome $j_i^{\ast}$ | $s_i$ | $s_i \ge \tau$ | Verdict |
|--------|---------------------------|-------|----------------|---------|
| $c_1$ A.5.1 policy | $l_1$ | 0.81 | yes | covered |
| $c_2$ A.5.7 threat intel | $l_2$ | 0.44 | no | **gap** |
| $c_3$ A.5.24 incident mgmt | $l_2$ | 0.71 | yes | covered |
| $c_4$ NIS2 supply chain | $l_4$ | 0.39 | no | **gap** |
| $c_5$ NIS2 hygiene & training | $l_4$ | 0.78 | yes | covered |
| $c_6$ NIS2 MFA | $l_3$ | 0.85 | yes | covered |

Coverage ratio $\rho_{0.60} = 4/6 \approx 0.67$. The gap set is
$$ G_{0.60} = \{\, c_2 \text{ (threat intelligence)},\; c_4 \text{ (supply-chain security)} \,\}. $$

### 8.3 Reading the result

A covered clause behaves as expected. Clause $c_6$ (multi-factor authentication) matches outcome $l_3$ at 0.85, the highest score in the matrix, because both texts name the same control directly. The verdict function returns $v(c_6) = l_3$, and an auditor confirms the match in seconds.

The two gaps are the point of the exercise. The syllabus never addresses threat intelligence ($c_2$) or supply-chain security ($c_4$); its closest outcomes — incident reporting and general hygiene — score well below $\tau$. A coverage percentage of 67% on its own would not tell an auditor *which* requirements failed. The explicit-gap output names them, so the curriculum owner knows precisely that two modules must be added before the programme can claim alignment with Article 21. This is the practical payoff of treating $G_\tau$, not $\rho_\tau$, as the primary result.

### 8.4 Threshold sensitivity

The gap set depends on $\tau$, so the audit reports its sensitivity rather than fixing one value silently. Raising and lowering the threshold around the borderline clause $c_3$ (incident management, $s_3 = 0.71$) shows the trade-off:

| $\tau$ | Covered | Gap set | Risk |
|--------|---------|---------|------|
| 0.50 | $c_1,c_3,c_5,c_6$ + $c_2$ | $\{c_4\}$ | $c_2$ admitted on a weak 0.44 match — false assurance |
| 0.60 | $c_1,c_3,c_5,c_6$ | $\{c_2,c_4\}$ | balanced |
| 0.75 | $c_1,c_5,c_6$ | $\{c_2,c_3,c_4\}$ | $c_3$ now flagged — conservative, more manual review |

A lower threshold hides real gaps behind weak matches; a higher one floods the auditor with borderline clauses. The method does not choose $\tau$ for the user. It exposes the consequence of the choice, which keeps the audit reproducible and the residual judgement with the human expert.

### 8.5 False matches and their containment

Cosine proximity can reward topical overlap that is not true coverage. Suppose an outcome read "control physical access to the server room." Against clause $c_6$ (multi-factor authentication) it might score moderately, because both concern *access control*, yet a building-access lesson does not satisfy an MFA requirement. The explicit-gap design contains this failure mode in two ways. First, every covered pair is surfaced with its score and its source outcome for human confirmation, so a plausible-but-wrong match is visible rather than asserted. Second, the load-bearing claim of the method is recall on the gap list — catching missing requirements — not precision on matches, so a conservative auditor can raise $\tau$ and let borderline matches fall into the gap list for review. This is the same propagation-of-error caution that Skliarenko et al. (2025) documented when a single pipeline stage produced spurious similarity.
