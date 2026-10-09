# Full-chain usage examples

The following are route examples, not completed customer investigations; they do not presuppose benefit percentages, model accuracy, prices, or approvals. Bring in actual materials step by step; users are not asked to fill in every table at once.

After installing the unified entry, you can organize the routes below with `/fde-research complete preparation chain …`, or limit work to a single skill with `/fde-research only 2 …` and the like. Numbers, names, and continuation examples are in the [unified entry guide](unified-entry.md). An example route does not mean every call must execute all of it.

## Starting from one vague request: an NGS efficiency investigation

### Starting point: state the goal only, no need to choose a solution in advance

> I want to use AI to improve how efficiently our department uses and analyzes NGS.

This sentence is enough to start an investigation. While it is still unknown which process to change, what product to build, or how to quantify, the unified entry first selects 1 investigation guide, and then continues into 2 baseline analysis and 3 business diagnosis as the materials require. At this stage an NGS chatbot is not set as the predetermined solution; the chatbot example later in this file is a different entry point after the requirement has become clearer.

The complete launch prompt is in [section 1.1 of the master README](../README.md). When already in a customer project session, reuse the project directory; if no location has been given, add an actual directory. The dialogue below is an **explicitly labeled teaching assumption** that demonstrates the guiding method; it must not be copied as customer facts or interview records. The actual pace depends on answers and evidence, and completion is not judged by a fixed number of rounds.

### Example 1: from "inefficient" to a concrete task

**The agent can ask:** "Let's start from the most recent task: who raised the analysis request, who was it handed to, and what did they finally need to receive? Which step made you feel the most time was wasted?"

**Assumed user answer:** "Lab scientists want to use the existing analysis workflows, but they always have to ask bioinformatics colleagues which files to prepare and how to fill in parameters, and after submitting they often chase for progress."

**What the agent should do now:** register this as the user's verbal account and provisionally locate it in input preparation, communication, and status tracking; ask the user to pick one concrete task to reconstruct further. At this point it cannot assert that compute resources are insufficient, nor prove that communication really takes the most time.

**What this round can produce:** the original request and investigation scope, preliminary role relationships, the investigation action list, and the project artifact index. Materials not provided and judgments not confirmed are marked separately.

### Example 2: ask for the minimum necessary material along a real case

**The agent can follow up:** "Can you find this task's input requirements or sample sheet, the record of how it was processed, and the way task progress is currently checked? Let's start from existing material; you don't need to rewrite a full set of documents."

**Assumed user answer:** "There is a process description and a sample sheet; the task's history is mostly in chat messages, and there is no unified log for now."

**What the agent should do now:** actually read the materials the user provides, draw the current steps and responsibility handoffs, and register each original's entry. List "verbal description", "existing documents", and "actual records" separately; put actions that need on-site checking as the next step, and do not fabricate observations or screenshots.

**What this round can produce:** the current-state process, the workflow and material catalog, role responsibilities, concrete problems, and evidence locations. Raw sequencing data is not default required material for starting this business investigation; when further verification is needed, select material according to the real purpose and permissions.

### Example 3: keep going without complete logs

**The agent can suggest:** "First define the metrics you want to measure, then find the parts that existing task records can support; list missing time or operation information as items to collect later."

2 baseline analysis handles manual preparation, follow-up questions/rework, waiting, and actual run time as separate definitions. Only after the user provides real, usable records and they are actually computed are results written up as measured; a department's average efficiency or savings ratio cannot be extrapolated from a few complaints. When data is insufficient, output metric definition cards, data gaps, and a collection plan, and continue the process analysis the evidence allows.

**What this round can produce:** metric and field descriptions, calculation results and run records supported by existing data, and items not yet measured. "Less manual time" and "faster NGS algorithm computation" are not merged into one result.

### Example 4: form the diagnosis and state the conditions for the recommendations

3 business diagnosis combines the actual process, verbal accounts, originals, and the baseline, separating confirmed problems, causes still to be verified, and candidate improvements. It can compare directions such as a unified input standard, better task-status lookup, AI assistance in clarifying inputs, or explaining usage steps; these are only candidates, and the specific recommendation is still decided by evidence.

If the user asks only for investigation, this round closes with the diagnosis delivery and does not automatically implement a chatbot. If data is still insufficient, the report explains which judgments are only preliminary, what evidence is missing, and which decisions it affects. When the user goes on to ask for an implementation plan, hand over to 5/4 and the other later skills.

### How outputs accumulate and are handed over

The paths below are illustrations inside a project, not customer outputs bundled with the skill package; update the index after the files are actually formed.

|Project material|How it accumulates|When it counts as available|
|---|---|---|
|Project artifact index|Records this round's scope, actual files, current versions, status, and next step|Has real file paths; steps not yet started say explicitly that there is no output|
|Investigation record|Keeps received answers, sources, representative tasks, and investigation actions|Distinguishes actual answers from the assumed examples on this page|
|Current-state process and asset package|Builds up the process, roles, original entries, fields, and evidence locations|Actual materials can be found and checked by following the index|
|Baseline analysis materials|Metric cards, data and definition snapshots, scripts, actual runs, and limits|Actually computed or an existing reliable baseline checked; a collection plan is kept when there is no data|
|Investigation and diagnosis report|Combines problems, causes, baseline, opportunities, and recommendations|Conclusions have a basis, unknowns and conditions are stated, and the scope matches this round's task|

The user does not have to provide all materials at once, and the agent should not just keep asking without organizing. Each round keeps known facts, updates existing files, and points out the few gaps that most affect the next step; questions already answered or materials already provided are not requested again. For a new session you can send:

```text
/fde-research continue the NGS efficiency investigation. Please first read the
current project's project artifact index, restore the confirmed scope, actual
materials, and open items, and continue to complete this round's investigation
and diagnosis.
```

### Where to stop, and when to enter the next stage

For investigation only, the main deliverables are the Business Diagnosis and AI Opportunity Assessment Report, the process and role division, the evidence and asset index, the baseline or a list of unmeasured items, and improvement suggestions with the conditions for them to hold. The work can close once the investigation conclusions have a basis and meet this round's scope; there is no need to force all nine skills. Remaining critical gaps can keep conclusions conditional; "the report has been generated" cannot replace complete evidence.

When the user goes on to ask for a solution, 5 describes future task scenarios, 6 prepares or implements a prototype as needed, 4 forms the business proposal, and then 7 reviews implementation conditions, 8 designs the technical solution, and 9 estimates the implementation plan and quotation. Real integration, run verification, scientific decisions, and benefit confirmation still require actual work.

## Ticket handling efficiency improvement

Original request: "Use AI to improve ticket handling efficiency."

|Step|Inputs and processing|Passed to the next step|
|---|---|---|
|1 Investigation|Real tickets, role descriptions, handling process, failure/rework cases|Process, originals catalog, problems, and data definitions|
|2 Baseline|Actual status times and operation records; separate manual effort from queuing|Recomputable waiting, missing-material, rework, or effort metrics|
|3 Diagnosis|Verify whether the burden comes from missing material, routing, search, or judgment|Compare form/rule/system improvements with AI summarization/assisted assignment|
|5 Scenarios|Demonstrate the original and proposed steps on the same ticket|The complete process of receiving, follow-up questions, viewing the basis, human decision, and handoff|
|6 Prototype, optional|Connect the ticket list, details, to-dos, and handling record|Actual local state, operation captures, requirement gaps|
|4 Business proposal|Integrate the baseline, scenarios, and prototype feedback|Recommended scope, responsibilities, targets, exceptions, and enabling conditions|
|7 Readiness review|Real ticket interfaces, identity, data, network, and resource information|What is available, what is pending, and how it affects the solution|
|8 Architecture|Research models, retrieval, tools, and application composition under real conditions|System chain, failure takeover, development slices, and verification tasks|
|9 Plan and quotation|Scope + conditions + technical design + staffing/commercial basis|Feasible schedule, acceptance, service price, customer-paid/recurring costs, and assumptions|

For example, if 7 finds that tickets can only be read and not written back, the solution must not still claim that "automatic assignment is available". 8 can design a suggestion entry and the conditions for later write-back; if this changes the phase-one business scope, go back to 4 for confirmation, and 9 reflects the integration work and external waiting.

## An NGS chatbot for wet lab scientists

Original request: "Connect to the department's existing NGS workflows so scientists can start and track analyses in natural language without writing code themselves." NGS means next-generation (high-throughput) sequencing. The general vision has to be narrowed to a phase-one scope the department actually supports.

|Step|Focus in this example|Output dependency|
|---|---|---|
|1/3 Investigation and diagnosis|Actual workflows, maintainers, sample sheets, inputs and outputs, requests and failure cases|Current-state process, workflow catalog, controlled material locations, and improvement directions|
|2 Baseline|Count clarification rounds, manual preparation, bioinformatics support, queuing, and compute time separately|A business-handling baseline; not a biological analysis result|
|5 Scenarios|Raise task → follow-up questions → show plan → necessary scientific decisions → submit → track → return results|Original/new process for the same task, key conditions, and responsibilities|
|6 Prototype, optional|Choose a supported workflow, edit the plan, view local task status and a simulated receipt|An operable demonstration; explicitly no real compute job submitted|
|4 Business proposal|Phase-one workflow scope, input contract, scientific decisions, cancel/retry/failure takeover|A business document that scientists and the bioinformatics lead can review|
|7 Readiness review|Real execution entry, sample permissions, reference data versions, resources, status queries, and result locations|Interface and runtime conditions; "a workflow exists" does not mean "an API exists"|
|8 Architecture|Separate conversational explanation from controlled execution; make task IDs, versions, data, and run events traceable|Queue/execution adapter, authentication, idempotency, results, and exception design|
|9 Plan and quotation|Estimate from the actual amount of workflow adaptation, data and execution conditions, and the pilot window|Work packages, resource arrangements, acceptance, cost responsibilities, and unknown run costs|

Raw sequencing data is not copied by default for the investigation; register its approved location. Scientific comparison directions, sample grouping, and quality rules come from the responsible people or valid records; demonstration data cannot become a real scientific decision. Prototype run time cannot prove savings in NGS compute time.

Running real pipelines, verifying quality and biological conclusions, production identity and resource isolation, and measuring pilot benefits belong to later engineering and professional work. The nine-skill preparation package lays out that work, its conditions, verification methods, and budget arrangements; it does not pretend that runs have already taken place.

## A short path when a technical solution already exists

The user already has a complete business scope, implementation conditions, and final architecture, and asks to keep given prices and periods: read 9 directly and use inherited mode. Check the old solution and its actual sources, complete the delivery and acceptance arrangements, and keep the original prices/periods and open items. Do not redo the investigation to fill nine steps, and do not replace specified values when no re-estimate was requested.
