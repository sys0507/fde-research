# Word Format and Delivery Check

## Format priority

The client's specified template and standards come first. Where there is no template, the following business defaults may be used; state in the production notes that they are the project's default styling, not a legal or mandatory national standard.

|Element|Default and handling|
|---|---|
|Page and margins|A4; roughly 2.5 cm on all four sides; use a separate landscape section for wide tables or large figures where genuinely needed|
|Body text|A serif body face (SimSun for Chinese text), 12 pt, about 1.5 line spacing; 0 pt space before, 6 pt after, with a consistent first-line-indent or space-between convention|
|Headings|Use Word's named styles; a sans-serif face (SimHei for Chinese text); level 1 at 16 pt, level 2 at 14 pt, level 3 at 12 pt; consistent numbering levels|
|Tables|10.5–12 pt; clear header row, repeated on each page for tables that break across pages; column widths allocated by content, not compressed into a page of dense text|
|Figures and captions|Separate original images keeping their proportions; figure number, feature/scenario ID, and nature stated clearly; captions about 10.5 pt|
|Header and footer|Concise project/document name, version or status, and page number; cover set per the template|
|Table of contents|Generated or refreshed from the real heading levels; check that the final page numbers match the actual pages|

The fonts used must actually be installed and available to Word or the renderer; check the CJK font declaration and the Latin font setting separately. If font substitution occurs, state the actual substitute name and check the layout; never conclude that a font is in use just by reading the style code.

## Image placement

For the same task, insert "before → after → result" separately, with their own figure numbers or sub-figure numbers, titles, and explanations. Prefer presenting each at body-page width on its own; where a larger size is needed, put it on its own page or use a landscape page. Do not stitch ultra-wide long images, and do not shrink an image to illegibility just to force it onto one page.

Text the reader has to check must be legible; a complex desktop interface may use a separate landscape page, or keep the full image while adding a detail crop. Crops must come from the real original image and keep their explanation; never redraw factual content. If it is still illegible in print, adjust the layout and the number of images chosen — a downloadable high-resolution image is not a substitute for the explanation the printed page needs.

Each image set states the operator, the task, and the key change shown. Label prototypes consistently as "requirement prototype / target process illustration"; for a longer-term scenario, state its assumed conditions. A complete image catalog can be a companion appendix, while the body keeps the images required to settle scope and responsibilities.

## Generation and real rendering

Generate the `.docx` with the available document tooling; in a supporting environment, open it or convert it to PDF or page images, then check the actual pages. Save the final version used for checking; never use an older rendering of changed content to prove the new version passes.

The check covers: cover and table of contents, headings of each level, pages mixing figures and text, the longest table and where it breaks across pages, the appendix, and the last page. Check mechanically for embedded images, complete body text, the number of figures and tables, and the targets of their references; check visually for fonts and layout. After fixing problems, re-render the affected files — there is no need to redo unrelated ones.

- Are the table of contents and page numbers correct, and do the page-number fields display rather than appear blank?
- Is a heading stranded at the bottom of a page, or a table header left alone on its own page?
- Are table cells truncated or past the margin, and does line wrapping break readability? If preventing row splitting causes the table to overflow the page, split it into separate tables instead.
- Are images distorted, is their text too small, or are they separated from their explanation? Are the before and after images still distinguishable?
- Is there any leftover path, placeholder, garbled text, broken external link, or internal production instruction?
- Does the Word file contain the complete body and the necessary appendices, consistent with the final source draft in version, scope, numbers, and captions?

If the work is used for teaching, screenshots should come from the real skill files, a real execution record, or an actual Word/PDF rendering. Next to the screenshot, explain what is being read at that point, why it is written that way, and how to check it next. Never compose a software window to impersonate an execution process.

## Human review checklist and status

On delivery, keep the following items for a human to check; do not pre-fill them as "passed":

1. Are the business facts, people's duties, document statuses, and sources correct?
2. Do the phase 1 scope, conditional capabilities, and later exploration match what was discussed?
3. Does the AI/human split retain the necessary approval, correction, and handover?
4. Are the proposed targets and assumptions reasonable, and have any been mis-written as hard commitments?
5. Are the data boundaries and the technical conditions still to be verified complete?
6. Are the proposal prototypes, the already-built system, and long-term demonstrations clearly distinguished?
7. Are the Word file's content, formatting, figures and tables, and open items ready to be reviewed on their own?

The statuses run in order: agent output and self-check complete → author / project lead has completed human review → requesting-party review and confirmation. Record what actually happened at each step; completing the previous step does not stand in for the next. The human review here is about the file's readiness for review; it must never be described as the client having agreed to the scope, granted business operating rights, or approved development.
