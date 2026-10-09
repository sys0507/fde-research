# Business baseline analysis

`fde-baseline-analysis` · [Agent instructions](SKILL.md) · [Nine-skill overview](../README.md)

Turns business problems into clearly defined, actually executed, recomputable metrics. It measures business elapsed time, manual effort, and business status separately, so expected benefits are never written up as measurements.

## Place in the full chain

The specialized calculation step of investigation Stage 4; it can also update the baseline of an existing project.

## Inputs

|Category|Contents|Source|
|---|---|---|
|Problems and scope|Identified problems, current-state process, observation period, and purpose of measurement|Investigation/diagnosis or equivalent material|
|Actual data|CSV/Excel/JSON, timing and observation records, field dictionary|Originals already provided upstream; an inventory cannot replace the data|
|Definitions and earlier results|Field meanings, inclusion/exclusion, start and end events, missing-value rules, reliable earlier baselines|Valid records; ambiguities verified with business staff|

## Outputs and downstream use

|Output|Contents|Handed to / used for|
|---|---|---|
|Metric definition cards|Metric ID, unit, period, sample, numerator/denominator, and limits|Diagnosis, target estimation, later comparison|
|Recomputation package|Actual scripts, dependencies, input versions, run commands/records|Review and update|
|Results and charts|Tables and charts from real runs, metric-by-metric interpretation|Stage 4, diagnosis, business proposal|

Project outputs are saved to the project directory the user specifies; this skill's folder stores only methods and resources. Existing originals, artifact indexes, and IDs are reused first and are not all moved just to match the templates.

## How to use it

1. Check for a reliable existing baseline; if no new measurement is needed, verify it and reuse it.
2. Define each metric and check encoding, primary keys, duplicates, joins, time zones, unfinished records, and missing values.
3. Actually execute the calculation, save the script, input versions, and results, and complete the necessary sanity checks.
4. Charts come from the result tables; explain what each conclusion does and does not show, and hand back the effective run and its limits.

Invocation example (with materials and the project path as this round's actual inputs):

```text
Read fde-baseline-analysis/SKILL.md and build a baseline from the ticket export, field descriptions, and process I provide. Count manual effort, waiting, and handling elapsed time separately, and save the actual script and recomputation record; locate definition conflicts first, and keep metrics without data as not measured.
```

Hosts that support skill syntax can use `$fde-baseline-analysis`; other agents read this folder's SKILL.md directly. Use existing equivalent materials directly; there is no need to rerun upstream skills just to complete the chain.

## Selecting this skill through the grouped unified entry

With the whole `skills` package installed as a group, you can use this in a Claude Code conversation:

```text
/fde-research only fde-baseline-analysis. Use the current project's actual materials and complete only this skill's task for this round.
```

The unified entry reads and executes this folder's SKILL and does not require the skill to be registered as a separate command first. Using `/fde-baseline-analysis` directly assumes the host already recognizes this skill separately. Other agents can read this SKILL directly by its actual path; standalone installation remains valid and does not depend on the unified entry. See the [unified entry guide](../docs/unified-entry.md) in the package.

## Standalone use and runtime conditions

Yes. The investigation guide need not run first, but there must be problems that support measurement, actual materials, and definitions. When only summary numbers are available, verify their calculation basis; model estimates cannot replace execution.

## Completion criteria and boundaries

A reliable existing result has been verified and reused, or this round's calculation actually succeeded, and metrics, inputs, scripts, runs, results, and charts can be traced to one another; metrics without data are explicitly not measured.

It is not a production analysis pipeline and does not automatically run domain analyses such as NGS. The current baseline is not an AI benefit, and normal approval/queuing cannot all be counted as time that can be saved.

## Handoff and continued changes

Read effective problems, process, originals, and definitions; hand metric IDs, run versions, results, limits, and recomputation entries to diagnosis and the business proposal. Changes in data or definitions create a new run and notify affected targets and reports; old results are not edited directly.

When new material arrives, first judge its impact and keep old versions and manual edits; update only the related facts, results, documents, and verification. When the whole package is used, the [shared handoff contract](../docs/handoff-contract.md) can be consulted; a standalone installation keeps this skill's own input/output contract.

## Further reading

- [Metric definition card](assets/templates/metric-definition-card.md)
- [Calculation run record](assets/templates/calculation-run-record.md)
- [Stage 4 template](assets/templates/Stage4-business-quantification-and-baseline.md)

## Recovery and material handling

Standalone use also follows the recovery and material boundaries at the start of this skill's SKILL. After compaction, a new session, or a stage switch, restore the effective instructions; the project index keeps the skill's relative path, package version, output versions, and next step. Specific materials are used only within existing authorization and this round's goal.
