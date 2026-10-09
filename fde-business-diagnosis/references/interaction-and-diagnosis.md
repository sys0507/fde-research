# Interaction and Diagnosis Method

## Organize follow-up questions around the whole business picture

State first what the business does. For example: "an employee submits travel expenses, the relevant roles confirm whether it is reimbursable and which project bears it, and the cashier arranges payment." Then look at how different situations are handled. Avoid opening with a pile of table names and document numbers as background.

Stakeholder mapping helps find "who raised the request, who actually does the work, who owns the rules and the data, and who is affected." SIPOC helps confirm suppliers, inputs, the main process, outputs, and receivers. They are used to find the investigation scope and the unknown relations; adjacency of elements alone never proves the company has a problem. The as-is workflow reflects how work is actually done today; a proposed new flow should only be discussed once there is enough evidence.

Semi-structured interviews keep the investigation themes and follow up based on the answers. A useful follow-up usually develops along the relations below — choose according to the actual business, there is no need to read through every item:

- Entering from the original request: "What did it happen on most recently? Can you walk me through one specific case?"
- Reconstructing the current approach: "What do you look at first, and where do you go to cross-check? When the information differs, who confirms it?"
- Tracing to the real burden: "What extra work did this round require? Which condition were you waiting on? What has the system already done automatically?"
- Checking against evidence: "May I see the corresponding record, the original document, or the operation itself? What exactly do the time in this table and the time you described each refer to?"
- Separating the common from the exceptional: "Which situations usually turn out this way? Is there a normal case for comparison? Which figures are already recorded, and which are estimates?"

Do not ask leading questions to prove a preconceived AI solution. For example, "you must be losing a lot of hours every day, right?" is not evidence gathering; ask about existing records and observable operations, then calculate. Phrases such as "the most recent case," "how it is handled now," and "how it gets updated after the material changes" make questions easier to answer.

## Write problems in a form that can guide improvement

Each significant problem forms one complete causal chain, expanded in natural language in the body:

**The specific situation → how it is completed today → the extra checking, follow-up questions, waiting, or rework → the cause supported by evidence → the impact and the improvable part.**

"Cross-project expenses require approval" is a business requirement and does not automatically equal a pain point. "Finance must search three systems for the old approval and the new material, then confirm item by item whether the project allocation has changed" is what shows the actual workload. It still has to be investigated whether the repeated searching comes from unlinked systems, from material whose meaning is hard to interpret, from conflicting rules, or from a negotiation that inherently needs a person; different causes call for different improvements.

Record the source and the level of confidence, distinguishing:

- facts supported by originals, logs, or recomputable records;
- statements from a role, not yet cross-checked against records;
- causes inferred by combining several facts;
- teaching setups or simulated data;
- conditions still to be confirmed.

A fictional teaching case may be used for practice on explicitly stated facts, but a teaching setup must never be presented as a measured enterprise figure. When versions conflict, mark the difference, which data snapshot is used, and why; "the file is the newest" never automatically means "the approval is valid."

## Connect value to feasibility

Compare three kinds of directions around the real work; a combined recommendation is fine:

| Direction | Questions to answer | Typical output |
| --- | --- | --- |
| Information foundation building | Can the information about one piece of business be linked? Are the states and rules consistent, timely, and grounded? | Object and relation modeling, data linkage, state display, rule provenance |
| Decision support | What does a person need to read or verify? Can AI organize the material, the differences, and the basis so the person can judge faster? | Material summaries, missing-item notes, difference comparison, recommendations with their basis |
| Bounded automation | Which segment has clear rules, obtainable input, detectable failure, and recoverable results? | Closed-loop tasks such as intake and classification of material, rule checking, state updates, specific notifications |

For each worthwhile candidate, answer: what is being improved, how much the existing systems or rules can already do, what AI adds, what the data and interfaces currently support, and how the improvement will be proven. Business conditions involved in approval responsibility or payment operations still require real confirmation; do not conclude that a whole project has no value merely because a deal or a payment cannot be fully automated.

Do not force a complex scoring scheme. A priority rationale may rest on how often the problem occurs, how much labor can be improved, the impact on a key business result, data availability, and verification cost. When the sample is insufficient, keep a directional recommendation and note the verification premise. Where model performance has not been validated, do not write unfounded figures such as "expected accuracy 99%."

## Measurement cautions

For each key metric, state the unit, the sample or population, the period, the start and end of the event, the denominator, the calculation method, and the source. When citing a calculation script, actually verify its inputs and results; for new calculations, use a recomputable formula or script.

Count different data populations separately. Total elapsed time includes waiting, and human actions may run in parallel; breakdown labels may overlap and must not be summed as if they were distinct cases. Recalled self-reports differ from on-site timing; a simulated exercise differs from an enterprise baseline. Actions and waits that were not observed stay marked as unmeasured. Improvement headroom and actual savings can only be separated after a trial.

## How to close one round of interaction

Three short paragraphs are enough: "what can be confirmed now," "which diagnosis or recommendation this changed," and "what is most worth adding next." Continue after updating the working record; there is no need to ask the user to re-approve writing actions that were already authorized. When the user explicitly chooses to leave something unknown, the report should give a conditional conclusion rather than loop endlessly on questions.
