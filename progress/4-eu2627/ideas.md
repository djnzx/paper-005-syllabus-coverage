# Ideas: Connecting eu* References to the Partial Functions Article

Article topic: **ASPECTS OF USING PARTIAL FUNCTIONS TO MODEL NARROWED DOMAINS IN
PROGRAMMING**

---

## Idea 1 — Implicit partiality in expert systems and anomaly detectors

**Cite:** eu2, eu6 (anomaly/cyber-attack classification), eu5 (intelligent DSS
for cyber protection)

Expert system decision rules and anomaly classifiers are textbook partial
functions: the classification function is defined only for feature vectors
within the trained distribution. eu2 and eu6 build sign-clustering classifiers
for cyber-attack recognition — the functions are implicitly partial (undefined
for unknown sign combinations) but modeled as total. A subsection of the body
could argue that formalizing such decision rules as
`PartialFunction[FeatureVector, Verdict]` instead of
`FeatureVector => Option[Verdict]` makes the undefined region explicit rather
than collapsing it into a fallback branch. eu5's DSS is a second example of the
same phenomenon at the system level.

**Effort:** medium — requires ~1 page added to the body with one new code-level
example.

---

## Idea 2 — Domain stability bounds in formal stochastic models

**Cite:** eu9 (semi-Markov ISMS), eu1 (bilinear differential game for
investment)

Both papers derive analytical results valid only within a specific region of the
state space: eu9's stability theorem holds near the zero solution (equilibrium),
eu1's winning-strategy sets exist only when initial endowments lie inside a
particular polytope. Neither paper formalizes these restrictions at the model
interface level. A subsection could argue that the applicability bounds of
mathematical models — the state-space region where the result is meaningful —
are precisely the domain of a partial function, and that encoding them as such
at the API boundary prevents misuse by downstream components. This extends the "
contextual domain narrowing" thread already present in `06-related-works.md`.

**Effort:** medium — extends the existing related works section.

---

## Idea 3 — Preprocessing pipelines and compositional partiality

**Cite:** eu7 (deep learning for legal text comparison)

eu7's NLP pipeline is a chain of partial transformations:
`parse_html → segment_articles → embed → compute_cosine`. Each step is defined
only for specific input shapes (non-empty articles, non-zero vectors), and the
paper documents how a failure at one step (spurious similarity at low threshold,
tables breaking HTML parsing) invalidated all downstream results. This is a
concrete real-world illustration of composed partial functions and the
propagation of domain violations through a pipeline. A new subsection on "
compositional partiality in data processing pipelines" could use it as a
motivating example, showing how `andThen` chaining in Scala or `>=>` in Haskell
makes the overall domain explicit rather than hidden in ad-hoc guards.

**Effort:** medium — ~0.5–1 page of new material and one new diagram or code
block.

---

## Idea 4 — Partial functions as a contract mechanism in DSS integration

**Cite:** eu4 (management of information protection via integrated DSS), eu3 (
cyber security support for transport)

eu4 argues that integrating multiple decision support subsystems into a unified
platform introduces consistency risks — the article's introduction already
identifies exactly this problem (model components designed by one engineer,
consumed by another in a different context). eu3 and eu4 are applied instances
of that failure mode: each DSS module has an implicit domain, and integration
without formalizing those domains causes unreliable results. They can be cited
in the introduction or related works as empirical evidence from the applied DSS
literature that domain ambiguity at integration boundaries is a real engineering
problem — motivating the formal solution that the rest of the paper develops.

**Effort:** low — 2–3 sentences added to the existing introduction or problem
statement; no new sections required.

---

## Pragmatic Ranking

| Idea                          | Effort | Naturalness                                           | Best candidates |
|-------------------------------|--------|-------------------------------------------------------|-----------------|
| 4 — DSS integration contracts | Low    | High — directly supports existing intro argument      | eu3, eu4        |
| 1 — Expert system partiality  | Medium | High — concrete code-level argument                   | eu2, eu6        |
| 2 — State-space domain bounds | Medium | Medium — requires bridging math models to types       | eu9, eu1        |
| 3 — NLP pipeline composition  | Medium | Medium — requires extending scope to data engineering | eu7             |

**Recommended path:** Idea 4 as the lowest-risk entry point. Ideas 1 and 3
together give a natural "applied examples" section with strong diversity (
cybersecurity + NLP). Idea 2 is strongest intellectually but requires the most
bridging work.
