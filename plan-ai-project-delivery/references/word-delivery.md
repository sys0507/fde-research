# Editable Word delivery and actual rendering

Deliver a formal editable report pending human review. Codex and generic paths share the Markdown builder/TOC finalizer. The agent writes commercial content, estimate.py calculates, and the selected [runtime profile](runtime-profiles.md) provides real layout/rendering.

## 1. Document path

Prefer a supplied template, preserving cover/styles/headers/footers/contents/figures/tables/signatures/version records through capable document tools (Codex: documents). Do not replace customer formatting with a new default document.

Without a template use build_report.py: A4, black headings, 12 pt body/18 pt spacing, headings 17/14/12 pt, tables 10.5 pt, content-weighted columns/repeated headers. Cover unnumbered; control/contents use lower-case Roman pages; body starts at 1. Footer “Page X” uses 9 pt text/numbers and omits a potentially ambiguous total. These are readability defaults, not mandatory standards.

The builder creates native Word `TOC \o "1-2" \h \z` with clickable heading levels 1–2, right-aligned pages, and dot leaders. Level 3 stays out; the purpose heading uses a non-outline style. Finalize from real pagination as below; setting updateFields alone is incomplete. Keep native TOC for later Word maintenance. Arbitrary multilevel numbering, footnotes, merged tables, and tracked revisions need capable template tools. Do not substitute manually spaced fake page numbers if update is unavailable.

Include recommendations, scope, team/schedule, milestones, acceptance, price/payers, and review matters, adapting section count. Disclose customer-affecting dependencies while keeping sensitive internal discussion separate.

## 2. Input contract

Builder: Python 3.10+, python-docx, Pillow. Finalizer also uses pypdf, pdfplumber, lxml. Codex uses discovered bundled Python and documents requirements/artifact operation. Generic additionally needs pypdfium2 and installed LibreOffice, without Codex markers. Resolve `python` on this machine; `-X utf8` makes text handling explicit. Record missing dependencies rather than silently switching profiles.

```sh
python -X utf8 scripts/build_report.py --markdown project-output/report.md --metadata project-output/report-metadata.json --output project-output/implementation-plan-and-quotation.docx --body-font "Arial" --heading-font "Arial"
```

Use the actual installed script path when not in the skill directory. Preserve prior outputs/manual work before explicit `--overwrite`. Images resolve relative to Markdown.

```json
{
  "title": "Maintenance assistance system\nImplementation plan and quotation",
  "subtitle": "First-phase proposal",
  "layout": {"chapter_page_break": true},
  "version": "V1.0",
  "status": "Pending human review",
  "date": "2026-10-08",
  "audience": "Business, IT, and delivery owners",
  "purpose": "Review scope, organization, schedule, acceptance, and expenses.",
  "document_control": [
    ["Document ID", "Assigned by the project"],
    ["Scope", "Confirmed first-phase capabilities"],
    ["Change", "V1.0 initial review draft"]
  ]
}
```

Required nonempty title/version/status/date/purpose; optional subtitle/audience and two-column string-array document_control. Unknown keys fail. Illustrative metadata is not a project fact. Cover/control are generated; do not duplicate them in the body. JSON `\n` may break titles semantically, without spacing tricks. Optional layout accepts only boolean chapter_page_break, default true: subsequent level-1 chapters/appendices start a page; false permits compact continuous documents. Levels 2–3 flow with the next paragraph. Do not add duplicate explicit breaks before automatic chapter breaks.

Supported body subset:

- `#`, `##`, `###` without skipped levels. Authors control numbering/text; TOC uses identical titles.
- Blank-line paragraphs; joined ordinary lines; bold and inline code as plain text; HTTP(S), internal bookmarks, and portable attachments inside client. Attachment targets must exist; percent-encode spaces when needed. No absolute machine/internal-cost links.
- Single-level bullets and numbered lists, preserving written numbers.
- Pipe tables with header/separator, equal cells, at most six columns, outer pipes; escape embedded pipes as `\|`.
- Standalone image lines with real local relative PNG/JPEG; no remote download, skipped missing images, or SVG insertion.
- `<!-- page-break -->`.
- `<!-- figure-page: a3 -->` or `<!-- figure-page: a4-landscape -->` immediately before one image. Contiguous headings immediately before the image accompany it, avoiding a heading-only portrait page. Image space accounts for those headings; later text returns to A4 portrait and continuous body numbering without a final blank page.

Rewrite unsupported code fences, HTML, quotes, checklists, nested lists, level-4 headings, and unsupported inline structures or use capable document tools. Preserve information. The parser rejects recognized unsupported syntax but is not a full Markdown implementation; actual rendering remains necessary.

The sibling .build.json binds Markdown/DOCX hashes, heading/image/table counts, fonts, layout, toc_heading_count, and `BUILT_RENDER_AND_VISUAL_QA_REQUIRED`. Before finalization toc is `native_toc_h1_h2_requires_field_update`; afterward `verified_native_toc_h1_h2`. heading_count includes levels 1–3 and differs from TOC count. Build success is not delivery acceptance; receipts stay internal.

## 3. Fonts and figures

English defaults use Arial; verify availability and receiving-system compatibility/licensing, selecting another actual font when appropriate. Multilingual documents need suitable coverage. Do not hardcode a machine's font path.

The builder sets body/headings/TOC/footer font attributes and removes conflicting theme fonts; explicit settings still do not prove renderer discovery. If installed fonts render blank, examine renderer font search. A run-local fontconfig file supplied through FONTCONFIG_FILE may help; do not alter global configuration or write local paths into the skill. Build receipt retains font_availability=NOT_VALIDATED until actual inspection.

Fix missing glyphs/boxes/blank regions/substitution pagination by font repair or font choice followed by rebuild/render. Split dense diagrams, preserve captions/arrows/boundaries, and identify presentation-tool screenshots. Do not solve density by making text unreadable.

## 4. Final delivery gate

Actually render the latest DOCX to every page image. Codex uses documents' render_docx.py with bundled LibreOffice; generic uses section 7. Finalize fields/pagination before review; old images cannot validate a changed document.

Inspect all pages for text, font, images/captions, table continuation/repeated headers, heading separation, page numbers/contents, mixed paper sizes, blanks, and links. Check agreement with calculations/scope/external conditions. Reorganize long cells/wide tables rather than shrinking excessively.

Record final DOCX hash, page count, inspected range, issues/repairs, and remaining gaps. Only complete readable final pages pass. Without rendering state “generated; layout acceptance pending.”

Deliver DOCX, Markdown, acceptance, and separate external assumptions. Keep sources/build records for continuation; QA PDF/PNGs, test fixtures, and logs remain internal.

## 5. Codex field update and rendering

1. Read the available documents skill; use load_workspace_dependencies to locate bundled Python, Node, override-bin, and the documents renderer. Paths are run arguments, not package constants. Follow host artifact-operation requirements.
2. Choose available fonts. Repeated --font-dir arguments may provide real directories; the finalizer makes fonts.conf/cache in this QA run only.
3. After build:

```sh
python scripts/finalize_word.py --docx output/v001/client/report.docx --output-dir output/v001/qa/word-final --renderer DOCUMENTS_SKILL_ROOT/render_docx.py --runtime-bin CODEX_BUNDLED_OVERRIDE_BIN --font-dir ACTUAL_LOCAL_FONT_DIRECTORY
```

Resolve uppercase placeholders yourself. Retain bundled renderer/soffice instead of silently using desktop LibreOffice.

The finalizer rebuilds native TOC entries from Heading 1–2, preserving the outer field, internal jumps, and PAGEREF page fields. It renders real PDF/PNGs, finds heading physical pages through PDF outlines/text, converts to body logical pages, writes field results, and renders again until stable (at most four iterations). This is actual rendered-page-based field-result rebuilding; it does not claim to call Word/UNO's update engine.

It checks visible TOC titles/pages/link destinations and continuous 9 pt body footers. Legacy builder PAGEREF contents retain their compatibility path. Arbitrary customer REF/SEQ/TOC templates are outside this finalizer's contract.

`.build.json.field_update.page_map` is body logical pages; physical_page_map is PDF pages. Method is native_toc_result_rebuild_from_rendered_heading_pages. Finalization records final hash, page count, last images/hashes, logs, and attachment checks; update receipts only after stability. On failure preserve QA, repair, rebuild from source, and use a new QA directory.

`FIELDS_UPDATED_VISUAL_REVIEW_REQUIRED` is not visual acceptance. Read every final image identified in word-finalization.json. Verify TOC/body agreement, readable text/tables/links, and no raw Markdown. After actual review create section 6's QA record with paths relative to the version root. Never mark PASS before inspection or ask the customer to update the TOC to finish this run.

## 6. Calculation/source/Word binding

```sh
python scripts/check_delivery.py --root project-output/v001 --markdown client/report.md --docx client/report.docx
```

Without QA this records BUILT_NOT_VISUALLY_VERIFIED. After actual inspection add `--qa qa/word-qa.json`. Required fields: docx_sha256, renderer, page_count, inspected_pages (1 through actual count), status=PASS, unresolved_issues=[], and page_images entries with relative path/sha256 for every page.

Checks bind final files/images, not visual judgment. delivery-index.json classifies client paths while build receipts remain internal. Directory placement alone does not establish disclosure suitability: review contents. Existing delivery index is not overwritten; use a new version for a new report.

Native TOC uses dot leaders/right-aligned page fields/clickable entries, never hand-typed dashes/spaces or old pagination. Keep updating to stable final pages after content changes.

## 7. Generic local Word path

Claude Code and other local agents need no Codex-specific tools. Locate Python and LibreOffice and verify [requirements](../scripts/requirements-word-generic.txt). Build using section 2, then:

```sh
python -X utf8 scripts/finalize_word.py --renderer-mode generic --docx output/v001/client/report.docx --output-dir output/v001/qa/word-final --renderer scripts/render_word_generic.py --soffice /actual/path/to/soffice
```

On Windows the executable may be `C:/Program Files/LibreOffice/program/soffice.exe`, but inspect actual installation first. Optional --font-dir takes real run-local discovery paths. Generic needs no runtime-bin; Codex keeps its original contract.

render_word_generic.py uses an isolated temporary LibreOffice user profile, converts actual DOCX to PDF, and renders all page-N.png with pypdfium2. It does not overwrite the user's Office profile and retains PDF/logs/images. The shared finalizer checks TOC/pages/links/hashes until convergence. Its result still requires every-page inspection and QA.

Standalone renderer diagnosis:

```sh
python -X utf8 scripts/render_word_generic.py output/v001/client/report.docx --output_dir output/v001/qa/render-only --soffice /actual/path/to/soffice --emit_pdf
```

It does not estimate prices or declare visual success. Missing programs/libraries/fonts or unverified outlines/TOC leave logs and partial artifacts with explicit incomplete status. Repair supported causes, use new QA directories, and never remove acceptance requirements to pass.

## Font availability and final PDF verification (2.2)

The builder's font_availability=NOT_VALIDATED means DOCX generation did not verify fonts. The standalone scripts/check_pdf_fonts.py requires pypdf and pdfplumber and supports codex/generic paths. Discover actual tool/interpreter locations and use the intended fonts:

```sh
python -X utf8 scripts/check_pdf_fonts.py --preflight --font "Arial" --output qa/font-preflight.json
python -X utf8 scripts/check_pdf_fonts.py qa/final.pdf --font "Arial" --output qa/pdf-fonts.json
```

Replace examples with the actual final PDF and new internal report locations. Preflight returns AVAILABLE/MISSING/UNVERIFIED; registration does not prove renderer selection. PDF inspection normalizes subset prefixes, common style suffixes, and family aliases, recording actual text fonts, pages, and resource embedding. Unembedded standard fonts are not automatically a mismatch; the report preserves evidence and limits.

Only for an already accepted substitution add --allow-substitute "Arial=Liberation Sans", using actual environment names. Substitution flags only declare an acceptable result; they do not make the renderer use that font. The right-hand name must be a font that actually appears in the final PDF. What the renderer actually selected is decided by used_fonts in the final PDF (a first run's pdf-fonts.json shows it). Fontconfig's fc-match only reflects generic matching under the current configuration; renderers apply their own replacement rules, so it is an aid only, and Windows does not include it by default; availability depends on installed tools. Distinguish discoverable from selected: installing a font or passing --font-dir only makes a font discoverable, and the document still uses the fonts its styles request. To switch to a font, specify it through --body-font, --heading-font, or the document styles, then rebuild from the source, render, and inspect again. PDF states are MATCHED, SUBSTITUTION_ACCEPTED, MISMATCH, or UNVERIFIED (such as image-only PDFs). Exit codes are 0 for matches/accepted substitutions, 2 for mismatch, 3 if unverified. None establishes visual acceptance: explain/review unobserved expected fonts, pages without extractable text, image text, and missing glyphs. When a substitute font is accepted, page review must also explicitly check bold, italic, and glyph shapes: a substitute may lack the needed weight or style, and the renderer may synthesize it or fall back to regular while the font-name check still passes. The report binds the final PDF hash; rerun after PDF changes.

finalize_word.py now checks fonts after final pagination converges and binds font-preflight.json/pdf-fonts.json into receipts. A mismatch or unverified result preserves reports and stops a success claim; repair and rebuild into a fresh QA directory. Pass an already accepted substitution through --font-substitute "Arial=Liberation Sans", never merely to make a check pass.
