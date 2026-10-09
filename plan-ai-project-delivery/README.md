# Implementation plan, cost estimation, and quotation

`plan-ai-project-delivery` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Produces a proposal that can organize implementation, support fee review, and be discussed as a contract annex: work breakdown, per-person resource schedule, acceptance, service quotation, separately paid and recurring costs.

## Place in the full chain

The implementation and commercial-preparation end of the full chain, taking over the effective business scope, conditions, and final technical route.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Required business basis|Current scope, delivery and quality targets, actual confirmation status|Business proposal or equivalent output|
|Implementation and technical basis|Final implementation-readiness handoff/originals, final architecture, starting points for work and verification|7/8 or equivalent material|
|Cost and resources|Staff capacity, actually reusable code, cost/commercial/time and fee responsibilities|The user's existing material; when missing, explicit presets with a basis can be proposed|
|Existing estimate, optional|A complete old quotation or partial prices/periods the user specifies to keep|Enters inherited mode; automatic full re-estimation is forbidden|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|Customer main report MD/Word|Scope, organization, schedule, cooperation, acceptance, service price, taxes/separately paid/recurring costs|Human review and commercial discussion|
|Customer annexes|Delivery scope and acceptance details, external preset conditions|Basis for project contract/implementation discussion; not a signed contract|
|Internal calculation and notes|Model/inherited baseline, result CSV, cost and profit basis, sensitivity|Supplier-side accounting; must not be distributed with the customer package|
|Real verification record|Input/output index, calculation and Word hashes, full-page QA, changes|Review and targeted recalculation|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. Confirm first full estimate or inherited mode, and read the authoritative versions of the three kinds of facts.
2. For a first estimate, break down manual activities, agent work, real prerequisites, and API requests under ai_collaborative_v1, and schedule capacity per person per day.
3. Calculate with the script, separating staff occupancy from active hours, external waiting, customer/supplier responsibility, development API, and production run costs.
4. Write the complete commercial body first, then generate the report from the same numeric source; keep internal and external presets separate.
5. Generate Word along the codex or generic path, update the table of contents, actually render and review page by page, and record hashes and the delivery index.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read plan-ai-project-delivery/SKILL.md and make a first full estimate based on the specified business, implementation conditions, and technical design. Use the generic document path, proactively propose staff/cost presets with a basis, and produce a feasible schedule, acceptance, a customer quotation Word document, and separate internal workpapers. Unknown run costs are marked unknown.
```

Hosts that support skill syntax can use `$plan-ai-project-delivery`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only plan-ai-project-delivery. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/plan-ai-project-delivery` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

Yes. Not having call records of earlier skills does not affect use, but equivalent effective material is needed. Calculation needs only the Python standard library; complete Word supports the Codex documents path and the generic local Python/LibreOffice path, suitable for Claude Code and other agents with the needed capabilities.

## Completion criteria and boundaries

Model/inherited numbers agree, work maps to requirements, staff capacity is feasible, fee responsibilities are clear, customer and internal material are separated, and the complete source draft, an actual editable Word document, and real check records are all present. Without Word rendering it is marked as acceptance check not completed, and a first draft is not treated as customer acceptance.

It does not reselect technology, procure, sign, or deploy. A demonstration prototype does not automatically count as production reuse; person-days are not schedule duration, and a correct calculation does not prove a credible estimate. Having only one lead FDE is an optional recommendation and does not assume that person can carry any project.

## Handoff and continued changes

Inherit the business scope, implementation conditions, and final technical design; do not infer production capability from architecture diagrams or prototype captures. Make the estimate/inherited mode and the codex/generic path explicit, and deliver the customer report/acceptance/presets and the separate internal calculation; when the budget or schedule does not hold, feed back to the technical/business choices and do not silently cut scope.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [General workflow](references/workflow.md)
- [Codex-specific path](references/codex-workflow.md)
- [Runtime environment choice](references/runtime-profiles.md)
- [Two modes and versions](references/run-and-assumptions.md)
- [Inherited estimate](references/inherited-proposal.md)
- [Model contract](references/model-contract.md)
- [Word path and commands](references/word-delivery.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.

Actual PDF font checks are described in [Word delivery](references/word-delivery.md) and the [font inspector](scripts/check_pdf_fonts.py). The build and delivery-acceptance tools of 8 and 9 are intentionally maintained separately; only the font inspector is synchronized as a shared copy.
