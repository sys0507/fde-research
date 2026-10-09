# Changelog

## 2.3.0 — 2026-10-09

- Added an original English project-dossier cover illustrating business evidence, the optional prototype, and final preparation deliverables from the nine-skill package.

- Independent repository structure, all-rights-reserved notice, and provenance inventory.
- Cross-platform installation, deterministic ZIPs, complete manifests, overwrite protection, pinned direct test dependencies, and a self-contained regression runner.
- Windows/Linux CI, manual LibreOffice check, and independent edition-only historical rendering evidence.
- Removed course-drive installation paths and cross-edition release coupling; preserved all nine methods, calculation rules, and Codex/generic runtime paths.
- Publication text normalized to LF; historical evidence retains its byte/pixel verification contract.


## 2.2.2-en.1 — 2026-10-08

- Word delivery guidance (quotation and architecture) adds that, when a substitute font is accepted, page review must explicitly check bold, italic, and glyph shapes; a substitute may lack the needed weight or style while the font-name check still passes.
- The English teaching and guide documents (master README, docs, and all nine skill READMEs) are now faithful translations of the Chinese edition, which is canonical, so both editions teach the same content. Material that existed only in the English READMEs of skills 1–4 was removed, and every skill README follows the Chinese ten-section structure.
- The Chinese master README corrects its implementation-readiness handoff path example to match the skill; the English edition already used `implementation-readiness/round-01/implementation-conditions-and-design-handoff.md`.
- Only guide documents changed; scripts, templates, JSON examples, and calculations are byte-identical to 2.2.1-en.1. Package checks and all 102 tests were rerun; the program files covered by the 2.2.1 Linux render evidence are unchanged, see [validation](docs/validation.md). The Chinese edition moves to 2.2.2 in step.

## 2.2.1-en.1 — 2026-10-08

- Word delivery guidance (quotation and architecture) now states that substitution flags only declare an acceptable result and do not change the font the renderer selects; what was actually selected is decided by used_fonts in the final PDF, with fc-match as an aid only; installing a font or passing --font-dir only makes it discoverable, and switching fonts requires --body-font, --heading-font, or document styles followed by rebuild and inspection.
- The baseline skill requires customer text inputs to be read read-only in their confirmed encoding, recording how it was confirmed; the calculation run-record template shared by skills 1/2 adds an "Encoding and how confirmed" column.
- check_package rejects virtual environments, node_modules, and folders containing pyvenv.cfg or conda-meta inside the package, without scanning their third-party code; one new maintenance test brings the total to 102.
- Validation adds a real Linux + LibreOffice render and font check of this version; the evidence bundle is stored outside the skill package and bound to package hashes.
- Sources changed after the 2.2.0-en.1 release, so the version is raised to avoid one version number covering different content. The Chinese edition moves to 2.2.1 in step.

## 2.2.0-en.1 — 2026-10-08

- Added explicit encodings to text I/O and subprocess output; strict EncodingWarning and synthetic GBK-default tests cover Unicode paths, inputs, and outputs without relying on callers enabling UTF-8 mode.
- Added context recovery to the router and all nine specialists, with active skill paths, package/artifact versions, and next actions recorded in project indexes and handoffs.
- Made the evidence-versus-authorization boundary explicit for customer documents, staff replies, web pages, and tool output, including standalone calls. Added data minimization, controlled originals, de-identified derivatives, process/role aggregation, and no default individual performance ranking to the first three skills.
- Standardized installed/archive parent folders as fde-research while retaining source folder names. Made the first two skill descriptions platform-neutral and kept installation paths portable.
- Retained the complete master README; added a compact agent workflow/handoff map and typical sequence positions alongside stable skill IDs.
- Documented intentional shared copies versus independent Word/delivery implementations. Package checks enforce explicit encodings, portable paths, installation names, and four shared-file pairs.
- Added local font preflight and actual final-PDF font/embedding evidence inspection; quotation finalization enforces the result and supports explicitly accepted substitutions. Both Codex and generic-agent document paths remain available.
- The edition contains 124 files and passes 101 regression tests, temporary installation/hash checks, and numeric parity checks against the Chinese edition. See [validation](docs/validation.md) for scope and the narrow third-party encoding-warning exception.

Both source editions were backed up before this update. Source folders and personal agent installations were not renamed or replaced.

## 2.1.1-en.1 — 2026-10-08

English edition aligned with the finalized Chinese 2.1.1 package.

- Retained the four existing English specialist methods, references, templates, and detailed README material; added explicit nine-skill handoffs.
- Added the fde-research unified entry and the remaining five specialist skills, including their detailed methods, templates, metadata, tools, and per-skill READMEs.
- Added the complete-chain master README, two relationship diagrams, full file catalog, project-index/handoff templates, grouped installation, standalone usage, and one-sentence NGS investigation example.
- Preserved standard/Archify architecture profiles and both Codex and generic-agent Word paths, including inherited quotations and activity-based new estimation.
- Localized generated scenario pages/reports, customer tables, Word front matter/footers, error text, and illustrative JSON text. Preserved IDs, schema/CLI fields, calculations, numeric example inputs/currencies, and traceability controls.
- Used English filenames and document defaults; examples are not project facts, market rates, or guaranteed outcomes.
- Kept the Chinese source package unchanged and preserved the original English package in a separate backup.

See [validation](docs/validation.md) for tests actually performed on this edition. This version does not claim production deployment, universal host discovery, or unperformed Office/browser acceptance.
