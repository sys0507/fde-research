# Complete report workflow for any capable agent

The user supplies business assets, implementation conditions, technical design, and existing commercial requirements. The agent reads originals, recommends a conditional plan, prepares internal calculation data, and writes complete documents; users need not prepare JSON, package hours, or outlines. Use this skill's methods/scripts and choose a verified [runtime profile](runtime-profiles.md) for Word. Never claim missing tools.

When designated prior prices/duration must be preserved, follow [inherited proposal](inherited-proposal.md), skipping re-estimation in steps 2–3 while retaining document delivery in steps 4–6.

## 1. Establish the input baseline

List inputs and authoritative entries for business decisions, implementation facts, technology, and commercial conditions. Read formal bodies and originals supporting scope, resources, quality, interfaces, and cost. Read long documents in sections and use appropriate Word/PDF/spreadsheet extraction, viewing originals when needed. Explicit amendments prevail; drafts only fill gaps with labels. Without approval records keep proposed status.

Write `work/source-selection.json` as an array with `id`, relative `path`, `title`, `version`, `status`, `use`, and `decision` (adopted/reference/superseded). For unknown version say the original is unversioned and identify it by hash.

```sh
python scripts/index_inputs.py --root INPUT_ROOT --selection work/source-selection.json --output work/input-index.json
```

Use the actual input root, not a fixed machine location. Keep originals read-only. Reference source IDs and passages in requirements/cost bases; preserve conflicts in assumptions/decisions.

## 2. Derive deliverable work

Create scope/deliverable mapping, then shared foundations, cross-layer business increments, integration, verification, deployment, and handoff. Each package identifies requirements, materials/components, human/agent work, returnable result, completion, and cooperation timing. State reuse maturity; prototype, demo interface, and production backend differ.

Use an FDE or lean team across layers with specialist support where needed. Do not assign conventional department headcounts before work, or assume one FDE handles every project. Estimate bottom-up, quantities, and finite iterations into active hours, agent execution, waiting, and realistic personnel reservation. Missing data requires explicit assumptions, not handing breakdown back to the user.

Inspect reusable source/runtime/interface evidence before dependencies. Screenshots/README alone prove neither reusable production code nor total rebuild. Split early contracts/adapters/first increments from later completion/integration so independent work can run in parallel. Every dependency answers which missing output prevents this slice starting. A busy FDE changes allocations/dates, not `depends_on`. Referencing a shared package does not necessarily require waiting for all of it.

## 3. Model capacity and cost

Write `work/model-input.json` using the [model contract](model-contract.md). New estimates use `ai_collaborative_v1`. Derive `human_effort` by person/activity/quantity/unit time/basis, then `agent_work` outputs/checks with already-counted review activities, then schedule identical hours in allocations. Conservation is per package/person, not only the project total. `estimate_basis` summarizes without replacing detail. `dependency_basis` records real output/blocking reason.

Active hours constrain capacity; reserved periods determine full personnel costs; genuinely released support may be hourly. Record source gaps, payroll/employer/overhead boundaries, and verification in assumptions.

Development API `request_groups` reference `package:agent-work`. Derive iterations, requests, average context components, and outputs for implementation/testing/normal repair, aligning each model's input/output totals with pricing lines. Cached input is a disjoint pricing subset, not additional total input. Map separately billed reasoning according to provider rules without duplication. Explain budget excess in `buffer_basis`. Do not reverse-inflate requests to hit a desired allowance or quote percentage.

Verify prices from official sources/contracts. Separate client-paid API from vendor costs. Use this invocation's pricing method; if margin is missing, propose an internally explained assumption, never a fixed example default.

```sh
python scripts/estimate.py run --model work/model-input.json --output output/v001
```

Repair capacity/dependency errors yourself or disclose a condition; users need not debug JSON. Save the input index at the version root. Check complete/shared scope, reserved-person commitments, pilot/support windows, API/equipment boundaries, and consequential sensitivities.

Review `activity-workload.csv` and `collaboration-evidence.json`. Explain human/agent responsibilities, dependencies, and request bases internally and relevant parts externally. Numeric conservation does not prove credible activity granularity, unit time, or dependency prose.

## 4. Write the commercial report

Read [report writing](report-writing.md) now. Wording-only work preserves model/conclusions and adds no tasks, commitments, or fees. Record analytical doubts internally instead of silently re-estimating.

Use [delivery contract](delivery-contract.md) and [report template](../assets/report-template.md) to write full `work/report-source.md` from this project's facts. Explain deliverables, method, owners/prerequisites, acceptance/failure, procurement/payment, training/support, and change. Do not merely turn JSON into tables.

Follow recommendation → scope/results → organization → schedule/cooperation → acceptance → quotation/other expenses → handoff/support → risk/review. Adapt sections, not a page target. Put bulk detail in referenced appendices. Use `public_facts` tokens for price, payment, schedule, and client expenses; other material numbers need the same model/input index or a sourced supporting table.

```sh
python scripts/estimate.py render --results output/v001/results.json --template work/report-source.md --output output/v001/client/report.md
```

Also produce `client/deliverables-and-acceptance.md`, `client/assumptions-and-basis.md`, necessary work/usage appendices, `internal/workload-and-cost-basis.md`, and `internal/assumptions-and-sensitivity.md`. Customer files exclude payroll, margins, and internal allocations. Embed essential appendices in Word for independent review; portable links must resolve within the supplied client bundle, never internal costs or machine paths.

## 5. Generate and accept Word

Read [runtime profiles](runtime-profiles.md), then [Word delivery](word-delivery.md). Without a customer template use the shared builder/finalizer. Complex templates use capable document tools preserving full content, editability, and real rendering.

Inspect every final page, binding document hash, page images, and issues. Continue other outputs when capabilities are missing; distinguish missing DOCX, unupdated TOC, and unverified layout. Asking the customer to update the contents does not complete this delivery.

## 6. Deliver and revise

Return customer MD/DOCX/appendices, internal calculations/assumptions, input index, and delivery index, explaining recommendation, expense boundaries, and a few review items. A skill folder or numerical table is not the requested project report, and a review proposal is not signed.

For changes create v002, preserve inputs/new evidence, compare hashes, and use `--previous`. Propagate scope → work → reservation/active hours → schedule → price/appendices/Word. Keep unaffected accepted text. Changed inputs are not additional-fee authority; distinguish original defects from scope additions.
