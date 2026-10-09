# Business scenario and before/after design

`fde-ai-scenario-design` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Writes candidate functions as understandable work processes for specific roles, and builds local HTML simulations and real browser captures of before, after, and the results of key operations.

## Place in the full chain

Usually after diagnosis and before the business proposal is finalized; it can also iterate repeatedly together with the proposal.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Factual starting point|Business overview, diagnosis, current-state process, documents, roles, rules, definitions|Investigation/diagnosis outputs and originals|
|Candidate functions|Work to improve, proposed functions, and their current status|Diagnosis recommendations, user ideas, or an existing proposal|
|Supplementary conditions|Key actions, permissions, exceptions, and handover rules|Effective records or a collaborative draft; teaching fabrication needs explicit authorization|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|scenario-comparison.md/html|Complete before/after steps, operation results, responsibilities, sources, function mapping, and open items|Business proposal, prototype requirements, implementation readiness|
|screens/|Local pages that open directly and whose main operation produces a concrete content change|Demonstration and prototype reference|
|images/ and actual receipts|Actual browser before/after/result captures and check status|Report illustrations and traceable evidence|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. Each scenario centers on a main operator, a task, and a result; before and after use the same object and point in time.
2. First write entry, actions, returns, judgments, and handovers, then design the matching pages; do not turn every capability into a chat box.
3. Actually open the pages, perform the main operation, check the content, and capture; the overview page is not a simulated system capture.
4. Hand over the complete scenarios and the function/original mapping for the business proposal to use directly or for the prototype to implement further.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read fde-ai-scenario-design/SKILL.md and, based on the specified diagnosis and candidate functions, design the ticket intake, missing-material follow-up, and assignment scenarios. Use the same business starting point, build before/after HTML simulations, perform the main operation and capture it, and output MD/HTML with sources. Mark the interface as a proposal simulation; do not fake the live system.
```

Hosts that support skill syntax can use `$fde-ai-scenario-design`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only fde-ai-scenario-design. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/fde-ai-scenario-design` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

Yes. Candidate functions and sufficient business basis are enough to start; a final business proposal, a real model, or enterprise interfaces are not required. The bundled build and capture scripts are optional helpers; the host's existing browser capability can also be used.

## Completion criteria and boundaries

The scenario text can be understood on its own, before/after and captures have consistent data states, the main operation has a concrete result, and the MD/HTML and page links work. Without a browser, text and pages can be delivered with captures pending.

Local scenario pages are not a complete cross-scenario application and do not prove model effect, enterprise approval, or real integration. Fixed teaching numbers are for examples only. The default simulation marker is configurable but cannot hide the simulated nature.

## Handoff and continued changes

It takes over the diagnosis, originals, and candidate functions; it gives the business proposal the complete scenarios, before/after images, and responsibilities directly, and gives the prototype the pages, states, and sources. Scenario IDs are kept; a new button on a page does not automatically become a confirmed requirement.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [Scenario template](references/scenario-description.md)
- [Simulated interfaces and captures](references/simulation-and-screenshots.md)
- [Delivery data and script use](references/delivery-data-and-rendering.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.
