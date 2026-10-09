# Implementation-readiness review and technical handoff

`fde-implementation-readiness` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Uses a six-dimension investigation to establish the real conditions, limits, reasonable estimates, and later verification needed for design and estimation, organizes new assets, and produces the final handoff.

## Place in the full chain

Takes over the currently effective business requirements and comes before technology selection and effort/quotation.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Business baseline|Current requirements/proposal, scope and human–machine responsibilities, review or provider notes|4 or equivalent effective material|
|Scenarios and originals|Policies, role permissions, samples, historical data, business processes|Reuse of earlier material; 5/6 provide design reference|
|Technical facts|Systems, interfaces, identity, network, deployment and resource material, role answers|Real owners/originals; simulated material cannot be a fact|
|Continuation material|Previous round's report, issue IDs, latest effective status, and this round's answers|This skill's history and new originals|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|Complete per-round review report|Six-dimension coverage, known/assumed/limits/key questions, consolidated evidence requests|The FDE drives the investigation|
|Unified asset entry|Original business assets, new material, issue status, and sources|Lookback for architecture and quotation|
|Final handoff report|Established conditions, handling approaches, estimation assumptions, later verification, and design tasks|8 architecture, 9 implementation plan and quotation|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. Inherit the effective requirements without redoing a full requirements engineering pass; locate shared technical dependencies by function.
2. Review along V1 non-functional, V2 quality scenarios, V3 systems and data, V4 interfaces/identity/permissions, V5 network and deployment, and V6 tracking assumptions.
3. Reuse material first, then request evidence consolidated by provider; aim for one round, with three rounds as a soft upper limit in principle.
4. Once the standard sufficient for candidate solutions and reasonable estimates is reached, automatically complete the final handoff and the index.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read fde-implementation-readiness/SKILL.md and review implementation conditions based on the confirmed business proposal, scenarios, and technical material. First organize what is known and reasonable estimates, ask follow-up questions only about gaps that affect the main solution, and on closing automatically deliver the final report and complete asset entry.
```

Hosts that support skill syntax can use `$fde-implementation-readiness`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only fde-implementation-readiness. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/fde-implementation-readiness` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

Yes. Input file names are not restricted, and it does not depend on the course or on earlier skills having run. Pure material analysis needs no enterprise tools installed and no production connection; real checks must stay within existing authorization and tool scope.

## Completion criteria and boundaries

Current conditions are sufficient to support the main design and a reasonable effort estimate, key limits have acceptable handling, and the final report and a usable index have been delivered. Marking questions complete or having only a progress report does not count as final handoff completion.

It does not make the final selection or the formal quotation; POCs, load tests, procurement, and production enablement are not thresholds that must always be completed at this stage. Yet the availability of key data and business authorization cannot be filled in with assumptions.

## Handoff and continued changes

It takes over the effective scope and status of the business proposal, looks back at the actual originals, and saves new technical material. It gives architecture/quotation the final handoff, the unified asset index, limits, assumptions, and later verification; if conflicts in business scope or responsibilities are found, it feeds them back to the business proposal and does not delete requirements on its own.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [Six-dimension review](references/verification-dimensions.md)
- [Interaction and closing](references/interaction-and-report.md)
- [Assets and final handoff](references/assets-and-handoff.md)
- [Final handoff template](assets/handoff-report-template.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.
