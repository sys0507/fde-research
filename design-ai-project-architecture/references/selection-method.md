# From business tasks to actionable technology selection

Use after reading assets and current conditions. Manage gaps with [interaction and conditions](interaction-and-conditions.md), then combine choices using [system design](system-design.md).

## 1. Establish the decision basis

Start with tasks, not product menus: input/provider, judgment/action, recipient, completion, and error impact. Group by actual technical needs such as understanding materials, explaining knowledge, combining sources, deterministic calculation, dynamic investigation, and controlled execution. Functions may share capabilities; role count is not agent count.

| Requirement/task | Required capability | Quality/latency | Authority/side effects | Component or decision |
|---|---|---|---|---|
| Actual ID/work | Parse, retrieve, judge, calculate, act | Confirmed target or unknown | Authoritative source; external changes | Capability location, then selected component |

Extract complexity, modalities, context size, peaks, failures, evidence, processing locations, permissions, and maintenance. Replace “good quality” with observable success/failure cases and a judge/method if unquantified. Material gaps enter conditions; ordinary settings may be assumptions, permission may not.

## 2. Compare and recommend

1. Identify nonnegotiable effectiveness, performance, permissions, and deployment versus preferences.
2. Choose a small set with meaningful differences; exclude proven hard-constraint failures.
3. Compare the same inputs/results with comparable supporting components/resources.
4. Explain which mechanism changes which step, benefit, ongoing responsibility, and relevance.
5. Recommend a route/configuration/work, retaining genuine alternatives and switch triggers.

Each consequential choice needs decision/responsibility, task-linked rationale/evidence, resources/data/development/maintenance/unknowns, alternative trigger/affected design, and verification/failure treatment. Meet targets before optimizing investment. Do not recommend an inadequate easy route or unjustified complexity. Resource conflicts require explicit tradeoffs, not silent degradation. No forced three options or indefinite “POC later”; give a grounded conditional recommendation.

## 3. Models and deployment

### 3.1 Capability-based candidates

Assess language, domain reasoning, tools, structured output, visual/layout understanding, long materials, multilingual use, and latency separately. Leaderboard totals do not cover every capability. Consider lightweight frequent tasks, general primary tasks, and difficult reasoning/fallback only as relevant.

Discover current families through official catalogs, releases, and model organizations before opening individual cards. Revisiting a remembered old model with today's date does not establish current research. Older models may remain appropriate for compatibility, stability, or task evidence, with reasons against current alternatives. Parameter count, generation, dense/MoE, and quantization are not interchangeable ability rankings.

Compare reference frontier models only for evidenced capabilities/conditions, not universal equivalence. Multiple models need benefits sufficient to justify routing error, operations, and extra evaluation; lower inference price alone does not mandate a small-model route.

### 3.2 License and service location are separate

Open source/open weights concern license/deployability; API/private service concern delivery form. Check:

- Permitted regions/organizations, terms, retention/training rules; sanitization does not automatically authorize transfer.
- Internal service's exact model/version, quota, interface, context, tool behavior, effects, and allocatable capacity.
- Hardware, drivers, inference engine, operators, and isolation from parsing/other workloads for self-hosting.
- Network access, organizational permission, rate limits, and sustained availability for online services.

Evaluate local/international options by actual conditions. Coding-assistant API permission does not permit production business data on that API. Recommend both a model/version or identifiable configuration and a service-acquisition route. Internal-service reuse still needs an application target and requirements; actual supply/quota/SLA remain dependencies. “Group model, choose later” is incomplete selection. An appropriate requested model is not a claim that the organization already operates it.

### 3.3 Actionable deployment recommendation

Specify device class/count, VRAM, RAM, disk, engine, precision, context, starting concurrency, and existing/requestable/new status. Use official version requirements and comparable measurements; label estimates.

Fitting weights does not prove service performance. Account for KV cache/context, concurrency, prefill/generation, image tokens, tool round trips, and shared devices. For MoE consider total resident weights and actual runtime, not only active parameters.

Quality checks cover wrong rules, missed exceptions, bad tool calls, unsupported conclusions, and invalid format. Distinguish first useful result, full completion, throughput, and queueing; first token is not business completion.

Resource cost includes acquisition/rental, facilities/power, network, operations, monitoring/upgrades, and redundancy. Internal services still consume resources and may charge allocations. Provide drivers/basis when amounts are unknown; final quotation is later.

### 3.4 Document vision

Where the primary model lacks needed vision, evaluate a specialist parser/model for text, tables, layout, and image semantics. Verify current capability rather than assuming OCR only reads characters. Preserve crops, coordinates, and original-image access when transcription loses chart or cross-image evidence, or use a model handling that modality directly. Compare quality, speed, and maintenance on relevant samples.

## 4. Documents and knowledge

Separate one-off parsing, exact clauses, contextual explanation, cross-document synthesis, structured fact queries, and updates/corrections. Authoritative records/APIs supply changing business facts; old retrieved documents cannot replace current state.

Choose parsing, retrieval, reranking, generation, compilation, and platform separately, then check composition.

| Problem | Mechanism to examine | Added responsibility |
|---|---|---|
| IDs/names plus semantic queries | Lexical/vector retrieval, filters, reranking | Fields and retrieval/reranking evaluation |
| Charts/layout are evidence | Structured/multimodal parsing or original view | Coordinate mapping, storage, sample checks |
| Stable knowledge repeatedly synthesized | Traceable compilation/wiki plus source lookup | Compilation quality, dependencies, versions/updates |
| Entity links/multihop determine result | Explicit relations, graph queries/GraphRAG | Disambiguation, relation quality, maintenance |
| Rapid facts/exact values | Controlled queries and deterministic code | Interfaces, authority, freshness, errors |

These combine; RAG → GraphRAG → wiki is not a maturity ladder. Diagnose the failure point and compare query-time synthesis with precompilation for stable recurring knowledge. Do not force one-off documents into permanent knowledge systems.

Platform-versus-components comparison covers actual parsing, management, retrieval, updates, permissions, citations, and public API reuse/gaps—not just first-demo code. UI availability does not prove an API; vector storage does not prove compiled pages persist there. Verify compilation, persistence, revocation, deletion, and upgrades for the chosen version.

Evaluate correct evidence retrieval, context completeness, citation support, applicable version, and unauthorized exclusion. One satisfaction score cannot locate failures.

## 5. Agent frameworks

Compare composable runtime frameworks, harnesses with execution loops/support, and customization of mature products against required capability. Ecosystems overlap; use actual version responsibilities.

Map model/tool adaptation, task state, checkpoints/recovery, human intervention, files/workspaces, sandbox, memory, subagents, event streams, observability, and service deployment. Verify capabilities; do not assume a harness lacks memory or that built-in memory satisfies enterprise isolation.

Separate available capability, configuration/adaptation, and new construction. Assess service integration into a web app with identity/task/permissions; state/cancel/retry/recovery semantics and public APIs; workspace/tools/memory/user isolation; extension compatibility; and remaining business state/evidence/management responsibilities.

No universal winner: controlled customization may favor a runtime, dynamic long tasks an existing harness, and reusable complete interactions a mature product. Tie the recommendation to this project and residual work.

## 6. Task organization

Control flow and agent count are independent. Fixed workflows may contain several agents; one agent may run inside mandatory gates. Ask whether the next step is known, evidence gathering dynamic, validation mandatory, subproblems independent, context shared, and adjudication owned.

Use deterministic workflows for fixed contracts/gates; agents for semantic judgment or bounded exploration with exits/handoff. Add agents only for independent evidence, specialized tools, context separation, or real parallel gain. If multi-agent architecture is justified, choose supervisor delegation, pipeline, parallel aggregation, or handoff as needed, not all patterns.

Compare complete-task success, evidence coverage, latency, calls/cost, conflict resolution, and recovery. Repeated answers sharing one erroneous source are not independent verification.

## 7. Extension mechanisms

Prompts constrain role/boundary/output; skills encode repeatable methods/resources; tools execute actions; MCP standardizes tool/resource access; plugins package/distribute according to an ecosystem. Verify how the chosen framework implements each rather than assuming equivalence.

A native interface may suffice for one application; reusable multi-client services may justify MCP. Protocols do not replace business identity, query limits, or error semantics. Build plugin management only for actual install/composition/distribution/lifecycle needs. State publishers, enablers/callers, version impact, and failure/withdrawal recovery.

## 8. Application and deployment

Recommend ordinary frontend/backend, database, object storage, queue, observability, and deployment from existing stack, team, load, and constraints without broad product catalogs. Separate short requests/long jobs, durable records/queue cache, monitoring/audit, and development/test/production data/credentials. A model framework is not a whole backend.

Before freezing the stack check model tools/framework compatibility, parser/index formats, identity/tools, persistence/recovery, and deployment dependencies. Put unknowns in conditions, not hidden diagram boxes.

## 9. Current research and stopping

Reuse valid research, then verify changing facts that affect choices through official docs, repositories, releases, and technical reports: version, license, deployment, API, maintenance, and material prices. Record date/version/URL, supported claim, boundary, and whether vendor claim, public evaluation, project test, or inference. Public benchmarks are not project accuracy.

Search abstract technical needs without business originals, internal addresses, or credentials. If offline, identify unverified facts/recovery and complete other work without claiming current verification. Move to system design when scope is covered, recommendations supported, and unknowns actionable; do not search endlessly for a complete product inventory.
