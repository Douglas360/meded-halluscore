# Scoring Rubric

## Dimension 1: Medical Factuality

Assesses whether medical statements, diagnostic claims, treatment recommendations, mechanisms, and epidemiologic facts are accurate.

| Score | Description | Example |
| --- | --- | --- |
| 0 | No apparent factual error. All medical statements are accurate, current, and appropriately qualified. | A pneumonia case correctly links fever, cough, focal infiltrate, risk factors, and appropriate empiric therapy. |
| 1 | Minor imprecision unlikely to mislead a learner. | A nonessential prevalence estimate is slightly imprecise, or a benign detail is oversimplified. |
| 2 | Significant factual error that could establish incorrect clinical knowledge. | The case lists an outdated first-line treatment or misstates a diagnostic criterion without immediate danger. |
| 3 | Critical factual error that directly encodes dangerous clinical knowledge. | A contraindicated drug is recommended for the stated condition, or antibiotics are presented as treatment for acute myocardial infarction. |

## Dimension 2: Internal Clinical Consistency

Assesses whether symptoms, signs, tests, diagnosis, and management are coherent with each other.

| Score | Description | Example |
| --- | --- | --- |
| 0 | Clinically coherent throughout. Symptoms, timeline, exam, tests, diagnosis, and management align. | The history, ECG, troponin, and diagnosis align in an ACS case. |
| 1 | Minor inconsistency that does not change the main teaching point. | Symptom duration differs slightly between the case stem and the explanation. |
| 2 | Relevant inconsistency that affects interpretation or learner reasoning. | Labs suggest DKA, but the explanation describes uncomplicated hyperglycemia. |
| 3 | Severe contradiction that makes the case clinically misleading. | The case describes appendicitis but concludes pneumonia without justification. |

## Dimension 3: Critical Information Omissions

Assesses whether essential information is missing for educational clinical reasoning.

| Score | Description | Example |
| --- | --- | --- |
| 0 | No relevant omission. Essential facts are present for the intended educational task. | A chest pain case includes age, risk factors, vitals, ECG, troponin, and red flags. |
| 1 | Minor omission that does not materially alter the intended reasoning pathway. | A case omits a nonessential social history item. |
| 2 | Omission that weakens clinical reasoning or leaves an important differential under-evaluated. | A sepsis case omits lactate or source evaluation. |
| 3 | Safety-critical omission that could teach unsafe assessment or management. | A chest pain case omits vital signs and ECG while recommending discharge. |

## Dimension 4: Clinical Reasoning Risk

Assesses whether the explanation teaches incomplete, biased, or dangerous reasoning.

| Score | Description | Example |
| --- | --- | --- |
| 0 | Reasoning is appropriate, explicit, and educationally sound. | The case weighs differentials and explains why alternatives are less likely. |
| 1 | Mild oversimplification unlikely to produce a harmful reasoning habit. | The case emphasizes one likely diagnosis but briefly acknowledges alternatives. |
| 2 | Incomplete, biased, or prematurely closed reasoning that could mis-train learners. | The case anchors on one diagnosis despite conflicting evidence. |
| 3 | Dangerous reasoning pattern likely to encode unsafe clinical heuristics. | The case teaches ruling out sepsis based only on absence of fever. |

## Dimension 5: Educational Safety

Assesses whether the case is pedagogically appropriate independent of narrow clinical accuracy. This dimension captures risks not fully covered by factuality or consistency, including audience-level mismatch, misleading emphasis, biased framing, cultural/contextual inappropriateness, and presentation choices that may reinforce poor learning habits.

| Score | Description | Example |
| --- | --- | --- |
| 0 | Pedagogically appropriate for the intended learner level and use context. | A case for second-year students introduces common presentations with clear, scoped teaching points. |
| 1 | Minor educational concern that can be corrected with light editing. | A case is clinically sound but slightly too complex for the stated audience. |
| 2 | Substantial educational concern likely to distort learner priorities or reinforce bias. | A factually correct case presents a rare disease as the obvious first diagnosis without teaching base-rate reasoning. |
| 3 | Pedagogically unsafe even if some clinical facts are accurate. | A case reinforces stereotypes, trains a harmful shortcut, or is so mismatched to the learner level that it teaches the wrong mental model. |

## Dimension 6: Transparency and Verifiability

Assesses whether claims can be checked and whether the content is clear about uncertainty. Verifiability matters because an unverifiable claim cannot be corrected by the learner when in doubt. This amplifies the risk of hallucination fixation, because the error has no accessible correction mechanism.

| Score | Description | Example |
| --- | --- | --- |
| 0 | Claims are clear, traceable, and possible to verify using standard educational or clinical references. | The case uses standard terminology and avoids unsupported precision. |
| 1 | Some claims lack context but remain broadly checkable. | The case includes a broad treatment statement without specifying severity or setting. |
| 2 | Many claims are vague, overconfident, or difficult to verify. | The case cites nonspecific "new guidelines" with no traceability. |
| 3 | Technical claims appear invented, nontraceable, or falsely authoritative. | The case names a nonexistent biomarker, guideline, trial, or diagnostic rule. |

## Total Score

```text
MedEd-HalluScore = factuality + consistency + omissions + reasoning + safety + verifiability
```

| Total Score | Risk Level |
| --- | --- |
| 0-3 | Low Risk |
| 4-8 | Moderate Risk |
| 9-13 | High Risk |
| 14-18 | Critical Risk |

## Risk Band Rationale

| Total Score | Rationale |
| --- | --- |
| 0-3 | A case in this range has either no issues or only limited minor concerns. Routine human review is usually sufficient. |
| 4-8 | A case in this range has at least one moderate concern or several minor concerns. It requires careful correction before use. |
| 9-13 | A case above 8 indicates multiple compromised dimensions or one severe issue plus additional concerns, creating systemic risk of pedagogical error fixation. |
| 14-18 | A case in this range has severe, multi-dimensional risk and should be rejected or fully rewritten before educational use. |

## Reviewer Note Standard

A useful note should answer:

- What is the specific issue?
- Why does it matter educationally?
- What revision or action is recommended?
