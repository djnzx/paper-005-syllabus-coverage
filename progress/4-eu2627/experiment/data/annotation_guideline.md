# Annotation Guideline — Curriculum Coverage of Regulatory Clauses

**Purpose.** Produce the ground-truth labels against which the automated method is
measured. Two annotators label independently; we then compute Cohen's κ and adjudicate
disagreements into the single gold file `gold_adjudicated.csv`.

## What you are labelling

For **each clause** in `clauses.csv` (47 clauses: NIS2 21(2) + ISO/IEC 27001 Annex A.5),
decide whether the **curriculum as a whole** — the union of all learning outcomes in
`outcomes.csv` (all three curricula C1+C2+C3) — **covers** that clause.

You fill two fields per clause in your copy of `gold_template.csv`:

- `covered` ∈ {1, 0} — 1 if at least one learning outcome covers the clause, else 0.
- `covering_outcome_ids` — semicolon-separated outcome IDs that cover it (e.g. `o05;o21`).
  Leave empty when `covered = 0`.
- `note` — optional one-line justification (encouraged for borderline calls).

## The decision rule (read carefully)

A clause is **covered** when a learning outcome would let a trained person **satisfy or
perform the obligation the clause states** — not merely when the two texts mention the
same topic.

- Ask: *"If a student achieved this outcome, would the clause's requirement be met for
  that person's role?"* If yes → covered.
- **Topic overlap is not coverage.** Sharing a keyword is not enough.
- A clause may be **organisational** (something the organisation must do, e.g. "establish
  contact with authorities") rather than something taught to staff. If no learning outcome
  could reasonably satisfy it, it is a **gap** — that is a legitimate and expected result.

## Worked examples

**Covered (positive):**
- Clause c10 (NIS2 multi-factor authentication) ← outcome o06 "Use multi-factor
  authentication to access corporate systems." The outcome directly satisfies the clause.
- Clause c11 (ISO A.5.1 policies for information security) ← outcome o01 "Explain the
  purpose of the organisation's information security policy and each employee's duties."
- Clause c07 (NIS2 basic cyber hygiene and training) ← outcome o07 "Follow basic
  cyber-hygiene habits…".

**Gap (negative) — the important cases:**
- Clause c34 (ISO A.5.24 **incident management planning and preparation** — an
  organisational duty) vs outcome o04 "Report a suspected security incident to the
  service desk." Both contain "incident", but reporting an incident is **not** planning
  and preparing incident management. → **gap** (do not mark covered on the shared word).
- Clause c17 (ISO A.5.7 threat intelligence) — no awareness outcome produces or analyses
  threat intelligence. → **gap**.
- Clause c30 (ISO A.5.20 information security in supplier agreements) — an organisational
  contracting duty, not a staff competence. → **gap**.

## Rules of thumb for borderline calls

1. **Perform vs mention** — require the outcome to enable doing the thing, not knowing of it.
2. **Role fit** — a general-staff outcome does not cover a specialist/organisational duty.
3. **Partial topics** — if an outcome covers only part of a multi-part clause, mark covered
   only if the part it covers is the clause's core obligation; otherwise gap + note.
4. **When genuinely unsure**, label your best judgement and flag it in `note` with `?`.

## Procedure

1. Each annotator works **independently** from their own copy:
   `cp gold_template.csv gold_<initials>.csv` (e.g. `gold_or.csv`, `gold_a2.csv`).
2. Do not discuss items during round 1.
3. Run `python src/stats.py --kappa gold_or.csv gold_a2.csv` → reports Cohen's κ.
   - If **κ ≥ 0.6**, proceed to adjudication.
   - If **κ < 0.6**, revise this guideline (sharpen the rule that caused disagreement) and
     re-label the disputed items.
4. **Adjudication session:** review every disagreement together; agree a final label.
   Write the agreed labels to `gold_adjudicated.csv` (same schema). This is the only file
   the metrics use.

## Output schema (`gold_adjudicated.csv`)

```
clause_id,covered,covering_outcome_ids,note
c01,1,o01;o12,policy + legal-obligation outcomes
c17,0,,no threat-intelligence content in any curriculum
...
```
