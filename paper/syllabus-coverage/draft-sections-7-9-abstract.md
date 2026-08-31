# Draft — Sections 7 (Novelty), 9 (Conclusion), and Bilingual Abstract

*Headline contribution: explicit-gap design. Final connective and closing sections.*

---

## 7. Novelty of Results

The novelty of the work lies in three results that together distinguish it from the methods reviewed in Section 2.

The first and central result is the **explicit-gap design**. Prior compliance-checking systems report what they match — a coverage score, a classification, or a generated answer — and absorb the unmatched remainder into an aggregate or a default branch. We instead model the audit verdict as a partial function whose undefined region is computed and returned as the primary output. The set of uncovered clauses $G_\tau$ is a first-class artefact, ranked and presented to the auditor, rather than a residue inferred from a percentage. To our knowledge no prior curriculum- or contract-auditing method treats the gap, rather than the coverage, as the deliverable.

The second result is **language-neutral auditing without a translation stage**. By embedding clauses and learning outcomes into the shared LaBSE space, a Ukrainian curriculum is audited directly against an English standard. This removes the manual translation step that earlier compliance pipelines assume, and with it a documented source of propagated error (Skliarenko et al., 2025). The contract-checking work of Amaral Cejas et al. (2023) and the regulatory question-answering systems of Gokhan et al. (2024) and Zheng et al. (2025) operate monolingually; cross-lingual coverage auditing is new in this setting.

The third result is **reproducibility with the residual judgement kept explicit**. The method fixes no threshold silently. It reports the coverage matrix, the gap list, and a threshold-sensitivity analysis, so a second auditor replaying the pipeline obtains the same scores and sees the same consequence of any threshold choice. This contrasts with manual auditing, where Section 3 noted that two experts rarely agree or leave a replayable record. The pipeline does not replace expert judgement; it makes the point at which judgement enters visible and auditable.

---

## 9. Conclusion

This paper presented a sentence-embedding method for auditing cybersecurity training curricula against the clauses of NIS2 and ISO/IEC 27001. The method embeds clause and learning-outcome texts into a shared multilingual space, matches them by cosine similarity, and models the audit verdict as a partial function whose undefined region — the uncovered clauses — is returned as the primary result. A worked example over a slice of ISO/IEC 27001:2022 Annex A.5 and NIS2 Article 21(2) showed the pipeline locating two genuine coverage gaps that an aggregate score would have concealed.

The contribution is the explicit-gap design. By reporting what a curriculum fails to cover, rather than only what it covers, the method gives a curriculum owner an actionable list and gives an auditor a reproducible, language-neutral screen. The approach reuses the text-comparison method of Skliarenko et al. (2025), draws its competence framing from Arsenovych et al. (2024), and sits within the formal information-security-management context of Lakhno et al. (2022); its partial-function treatment of the undefined region extends earlier work on narrowed domains of definition (Rykhalskyy, 2025a) and on semantic matching of models (Rykhalskyy, 2025b).

### 9.1 Limitations

Three limitations bound the claims. Cosine similarity signals topical relatedness, not proven requirement satisfaction, so a high score can reward overlap that does not amount to compliance; the method is therefore a triage screen, not a verdict. The gap set depends on the threshold $\tau$, and although the pipeline exposes this dependence, choosing $\tau$ remains an expert decision without a principled optimum. The worked example demonstrates feasibility on a small slice rather than measuring accuracy on a labelled corpus, so precision and recall on the gap list are not yet quantified.

### 9.2 Future work

Three directions follow from these limits. An empirical study on a labelled curriculum-and-standard dataset would quantify gap-recall and calibrate $\tau$. A domain-specific encoder such as SecureBERT 2.0 (2025) could replace the general LaBSE model where cybersecurity vocabulary dominates, and its cross-lingual coverage would need evaluation. Finally, an LLM re-ranking stage could review borderline matches near $\tau$ and supply the explanation that requirements-engineering researchers have argued compliance tools should provide (Hassani et al., 2024), turning the screen into an explained audit while keeping the explicit-gap output at its core.

---

## Bilingual Abstract

### Abstract (English)

The NIS2 Directive makes demonstrable cybersecurity training a legal obligation, yet auditing whether a training curriculum covers the required regulatory clauses is still manual, subjective, and bound to one language. This paper presents a sentence-embedding method that audits a curriculum against the clauses of NIS2 and ISO/IEC 27001 and reports the uncovered requirements as its primary result. Clause units from the standard and learning-outcome units from the curriculum are embedded into a shared multilingual space with a language-agnostic encoder, matched by cosine similarity, and separated by a threshold. The audit verdict is modelled as a partial function whose undefined region — the clauses no learning outcome addresses — is returned as a ranked gap list rather than hidden inside an aggregate coverage score. This explicit-gap design is the contribution: it gives a curriculum owner an actionable list of missing topics and gives an auditor a reproducible, cross-lingual screen that needs no prior translation. A worked example over a slice of ISO/IEC 27001:2022 Annex A.5 and NIS2 Article 21(2) locates two genuine coverage gaps that a coverage percentage alone would conceal, and a threshold-sensitivity analysis keeps the residual judgement explicit and with the human expert. The method is positioned as a triage screen whose load-bearing claim is recall on the gap list, not precision on matches. Limitations and an empirical evaluation are identified as future work.

**Keywords:** sentence embeddings; compliance auditing; NIS2 Directive; ISO/IEC 27001; semantic textual similarity; cybersecurity training; partial functions.

### Анотація (українською)

Директива NIS2 робить документально підтверджене навчання з кібербезпеки правовим обов'язком, проте перевірка того, чи покриває навчальна програма потрібні нормативні положення, залишається ручною, суб'єктивною та прив'язаною до однієї мови. У статті запропоновано метод на основі речникових вкладень (sentence embeddings), який зіставляє навчальну програму з положеннями NIS2 та ISO/IEC 27001 і подає непокриті вимоги як основний результат. Одиниці положень стандарту та одиниці результатів навчання програми відображаються у спільний багатомовний простір за допомогою мовнонезалежного кодувальника, зіставляються за косинусною подібністю та розділяються пороговим значенням. Рішення аудиту змодельовано як часткову функцію, область невизначеності якої — положення, що їх не охоплює жоден результат навчання — повертається як впорядкований перелік прогалин, а не приховується в агрегованому показнику покриття. Саме цей підхід явного виявлення прогалин є внеском роботи: він дає власникові програми дієвий перелік відсутніх тем, а аудиторові — відтворюваний міжмовний інструмент попередньої перевірки без потреби у попередньому перекладі. Наведений приклад на фрагменті ISO/IEC 27001:2022 (додаток A.5) та статті 21(2) NIS2 виявляє дві справжні прогалини покриття, які відсоток покриття приховав би, а аналіз чутливості до порогу залишає остаточне рішення за експертом. Метод позиціоновано як інструмент попереднього сортування, ключове твердження якого — повнота виявлення прогалин, а не точність зіставлень.

**Ключові слова:** речникові вкладення; аудит відповідності; Директива NIS2; ISO/IEC 27001; семантична подібність тексту; навчання з кібербезпеки; часткові функції.
