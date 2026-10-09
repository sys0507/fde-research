# Inputs and Evidence Handling

## What to record when receiving the task

The following are suggested fields for the input statement; they can be merged into the invocation prompt or into the production record itself. Use what the user has already provided directly; do not ask again.

|Field|Information to obtain|
|---|---|
|Project and readers|Business subject, phase, the decisions the main reviewers care about, document status|
|Input files|Valid paths and versions for the business diagnosis, original assets, feature and condition verification, target process, and outcome estimates|
|Scope boundary|Phase 1 candidates, exclusions, conditional capabilities, existing approvals, and decisions that must not be changed|
|Handling constraints|Where data is processed, who may access and operate, business approval authority, the tools the environment is authorized to use|
|Visual materials|Feature ID, scenario ID, prototype version, separate image paths for before/after/result, whether it is a prototype or a real system|
|Delivery requirements|Output directory, editable source, Word or specified format, client template, human review status|

Example invocation (replace the angle brackets with real information):

> Use write-business-ai-proposal. Read the business diagnosis, asset index, feature and condition verification, target process, and estimate results in the attachments, and write a phase 1 business transformation proposal for the specified business. Scope and hard constraints follow the latest valid conclusions in those materials. For each feature, write the input, output, human decision, and exception handover clearly. Use separate images for the before and after interfaces. Deliver a complete editable source and a Word file, actually rendered and checked, with open items and a human review checklist recorded. Current status is pending final confirmation; do not generate a client signature, and do not include a detailed development schedule or pricing. Materials, output directory, and format requirements are as follows: <specific paths and constraints>.

## Evidence states must not be mixed

|Evidence type|How to use it in the proposal|What it cannot be turned into|
|---|---|---|
|Existing business originals, handling records, statistics|State what happened, preserving identifiers, dates, and statistical definitions|Downstream results that have not happened|
|Interview or meeting records|Note who confirmed which requirement, fact, or opinion|Formal approval beyond that speaker|
|Supplementary teaching scenarios|State their teaching nature in the document notes and keep them internally consistent|Interviews or signatures that really occurred at the enterprise|
|Feature concepts and prototypes|Express as "proposed, recommended, once conditions are met"|Realized capability, granted authorization, or settled phase 1 scope|
|Target estimates|List the baseline, formula, parameters, assumptions, and proposed range|Post-launch measured results or an unconditional commitment|
|Approvals or authorizations|Consume only the subject, action, scope, and time limit covered by a valid record|Approval authority inferred from seeing a technical entry point|

Sources do not need a path stuffed into every sentence. Section source notes, a source column on each feature, and an appendix index are enough — but load-bearing numbers, rules, authorizations, and statuses must be traceable to a specific location.

## Requirement traceability

Requirement traceability means being able to follow a requirement back to its business evidence, and forward to the work it changes and the way it is verified. It is used to spot unfounded scope additions, missing conditions, and targets that cannot be verified; it is not decorative numbering.

Keep one continuous relationship:

**Problem or long-term goal → feature ID → role task and target process → responsibility and conditions → verification definition → prototype scenario.**

The following columns are enough to form a minimal traceability table:

|Feature ID and name|Evidence and location|Proposed phase 1 status|Role/process change|Authorization or data conditions|Verification question|Scenario image|
|---|---|---|---|---|---|---|

One feature may have several role scenarios, and one scenario may illustrate several cooperating features. The number of scenarios does not stand in for the number of features. New capabilities proposed for long-term needs are allowed, but state the reasoning and what remains to be verified; do not force-fit them onto some historical document.

## Handling gaps

- **Items that cannot be settled without evidence**: write the question to be confirmed, the existing role suited to confirm it, which feature it affects, and the handling status until it is confirmed. Do not invent an authorizing party out of thin air.
- **Items expressible as a condition**: for example, "handover for approval is possible only once a valid delegation arrangement exists." Write the condition and the fallback owner in full first; do not pretend the delegation already exists.
- **Gaps that prevent writing a review-ready draft**: for example, core business rules are missing but a list of auto-approval ranges is requested. Complete the other writable sections and report the specific obstacle and the additional input needed.
- **Newly added business assets**: register only the files actually obtained, with their source, purpose, and access conditions; if there are none, write zero. Do not register agent-derived material as an enterprise original.
