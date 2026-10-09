# From scenarios to an interactive product

## A checkable development contract

Save `development-contract.md` in the requested project, or update an equivalent existing document. Specify:

- Who reviews which work; included/excluded functions and candidate/confirmed status.
- Materials, function conditions, scenarios, and versions actually read; teaching additions identified.
- Roles, objects, pages/navigation, start and finish.
- Each function/scenario's page, action, data, and observable result.
- Actual execution, local simulation, outstanding dependencies, runtime, and deliverables.

| Function/scenario | Operator and starting state | Entry | Input/action | Observable result and storage | Source/condition | Status |
|---|---|---|---|---|---|---|
| Existing ID | Role, object version, state | Route/navigation | Executable operation | Field, record, version, or task change | Original and prerequisites | Not implemented / untested / passed / partial |

The table indexes full narratives instead of replacing them. Multiple scenarios may share a page; coverage follows behavior. Resolve source/scenario conflicts through effective evidence rather than choosing the easier implementation.

## Organize pages by task

An inventory comparison might select a product, inspect stock/arrival dates, change demand assumptions, compare options, save a draft, and hand it to an authorized person. Lists, a comparison workspace, and record details may support this better than separate scenario slides.

A saved option appears in the draft list; reopening preserves changed quantities/evidence. Calculations use current inputs and explicit formulas. Approval-required actions save pending records; “Save” does not mean a purchase was sent.

| Task | Useful structure |
|---|---|
| Document Q&A | Question, concrete answer, supporting passages, limits, next action |
| Field support | Equipment/version, observations, applicable materials, steps, feedback/handoff |
| Business analysis | Period, definitions, current inputs, computed results/details, explanation and attribution limits |
| Forms/review | Original, checklist, differences, correction reasons, decision, next state |
| Cross-role work | Current owner, prerequisites, tasks, versions/history, actual continuation |

These guide layout, not a mandatory feature list. Add relevant incomplete-input, empty-result, or version-conflict cases rather than a universal exception menu.

## Existing assets

Scenario `screens/` are visual/behavioral references. Reuse their code only when suitable and allowed; isolated pages often need shared navigation/data/state. Displaying screenshots inside an app is not implementing business behavior.

Use the chosen project directory and existing repository conventions; `development/` is a possible new-project source location. Reference or copy controlled snapshots of necessary originals, documenting dependencies. Never copy unrelated private materials into a publicly served frontend folder.

If missing detail can be demonstrated through an explicitly permitted teaching assumption, record it. If alternatives change functionality, record the decision/impact. Unknown approval authority permits “submit for review,” not an invented manager approval.

## Work backward from the business endpoint

Walk a principal chain from input through roles/objects to a useful, persistent result. Add other normal tasks and important exceptions according to real value. If everything stops at “recommendation/pending,” check whether authorized teaching conditions, later human actions, or execution states are missing before shrinking scope.

Separate normal navigation from review controls: everyday work shows tasks, object state, and next actions; scene IDs, before/after switches, and demo progress belong to review tools. Each button has a result type/destination; “view → AI answer” is not a universal workflow.

## Capability allocation and a normal control

Map business action, ordinary system action, AI contribution, human decision, execution conditions, and next step. Ordinary lookup/display may have no AI contribution. Automatic action needs reliable input, clear rules, authority, and exception handoff; clicking a button automatically is not intelligence.

Retain smooth normal work as a control. Do not invent missing evidence or extra confirmation to make AI appear useful. State work removed and review added; not every existing task must start in an assistant.

Before/after comparisons share object, version, cutoff, and task start. The current-state page must not reveal target-generated summaries, missing-item lists, rankings, or recommendations. If new teaching conditions change the starting point, explain the difference rather than attributing all improvement to AI.
