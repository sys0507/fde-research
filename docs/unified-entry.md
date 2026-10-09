# FDE unified entry and single-skill invocation

Version 2.3.0. There are still nine professional skills, plus one entry responsible for selection and continuation; the package now contains 10 SKILL.md files. [Back to the master README](../README.md).

## Where it goes

The source package entry is the root [SKILL.md](../SKILL.md). When the whole package is installed by domain into Claude Code, the entry is at:

```text
~/.claude/skills/fde-research/SKILL.md
```

Do not place the entry at `~/.claude/skills/SKILL.md`; that is the container directory for all skills. Do not copy only the entry file either: the nine professional skills and shared resources should stay together inside `fde-research`.

```text
~/.claude/skills/
  fde-research/
    SKILL.md                       unified entry: name is fde-research
    README.md                      master README
    CHANGELOG.md
    docs/
    templates/
    scripts/
    fde-discovery-guide/SKILL.md    1
    fde-baseline-analysis/SKILL.md  2
    fde-business-diagnosis/SKILL.md 3
    write-business-ai-proposal/    4
    fde-ai-scenario-design/        5
    fde-prototype-development/     6
    fde-implementation-readiness/  7
    design-ai-project-architecture/ 8
    plan-ai-project-delivery/      9
  skills-for-other-domains/
```

The source folder can keep the name `skills`; formal installation and release use `fde-research`, matching the entry's `name: fde-research`, and conversations use `/fde-research`. Claude Code's current official rules let `name` set the command name; if a same-named command exists on the machine, first check which SKILL path the menu is actually bound to. [Command naming rules](https://code.claude.com/docs/en/skills#how-a-skill-gets-its-command-name).

## Whole-package installation example: native Windows Claude Code

The following is a PowerShell example, to be run manually only once you decide to install. Upgrading this package never installs into your personal directory for you. If the target already exists, preserve and compare the old version first; do not overwrite it directly.

```powershell
# Run from the downloaded repository root.
python -B -X utf8 scripts/release_package.py --install "$env:USERPROFILE/.claude/skills/fde-research"
```

After copying, `fde-research/SKILL.md` should appear directly; avoid an extra nested level such as `fde-research/fde-research/`. Customer projects still live in their own location. Changing the source package does not update installed copies automatically; record the version used in this round and synchronize upgrades explicitly.

## Three ways of use

|Way|Invocation example|Do the nine child skills need separate registration?|
|---|---|---|
|Unified entry organizes the chain|`/fde-research complete preparation chain …`|No|
|Unified entry runs only one skill|`/fde-research only baseline analysis …`|No; this is single-skill execution|
|Call a child skill command directly|`/fde-baseline-analysis …`|Yes, the host must recognize that child skill separately; a nested grouped installation does not promise these commands automatically|

**"You can run only one of the skills" does not mean "nine separate commands appear automatically".** The unified entry routes by reading the child SKILL inside the package. If you also need nine separate commands, you can add sibling symbolic links for each child skill in the host's skills directory, or use the flat copy method in section 11.3 of the master README; how each of the two hosts actually loads them depends on the current environment. Do not keep several same-named copies without checking the load location. [Claude Code skill directories and links](https://code.claude.com/docs/en/skills#choose-where-skills-load).

With other agents, the same entry can also be read directly by path; Codex can use the discovered `fde-research` skill or the actual entry path. There is no dependency on Claude Code's argument substitution variables, subagent tools, or a dedicated runtime. When using the whole package with Codex, keep the same directory structure and confirm the load path on the actual host; do not treat a single scan experiment as a guarantee for every version.

## Conversation examples you can use directly

The following are sent to the agent, not executed in a terminal. Replace directories and material names with actual locations; an explicit request for a single skill does not automatically run the other eight.

If all you have is one vague goal such as "I want to use AI to improve NGS efficiency", first see the [one-sentence launch example](../README.md) and the [round-by-round guiding example](examples.md), then start as below.

Start investigation preparation:

```text
/fde-research complete preparation chain. The project directory is D:/FDE-Projects/ticket-efficiency and the goal is to shorten ticket handling time. There are no materials yet; this round does Stage 1 investigation preparation first and creates the project artifact index and investigation action list.
```

Baseline analysis only:

```text
/fde-research only 2. The project directory is D:/FDE-Projects/ticket-efficiency. Use the ticket details and field dictionary in the project index, compute the timeliness metrics agreed for this round, and output definitions, actual results, and the run record.
```

Select the same skill by English title or full skill name:

```text
/fde-research only baseline analysis. Keep the current project and the data already provided, and complete this round's quantification task.
/fde-research only fde-baseline-analysis. Keep the current project and the data already provided, and complete this round's quantification task.
```

Prepare a prototype handoff only, without development:

```text
/fde-research only prototype preparation. Read the currently effective scenarios and produce only the development handoff package; do not implement the prototype this round.
```

Keep an existing quotation:

```text
/fde-research only implementation plan and quotation. Read the old quotation I specified in the project index, use inherited mode to complete the report, keep the given prices and periods, and do not re-estimate.
```

Continue an existing project:

```text
/fde-research continue. First read D:/FDE-Projects/ticket-efficiency/project-artifact-index.md, restore the scope agreed last time and the currently effective versions, then complete this round's work and update the index.
```

These selection words are task conventions understood by the entry, not command-line arguments of an external program. The entry limits scope according to this round's instruction, keeps gaps open when real material is missing, and does not aim to run all nine stages. Each skill's number, inputs, and outputs are in the [master README](../README.md).

## How to tell it really works

First confirm that `fde-research` in the menu points to this unified entry. After sending an "only 2" task, the agent should read `fde-baseline-analysis/SKILL.md` inside the package, do only that work, and save actual outputs in the project directory. Being discoverable, choosing the right skill, and executing successfully are three different levels of verification.

This package provides entry instructions and static checks; actual Claude Code loading and model routing still need to be verified on your host with a real task, see the [validation record](validation.md). A child skill that is not registered separately should not be reported as supporting a same-named native command.


See [repository installation](github-installation.md) for Windows, macOS/Linux, Codex, and project-scoped installation.
