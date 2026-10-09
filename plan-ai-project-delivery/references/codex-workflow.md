# Preserved Codex entry

This is the Codex-specific path. Use the [common workflow](workflow.md) for estimation, scope, inheritance, and writing so commercial rules remain identical across agents.

1. Read the available `documents` skill and use `load_workspace_dependencies` to locate bundled Python, Node, and rendering dependencies.
2. Follow that skill's actual artifact-operation requirements. A host execution marker is not a customer-facing company watermark and does not apply to generic agents.
3. Run this builder with bundled Python, or follow the documents template workflow for customer templates.
4. Follow [Word delivery](word-delivery.md), section 5, with default `--renderer-mode codex`, the documents renderer, and bundled runtime-bin.
5. Inspect every final page, bind QA to the final hash, then run check_delivery.py. Field checks do not replace visual inspection.

Preserve dependency selection and quality gates. Do not silently fall back to desktop LibreOffice after failure. If the user/host explicitly chooses generic, record that choice and follow [runtime profiles](runtime-profiles.md).
