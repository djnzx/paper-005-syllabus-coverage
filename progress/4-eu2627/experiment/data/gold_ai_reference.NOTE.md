# About `gold_ai_reference.csv` — READ THIS

## What it is
A **single, AI-proposed labelling** of the 47 clauses against the verified
`outcomes.csv`, with reasoning in the `note` column. It is a labour-saving *draft*
and a *third opinion*, nothing more.

## What it is NOT
- It is **not** `gold_adjudicated.csv`. The pipeline (`run_all.py`) deliberately does
  not read it. Do not rename it to `gold_adjudicated.csv` and run metrics off it — that
  would mean the paper's results were labelled by an AI, not by human experts.
- It is **not** one of the two annotators. There is intentionally **no `gold_a1.csv`
  and no `gold_a2.csv` generated here.**

## Why there is no gold_a1 / gold_a2
Cohen's κ only means something if the two label sets come from **two independent human
annotators**. If both were produced from a single source (here, one AI), the κ would be
fabricated and the manuscript sentence *"two qualified annotators labelled independently,
κ = …"* would be false. That is data fabrication — the exact thing that turns a thin
paper into a retractable one. So the two annotator files must be produced by two people.

## The integrity-preserving way to use this file
1. Two human annotators **label the blank `gold_template.csv` independently and blind**
   — without looking at this AI reference first. Save as `gold_or.csv`, `gold_a2.csv`.
2. Compute κ: `python3 src/stats.py --kappa data/gold_or.csv data/gold_a2.csv`.
3. **Only during adjudication** may this AI reference be consulted as a tie-breaker /
   checklist, the same way you might consult a colleague's third opinion. Record the
   final agreed labels in `gold_adjudicated.csv`.
4. Disclose the AI-assisted pre-labelling in the manuscript's AI Usage statement.

This keeps the κ a real measurement of two humans, while still letting the AI draft save
time and catch oversights.

## Snapshot of this draft
- 6 clauses proposed *covered*, 41 proposed *gap* — gap-heavy, because the verified
  curriculum (an ENISA SME awareness set + a cryptography-focused university course)
  genuinely does not address most organisational and management controls.
- Borderline calls are flagged in the notes (c01, c17, c27, c44) — these are exactly the
  rows where independent human judgement matters most.
