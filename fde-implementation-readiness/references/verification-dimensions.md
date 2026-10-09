# Six technical verification dimensions

The six dimensions define what to investigate; the five-step workflow defines how. Begin with existing assets and confirmed requirements so architecture and investment estimates have a basis. Record shared conditions once and scenario differences separately; do not issue six questionnaires for every function. These dimensions identify knowledge/objects to examine, not a checklist requiring immediate measurements for everything. Obtain sufficient evidence for candidate designs and reasonable estimates: never invent authorization or feasibility, use grounded quantity/capacity estimates, and defer appropriate engineering details.

## V1. Nonfunctional requirements and technical constraints

Functions say what to do; nonfunctional requirements specify quality and operating levels. Scale, concurrency, response, freshness, recovery, and retention change compute, integration, storage, and operations effort. Constraints define allowable processing boundaries, mandatory systems, budgets, and resources.

Response time is request-to-result; update latency is source-change-to-visible-change. Quickly returning old data is not freshness. Daily active users, simultaneous users, simultaneous requests, business transactions, and API requests are different quantities. Separate tolerable interruption from acceptable data loss and state who continues work during failure.

1. Inherit confirmed metrics, deadlines, constraints, scope, and sources. “Start review within two working days” does not mean “finish processing in two days.”
2. Investigate ordinary/peak scale, interactive/background work, freshness, failure handoff, record types, and retention only where gaps affect design. Prefer existing owner explanations, logs, statistics, and capacity materials.
3. Use ranges or conservative assumptions from known scale, rhythm, or role estimates with basis, applicability, sensitivity, and calibration. A few examples do not measure production concurrency or annual volume; any extrapolation needs method/limits.
4. Translate metrics into operating conditions. Separate existing contract fees and project increments. With missing price evidence, identify cost drivers and where to obtain prices; sourced planning ranges remain estimates, not quotations.

Possible conclusion: business accepts a specified update delay under a defined load, while the source's actual update capability is pending. Keep requirements separate from capability. A processing boundary is a constraint, and becomes a conflict only with an incompatible candidate.

## V2. Quality scenarios and verifiability

Turn “timely, reliable, traceable” into observable situations. A quality scenario has six elements: source/actor, stimulus, environment, affected artifact, response, and response measure. It operationalizes V1 rather than duplicating a metric list.

Choose situations that affect design/investment. State who does what under which conditions, which object should change, and how to judge it. For example, after an authorized clerk saves a plan, another role sees the new value within the agreed interval; on read failure the page identifies its data time and failure state.

Match inputs/results to the same object, version, and time. Compare timestamps for freshness, cross-role access for isolation, and repeated effects for reliable execution. Not every judgment needs a percentage. Grounded planning targets may precede commitment, with a decision method. Material commitments need an authorized owner; ordinary planning values do not each need a signature.

Track target defined, method defined, and target actually met separately. This stage can define later verification without claiming POC/performance success. Identify samples, environment, permissions, and load needed later. One normal sample proves no recovery behavior; a proposed fault exercise is not a historical incident.

## V3. Systems and data

Information appearing in a document proves existence, not continuous programmatic access. Format answers how to read it, semantics what it means, identifiers/versions which item/change it belongs to. Update mechanisms, available history, and retention affect different design responsibilities.

“Passed” might mean a document check, manager approval, or successful payment. Amount might be requested, approved, or paid. Null may mean not yet happened, omitted by an API, or inaccessible; it does not necessarily mean the business item does not exist.

- Locate the authoritative source and maintainer, normal system/ledger, business-recognized record, and export delay.
- Compare actual examples with field definitions: types, semantics, required/key fields, enums, timezone/event time, and missing values.
- Check keys among records, projects, people, attachments, and versions; distinguish correction, withdrawal, and supplementation.
- Investigate update/history/retention that changes candidate paths. Separate boundaries for originals, parsed data, indexes, and logs. Defer exact latency or attachment-expiry details when they do not change the current decision.
- Inspect samples relevant to confirmed functions for missing, duplicate, inconsistent, and versioned data. State coverage/limits and maintenance responsibility. “Cleaning” is not automatically a one-time task.

Conclude what data supports, missing fields/links, history needs, transformation/repair, and continuing maintenance. Identify effort drivers. A complete demonstration sample does not prove complete production data.

## V4. Interfaces, identity, and authorization

Reading, writing, workflow handoff, attachments, and notifications are distinct capabilities. UI actions may not be exposed to a new program. Authentication identifies the caller; authorization determines allowed records/actions. Employee, service, and administrator identities differ. Technical access is not business approval.

A write timeout may occur after the source committed an action. Blind retry can duplicate records/tasks/notifications. Idempotency means repeated requests do not repeat the intended business effect. Identify deduplication, result lookup, and recovery owners. This stage establishes available mechanisms or new work for estimation; detailed request IDs/error branches can follow in design/integration.

1. For each business action determine entry, caller, allowed scope, key data, success meaning, limits, and maintainer. Obtain contract details proportionate to decision impact.
2. Clarify what “API supported” means with located documentation, sanitized examples, or authorized checks. A successful read supports only that identity/object/environment.
3. Check person-to-record/organization mappings, roles/delegation, validity, and application processes. A broad service account does not prove employee isolation.
4. Examine save, handoff, notification, and receipt step by step. Without a separate task API, check whether saving triggers the source workflow before declaring it missing.
5. Identify feasible result recognition, deduplication, and failure handoff for writes/retries. Count new work if absent. Actual writes require authorization and controlled objects; documented mechanisms may support planning while implementation tests remain pending.

Conclude what can be reused, built, activated, purchased, or handled manually, with both technical and business limits. Missing documents are not proof of no API. Concrete capability/authority explanations can permit estimation while details await integration. An existing API does not prove enabled access, connectivity, or tested performance.

## V5. Network and deployment

Connectivity depends on source environment, target, identity, and route. An administrator's laptop reaching a service does not prove the future application can. DNS resolves names; firewalls restrict connections; proxies relay; TLS/certificates protect and identify services; egress policies limit external destinations.

Cloud, private, and hybrid labels are insufficient. Trace where originals, model context, parsed data, retrieval indexes, logs, and backups are processed/stored and which connections they use.

First obtain existing hardware and internal model-service information: configuration/capability, environment/boundary, quota basis, application conditions, and operations ownership. Existing screenshots/lists are enough; exact endpoints/quotas may follow during setup. Resources existing does not mean reserved for this project; an internal deployment does not imply available model compute.

If insufficient, examine permitted expansion/procurement, decision owners, resource/application conditions, and known lead times. Do not predetermine vendor or price. Record any provided allowance's approved/proposed status, coverage, and source. Permission to apply is not approval. Lack of procurement does not exclude suitable existing services.

Estimate capacity from configuration, business scale, and grounded experience/calculation, recording load assumptions, sensitivity, and calibration. Distinguish allocated quota, technical estimate, and measurement. “Enough” from an administrator is not a measured result, though grounded explanations may support preliminary planning with POC/load testing later. Seek another critical answer only when even a usable route or supplementation path is unknown and decisive.

Map necessary application connections to sources, models, identity, and messaging without prematurely choosing architecture. When necessary and authorized, check DNS, TLS trust, connectivity, and access from the relevant environment. Do not bypass certificate verification or expand into network scans.

Conclude permitted processing/storage, reusable resources, applications/connectivity to arrange, ownership, and constraints affecting deployment, environment changes, procurement, and maintenance. Unprovided hardware/service/deployment commitments remain unknown.

## V6. Traceability, assumptions, and condition judgments

Link functions, scenarios, conditions, evidence, and issues so changes can be traced to design/estimates. Functions organize scope; scenarios expose role/action/exception differences; samples provide factual entry points without defining scope.

Keep requirements, facts, and assumptions distinct. Conditions may be available, pending verification, needs supplementation, constrained, or conflicting. Known limitations are useful facts. A question can be resolved by confirming no write interface while its condition remains needs supplementation. Proceed-under-assumption and later-verification dispositions may support closure; neither fabricates confirmation nor bypasses critical authority.

Reuse function/scenario/sample IDs and stable condition/question IDs. Record provider, environment/version/time as relevant; leave unknown metadata honestly rather than forcing unrelated details. Preserve conflicts and decision owners instead of selecting the optimistic answer.

For new answers identify the question, supported scope, remaining decision impact, possible inference/later verification, and affected previous conclusions. Ask only new critical differences. Evidence cannot exceed its scope: documentation supports design; a controlled read supports that object/identity; load testing may support performance under specified conditions.

Conclude with traceable changes/remaining unknowns, coverage of all current scope, shared conditions without duplicate questions, and explicit scenario differences. Use [interaction and reporting](interaction-and-report.md) for closure criteria.
