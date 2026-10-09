# AI technical architecture and development plan

`design-ai-project-architecture` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Researches technical choices from the business effect and constraints, designs systems, data, permissions, deployment, failure, and human takeover, and breaks down development and verification tasks.

## Place in the full chain

Takes over business requirements and implementation conditions and outputs a reviewable technical design for implementation scheduling and quotation.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Requirements and business|Final functions, scope, responsibilities, quality targets, scenarios, and originals|4/5/6 and real effective decisions|
|Implementation conditions|Final handoff, limits, resources, interfaces, and new assets|7 or equivalent effective material|
|Technical basis|Existing experiments/code/technical decisions, current official material|User assets and this round's actual research|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|Technical design MD/Word|Recommended route, component responsibilities, end-to-end chain, development/verification, and resources|Technical review, 9 work breakdown|
|Standard diagrams|Editable diagram sources, actual static renderings, and checks|Report illustrations, design handoff|
|Archify enhancement, optional|Specification, interactive HTML, static images, tool receipts, and browser checks|Explicitly requested interactive explanation|
|Internal basis|Baseline conditions, inputs/research/decisions, rounds, delivery manifest|Version recovery and targeted revision|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. Read the complete effective scope and originals, and set up confirmed / design presets / to be settled / key unknowns.
2. Research current candidates and make an explicit recommendation with conditions for switching; do not fix a model list.
3. Along a representative task, design entry, identity, data, tools, results, persistence, and failure recovery, forming the starting point of the work packages.
4. New projects default to standard diagrams; use archify when it is specified or inherited; generate the complete Word document and actually render it / look at the images.
5. Check files and hashes with the manifest, then check semantics, text–diagram consistency, and requirement coverage, and hand over to 9.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read design-ai-project-architecture/SKILL.md and complete the technical design based on the specified business proposal and implementation conditions. Use the standard diagram contract, verify current technology, and produce a complete Word document, editable diagram sources, and actual static images, stating component responsibilities, work dependencies, verification, and unsettled conditions.
```

Hosts that support skill syntax can use `$design-ai-project-architecture`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only design-ai-project-architecture. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/design-ai-project-architecture` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

Yes. It accepts equivalent effective business and technical conditions. Standard for new projects does not depend on Archify; an existing archify contract is not downgraded automatically. It needs files, current-material search, diagram rendering, and Word capability; when these are insufficient, mark a partial delivery.

## Completion criteria and boundaries

Every complete requirement has a technical owner, load-bearing choices have a basis, and the report, diagrams, conditions, development, and verification agree; the deliverables and real visual checks are complete. A diagram source or a successful command is not text–diagram acceptance by itself.

It can break down development work, but detailed per-person calendars, service quotation, and profit go to 9. A design recommendation is not a live implementation and does not automatically connect to production or procure equipment. 20 rounds is this skill's upper limit on proactive questions, and continuation does not reset it.

## Handoff and continued changes

Read the business scope, the implementation-readiness final handoff, and the originals index, and make diagram_profile explicit. Give the implementation plan the technical design version, shared/incremental work, real prerequisite outputs, resources, verification, and conditions; new enterprise facts flow back to the readiness review, and business changes flow back to the proposal.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [Run and manifest contract](references/run-contract.md)
- [Selection method](references/selection-method.md)
- [System design](references/system-design.md)
- [Standard and Archify diagrams](references/architecture-delivery.md)
- [Word delivery](references/word-delivery.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.

Actual PDF font checks are described in [Word delivery](references/word-delivery.md) and the [font inspector](scripts/check_pdf_fonts.py). The build and delivery-acceptance tools of 8 and 9 are intentionally maintained separately; only the font inspector is synchronized as a shared copy.
