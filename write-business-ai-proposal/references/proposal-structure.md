# Proposal Structure and Business Depth

The following is the content skeleton of a complete business transformation proposal. Adjust section names, grouping, and level of detail per project, but keep the content that supports the review decision. The file must be readable on its own, without the course or the chat history; word count is not a substitute for completeness.

|Content|Review question it answers|How far to write it|
|---|---|---|
|Cover, version, document notes|Which phase, which version, what status|Name, version, purpose, pending-confirmation status; teaching-case note; no fabricated approval signatures|
|Decision summary|What has to be decided this round|Proposed scope, targets, key changes in work, human decisions retained, constraints, and open items|
|Background and current state|Why change is needed|Organization and existing systems, main processes, problems, baseline, and existing effective capabilities|
|Goals and scope|Who and what business is covered|Goals; recommended for phase 1 / conditionally included / explore later / excluded, with reasons|
|Overall business solution|How the capabilities work together|Relationship to existing systems, entry points for people, information coordination, judgment support, and authorized operations combined|
|Per-feature requirements|How the role will work from now on|The feature entries below; the necessary separate before/after and result images; matched to feature and scenario IDs|
|Target process and states|How work is handed over and closed|Normal path; missing-item / exception / correction / failure branches; completion conditions; who takes over and what is recorded|
|AI and human responsibilities|What the system does and what a human decides|The action-level responsibility table below, plus the conditions where crossing the line is forbidden|
|Data and operating constraints|Under what conditions the solution holds|Sources, versions, access, operations, logging, update mechanism, and this project's hard constraints|
|Organizational support and maintenance|How it keeps working long term|Material maintenance, rule confirmation, exception handover, user feedback, version change ownership|
|Rollout and phase outcomes|What the business side does next|Entry/exit conditions for condition fulfillment, prototype review, pilot preparation, verification, and adjustment; no invented detailed schedule or cost|
|Outcomes and verification|Whether the expected improvement has a basis and how to check it|Baseline, formula, assumptions, proposed range, quality constraints, measurement scope and method|
|Risks and open items|What cannot be committed yet|Specific cause, impact, handling, the role who confirms, and the status until the decision arrives|
|Appendix|How to verify the body|Source index, feature traceability, business material / prototype catalog, human review checklist, and other necessary attachments|

## Per-feature entries

Each feature name must be followed by business requirements the role can check against. Organize a coherent explanation around the questions below; not every item has to become the same kind of large table:

1. Who uses it and when, and which piece of current work needs improving?
2. Which current-version materials, records, and rules does it read, and what happens when the evidence is insufficient?
3. What does the system organize, compute, explain, or execute, and is it reusing existing capability or adding new capability?
4. What is the output, what does the user do next based on it, and which state counts as complete?
5. What must be decided by a human, and what conditions are required for use and for operation respectively?
6. On error, out of scope, mismatched material, or missing authorization — where does it stop, and who takes over how?
7. Which business scenario is used to check that the requirement is met, and which step does the prototype show?

For automated operations, additionally explain how repeated triggering avoids duplicate business results, how partial success is displayed, and whether recovery requires a human decision. State the business requirement here; do not pick the specific technical implementation for the development plan ahead of time.

## AI and human responsibility table

The subject of the table is a specific business action, not a department. The following columns work:

|Business action|What the system may provide or execute|What a human must decide/execute|When to stop or hand off|Handover and correction record|
|---|---|---|---|---|

At minimum, check the following distinctions where this project touches them:

- **Explanation vs. rule**: a model explanation is not a valid policy; an answer shows its source and scope of applicability, and a rule is activated through the designated confirmation process.
- **Suggestion vs. decision**: extracting facts, proposing an assignment, or flagging a risk is not the valid opinion of the person concerned, nor a formal approval.
- **Prompt vs. block**: only a hard condition backed by an explicit rule and confirmed authorization may block; where the model is uncertain, route to verification.
- **Preparation vs. execution**: producing a draft to-do is not a submission; a successfully sent notification is not a completed handover.
- **Technical permission vs. business authority**: having a write interface does not permit approving on someone's behalf; the scope of automation must rest on a valid authorization.
- **Change vs. invalidation**: how new material affects an earlier judgment should be verified by the corresponding role; keep the old version and the change chain, never silently overwrite.
- **Correction vs. responsibility**: people can inspect the original, reject a suggestion, correct a summary, or stop the automation; system errors must still be handled, tracked, and fixed.

## Cross-check after writing

Check item by item: whether each feature lands somewhere in the process, whether each action in the process has an authority basis, whether the scope status agrees with the summary and the image captions, whether any target depends on a capability not yet in scope, and whether any target omits an added burden or a quality requirement. Where conflicts appear, fix the corresponding entry; do not try to cancel out contradictions in the body with one generic disclaimer at the end.
