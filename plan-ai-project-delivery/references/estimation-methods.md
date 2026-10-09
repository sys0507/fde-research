# Six groups of implementation estimation methods

Use one connected workbook for work, human/agent effort, resource scheduling, acceptance, lifecycle cost, and quotation/change. Do not create six competing ledgers.

## 1. Work breakdown from architecture and deliverables

A WBS divides delivery goals into manageable work. Functions describe what users can do, packages what must be done to deliver, and schedules when/by whom. Organize by checkable outputs, not equal frontend/backend days or a price per scenario.

Map included requirements to system responsibilities/results, then shared capabilities, business increments, interfaces, and integrated delivery. Label build/configure/reuse/verify; identify input, owner, output, completion, and basis. Validate reused versions, access, capacity, and integration. Stop decomposing when someone can start, an estimator can explain, and a reviewer can judge—not at every function or model call.

Count shared identity, retrieval, permissions, and task state once, with incremental module work and references. Give included, conditional, and excluded scope explicit dispositions. Check complete platform dependencies: a business database does not replace a knowledge platform's store; observability may require storage/queues/backups; checkpoints do not replace transactions; revocation propagates through originals, indexes, wiki, caches, and history. Reliability, idempotency, human recovery, retention/deletion, and backup/recovery require actual work even for free components.

For another domain replace business objects, authority, and evidence while preserving shared-once/increments/integration. Example: maintenance-manual search and work-order explanation share retrieval/citations but need separate page integration, work-order adapter, and deterministic checks. If the platform is absent, include platform/dependency deployment and permission setup; a small module example's “platform ready” premise cannot be inherited.

## 2. Human/agent effort and uncertainty

Estimate packages bottom-up. Repetition = quantity × unit effort; fixed integration = explicit fixed hours; quality iteration = initial work + finite rounds × effort. Prefer team history; otherwise label expert estimates or authorized trial evidence with complexity, reuse, and confidence limits. Do not fabricate measurements or vendor quotes.

Organize one or a lean FDE team across frontend/backend/data/agent/deployment; role does not equal headcount. Agents may help planning, implementation, automated tests/browser checks, diagnosis/repair, scripts, and docs. FDEs prepare inputs, decide, review high-risk outputs, integrate, and confirm delivery—not just final code review. Specialists join for independent checks/authority, not automatically one person per conventional discipline.

Derive concrete preparation/decision/review/integration/failure-analysis activities with quantities and active unit hours, then agent outputs and review links. “Six features × four hours” still omits the actual collaboration. Count manual implementation explicitly where needed; no arbitrary AI savings multiplier.

Keep four quantities separate: active human hours for capacity, reservation period/releasable share for personnel cost, unattended agent hours for execution windows, and external waiting for calendar dependencies. Tokens/calls determine model fees, not runtime. Two agent hours plus half-hour review is not 2.5 person-hours; three days waiting with one coordination hour is one human hour plus three days waiting.

Baseline includes normal tuning, defects, and regression. Extra contingency needs reason, trigger, affected work, and upper bound. Allocate risk labor to people/dates; pure waiting creates no imaginary effort. Contingency is neither guaranteed consumption nor authority for extra charges. Show a meaningful sensitivity in scale, iterations, critical-person capacity, or interface delay.

Re-estimate quantities, complexity, skills, and reuse for each project. Do not require all development experiments before quoting. Illustrative maintenance calculation: 8 h initial + 3 × 8 h iterations = 32 h; each round may contain 2 h diagnosis, 4 h guidance/review/integration, 2 h regression. A separate 8 h certificate/proxy risk is justified only for that risk, not an automatic 20% rework surcharge.

## 3. Resource-constrained scheduling

Effort is person-hours; activity duration is its span; project duration is constrained by dependencies and resources. Person-days divided by people is only a rough lower bound.

Build dependency edges from required outputs, not chapter order or one person's queue. Split early contracts/adapters from whole subsystems when sufficient to start another slice. Then allocate each actual/assumed person's daily capacity/windows with one ID across roles; do not duplicate IDs to evade overload. Include independent tests, live integration, deployment, pilot, training, and customer confirmation windows.

Allocate long packages by defensible phases/days; total hours below days × eight does not prove each day feasible. The engine uses integer working days and finish-to-start with successor starting the next day. Same-day handoff requires a finer explicit planning method, not silently ignoring conflicts. Without start date use relative days; calendar conversion must separately handle weekends, holidays, and customer windows.

Compute the logical dependency critical path, then explain resource/window completion constraints. Human review, shared environments, GPUs, and business owners may dominate; the tool cannot infer them, so record and schedule them. Parallel agents do not increase FDE review capacity.

A week-long observation period does not shrink to one day because support effort is eight hours. Work can proceed around late dependencies, but mocks do not replace real integration acceptance.

Historical small example only: FDE 104 h = 13 person-days, with 24 h QA and 8 h operations partly parallel; next-day user trial yields 14 working days, and a specific environment risk may add one before trial. Do not reuse a fixed 15-day schedule elsewhere or add already-parallel QA afterward.

## 4. Evaluation-led staged delivery

Define completion before development/repair. Fluent answers prove neither correct evidence, permission, nor approval. Separate retrieval, faithfulness, deterministic calculation, permissions/versions, durable state/recovery, performance, and business usability.

For each deliverable record requirement, inclusions/exclusions, inputs/environment, action, executable pass condition, evidence, executor, confirmer, and failure route. “Good results” and “testing complete” alone are insufficient. Examples: unauthorized identities cannot read originals or historical results; calculations match a reviewed reference.

Keep tuning sets separate from independent acceptance sets controlled by QA/business roles, with normal/boundary/failure/high-impact cases. Counts/thresholds are project inputs or suggestions, not universal standards. Business authorities provide reference judgments; model judges only assist. Performance specifies model/precision, environment, size/load, window, and timeout. Targets are not measurements.

Stage exits address critical model/interface/authority assumptions early, complete paths/recovery midstream, independent final-environment/load/backup tests, then pilot/handoff. Define return package and who changes scope/resources after failure, including normal repair/regression effort. A quote provides the plan, not a false claim of completed tests.

Preserve domain boundaries: maintenance safety authority, clinical responsibility, or formal purchasing approval do not weaken because AI implements a step. A manual's torque value does not authorize servicing a specific machine. Test applicable model/version/source, shutdown permission, old/revoked/missing material, not only a familiar example.

## 5. Full lifecycle cost

Separate construction, recurring operation, and maintenance; then vendor-paid and client-paid. Vendor service cost includes grounded labor, vendor resources, and contingency. Client-direct expenses are not vendor costs plus margin. Do not count equipment purchase cash and depreciation twice in the same budget.

Choose labor costing from real reservation:

- **reserved_period:** continuous/primary commitment. Period cost = (gross salary + employer contributions + included overhead) × realistic project share. Employee deductions already inside salary are not added again. Fragmented agent-running idle time is not automatically saleable capacity. Active package hours allocate the period cost, never add hourly wages on top.
- **hourly:** genuinely shareable or purchased support. Explain how other time can be reassigned. Low-frequency post-acceptance support may use explicit outside-period rates; exclusive on-call residence is not a few hourly tasks.
- State overhead inclusions and avoid duplicate benefits/management in expenses. FDE coordination does not automatically imply another full-time project manager.

Project working days, statutory payroll periods, and budget months differ. Full-month commitments need dates/basis. Reassess delays, project switching, return effort, and overlap; neither all waiting is full-time billing nor wages zero. Client cooperation may constrain capacity without entering vendor service cost.

Development API use comes from iterative coding reads/generation/review/repair/regression/retries including repeated context. An agent task is not one request, and production business volume is not coding usage. Verify model, price date/currency/unit, cache, output/reasoning, and time-based rules from official sources/contracts. Offline prices are assumptions with verification tasks.

Budget may exceed estimated token cost with explained buffer, without duplicating labor contingency. Separate coding API, production models, OCR, embeddings/rerankers, knowledge compilation, storage, backup, monitoring, and network. Self-hosted models/OCR do not create invented outsourced per-token/page fees but still have build/equipment/compute/power/maintenance costs. Internal allocations need evidence and no duplicate purchase/depreciation/platform/unit charges. Unknown running fees remain unknown; do not sum monthly/yearly amounts into a periodless total.

When equipment is outside procurement scope, show separately quoted/unknown without inventing zero or seeking vendor quotes. Keep in-scope deployment/driver/model/configuration/integration labor. Explain normal-pilot and scale/peak drivers. A subtotal excluding equipment/resources/long-term support is “known listed funding,” not total project investment.

Payer conventions are project-specific. Vendor-purchased API enters vendor costs only under that actual agreement.

Historical hourly-method illustration, not a current/default quote: 104 × 200 + 24 × 125 + 8 × 175 + 800 = 26,000; specific risk 8 × 200 = 1,600; total 27,600. Client coding API 400 is separate and not all AI cost.

## 6. Quotation, scope, and change

Cost C, price P, and customer budget differ. Target gross margin g uses sales as denominator: P=C/(1−g). Markup m uses cost: P=C×(1+m). Fixed pricing is another explicit choice. Internal model balance is not automatically accounting gross profit or after-tax net profit.

Generate service lines, total, tax, and payments from one model. External lines describe deliverables/stages at selling price, not internal rates. Line totals equal price; payment ratios total 100%; tax basis is consistent; rounding remainder goes to the last payment without negative balances. Unknown tax permits an explicitly tax-exclusive review price, not a confirmed tax-inclusive total.

State inclusions/exclusions, data/resources, acceptance, training, defect-support term, knowledge updates, maintenance, validity, and changes. Defect correction is not unlimited new features. Payment milestones need confirmable outcomes; unnegotiated terms stay proposed, with no invented signature.

Preserve old versions and trace changed work, capacity, dependencies, acceptance, and expenses. Normal repairs already included cannot be charged again as risk. Present options for scope/scale/external changes; only actual commercial confirmation changes commitments. Sensitivity is not an approved change price.

Illustrative algorithm only: with an invocation-specific 25% margin, 27,600/0.75 = 36,800; 25% markup yields 34,500 and 20% margin. Adding client API 400 gives 37,200 known listed incremental funding, not full investment. No universal reasonable margin is implied.

## Sources and example interpretation

[GAO Cost Estimating Guide](https://www.gao.gov/products/gao-20-195g) and [Schedule Assessment Guide](https://www.gao.gov/products/gao-16-89g) inform links among baselines, WBS, assumptions, resources, sensitivity, and updates; they are methodological references, not mandatory rules for every enterprise. Verify model prices at execution using the [provider's official pricing](https://api-docs.deepseek.com/quick_start/pricing/) or applicable contract. Bundled examples retain historical dates for algorithm checks.

## Reserved-period example and sensitivity

`assets/reserved-period-example.json` is an independent maintenance-assistant algorithm example. One reserved period includes gross salary 24,000 and employer contributions 4,800; 140 active construction hours do not add wages. Outside-period support 720, QA/operations 2,000, environment 900, and overhead 1,200 produce cost 33,620. Fixed price 42,500 leaves model-basis balance 8,880; a 20% target gives 42,025. These are example currency units and assumptions, not accounting net profit or market prices.

For a new project obtain actual payroll/contributions/share/support/basis/pricing. Test an extra reserved month, truly releasable shares, and interface delays requiring exclusive availability. Removing 48 active hours does not automatically save 48 hours of salary.

API budgets must not be increased merely to look AI-intensive. Record tasks, iterations, requests, context/cache/output, and model mix; calibrate against invoices/controlled traces. Include a meaningful cache or iteration sensitivity. Low-price models can make API cost much lower than people; no minimum API-to-quote ratio applies.

## Automated regression activity example

Forty samples do not mean forty manual tests. With a callable interface/fixture, agents maintain scripts, run assertions, save failures, repair, and rerun. Illustrative QA active work: standards/stratification 4 h + 10 high-risk results × 0.2 h + 6 expected failures × 0.25 h + final judgment 0.5 h = 8 h. About one machine hour is separate. Other low-risk results use reviewed assertions, not no checks.

The reserved-period example records these activities and per-person conservation. Counts/failure rates/unit times are assumptions; replace them from risk/traces. High-impact nonautomatable judgments need humans. If fixtures do not exist, include agent generation and FDE preparation/review/integration.

Both JSON examples derive coding requests/context from deliverable slices. Their prices are algorithm assumptions, not current vendor prices. Historical prose examples and the newer activity-based JSON are different examples, not inconsistent versions of one quote.
