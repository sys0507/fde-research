# Environment, installation, and standalone use

This document supplements chapter 11 of the [master README](../README.md). Grouped installation with the unified entry is the recommended way; complete installation steps are in the [unified entry guide](unified-entry.md). This document keeps the notes on registering the nine skills separately, capability discovery, and environment troubleshooting. Checked on: 2026-10-07. First distinguish skill source files, installed copies, and customer projects, so customer reports are not generated in the wrong place.

## 1. Minimum requirements

The minimum prerequisite is that the agent can read the skill and input files and write outputs to the specified project location. You can start by giving the source package path and asking the agent to read the relevant `SKILL.md`. For a unified native entry, place the whole package in an fde-research subfolder of the host's skills directory; register the nine folders separately only if you need nine separate commands. A host that offers only text chat and cannot read local files needs the actual materials provided first through its supported upload or file tools, and must not claim to have read the example source location.

The whole package keeps the root SKILL, the nine sibling professional skill folders, the root README, and `docs/templates/scripts`. A single skill must be copied with its complete folder; the investigation guide's full Stage 4/5 also needs the sibling baseline and diagnosis skills. Other skills accept equivalent external outputs and do not force upstream skills to be called again.

`agents/openai.yaml` is optional interface metadata that other hosts can ignore. When only the nine skills are copied, "back to overview" in their READMEs is optional navigation to the source package; read it from the original source package path instead. Links inside each skill remain unchanged. The nine skills are not an automatically running program, and no additional enterprise connectors need to be installed to start investigation preparation.

## 2. Optional: register the nine skills separately

If you already use the unified entry at `~/.claude/skills/fde-research/SKILL.md`, you can simply use `/fde-research only <skill title>` without the flat installation in this section. This section serves those who want nine separately registered commands.

Native Windows personal directories:

|Host|Installed to in this example|Example skill entry|
|---|---|---|
|Codex|`%USERPROFILE%\.agents\skills`|`fde-discovery-guide\SKILL.md`|
|Claude Code|`%USERPROFILE%\.claude\skills`|`fde-discovery-guide\SKILL.md`|

On Mac/Linux the corresponding personal directories are the running user's `~/.agents/skills` and `~/.claude/skills`. Project level means the same-named hidden folder under the project root. Paths and invocation follow the [Codex official skills documentation](https://learn.chatgpt.com/docs/build-skills) and the [Claude Code official skills documentation](https://code.claude.com/docs/en/skills); check the loading result with your own current host version.

The complete copy script is in section 11.3 of the master README. The personal level is the default and allows reuse across projects; if the team needs to manage skills with the project, change the destination line in the script to one of the following:

```powershell
# Codex project level: first change this to your actual project directory.
$fdeSkillsDestination = 'D:\FDE-Projects\ticket-efficiency\.agents\skills'
```

```powershell
# Claude Code project level: choose only the destination matching the host you use.
$fdeSkillsDestination = 'D:\FDE-Projects\ticket-efficiency\.claude\skills'
```

**These two snippets only set the copy script's destination variable; running them on their own does not install anything.** Run the complete copy example from the master README with the destination line replaced. If a same-named folder already exists, the example stops first; compare contents and versions, save customizations, and then decide where to update. Do not put old and new same-named skills in several locations that will all be loaded.

Project-level layout example:

```text
ticket-efficiency/
  .agents/skills/nine skill folders...      when using Codex
  .claude/skills/nine skill folders...      when using Claude Code
  project-artifact-index.md
  business-analysis/...
```

The diagram shows locations for both hosts; with one host you only need its folder. After copying, start the agent from the customer project root. The source package stays on the example source location; give its README path at launch so the package-wide conventions can be read. When sharing across computers, bring the source package too and update the path in the project conventions.

## 3. Launch, check, and continue

In grouped mode, use `/fde-research` after launch; to choose a stage use `/fde-research only 2`. The command-line launch below works for both installation methods; the later examples of calling the nine skills individually assume they were registered separately.

When using installed command-line tools, run the matching group in PowerShell; the project directory must already exist, and the examples do not install the Codex/Claude Code clients:

```powershell
Set-Location -LiteralPath 'D:\FDE-Projects\ticket-efficiency'
codex
```

```powershell
Set-Location -LiteralPath 'D:\FDE-Projects\ticket-efficiency'
claude
```

Then send the prompt from section 11.4/11.5 of the master README in the **agent's conversation box**. The Codex CLI/IDE supports `/skills` or `$` for choosing skills; Claude Code uses `/fde-discovery-guide` after the nine skills are registered separately, or `/fde-research only 1` in grouped mode. An ordinary natural-language request can also name the skill and its path explicitly. For each host's invocation mechanism, see the official documentation above.

The first verification should check four things:

1. Which `SKILL.md` was actually read, and whether its sibling 2/3 and internal resources can be read.
2. Whether the current write location is this project, and whether the source package that was read and the executed copy are the same version.
3. Whether real files were generated this round, and whether items not provided or not executed were kept as unknown.
4. Whether the project artifact index points to these files, and whether the next session can continue from it.

Later work does not require reinstalling or starting from 1. Read `project-artifact-index.md` and the currently effective materials first, then this round's skill; update the index when done. Whether the prototype is only prepared or actually implemented, and whether the quotation is a first estimate or inherits an old version, is stated in this round's task.

## 4. Optional: keep project conventions in the project

To reduce repetition when switching sessions, you can merge the following **project convention text** into an existing project instruction file. Common choices are `AGENTS.md` for a Codex project or `CLAUDE.md` for a Claude Code project; it can also be kept in an ordinary project note that the agent is explicitly told to read at each launch. Host reading rules are in the [Codex project instructions documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and the [Claude Code project memory documentation](https://code.claude.com/docs/en/memory). These files do not replace the skills directory and are not an extra prerequisite for using the package. If the file already exists, keep its original conventions rather than overwriting the whole file with the example.

```markdown
## FDE project working conventions

- FDE source package: D:/FDE-Tools/fde-research, version 2.3.0.
- The current directory is the customer project; the source package and installed skills are read-only.
- Fill in the actual installed or source package path of the FDE skill package used by this project; in grouped mode, read its root SKILL.md first and choose the child skill according to this round's scope.
- Read the source package README and this project's project-artifact-index.md as needed; a complete project without an index creates one from the template, and a temporary single-skill task can use a short handoff.
- State the actual location of the SKILL executed this round and read resources from its folder; keep 2/3 as siblings.
- Write outputs to the project, keep old versions and manual edits, and update effective versions, status, gaps, and next steps when done.
- Record simulations, estimates, facts, business confirmations, and run verification separately.
- Choose the technical diagram and Word paths according to the tools currently available; report only checks actually completed.
```

When only the project's skills folder is copied to another machine, the complete source package does not migrate with it. Bring the complete source package and change to the new path, or give the new source package directory explicitly in the new session. Do not copy a customer project's index, originals, or quotation workpapers into a personal shared skills directory.

## 5. Updates and switching runtime environments

The source package and installed copies are not synchronized automatically. Revise and check in the source package first and record the version once it passes; for installed copies, compare and back up customizations before updating. If the new version removed old files from a folder, deal with them after a migration check; overwriting same-named files alone does not make the versions fully identical.

The environment is wherever the agent actually runs. Native Windows uses Windows paths; in WSL the example source location is usually mounted at `/mnt/g`, and the user home is the WSL home; containers, remote machines, and cloud environments need readable skills and materials and a writable project location provided separately. A local personal installation does not mean a remote session already has the files. Do not mix the Windows and WSL installation directories.

## 6. Common problems

|Symptom|Check first|Action|
|---|---|---|
|Only fde-research is visible, not the nine child skills|Whether the grouped unified entry is used|Select a single skill through the entry; separate commands need separate registration, and a nested folder is not a guarantee of automatic registration|
|The skill list shows nothing|Actual running user, skills directory, `<skill-name>/SKILL.md` hierarchy, project launch location|Reopen the session from the correct project; if still not visible, read the files directly by path and continue investigation preparation|
|An old version was read|Whether personal and project levels both hold same-named skills, and the actual load path|Preserve customizations and choose one explicit version; record this round's actual source|
|1 cannot find 2 or 3|Whether the three skills share the same parent folder|Install all nine skills completely as siblings; do not copy only 1's SKILL|
|A README's back-to-overview link does not open|Whether only the nine skills were copied while the source package stays at a different location|Read the source package README directly; references inside each skill stay as they are|
|Source materials cannot be read|Whether the agent runs in WSL, a container, or remotely, and whether the actual path is accessible|Use that environment's correct path and an authorized file entry|
|Text can be generated but not Word/captures|Whether a specific runtime/rendering capability is missing, or the skill simply is not installed|Check the capability list below; deliver only what was actually completed and mark the remaining checks|
|Editing the source package changes nothing|Whether a previously installed copy is being executed|Check versions and update the copy; reopen the session if needed|

## 7. Discover capabilities by stage

1. Read the formats of the current materials and confirm a writable project location and version.
2. For calculation, check Python/data and charting tools; no reinstallation is needed when using a reliable existing baseline.
3. For scenarios/prototype, check local code execution and a browser; generating HTML alone cannot be claimed as completed captures.
4. For documents, check editable Word generation, contents/field handling, real rendering, and page-by-page review.
5. For architecture, check diagram sources, rendering, and necessary interaction under the standard or Archify contract.

## 8. Two quotation paths

Codex keeps the existing documents, dependency loader, bundled runtime, and marker contract. Claude Code and other generic agents use the actually selected Python, LibreOffice, and libraries; detailed parameters are in the [quotation runtime notes](../plan-ai-project-delivery/references/runtime-profiles.md). The algorithm, internal/external cost split, versioning, and delivery checks are shared; choosing generic mode does not exempt document rendering and visual review.

When running Python scripts on Windows, `python -X utf8` or setting `PYTHONUTF8=1` for the current process is recommended; child processes should inherit UTF-8 as well. All tool paths are discovered in the current round, and command arguments quote paths with spaces correctly. The generic dependency list gives a compatible range; formal environments can lock their own verified versions. This package never installs or changes global dependencies automatically.

A text-only agent without execution can still analyze materials and write, but cannot claim that calculation, prototype, captures, or Word rendering are complete. Supporting generic agents does not guarantee that every host/operating-system combination has been tested. This version did not perform a personal-directory installation, a Claude Code session, or a real enterprise full-chain validation; the actual scope of checks is in the [validation record](validation.md).

In the Windows path table, %USERPROFILE% means the user home directory; executable PowerShell examples use $env:USERPROFILE, and only CMD uses %USERPROFILE%. The installation directory is always fde-research; the source package can still be named skills. Before upgrading, preserve the old folder and check for same-named entries so old and new copies are not discovered together. See [maintenance and migration](maintenance.md).
