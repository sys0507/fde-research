# Maintenance, installation migration, and runtime contracts

Version 2.3.0. The source folder can keep the name skills; release archives and installed parent folders use fde-research, matching the root SKILL name. See the [naming standard](https://agentskills.io/specification#name-field). Do not activate same-named Chinese and English copies together.

## Upgrade an existing installation

Preserve installed copies/customizations, compare versions, and install the complete package as ~/.claude/skills/fde-research or ~/.agents/skills/fde-research. Move the old installed copy to a backup location outside the host's scan scope to avoid duplicate entries; do not only change name or scatter resources. This update changes sources, not personal installations. Source-mode checking permits a different root name with a warning; formal installation and release must add --installed to check the parent folder name strictly.

Claude Code accepts frontmatter and directory invocation names; other hosts/packagers need not provide this compatibility. Skill retention after compaction has per-skill and total budgets. Restore from project records and re-read as needed instead of treating current 5000/25000-token limits as portable guarantees. See [skill lifecycle](https://code.claude.com/docs/en/skills#skill-content-lifecycle).

## Copies that stay synchronized

| Files | Maintenance contract |
|---|---|
| Three Stage4/metric-card/calculation-run templates in 1/2 | Intentional standalone copies. Edit baseline-analysis and sync discovery-guide; check_package compares hashes. |
| scripts/check_pdf_fonts.py in 8/9 | Shared standalone inspector. Update in 9, copy to 8; check_package compares hashes. |
| build_report.py, check_delivery.py, word-delivery.md in 8/9 | Intentionally different. 8 handles technical/diagram delivery with default linked contents; 9 handles commercial/calculation binding and native page-numbered contents finalization. Do not require identical hashes. |

## Text encoding and checks

Package JSON, Markdown, HTML, and logs explicitly use UTF-8; existing Excel-oriented CSV may explicitly use utf-8-sig. Read customer originals in their confirmed encoding and record conversions; never assume GBK is UTF-8. Binary PDF/image APIs do not take text encoding. Scripts do not depend on callers adding -X utf8, although it remains useful for terminal consistency.

Virtual environments, node_modules, and folders containing pyvenv.cfg or conda-meta must not live inside the skill package; check_package reports them as errors and does not scan their third-party code. Keep environments outside the package and reference them by interpreter path or project convention.

check_package uses AST checks for common text APIs and subprocess text capture, rejecting omitted encoding/literal None while excluding binary modes and known PDF/image openers. It is not whole-program type inference; dynamic wrappers need runtime tests. Do not hide data corruption by discarding decoding errors.

```sh
python -B -X utf8 scripts/check_package.py
python -B -X utf8 scripts/check_package.py --installed
python -B -X utf8=0 -X warn_default_encoding -W error::EncodingWarning plan-ai-project-delivery/scripts/test_estimate.py
python -B -X utf8=0 -X warn_default_encoding -W error::EncodingWarning plan-ai-project-delivery/scripts/test_portability.py
python -B -X utf8 scripts/test_package.py
python -B -X utf8 plan-ai-project-delivery/scripts/test_fonts.py
```

Use the second command on a correctly named installed copy; the others can run from sources. Full regressions include test_runtime.py, test_delivery_profiles.py, and test_screen_labels.py. See [validation](validation.md) for dependencies and actual results. These checks do not establish interview truth, model routing, customer approval, or visual acceptance.

Font checks record local registration, then inspect fonts used by extractable text in the actual final PDF and resource embedding evidence. Missing/substituted fonts need explicit handling, not automatic installation or silent relaxation; record accepted substitutions in run arguments. Image text, glyph quality, and layout still need all-page review.

This repository is maintained and released independently; no other edition is a usage, test, or release dependency. See the [release guide](releasing.md).
