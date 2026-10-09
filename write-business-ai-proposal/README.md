# Writing the AI business transformation proposal

`write-business-ai-proposal` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Lets the requesting side judge why to change, which work changes, how it will be handled in the future, what people and machines each take on, what it depends on, and how the effect is measured.

## Place in the full chain

Integrates the diagnosis, candidate functions, scenarios, and optional prototype into a requirements baseline for business review; implementation-readiness review comes next.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Diagnosis and basis|Diagnosis report, actual originals, current-state process, and recommendations|The first three skills or equivalent outputs|
|Concrete proposal material|Candidate functions, target process, action-level permissions, conditions for success, baseline and target derivation|The scenario skill, business discussion, and effective originals|
|Demonstration and format|Scenario/prototype images with their nature and version, proposal readers, phase, customer template|Outputs of 5/6 (if any) or user material|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|Complete source draft and formal Word|Decision summary, scope, function process, human–machine responsibilities, targets, verification, and conditions|Business review and implementation-readiness review|
|Traceability and open items|Source–requirement mapping, human review list, open conditions|The currently effective requirements baseline|
|Production record|Actual input versions, build, and real rendering checks|Later revisions and cross-session handoff|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. Read the complete materials and distinguish facts, recommendations, teaching settings, derived targets, and approvals.
2. Settle functions as included / conditional / later / excluded, and state inputs, actions, results, takeover, and failure.
3. Check the baseline, target formulas, and assumptions, and count the new human review burden.
4. Put scenario or actual prototype captures next to the corresponding requirements, generate the complete Word document, and actually render it.
5. Deliver a draft pending human review, record the real review/requirement confirmation, and then hand the effective version to 7.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read write-business-ai-proposal/SKILL.md and use the specified diagnosis, baseline, scenarios, and condition records to write the phase-one business proposal, stating scope, human–machine responsibilities, targets, and verification; generate an editable Word document and check the actual rendering. Items without a confirmed basis stay as recommendations or to be verified.
```

Hosts that support skill syntax can use `$write-business-ai-proposal`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only write-business-ai-proposal. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/write-business-ai-proposal` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

Yes. Equivalent diagnosis, originals, process, responsibility, and estimation material is enough; calling the first three skills is not required. Scenarios (5) can support writing directly; the prototype (6) is an optional enhancement, not a precondition for writing.

## Completion criteria and boundaries

The body is complete and traceable, the Word/specified format matches the source draft, and real check results are explicit; when critical gaps remain unresolved, keep a draft or conditional status. Human review and requester approval are recorded separately.

The business proposal is not a technical architecture, engineering schedule, or contract quotation. Without an actual review it does not pose as passed; generating Word does not mean the requirements are approved.

## Handoff and continued changes

The complete scenario text/captures from scenario design can be used directly; the prototype only enhances as needed. Integrate the baseline and diagnosis; what is handed to implementation-readiness review is the effective scope, action-level responsibilities, targets, conditions, real confirmation status, and the originals index. The output file itself does not mean business approval.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [Inputs and evidence](references/inputs-and-evidence.md)
- [Proposal structure](references/proposal-structure.md)
- [Word format and review](references/word-format-and-review.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.
