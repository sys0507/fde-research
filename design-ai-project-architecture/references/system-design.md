# Integrate choices into architecture and development design

Selection is input; design explains how components jointly meet requirements. Share decisions/evidence with [selection](selection-method.md) and conditions with [interaction](interaction-and-conditions.md). Diagram/Word references govern artifact production; this file governs technical content.

## 1. Design depth and scope

Enable business, technical, and delivery owners outside the conversation to understand responsibility, reasons, cooperation, work, and completion. Define components, important data/state, interface semantics, boundaries, resources, dependencies, and checks. Full code, database DDL, and every API field are unnecessary, but consequential fields/rules/states must be clear.

Distinguish current approved scope and optional future work. Do not add a platform or remove confirmed requirements silently. Engineering dependencies may remain with impact/fallback. Review drafts stay review drafts, without invented approvals, allocations, or acceptance.

## 2. Complete paths and full coverage

Choose representative task types while mapping every effective requirement. Include meaningful exceptions, not only the easiest demo. Walk:

1. Initiator, identity, object scope.
2. Page/file/event/external input, validation, version registration.
3. Next-step control, evidence acquisition, deterministic actions.
4. Model/knowledge/tool results and insufficient/unreliable responses.
5. Recommendation, draft, pending action, or authoritative fact, and storage.
6. Progress/evidence/failure/tasks and who may continue/confirm/cancel.
7. Interruption, retries, changed inputs, and invalidated results.

“Frontend → agent → model → database” is insufficient for uploaded-material advice; include registration, parsing, retrieval, evidence, human decisions, versions, and failures. Assign orphan requirements and justify/remove components without consumers.

## 3. Components

For each necessary component record responsibility, inputs/outputs, data owned, call boundaries, and deployment. Backend owns identity, authorization, business state, task intake, and results; agent execution owns controlled reasoning/tool loops. Models do not own approval authority.

Use programs/authoritative systems for exact calculation, hard validation, and writes. Define rejection, evidence waiting, and human handoff around model proposals. Pages/modules follow tasks, with real progress, evidence, human tasks, and exception feedback.

Choose modular monolith/services/distributed deployment for load, isolation, team, and operational reasons. Logical modules need not each become services; required isolation cannot be sacrificed to a single process.

## 4. Five data/state responsibilities

| Category | Content | Boundary |
|---|---|---|
| Authoritative business | Formal objects, approvals, execution | Record system, allowed modifications, version authority |
| Task runtime | Phase, attempts, tasks, errors, recovery | Recoverability does not authorize repeating side effects |
| Agent memory/checkpoints | Context, execution, authorized long-term preferences | Scope, lifetime, cleanup, revocation, visibility |
| Knowledge/evidence | Originals, parsing, indexes, compiled results, dependencies | Version, applicability, provenance, updates, access |
| Monitoring/audit | Metrics, traces, controlled actions | Minimized sensitive content, retention, access |

Inspect framework persistence before adding missing work. Session summaries are not business databases. Identify authoritative facts and stale copies/cache/memory; generated text cannot silently become authority. Link file metadata to versions/pages/passages/records. Define history/recompute/retraction after changes. Separate users/organizations/objects as required; do not introduce unnecessary multitenancy.

## 5. Tools and source systems

Specify real interfaces, read/write direction, authentication/identity propagation, object scope, freshness, failures, and responsible systems. Distinguish live query, batch export, periodic sync, and manual input, including fields/filtering/pagination/increments. Design from available supply instead of drawing nonexistent live links.

MCP/SDK/native wrappers still need explicit business permission enforcement. Tool visibility and service credentials do not grant user object access. For formal writes define prechecks, human confirmation, idempotency keys, audit, and post-failure reconciliation. Without writes, explain completion in the source system.

Read-only sync still handles change, deletion, revocation, source failure, cursors/equivalents, compensation, and allowed delay. Planned mechanisms are not already implemented.

## 6. Long tasks, people, and recovery

Separate user requests, durable tasks, and execution attempts. Short intake validates/accepts; long execution persists and exposes progress/cancellation. Define meaningful states and transition authority/storage/client updates.

A queue is not automatically durable task truth. Explain crash-between-acceptance-and-enqueue handling. Distinguish temporary network failures, bad input, invalid model output, permission failures, and nonrepeatable actions. Use bounded retry/backoff where valid; reconcile existing external effects before replay.

Human approval binds a person and version. Recheck authority, source versions, and scope on resume; old approval cannot authorize new inputs. Explain worker release, rescheduling, and checkpoint retention during waits using real framework capability.

For justified multi-agent tasks define child state, deadlines/timeouts, partial-result policy, and aggregator responsibility. Retry/degrade/stop follows quality requirements, not arbitrary model preference.

## 7. Knowledge lifecycle

Define intake → original → parsing → index → compilation → validation → publication, distinguishing governed knowledge from temporary uploads. Key claims return to originals/authority with supporting content, valid version, and access scope, not just links.

Compilation creates dependency responsibility: corrections/deletion/revocation propagate to indexes, compiled pages, caches, and results. Set retention/cleanup separately for transient material and organizational knowledge; task closure neither automatically deletes nor permits permanent retention.

Specify permission filtering/checks at retrieval, content fetch, file access, and historical results as risk/components require. Hiding a button is insufficient.

## 8. Deployment, monitoring, and recovery

Show actual application, execution, knowledge, inference, data, and operations services/dependencies, environments, ingress/internal routes, volumes, and resources. Separate existing, requestable, and proposed resources with load/basis/validation. No equipment/test means no proven production capacity.

Choose containers, VMs, or orchestration for the team. Single instances need explicit failure/recovery limits, not implied high availability. Monitoring should locate availability, stalled tasks, business-impacting errors, and model/tool latency without automatically collecting full sensitive prompts.

Specify collected fields, sanitization, access, and retention. Audit identifies who did what to which object and must not rely solely on disposable debug logs. Back up irrecoverable records, originals, required configuration, and managed keys; rebuildable indexes do not imply their originals are backed up.

Recovery targets differ from commitments. Test restored file consistency, tasks, knowledge versions, and revocation, not just database startup. Separate development/test/production configuration, credentials, and data. Coding API calls belong in development, not the production inference diagram.

## 9. Development packages

Split into verifiable deliverables instead of three vague frontend/backend/AI buckets. State objective, included/excluded work, prerequisite outputs, deliverable, completion evidence, and pending conditions.

Reflect real dependencies: identity/object rules before meaningful retrieval-isolation tests, durable state/recovery before extended orchestration. Identify parallel contracts without making everything serial or parallel.

Build a first complete business increment with necessary authority/evidence/failure behavior, then expand. Specify concrete completion such as source-version evidence lookup and interrupted-task recovery. Provide dependency/stage gates without unsupported people, dates, or person-days; later planning estimates those.

## 10. Risk-based validation

For important requirements define object, sample/load, criterion, owner, evidence, and failure treatment. Inherit business acceptance; label proposed engineering targets.

Separate task/error categories, common/difficult/missing/conflicting materials, and meaningful boundaries. Limited samples limit conclusions. Distinguish parsing, retrieval, wrong-version, reasoning, and deterministic-calculation errors for targeted repair, while final acceptance tests user work.

Performance differentiates short queries, long analysis, batches, and human waits with concurrency, material size, windows, and resources. Fast acceptance is not fast completion.

Test relevant unauthorized access, input changes, dependency timeout, process interruption, repeat requests, and recovery. Do not invent write failures for read-only scope; real side effects need idempotency/reconciliation tests. POC targets risks likely to overturn the selected route rather than comparing everything indefinitely.

Without authorized data/environment deliver a runnable verification plan and prerequisites, not results. For actual experiments record versions, inputs, actions, observations, and measured-versus-target status.

## 11. Handoff for estimation

Identify work/cost objects: packages, adapted interfaces, resources, model calls, knowledge setup/updates, operations, tests, training/handoff. State real units/scale such as task types, pages, call ranges, retention, and concurrency. Business task counts are not model/retrieval calls.

Resource/service basis includes specification, quantity, duration, unit-price source/date or unknown parameter. Separate coding API, production inference, knowledge compilation, and evaluation. Free licenses/internal reuse do not mean free operations or unlimited quota.

Separate construction and recurring work without inventing sales price/margin/contract total. Explain uncertainty as additional adaptation, procurement waiting, or capacity expansion, not an opaque risk multiplier.

## 12. Consistent artifacts

Generate report/diagrams from the same components, paths, states, and choices. Split execution, knowledge, and deployment views when useful. Lead with decisions/reasons, not encyclopedic or debugging content.

Check every requirement assigned, exceptions/handoffs, supported recommendations, visible customer conditions, matched work/checks, and agreement of diagram/data routes and text. Repair affected decisions/outputs only, then genuinely render diagrams and Word. File existence or tool success alone is not completion.
