# Run and delivery contract

## Layout and evidence separation

Create a separate run inside the user's project; adapt names as needed and use actual relative manifest paths:

```text
run-YYYYMMDD-NN/
  technical-architecture-and-development.docx
  technical-architecture-and-development.md
  internal/architecture-conditions-and-open-issues.md
  evidence/inputs.md
  evidence/research.md
  evidence/decisions.md
  evidence/question-state.json
  architecture/specs/
  architecture/public/        selected presentation files only
  verification/               receipts, captures, Word checks
  delivery-manifest.json
```

Do not modify/copy originals unnecessarily. `inputs.md` identifies path, version, role, use, and hashes for consequential files; unreadable material has a coverage-impact note. Sources may be outside the run; final artifacts must be inside it. A new file is not automatically a new fact.

`research.md` records decision, candidates, version/access date, URL, supported claim, limits, and applicability. `decisions.md` records recommendations/reasons, conditions, actual FDE choices, changes, and a compact requirement/capability/work/verification map. Avoid an ADR per routine setting or copies of full websites/business repositories. Old project outputs are references, not new-project requirements. Reader-facing reports must stand alone.

## Runtime

Need input-format readers, official-source browsing, local execution, standard diagram rendering or Archify/its Node dependencies, Word generation, and real rendering. Helpers need Python 3.10+; DOCX builders need python-docx/Pillow. Codex uses its workspace dependency loader/document tools; other agents use verified available programs.

Locate dependencies first; do not silently install global services, copy large toolkits, or change host configuration. Continue analysis with explicit partial status if rendering is missing. Offline research remains not currently verified. Optional `agents/openai.yaml` is Codex UI metadata; other hosts can ignore it. External diagram/Word runtimes are not bundled.

## Question ledger

Substitute actual resolved paths/runtime in these shell examples:

```sh
python "$SKILL_DIR/scripts/run_state.py" --state "$RUN_DIR/evidence/question-state.json" init --project "Project name"
python "$SKILL_DIR/scripts/run_state.py" --state "$RUN_DIR/evidence/question-state.json" show
python "$SKILL_DIR/scripts/run_state.py" --state "$RUN_DIR/evidence/question-state.json" ask --file question.txt
python "$SKILL_DIR/scripts/run_state.py" --state "$RUN_DIR/evidence/question-state.json" answer --round 1 --file actual-reply.txt
```

`init` refuses existing state. Record `ask` before showing it; if recording fails, do not ask. It blocks round 21 and a new questionnaire while the prior answer is pending. The agent still owns relevance/quality. Resending the same recorded question after display failure adds no round. One owner writes the ledger sequentially.

Record actual answers including “unknown” or “not confirmed.” Never invent an answer to unlock another question. If the user wants delivery, pending questions can remain in a conditional result. Later corrections go into decisions without overwriting replies. Resume the same ledger across run directories/chats; do not reset the cap.

## Manifest

Use `schema_version: 1` and artifacts with `role`, relative `path`, and computed `sha256`:

```json
{
  "schema_version": 1,
  "diagram_profile": "standard",
  "status": "ready_for_review",
  "artifacts": [
    {"role": "report", "path": "technical-architecture-and-development.docx", "sha256": "<computed SHA256>"},
    {"role": "conditions", "path": "internal/architecture-conditions-and-open-issues.md", "sha256": "<computed SHA256>"}
  ]
}
```

This illustrates shape only; a final manifest needs all required roles and actual hashes. New runs explicitly select `standard` or `archify`. Missing profile preserves legacy `archify` behavior rather than silently downgrading.

| Role | Artifact |
|---|---|
| report | Formal DOCX |
| report_source | Maintainable Markdown body |
| conditions | Internal design conditions |
| inputs / research / decisions | Concise evidence/decision records |
| question_state | JSON ledger; empty questions if none asked |
| diagram_spec | Editable source per diagram; standard may use .mmd/.dot/.drawio/.svg |
| diagram_static | Actually rendered clear image per diagram |
| diagram_html | Standalone interactive HTML/SVG; required for Archify |
| diagram_receipt | Actual final Archify deliver receipt binding current source/HTML |
| diagram_visual | Actual diagram/capture review, covering every diagram |
| word_visual | Final Word rendering/all-page review tied to DOCX hash |

Standard requires all except diagram_html/diagram_receipt; Archify requires all. List each diagram's actual files/evidence. A provided diagram_html is still checked for complete HTML/SVG; an iframe-only portal belongs as a navigation entry in review notes, not that role. Do not fabricate Archify receipts with filenames or “PASS” text.

```sh
python "$SKILL_DIR/scripts/check_delivery.py" "$RUN_DIR/delivery-manifest.json"
```

The checker covers existence, nonempty files, containment, hashes, basic DOCX/HTML/SVG, and ledger consistency. It does **not** certify source truth, requirements coverage, diagram/text agreement, or visual readability. Verify current-byte receipt bindings and final-version page checks yourself.

For incomplete delivery use `partial` and list real files/gaps; nonzero checks truthfully indicate missing roles. Do not remove required roles to force success. A complete conditional review package may still depend on enterprise resources not yet provided.

## Updates and finish

Preserve replaced outputs under run history before changing them. Compare changed inputs and trace conditions → decisions → diagrams → work → checks. Regenerate/check affected artifacts and hashes only.

Finish with formal/internal report paths, diagram entry, completion state, and remaining conditions. Report a service URL only if started/verified, with start/stop instructions. A review draft is not approved and a work list is not an implemented system.
