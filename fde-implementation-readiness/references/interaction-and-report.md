# Interaction and reporting contract

## 1. Continuous project state

The report records one project's evolving conditions. Its body serves FDEs/designers with existing facts, usable estimates, critical evidence gaps, and later engineering checks; full traceability belongs in appendices.

Save each analysis in its own directory/report and link the previous round. Track completed human evidence rounds separately: initial material analysis is round count 0. Archive inputs/answers and update the unified index using [assets and handoff](assets-and-handoff.md). Record provider, intake round, date, environment, and evidence nature; unknown dates stay unknown. Simulated material cannot confirm real enterprise facts; explicit exercises follow [optional simulation](optional-simulation.md).

State what comparisons/estimates are now possible, what assumptions limit them, and whether customer questions remain. Choose “verification in progress” or “verification complete for the current scope.” Completion means sufficient design basis, not production activation, procurement, POC, or performance acceptance.

## 2. Facts, inference, and verification

| Evidence | Supports | Limitation |
|---|---|---|
| Confirmed business requirements | Required capability, responsibility, standards, constraints | Provider statement is not a signature or proof of existing capability |
| Role's oral/written explanation | Information within that role's responsibility | Preserve provider/scope; request originals based on decision risk, not automatically |
| Technical documentation/configuration | Specified capability, settings, limits | Check version/applicability; not project activation |
| Originals/data examples | Sample facts, structure, relationships | Not total scale, data quality, or continuous access |
| Actual check | Observation in stated environment, identity, object, time, method | Not untested load, objects, or lasting reliability |
| Reasonable estimate/inference | Planning range, capacity, effort | State basis/scope; not customer confirmation, commitment, or measurement |

No mechanical evidence-grade threshold. Obtain enough for feasibility, and calibrate detail to decision impact:

- **Must establish now:** critical data access, processing locations, access responsibility, authority for important actions, and limits that could invalidate the path. Never infer permission or treat silence as consent. Specific authorized-role explanations can support design before accounts are actually opened.
- **May estimate:** ordinary/peak load, initial capacity, work, and expense basis. Record grounded ranges/assumptions, source, applicability, necessary method, sensitivity, and calibration. Low-impact estimates can be brief; do not require a signed workbook for each. Never lower existing commitments through estimates.
- **Verify later:** detailed errors, connectivity, isolation, model effects, load/recovery, final prices, resource delivery, and production activation when the route/constraints are already supported. Record object, stage, role, and failure treatment. If failure would invalidate the entire plan without an alternative, it remains a current critical risk.

An unknown that does not affect major decisions may remain unknown; do not force a number. Record cost items, charging basis, sourced ranges, and variation instead of inventing prices.

## 3. Stable IDs and independent statuses

Reuse IDs; otherwise R=requirement/constraint, C=condition, Q=question, E=evidence, and A=assumption if helpful. Shared conditions reference multiple functions/scenarios. Conditions use available, pending verification, needs supplementation, constrained, or conflicting.

| Q status | Meaning/record | Ask again? |
|---|---|---|
| Resolved | Sufficient answer with basis/scope, including confirmed absence/limitation | No |
| Proceed under assumption | Grounded planning basis linked to impact/calibration | Only if a material decision changes |
| Later verification | Design basis sufficient; record stage, role, failure treatment | Not as current evidence request |
| Awaiting response | Critical current answer missing | Include a specific grouped task |
| Partial response | Useful facts plus a critical remaining difference | Ask only that difference |
| Approved deferral | Authorized decision with basis, scope, limits | At its trigger/time |

Assumed is not confirmed; deferred validation is not passed; the FDE's own scheduling is not approved deferral. For a compound old Q, preserve its ID and identify each part's disposition. A still-critical unanswered part determines whether to ask again. Keep IDs/evidence after closure or transfer. Superseded evidence remains historical but no longer supports the current conclusion. Do not report completion as a question-closure percentage.

## 4. Group only necessary questions

Organize facts, use justified inference, then ask. Every question must explain how answers change feasibility, major design, work, or major expense. Do not ask again for sufficient, low-sensitivity, or later-engineering details.

Group a complete evidence request by provider, reusing existing materials and explanations. Keep independently judged Q IDs but answer several in one interaction. Add conditional branches when one answer changes the next evidence needed.

For awaiting/partial critical questions specify:

1. Q, function, and decision affected.
2. Material holder and authorized decision role; do not invent named commitments.
3. Exact question, export request, or authorized check.
4. Minimum file/sample/fields/conclusion, without unrelated sensitive data or one form per question.
5. Return path, source, date, scope; combine explanations using the [verification record](../assets/verification-record-template.md).
6. What becomes known, estimable, or deferred.

Record oral statements accurately with provider, role, date, object/scope, basis, and actual confirmation state. Distinguish quotations and FDE paraphrases. Ordinary planning does not need repeated confirmation for formality; authority/scope/major commitments need an identifiable authorized role.

**Identity example:** request a permitted sanitized record containing transaction ID, employee ID, and field meaning; obtain mapping if login IDs differ, plus authorized record-access rules. Once mapping/authority support design, account opening and isolation testing can remain later integration tasks. Unknown access policy is a different, current critical gap.

**Resource example:** ask infrastructure/internal-model owners what can be requested, where it runs, entry/data boundaries, existing quota/fee basis, expansion options, approvers, and known lead times. Existing lists and application conditions may suffice. Estimate initial capacity from scale/configuration and grounded calculations, retaining alternatives and calibration. Do not demand final quota, procurement approval, and load testing as a readiness gate, or equate permission to apply with allocation.

## 5. Process responses

1. Save original answers/materials and index paths before analysis; associate Q by object if no ID is supplied. “Discussed” without content is insufficient.
2. Separate facts, role estimates, and conflicts by environment/scope. “Has API” does not prove every action but may combine with action details to support integration estimates.
3. Decide whether remaining differences affect current decisions. Estimate where justified, defer actual implementation checks, and ask only critical unknowns. A known absence becomes a limitation/treatment, not repeated demands for nonexistent documents.
4. Update R/C, Q status, impact, and sources. Preserve competing evidence and decision ownership.
5. Create Q only for genuinely new critical objects. Keep a complete readable report, summarizing changes in facts, assumptions, later checks, and remaining questions.

## 6. Completion and round control

Complete only when:

- All functions, scenes, and supplied samples are covered with original core/conditional/future scope intact; all dimensions reviewed and nonapplicable items explained.
- Candidate designs and reasonable effort/cost ranges are supportable; critical data, processing, authority, and paths are not invented.
- Known limitations have acceptable treatment. FDEs may propose engineering arrangements within scope; changing standards/responsibilities/scope requires the appropriate owner.
- Estimates have basis/range/calibration and later checks have object/stage/role/failure treatment proportionate to risk.
- No unanswered critical issue lacks an acceptable assumption or alternative. Not every Q must become resolved and not every effect/price/performance needs measurement now.

Aim for one grouped collection and normally finish within three human evidence rounds. Submitting necessary questions and receiving real answers counts as one; analysis/reorganization does not. Subsequent rounds ask only new critical differences. At closure say “No further customer evidence request is needed for this stage” and transfer assumptions/later checks.

Three is a soft limit. If still blocked, present concrete alternatives within scope, authorized scope change, or a pause of the blocked path with impacts. If more evidence rounds are necessary, explain the minimum need and follow the project's decision; do not loop indefinitely or fabricate closure.

## 7. Report organization

Use the template's five body sections and appendices. Keep consequential facts, assumptions, and next actions in the body. Explain causality, e.g., batch-only export requires scheduled import and routine operation, rather than saying “affects architecture.”

Use compact function/scene, sample-use, and dimension-coverage tables, adding real differences only. Do not create a function × scenario × dimension Cartesian table. Include every input ID and future-scope disposition.

## 8. Wait or finish

If a critical request remains, deliver the grouped tasks and wait for real feedback. Without new material, do not invent enterprise answers. At closure automatically create the final handoff and unified asset index, not just the last progress report. Link current report/index/state and preserve historical rounds when new evidence changes conclusions. Simulate only under explicit scope and stopping instructions.
