# Business diagnosis and AI opportunity assessment

`fde-business-diagnosis` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Explains the causes of actual problems, compares process, rule, existing-system, and AI improvement directions, and forms evidence-based recommendations and a complete business asset package.

## Place in the full chain

Investigation Stage 5 and the source of candidate functions; it can also advance a diagnosis independently from existing materials or a vague request.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Business facts|Request, roles, process, policies, interviews, and documents|User originals or reused from the investigation stage|
|Quantitative basis|Baseline, definitions, actual results, and sample limits|Baseline skill or a reliable equivalent output|
|Boundary conditions|Business authority, system limits, known constraints|Valid records; unknowns kept as to be verified|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|Seven-chapter diagnosis report|Current state, problems, causes, burden, opportunities, and recommendations|Stage 5, scenario design, business proposal|
|Investigation working record|Actual materials, targeted questions, answers, and revisions|Continuation and source tracing|
|Complete business asset package|Inventory, field dictionary, original materials, derived calculations|Every later stage traces back to originals|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. Read the materials along one concrete business case, distinguishing policy requirements, actual operations, and system capabilities.
2. Ask a few follow-up questions about gaps that affect the conclusions; information already known is not asked again.
3. Compare normal controls, extra labor, conventional improvements, and AI's actual contribution, keeping the baseline's limits.
4. Form the complete report and asset entries, and hand candidate improvements to scenarios and the business proposal for further detail.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read fde-business-diagnosis/SKILL.md. Using the specified investigation materials and baseline, determine the causes of the ticket handling burden, compare forms, rules, system interoperability, and AI assistance, and deliver the diagnosis report and complete asset package; keep recommendations in suggestion status.
```

Hosts that support skill syntax can use `$fde-business-diagnosis`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only fde-business-diagnosis. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/fde-business-diagnosis` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

Yes. It has the necessary investigation capability but is not responsible for the full five-stage process documents. With sufficient materials it analyzes directly; when quantification is insufficient it can work with the baseline skill, and items still unmeasured are stated as limits.

## Completion criteria and boundaries

The report matches the actual assets, important judgments have sources, and improvement suggestions state the object, the change in work, conditions, and human responsibilities; originals that cannot be copied have their controlled location stated.

It stops at problem diagnosis and opportunity recommendation; it does not directly approve a phase-one scope, designate the final technical route, or promise ROI.

## Handoff and continued changes

It takes over investigated facts, process, and the effective baseline, and hands over the diagnosis, candidate recommendations, original entries, and open items. Scenarios/business proposal can consume them directly; a recommended direction is not automatically upgraded into confirmed scope.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [Diagnosis method](references/interaction-and-diagnosis.md)
- [Asset delivery rules](references/business-assets.md)
- [Report template](assets/report-template.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.
