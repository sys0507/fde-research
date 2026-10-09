# Write scenarios a reader can retell

## Contents of each scenario

Use a title describing a person doing work, such as “A buyer compares replenishment options for blue size M.” Fill these fields with actual work, not generic one-line claims:

- **Person and event:** main operator, related roles, trigger, business item, and intended result.
- **Starting point and inputs:** information date, object, state, available/missing materials, and source IDs. State future-exercise assumptions separately.
- **Before:** in time order, what is opened/obtained, reviewed/compared, asked of whom, received, and handed off. Do not invent existing software names/buttons when originals do not identify them.
- **Specific difficulty:** the exact action at which information is hard to find, must be explained again, or lacks a decision basis. Necessary waiting and professional judgment are not automatically waste.
- **After:** from the same starting point, where the operator enters what, what the system reads/returns, how evidence is shown, and how the person reviews/corrects/continues. Label designed page names as proposed.
- **Result and next owner:** record, file, task, or state; who can see it and where work continues. A recommendation is not approval to execute.
- **Human decision and important exceptions:** who may decide what and how work proceeds with missing/conflicting inputs or failure. Do not add irrelevant exceptions for volume.
- **Work change and verification:** searches/retelling removed, review added, and effects still requiring measurement.
- **Basis and status:** separate factual sources from design suggestions; retain proposed/pending/approved status and workflow-affecting gaps.

Join scenarios to express cross-role workflows. One main operator per scenario does not remove handoffs: a preceding result becomes an explicit input to the next scene.

## Example: replace vague claims with observable work

Weak: “AI aggregates sources, aligns inventory semantics, produces replenishment decisions, and closes the loop.”

The reader cannot tell what was read, done, returned, or approved. The following is a **teaching example**, not a default project fact:

> A buyer must decide how to replenish blue size M at the Kuala Lumpur warehouse. The inventory sheet shows 72 units available and 48 in transit. The latest logistics notice changes their expected availability from September 18 to September 22. Today the buyer opens the sheet and notice separately, matches specification and batch, checks the date, confirms demand with operations, and asks logistics about transfer conditions.
>
> In the proposed “Supply position” page, the buyer selects that warehouse and specification. The page separately shows “72 available now” and “48 in transit, expected September 22,” each with its source. It flags the changed arrival date. After checking the notice, the buyer opens “Compare options.” A tool calculates from confirmed demand and transport conditions; AI explains ordinary purchasing versus transferring 24 and purchasing 48. If the sending warehouse's current stock is missing, the page marks it pending verification rather than recommending immediate execution.
>
> The result is a comparison draft with assumptions, sources, and pending conditions for the purchasing owner. Transport arrangements and execution approval remain outstanding. Saving the draft does not change inventory or purchasing ledgers.

These are proposed interface names. Designing fields/buttons does not create approval, arrival, or measured-benefit facts. Reuse the method, not the example's quantities.

## Language and granularity

- Replace abstract “alignment” with the actual fields, dates, or definitions compared.
- Explain traceability as the material/record a user can open, and handoff as where a result is saved, who takes over, and how receipt is known.
- Explain necessary terminology on first use, such as SKU for a separately managed color/size specification.
- Use the overview to locate full narratives, not replace them with “system displays, human confirms.”
- Judge clarity by whether a new reader can describe the next action, not by word, table, terminology, or image counts.
