# Calculation model contract: schema_version 1

Python 3.10+, standard library only. Runtime validation is authoritative; [JSON schema](../assets/model.schema.json) assists structure. Monetary/rate/hour values may be JSON numbers or decimal strings; no NaN/Infinity or negative money/hours. Day ordinals start at 1 and are not calendar dates.

## Commands

Run from this skill directory or substitute its installed path:

```sh
python scripts/estimate.py validate --model assets/example-model.json
python scripts/estimate.py run --model assets/example-model.json --output project-output/v001
python scripts/estimate.py run --model changed-model.json --output project-output/v002 --previous project-output/v001
python scripts/estimate.py render --results project-output/v001/results.json --template report-source.md --output project-output/v001/client/report.md
python scripts/estimate.py check --output project-output/v001
python scripts/test_estimate.py
```

`run` refuses an existing output directory. `render` refuses overwrite and requires a resolved output inside the result root; it records document hash and used facts. `check` verifies artifacts, recomputation, and rendering records. `--previous` must pass its own check and remains unchanged. New inputs require a new output version.

## Inputs

- `project`: name, version, ISO date, status, currency, positive hours_per_day (person-day display), change_reason.
- `requirements[]`: id, title, disposition (included/excluded/conditional), basis. Included must be covered; excluded cannot enter packages.
- `people[]`: id, role, payer (client/vendor), hourly_cost, capacity_hours_per_day, available_from/to, optional overrides (day-string → capacity). Rate is internal fully loaded cost, not selling price.
- `packages[]`: id, title, requirement_ids, kind (build/configure/reuse/test/deploy/handover/wait/risk), owner (person ID), deliverable, done_when, estimate_basis, start_day/end_day, depends_on, agent_hours, external_wait_days, allocations (person_id/day/hours), normal_rework_included (boolean). Optional shared_key, uses_shared (package IDs), risk_reason. Allocations are the sole scheduled active-hour source. Owner alone adds no effort; agent_hours add no labor. Shared work occurs once; uses_shared references it without copying hours, and separate depends_on is required for temporal dependency. Risk needs a reason.
- `expenses[]`: id, title, payer, period (one_time/month/year), category (api/compute/tool/other/equipment), required purpose (development/production/other), amount, basis, task_ids. Equipment may have null amount; other client costs may be null only with quote_status=unquoted. Unknown vendor service costs cannot silently become zero. Optional quote_status (estimated/quoted/unquoted) must agree with null. Optional api includes model, price_date, source, usage_basis, lines (kind/quantity_million_tokens/price_per_million), budget; amount equals budget and cannot be below usage estimate. Empty task_ids allowed; populated IDs must exist.
- `pricing`: method (gross_margin/markup/fixed), rate for the first two or fixed_price, tax_rate (nullable), tax_note, payment_basis (ex_tax/inc_tax), validity, payment_terms_status, payments (id/milestone/ratio). Unknown tax permits only ex_tax; ratios sum exactly to 1.
- `assumptions[]`: id, visibility (client/internal), status (fact/preset/confirmed/revised), statement, reason, basis, affects, verify, change_action.

IDs within an entity type must be unique. Validate package spans, availability, daily capacity, acyclic strict finish-to-start dependencies. Packages may overlap; duration is earliest start through latest end inclusive. External waiting cannot exceed its package span.

## Calculation and disclosure boundaries

Vendor labor plus vendor one-time nonequipment expenses form service_cost. Client labor/API/other expenses are separately classified; recurring costs retain payer/period; equipment is separate whether quoted or unknown. Gross-margin price C/(1-r), markup C*(1+r), fixed price as supplied.

Amounts accept at most two decimals. Round each hourly allocation to cents with ROUND_HALF_UP before aggregation for reconciliation. Output money likewise uses two decimals. Final payment/quote line absorbs rounding remainder; preceding payments cannot exceed the remaining total. Service price is allocated by package labor weights, task-linked expenses shared equally, and unrelated expense items. Public lines show price, not cost.

Internal outputs: model.json, results.json, workload.csv, costs.csv, schedule.csv, payments.csv, labor-reservations.csv, numeric-facts.md, changes.json, manifest.json. New collaborative models also output activity-workload.csv and collaboration-evidence.json. Results use decimal strings. Do not send complete result/CSV workbooks to customers. Changes compare project/task inputs, totals, duration, and packages while preserving old versions.

## Public rendering

Only `public_facts` tokens are accepted as `{{token}}`. Unknown/internal tokens fail. Available fields:

`service_price_ex_tax`, `tax_amount`, `service_price_inc_tax` (unknown tax = Pending confirmation), `payment_total`, `vendor_person_hours`, `duration_days`, `client_one_time_known`, `client_development_api_budget`, `client_incremental_known`, `public_schedule_table`, `public_payment_table`, `public_expense_table`, `public_quote_table`, `public_api_basis_table`.

The expense table includes client-paid items only. Vendor recurring/equipment costs remain internal; reselling needs a separately agreed selling price, not disclosure of acquisition cost. Development API budget sums only client-paid, one-time, development API expenses. Known incremental funding is the payment-basis service price plus known client one-time nonequipment expenses; it excludes client labor, recurring costs, equipment, and unknowns. It is not total investment.

Controlled tokens/hashes do not prove manually written numbers or prose; review them against sources.

## Personnel costing within schema_version 1

Optional `people[].costing` defaults to historical hourly. New projects explicitly choose a mechanism; retain hourly_cost without blindly adopting sample rates.

- `{"method":"hourly"}`: allocation hours × hourly_cost for shareable/purchased support.
- `reserved_period`: periods each require id, start_day, end_day, salary, employer_contributions, included_overhead, allocation_share (0 < share ≤ 1), basis. Values are totals for the whole period before share, not monthly unit prices. Periods cannot overlap and must fit availability. Cost = sum of three amounts × share, rounded to cents.
- Inside a period do not add hourly wages. Active hours allocate committed cost to packages but do not reduce reservation cost. A committed period with no active allocations still counts.
- Outside-period allocations require explicit outside_period_hourly_cost and outside_period_basis; no silent fallback to hourly_cost.
- Cost share and project daily capacity need consistent real resource arrangements. Software checks project capacity, not hidden double booking elsewhere.
- results.labor_reservations preserves commitments; workload.cost_method distinguishes hourly, reserved_period_allocation, outside_period_hourly. No duplicate wages.

API usage_status is estimated (default) or measured; measured needs traceable calls. Token lines are disjoint: total input plus cached/uncached subparts must not be counted twice. results.api_usage_details preserves model/date/status/basis/lines. unquoted_expenses retains unknown client nonequipment fees outside known totals.

Compatibility fields gross_profit/actual_gross_margin mean model-cost-basis balance/ratio, not necessarily accounting gross profit or after-tax profit.

## Required activity contract for new estimates

Top-level `estimation_profile` is `ai_collaborative_v1` for all new full estimates on any agent, or `legacy_v1` for historical compatibility. Missing profile is historical only. New validate/run rejects missing/legacy unless explicit `--allow-legacy`; check still supports old results. Do not downgrade to bypass requirements.

Every package explicitly includes:

- **human_effort:** id/person_id/activity/category/quantity/unit/unit_hours/basis. Hours = quantity × unit_hours. Categories: prepare, decide, review, integrate, verify, coordinate, manual_implementation. Include relevant activities, not every category mechanically. Derived hours must equal allocations exactly per package/person. Do not duplicate one activity across packages or reverse-fill activities from totals. Basis identifies source, reuse maturity, estimated/measured status, and quantity rationale.
- **agent_work:** id/activity/output/verification/reviewer/review_effort_ids/runtime_basis. Review IDs point to this package's already-counted review/verify/integrate activities owned by reviewer. One review may cover several outputs without duplicate human cost. Nonempty agent_work iff agent_hours > 0. Without agent work include no_agent_work_reason. Runtime remains separate from wages/tokens.
- **dependency_basis:** predecessor_id/kind/required_output/why_blocks_start, one-to-one with depends_on. kind is technical/external/acceptance. Engine stays FS. Split early prerequisites; personnel waiting changes dates/allocations, not technical edges. Semantic review must detect resource queues disguised in prose.

Development API expenses require api and request_groups:

- Group fields: id/model/phase/agent_work_refs/runs/requests_per_run/context_components/output_tokens_per_request/iteration_basis/evidence. References are `packageID:agentWorkID` and packages must appear in expense task_ids. Explain implementation/testing/repair, rounds/requests, and measured trace or assumption.
- Context components: id/description/tokens/basis, decomposing average instructions, relevant code/material, tool results, repeated history. Split differing models/context sizes; do not multiply whole-repository size by every request or omit repeated context.
- Requests = runs × requests_per_run; input = requests × sum(context tokens); output = requests × output_tokens_per_request. Aggregate by model and divide by one million to equal pricing lines. Lines add model and token_type=input/output. Cached/uncached lines may split input pricing but must conserve total input. If provider bills reasoning within output include it once; other non-token charges need separately grounded items.
- Budget above usage estimate requires buffer_basis tied to extra context/iterations or funding control. Measured groups require actual traces. Recompute after changed activity/context/model/iterations.

New results retain effort_details, agent_work_details, dependency_evidence, api_request_groups and the two collaborative evidence files in the manifest. Keep originals, model, results, and report at compatible versions.
