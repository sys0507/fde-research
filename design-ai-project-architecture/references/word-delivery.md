# Formal Word architecture delivery

Turn completed architecture judgments into a reviewable document explaining requirements, choices, component responsibilities, work, and completion. The builder automates layout, not architecture or editing.

## 1. Choose the document path

- Prefer customer templates, preserving cover, styles, headers/footers, contents, figures/tables, signatures, and version records. Use actual document-editing/rendering tools for complex templates rather than overwriting them with the default builder.
- Without a template, `scripts/build_report.py` offers professional defaults: A4, black headings, 12 pt body/18 pt spacing, 17/14/12 pt headings, 10.5 pt tables, repeating headers, and continuous pages. These are readability defaults, not fabricated standards.
- Its contents list is clickable **without page numbers**. For page-numbered native TOC, complex numbering, footnotes, merged tables, or revisions, use the host's document capabilities, update native fields, and render. Never invent TOC page numbers.

Organize chapters for this project, including recommendations, scope, design/rationale, work, validation, resource drivers, and review conditions. Customer-affecting dependencies must appear externally; internal discussion and sensitive details stay in conditions.

## 2. Builder contract

Requires Python 3.10+, python-docx, and Pillow. Resolve an allowed runtime first. Codex document work uses its dependency loader/bundled runtime and host document instructions; do not silently use unrelated desktop programs. Generic agents may use explicitly verified project-approved tools.

From the skill directory:

```sh
python scripts/build_report.py --markdown project-output/report.md --metadata project-output/report-metadata.json --output project-output/technical-architecture-and-development.docx --body-font "Arial" --heading-font "Arial"
```

Or use the actual installed script path. Existing outputs are preserved unless `--overwrite` is explicit after retaining prior/manual work. Images resolve relative to Markdown.

```json
{
  "title": "Maintenance assistance: architecture and development",
  "subtitle": "First-phase proposal",
  "version": "V1.0",
  "status": "Draft for technical review",
  "date": "2026-10-08",
  "audience": "Business, IT, and delivery owners",
  "purpose": "Review the technical route, integration responsibilities, work, and verification conditions.",
  "document_control": [
    ["Document ID", "Assigned by the project"],
    ["Scope", "Confirmed first-phase capabilities"],
    ["Change", "V1.0 initial review draft"]
  ]
}
```

Required nonempty strings: title, version, status, date, purpose. Optional subtitle/audience and two-column string-array document_control. Unknown keys fail. Example dates/identities/status are illustrative, not project facts. Cover/control come from metadata and should not be duplicated in the body.

Supported Markdown subset:

- Headings `#`, `##`, `###`, beginning at level 1 without skips.
- Blank-line paragraphs, joined ordinary lines, bold, inline backticks retained as plain text, and HTTP(S) links.
- One-level bullets and numbered items; original numbering retained, no nested lists.
- Pipe tables with header/separator, equal columns, leading/trailing pipes, at most six columns; escape a cell pipe as `\|`.
- A standalone image line referencing an existing local relative PNG/JPEG. No remote download, missing-image skipping, or direct SVG insertion.
- `<!-- page-break -->`.
- `<!-- figure-page: a3 -->` or `<!-- figure-page: a4-landscape -->` immediately before one image. The following body returns to A4 portrait without a trailing blank page.

Example body:

```markdown
# 1 Recommendation and scope

Use the **approved internal service route** for the current processing boundary.

## 1.1 Responsibilities

| Component | Responsibility | Verification |
|---|---|---|
| Task service | Persist tasks and human decisions | Retry without duplicate submission |
| Model service | Explain evidence and propose actions | Evaluate authorized samples |

<!-- figure-page: a3 -->
![Figure 1. Overall technical architecture](images/overview.png)

# 2 Development and verification

Subsequent body content returns to A4 portrait.
```

Rewrite unsupported fences, HTML, blockquotes, checklists, nested lists, level-4 headings, or unsupported inline structures into supported forms or use document tools. Do not delete information to pass parsing. The helper is not a complete Markdown parser; rendering must catch unrecognized layout problems.

The sibling `.build.json` records document/input hashes, counts, fonts, and `BUILT_RENDER_AND_VISUAL_QA_REQUIRED`. It proves construction only and remains internal.

## 3. Fonts and figure pages

English defaults use Arial; verify the renderer and receiving environment actually have a suitable font, or choose an available licensed family. For other scripts choose fonts covering them. Do not hardcode local font paths. Explicit Word font attributes do not prove font discovery; build records retain `font_availability: NOT_VALIDATED`.

Fix boxes, missing glyphs, blank regions, or substituted-font pagination through actual font configuration/rebuild/render. Split dense diagrams instead of shrinking them beyond readability; preserve captions, boundaries, arrows, and technology names. Presentation captures must be identified as architecture displays, not production software.

## 4. Final gate

Render the latest DOCX into all-page images using actual document tools. Codex follows host-resolved bundled rendering; generic agents may explicitly use approved LibreOffice/Word rendering, recording the tool.

Inspect every page: fonts, body, figures/captions, table continuation/repeated headers, stranded headings, page numbers, mixed paper sizes, blank pages, and contents links. Check agreement with decisions/conditions/diagrams. Reorganize wide tables/long cells/dense images rather than making text illegible.

Record final DOCX hash, page count, page-by-page review, issues/repairs, and remaining uncertainty. Only readable final pages with complete material content pass. Without rendering report “generated; layout acceptance pending.”

Deliver formal Word, separate internal conditions, and chosen diagram artifacts. Retain source/build records for continuation. QA PDF/page PNGs, tests, and debugging belong in internal verification, not the default customer bundle.

## Font availability and final PDF verification (2.2)

The builder's font_availability=NOT_VALIDATED means DOCX generation did not verify fonts. The standalone scripts/check_pdf_fonts.py requires pypdf and pdfplumber and supports codex/generic paths. Discover actual tool/interpreter locations and use the intended fonts:

```sh
python -X utf8 scripts/check_pdf_fonts.py --preflight --font "Arial" --output qa/font-preflight.json
python -X utf8 scripts/check_pdf_fonts.py qa/final.pdf --font "Arial" --output qa/pdf-fonts.json
```

Replace examples with the actual final PDF and new internal report locations. Preflight returns AVAILABLE/MISSING/UNVERIFIED; registration does not prove renderer selection. PDF inspection normalizes subset prefixes, common style suffixes, and family aliases, recording actual text fonts, pages, and resource embedding. Unembedded standard fonts are not automatically a mismatch; the report preserves evidence and limits.

Only for an already accepted substitution add --allow-substitute "Arial=Liberation Sans", using actual environment names. Substitution flags only declare an acceptable result; they do not make the renderer use that font. The right-hand name must be a font that actually appears in the final PDF. What the renderer actually selected is decided by used_fonts in the final PDF (a first check's pdf-fonts.json shows it). Fontconfig's fc-match only reflects generic matching under the current configuration; renderers apply their own replacement rules, so it is an aid only, and Windows does not include it by default; availability depends on installed tools. Distinguish discoverable from selected: installing a font or configuring a font folder the renderer can discover only makes a font discoverable, and the document still uses the fonts its styles request. To switch to a font, specify it through --body-font, --heading-font, or the document styles, then rebuild from the source, render, and inspect again. PDF states are MATCHED, SUBSTITUTION_ACCEPTED, MISMATCH, or UNVERIFIED (such as image-only PDFs). Exit codes are 0 for matches/accepted substitutions, 2 for mismatch, 3 if unverified. None establishes visual acceptance: explain/review unobserved expected fonts, pages without extractable text, image text, and missing glyphs. When a substitute font is accepted, page review must also explicitly check bold, italic, and glyph shapes: a substitute may lack the needed weight or style, and the renderer may synthesize it or fall back to regular while the font-name check still passes. The report binds the final PDF hash; rerun after PDF changes.
