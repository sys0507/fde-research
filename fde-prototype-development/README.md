# Business prototype preparation and development

`fde-prototype-development` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Prepares a complete package that can be handed to a developer on its own, or, when this round explicitly asks for implementation, builds a runnable, repeatable business prototype with continuous state.

## Place in the full chain

Connects scenarios into an operable work application for requirements review; it can run before the business proposal is finalized, and its findings flow back.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Business and scenarios|Complete originals, candidate functions, scenario steps/pages/captures or equivalent material|5 or another source; a final business proposal is not required|
|Rules and scope|This round's functions, states, responsibilities, normal and exception paths, simulation boundaries|User requirements, effective records, and collaborative clarification|
|Existing engineering|Source code, technical/visual conventions, current feedback, and demonstration data|The user's existing assets or earlier outputs|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|Preparation mode|Project introduction, complete development requirements, handoff prompt, originals snapshot, page/state/seed/acceptance conventions|Status handoff_ready, handed to developers|
|Implementation mode|Runnable source code, dependency and configuration examples, local data, start/demo/reset instructions|The requester actually walks through the process|
|Implementation evidence and feedback|Per-scenario coverage, real run captures, state verification, and requirement findings|Business proposal, scenario revision, implementation readiness/architecture reference|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. First decide whether this round is preparation or implementation, reuse an existing handoff, and do not go beyond scope on your own.
2. Unify lists, details, roles, to-dos, and records around business objects, and define each action's input, output, and state.
3. Implementation mode defaults to local data and reproducible simulated answers; queries, calculations, saving, and state must actually execute.
4. Actually start it and walk through the agreed scenarios, verify continuous state and important recovery, and then deliver source code, evidence, and feedback.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read fde-prototype-development/SKILL.md and use the specified scenarios and business originals to implement a locally runnable ticket prototype covering all agreed scenarios. State clearly that data and AI responses are simulated, share state between list and detail, actually verify saving, handover, duplicate submission, and important failures, and deliver the source code and run instructions.
```

Hosts that support skill syntax can use `$fde-prototype-development`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only fde-prototype-development. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/fde-prototype-development` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

Yes. It accepts the scenario skill or equivalent material and does not depend on Codex, a specific model service, or course tools. When only development preparation is requested, no source code or run captures are needed; application development starts only with an explicit implementation request.

## Completion criteria and boundaries

Preparation mode ends with a complete, readable handoff; implementation mode ends when the in-scope core functions are implemented, actually runnable, and the main path and load-bearing states are verified. Generated source code, a passing build, or page captures each cannot on their own stand for a finished application.

By default it is not a production application. Role switching is not production authentication, a simulated receipt is not a successful enterprise interface call, and preset answers are not real model inference. The prototype cannot serve as evidence of realized benefits.

## Handoff and continued changes

Keep the upstream function/scenario IDs. The preparation status handoff_ready is kept separate from run completion; feedback flows back to scenarios and the business proposal, and implementation readiness/architecture receive the explicit simulated nature and the entry to actually reusable code. Demonstration capabilities must not be counted as completed production integration.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [Standalone development handoff](references/development-requirements-and-handoff.md)
- [From scenarios to product](references/scenarios-to-product.md)
- [Data and simulation](references/data-state-and-simulation.md)
- [Verification and delivery](references/verification-and-delivery.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.
