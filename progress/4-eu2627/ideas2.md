# Research Ideas That Naturally Cite the eu* Articles

These are standalone research directions — independent of the partial functions
article — where the eu* papers would be cited as direct prior work, not as
forced references.

---

## Idea A — Ontology-based knowledge representation for cybersecurity expert systems

**Cites naturally:** eu2, eu5, eu6

**The gap:** eu2 and eu6 build adaptive expert systems where classification
rules are stored as implicit feature clusters (sign vectors). eu5 extends this
to operational cyber protection management. All three encode domain knowledge in
ad-hoc tabular or cluster structures without a shared semantic layer, making
cross-system knowledge reuse and rule auditing difficult.

**Research direction:** Propose an ontology (OWL/RDF) or knowledge graph schema
for representing cyber-threat signatures, response rules, and their
applicability conditions in a machine-readable, interoperable form. Show how the
clustering results from eu2 and eu6 map onto ontology classes and property
axioms, and how eu5's DSS decision logic becomes a SPARQL query or a
description-logic inference chain.

**Why the citation is natural:** eu2, eu5, eu6 are the empirical baseline — they
establish that rule-based expert systems work for this problem class but do not
address knowledge interoperability. The proposed paper positions itself as the
next step, improving on their architecture while crediting their validated
results.

**Target journals:** Eastern-European Journal of Enterprise Technologies,
Advances in Intelligent Systems and Computing.

---

## Idea B — Formal interface contracts for integrated cybersecurity DSS modules

**Cites naturally:** eu3, eu4, eu5

**The gap:** eu4 explicitly identifies that integrating multiple protection
subsystems introduces consistency risks across module interfaces. eu3 and eu5
build individual DSS modules for transport networks and
object-of-informatization protection without specifying formal
pre/postconditions at the integration seams. This mirrors a classical software
engineering failure mode: components designed independently and connected
informally.

**Research direction:** Apply design-by-contract (DbC) methodology —
preconditions, postconditions, invariants — to the module interfaces of
cybersecurity DSS architectures of the type described in eu3, eu4, eu5. Use a
formal notation (Eiffel contracts, JML, or Alloy assertions) to specify what
each module guarantees and requires. Demonstrate on a composed prototype that
contract violations at integration time are caught statically rather than
discovered at runtime.

**Why the citation is natural:** eu3, eu4, and eu5 are used as the architectural
case studies whose interface contracts are being retroactively specified. The
paper cites them as sources of the integration problem and as the empirical
context validating the proposed contract approach.

**Target journals:** Eastern-European Journal of Enterprise Technologies,
Information Systems Architecture and Technology (ISAT proceedings, Springer
AISC).

---

## Idea C — NLP-assisted automated compliance checking for cybersecurity training standards

**Cites naturally:** eu7, eu8

**The gap:** eu8 studies whether digital technology raises cybersecurity
competence in learners. eu7 develops a supervision-free NLP pipeline for
semantic comparison of multilingual legal documents. Neither paper connects the
two: no existing tool automatically checks whether a given cybersecurity
training curriculum satisfies the semantic requirements of regulatory
frameworks (NIS2 Directive, ISO/IEC 27001 Annex A, Ukrainian cybersecurity
standards).

**Research direction:** Adapt the multilingual sentence-embedding pipeline from
eu7 to compare training program syllabi against normative regulatory texts,
producing a structured compliance gap report. eu8 provides the pedagogical
baseline: which competency categories are targeted by current digital training,
and which are underrepresented. The combined output is a reproducible,
language-neutral compliance auditing tool.

**Why the citation is natural:** eu7 provides the NLP method being applied; eu8
provides the educational context and competency taxonomy that defines what "
compliance" means. Both are direct methodological predecessors.

**Target journals:** Bulletin of Taras Shevchenko National University of Kyiv (
Physics & Mathematics), WSEAS Transactions on Computer Research.

---

## Idea D — Digital twin architecture for cybersecurity monitoring of transport and smart city systems

**Cites naturally:** eu1, eu3, eu4, eu9

**The gap:** eu3 builds a DSS for transport network cybersecurity but relies on
manual data inputs and periodic reassessment. eu1 models smart city investment
as a differential game but does not address real-time state observation. eu4
integrates protection subsystems without continuous system mirroring. eu9
provides a formal stochastic ISMS model but lacks a simulation layer. Digital
twin technology — a continuously synchronized virtual replica of a physical
system — provides exactly the missing real-time observability layer.

**Research direction:** Propose a reference architecture for a cybersecurity
digital twin in which: (a) the stochastic ISMS model from eu9 serves as the
formal state-space backbone; (b) the transport-network threat taxonomy from eu3
defines the event schema; (c) the protection-subsystem integration model from
eu4 organizes the functional modules; and (d) the game-theoretic investment
logic from eu1 governs resource allocation when the twin detects an emerging
threat. Validate the architecture with a tabletop scenario.

**Why the citation is natural:** Each eu* paper contributes one architectural
layer. This framing makes every citation substantive — not background padding,
but direct conceptual input to the proposed system.

**Target journals:** Studies in Systems, Decision and Control (Springer), Smart
Innovation, Systems and Technologies (Springer).

---

## Idea E — Stochastic game model for multi-party cybersecurity investment with incomplete information

**Cites naturally:** eu1, eu9

**The gap:** eu1 models mutual investment in smart city technology as a bilinear
differential quality game with two investors. eu9 models the ISMS as a discrete
evolutionary system under random perturbations using semi-Markov dynamics.
Neither paper combines both aspects: eu1 ignores stochastic environment
transitions; eu9 ignores the multi-investor strategic interaction. Yet real
cybersecurity funding decisions involve multiple stakeholders (state, private
operator, insurer) each acting under incomplete information about the others'
budgets and threat assessments.

**Research direction:** Formulate a stochastic bilinear game in which the system
state evolves as a semi-Markov chain (following eu9's ISMS model) and two or
more investors simultaneously choose capital allocation strategies (following
eu1's game framework). Derive existence conditions for equilibrium strategies
under the stochastic dynamics. Discuss how the semi-Markov sojourn times —
absent from eu1's deterministic game — change the shape of the winning strategy
sets identified in eu1.

**Why the citation is natural:** This is a direct theoretical generalization of
eu1 and eu9 — both are cited as the models being extended, not as background
context.

**Target journals:** Cybernetics and Systems Analysis, Recent Research in
Control Engineering and Decision Making (Springer SSDC), Eastern-European
Journal of Enterprise Technologies.

---

## Summary

| Idea                                     | Core contribution                                              | Cites              |
|------------------------------------------|----------------------------------------------------------------|--------------------|
| A — Ontology for cyber expert systems    | Semantic interoperability layer for rule-based DSS             | eu2, eu5, eu6      |
| B — Formal contracts for DSS modules     | DbC methodology applied to DSS integration architectures       | eu3, eu4, eu5      |
| C — NLP compliance auditing              | Automated regulatory gap analysis for cybersecurity curricula  | eu7, eu8           |
| D — Cybersecurity digital twin           | Reference architecture for real-time transport/city monitoring | eu1, eu3, eu4, eu9 |
| E — Stochastic multi-party security game | Semi-Markov bilinear game for multi-investor ISMS              | eu1, eu9           |

Ideas A, B, and C are the most tractable for a single-author journal article (~
12–18 pages). D and E are richer but require more theoretical or architectural
depth.
