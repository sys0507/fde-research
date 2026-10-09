# Complete Business Asset Delivery Rules

"Complete" means a complete inventory of **the materials needed and actually obtained for this investigation**, including supporting evidence not cited in the body. It does not require every original in the delivered bundle. It is not merely a list of typical samples, nor is it copying every company directory without judgment.

## Classify the material first, then build the inventory

Take stock of each material root directory the user provided and its subdirectories; counts from an old README must not be carried over as this round's result. Judge each classification independently by purpose. The list below is only a prompt for catching omissions — it does not require every industry to have identically named categories:

- the original request, roles and organization, interviews and on-site observation;
- current and related historical policies, business rules, and notices;
- business master tables, line items, ledgers, logs, states, and versions;
- documents, attachments, images, original messages, or other unstructured content;
- system descriptions, interface documentation and response samples, operating and access conditions;
- organized relations, mappings, sampling, timings, statistics, calculation scripts, and results.

For each item, state "acquired and deliverable / acquired but on-site access only or not copyable / known but not acquired / no access yet." Future business events, instructor answer keys, hidden evaluation criteria, and internal R&D instructions found in the material must never masquerade as business evidence obtained during the investigation; when found, list them separately with their purpose and the reason for exclusion, and keep them out of the learner's current fact set. Teaching simulations may be kept in a separate category with an explicit label.

## complete-asset-inventory.md

Open with the investigation scope, the data snapshot, the counting method, and a classification overview. Then list the following **file by file / actual data object by actual data object**; splitting into several tables for readability is fine:

| Asset ID | Name and category | Content and purpose | Source / providing role | Time and version | Acquisition and delivery status | Path in the package or controlled location | Quality / limitations |
| --- | --- | --- | --- | --- | --- | --- | --- |

For a large workbook, list its worksheets; for an interface, make clear what the interface documentation and what the sample each are. A zip archive cannot be a single row that claims its contents have been inventoried. An index provided with the original directory is an input, not a replacement for inspecting the actual files. Keep a separate entry for each version, and note the correspondence for duplicate files rather than silently dropping them.

At the end of the inventory, list unacquired assets and their impact separately; do not count them as "acquired." For material that was acquired but cannot be copied, state the delivery restriction honestly in the report and never work around access controls. Keep the originals that are genuinely needed; do not copy credentials, session logs, or unrelated personal data.

## field-dictionary.md

The body explains the core business objects and their relations, so a reader understands the business identifiers and states before reading the technical fields. The complete dictionary expands every field of the structured material acquired this round: source file/worksheet or interface, field name, type, business meaning, unit/enumeration, nullability, example, primary key/relation, time definition, and known quality issues.

When a field's meaning cannot be confirmed, write "to be confirmed"; describing the observed values is fine, but never guess the business semantics from a column name. For CSV, keep every actual header; for JSON, also describe the hierarchy, objects, and array structures; an interface sample only proves the structure of that sample and is not a complete interface contract or proof that it is callable in production. A long dictionary may be split into per-object subfiles, but the main dictionary must provide the full list of subfiles and navigation, not just the commonly used fields.

For images, PDFs, interviews, and other unstructured material, keep the full text/original plus a content index, date, and the objects involved; where no structured fields exist, do not invent a "field count." Fields extracted manually from an original are derived assets and must note the original's location and the extraction method.

## Copying and traceability

- Copy only necessary originals permitted for delivery. Group them by source root and preserve relative structure/content without same-name overwrites. Keep restricted originals or unnecessary personal fields in controlled storage; deliver necessary de-identified derivatives with source pointers instead. Store derived material separately; originals and derivatives can never substitute for each other.
- Before bulk copying, form an inclusion list according to the scope above and drive the copying from that list. User-provided material without restrictions may be copied directly on request; external reads or publication that require authorization are not part of this action.
- Preserve source paths, output paths, and the necessary version mapping. Convert in-package references to relative links; for retrieval, give the page number, table name, row primary key, or original location. Never write machine-specific paths into a reusable template.
- If the source material contains cross-referencing documents, include the referenced targets that are needed, or note in the inventory that they were not obtained; do not copy files in a way that leaves every original's links broken.
- Deliver calculation results together with their inputs and formulas/scripts; state the input snapshot, and recompute the affected metrics after a business fact changes. When running scripts, watch for the original project paths and output side effects; never blindly re-run against production data.
- Check the inventory against the actual output item by item. For copied files, a content hash can verify the copy is correct; this proves the content is unchanged and does not replace a judgment about business truth.

The final body presents the source categories, the important object relations, representative evidence, and the real limitations; the appendix keeps the complete inventory, necessary field descriptions, and permitted originals/derivatives or controlled-location pointers. The reading storyline and asset completeness must both hold: do not drown the business conclusion in giant tables, and do not drop assets for the sake of readability.

## Process measurement and personal data

Investigation and active human effort measurement explain process workload; they do not automatically authorize employee performance assessment or individual rankings. Prefer aggregation by process, task type, role, or suitable group. Do not collect names, contact details, personal identifiers, or individual activity trails unless needed for the current objective. Explain task complexity, role responsibilities, waiting, and active effort separately; unadjusted durations do not establish individual ability.

Use substitute identifiers for necessary detail, keep identity mappings in controlled locations, and avoid re-identification through small groups or narratives. Continue analysis already covered by authorization; new personal assessments, wider collection, external sharing, or access changes need corresponding explicit scope. Possession does not establish permission to publish. A complete asset index covers necessary materials, status, and controlled locations without requiring every original in the delivered bundle.

Preserve originals permitted to be retained. Keep de-identified/sampled derivatives separate and record source, transformations, and quality effects; never label a derivative as an unchanged original. Limit analysis/delivery to necessary fields, record existing project access/retention requirements, and do not automatically delete originals or claim complete anonymity.
