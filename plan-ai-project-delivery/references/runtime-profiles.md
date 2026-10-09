# Runtime profiles

Inspect actual file, calculation, Word creation, field update, browser, and image-viewing capabilities. Brand is not capability discovery. Generic use has no Claude-specific API dependency; any agent able to follow SKILL.md, read inputs, execute scripts, and inspect page images can use it.

| Profile | Use | Tool source | Shared standard |
|---|---|---|---|
| codex | Codex with documents/workspace dependencies | documents skill, load_workspace_dependencies, bundled runtime | Editable DOCX, current TOC pages, actual all-page rendering/review, hash traceability |
| generic | Claude Code, another coding agent, or explicitly selected local workflow | Approved Python 3.10+, python-docx, Pillow, lxml, pypdf, pdfplumber, pypdfium2, LibreOffice | The same; code generation/PDF alone is not full acceptance |

Estimation needs only the standard library; load Word dependencies when needed. Discover installed tools before changing environments. [requirements-word-generic.txt](../scripts/requirements-word-generic.txt) declares dependencies; deployments may lock verified versions. LibreOffice is a separate program, not supplied by installing Python libraries.

Commands are in [Word delivery](word-delivery.md), section 7. Resolve interpreter/program paths on the current machine. PowerShell can invoke quoted executable paths with `&`; use appropriate quoting on other shells. Do not put one user's absolute runtime paths in reusable handoffs.

Internally record runtime_profile, interpreter/renderer, versions, fonts, logs, and gaps. Only the Codex profile follows host-required artifact markers; generic requires no OpenAI account, Codex MCP, or documents plugin. Neither profile authorizes external transfer/cloud document services.

Enterprise-approved Word/other rendering may handle complex templates with final-DOCX-bound page images, updated TOC, and QA. The bundled finalizer handles the bundled builder's TOC contract, not arbitrary template fields.
