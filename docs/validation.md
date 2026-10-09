# 2.3.0 validation record

Checked 2026-10-09. This edition was independently tested on Windows with a fresh Python 3.12.14 environment installed from this repository's requirements-test.txt. It needs neither a private Codex runtime nor the other language edition. The repository records results in `validation/results-2.3.0.json`.

|Check|Observed result and scope|
|---|---|
|Regressions|106 pass: quotation 68, runtime contracts 9, architecture delivery 5, scenario labels 3, encoding portability 4, fonts 5, package 8, release/install 4.|
|Strict encoding|UTF-8 default mode disabled; EncodingWarning treated as an error. Only the runtime suite exempts two third-party pypdfium2 version readers; package modules remain strict.|
|Static structure|136 installation files, root plus nine child SKILLs, complete catalog, JSON examples, local links, and four shared-copy pairs pass.|
|Release/install|Two independent output directories produce identical ZIP bytes. Extracted installed-name check passes; existing installations and unsafe manifest paths are rejected.|
|Language and professional logic|File mapping, Python structures, and JSON models align. Publication normalizes line endings without changing quotation rules. This one-time alignment review is not a future cross-repository release dependency.|
|CI and scripts|Both workflow YAML files parse; screenshot helper passes Node syntax check. GitHub-hosted execution has not occurred yet.|
|Historical evidence|All byte hashes for non-PNG files and decoded-pixel hashes for PNGs in this edition's independent evidence copy pass.|

Historical Linux 2.2.1 evidence is stored in `validation/evidence/2.2.1-linux/`, with this edition's two rendering cases. It demonstrates synthetic quotation-toolchain results under Python 3.13.16 and LibreOffice 24.2.7.2, not a new render. Both successful cases have six pages and two passes, with visual review still required. See the evidence README for extraction and summary-correction provenance. Evidence is excluded from agent installation archives.

Unverified: this release's GitHub-hosted execution, real Windows Word/LibreOffice conversion, macOS, a Claude Code model-driven full chain, real customer templates and all-page acceptance, production deployment, and business outcomes. Runtime tests include mocked Office calls, not real Office acceptance. The manual Linux workflow can generate new evidence; its configuration is not proof it has run.

See [release instructions](releasing.md) for reproduction.

## English cover addition

An English-only visual abstract is included at the top of the README and in the release manifest. An unfolding project dossier connects raw business evidence, AI scenarios, an optional prototype, and the final preparation deliverables. The nine skills are described as one reusable package. No professional skill behavior or calculation logic changes. Illustrative review marks are not evidence of actual customer approval. Static package checks and all four release/installation regressions pass after adding the cover.
