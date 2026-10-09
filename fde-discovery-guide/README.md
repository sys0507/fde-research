# Business investigation guide

`fde-discovery-guide` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Breaks a vague request into investigable questions and organizes interviews, evidence collection, process mapping, and asset accumulation along the real business process, so that later design rests on facts.

## Place in the full chain

The investigation entry of the full chain, organizing Stages 1–5; it reads baseline analysis at Stage 4 and business diagnosis at Stage 5.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Minimum to start|Original request, known background, project write location; one sentence of need is enough to start|User-provided|
|Added step by step|Interviews/verbal accounts, documents, real screenshots, system descriptions, actual exports and field meanings|User originals or obtained with authorization|
|Continuing|Current overview, stage documents, asset inventory, latest problems, effective decisions, and new materials|Reuse of earlier outputs and originals|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|Stages 1–3|Request breakdown, interviews, evidence collection, current-state process, assets and fields|Baseline, diagnosis, scenarios|
|Stage 4|Measurement results and limits after reading the sibling baseline skill|Diagnosis and business proposal|
|Stage 5|Recommendations and report entry after reading the sibling diagnosis skill|Scenarios and business proposal|
|Ongoing records|Business overview, investigation actions, revision impact, and actual material locations|Project artifact index and cross-session recovery|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. First read the current case and its effective versions, and list known facts and the gaps that most affect judgment.
2. Investigation preparation → interviews about representative business cases → on-site evidence collection; stages whose materials already exist can be reused directly, and interviews that never happened are not fabricated.
3. Define measurement tasks from the actual problems; Stage 4 reads the sibling fde-baseline-analysis and Stage 5 the sibling fde-business-diagnosis.
4. Update output entries, original sources, unmeasured items, and recommendation status, and hand the diagnosis and assets to scenarios/business proposal.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read fde-discovery-guide/SKILL.md and start the investigation from "we want to improve ticket handling efficiency". The project directory and existing notes are at the paths I provide. First map the current state and gaps, collaborate with baseline and diagnosis at Stages 4/5, and maintain the artifact index; metrics without data are written as not measured.
```

Hosts that support skill syntax can use `$fde-discovery-guide`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only fde-discovery-guide. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/fde-discovery-guide` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

It can serve on its own as the investigation entry. To execute Stages 4/5 fully, fde-baseline-analysis and fde-business-diagnosis must sit at the same level as this folder. Existing equivalent outputs can be reused; missing skill files must not be used as an excuse to claim the corresponding specialized work was done.

## Completion criteria and boundaries

Within this round's investigation scope there are actual stage outputs, sources, and explicit gaps; completing the full investigation chain needs a baseline or a not-measured statement, diagnosis recommendations, and usable asset entries. The work may end within bounds despite important gaps; completion is not judged by the number of chat rounds.

It does not directly replace data calculation, detailed technical design, or project quotation; it does not create real interviews, customer approvals, or production system screenshots.

## Handoff and continued changes

At startup, read the project artifact index (if any). Hand the original request, scope, process, actual original entries, and effective versions to baseline/diagnosis; after Stage 5, hand over to scenario design or the business proposal. Keep asset and problem IDs; changes update only the affected downstream work.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [Investigation template](assets/templates/00-business-case-overview.md)
- [Investigation action list](assets/templates/investigation-action-list.md)
- [Revision impact record](assets/templates/revision-impact-record.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.
