# One scenario source for screens, captures, and MD/HTML

The bundled scripts are optional. Agents may write pages/documents directly or use existing browser tools, while retaining the same content, delivery, and verification requirements. Build/overview scripts use Python 3.9+ and its standard library. Capture requires Node.js, Playwright, and installed Chromium. Inspect actual available dependencies, not agent branding.

## Layout and order

```text
delivery/
  scenarios.json
  screens/S01.html
  images/S01-before.png
  images/S01-after.png
  images/S01-result.png       # when needed
  capture-report.json        # bundled capture tool receipt
  scenario-comparison.md
  scenario-comparison.html
```

1. Write complete scenarios from originals and create each separate HTML/CSS page at its `demo` path.
2. Open pages in a browser, execute main actions, check results, and capture.
3. Inspect text, numbers, identity, time, and layout. Copy truthful capture records into `images` in `scenarios.json`. The capture script produces a receipt; it does not mark visual review passed or rewrite the JSON.
4. Render matching MD/HTML, then check reading interactions, links, and narrow screens.

```sh
python <skill-dir>/scripts/build_screens.py <delivery>/scenarios.json
node <skill-dir>/scripts/capture_screens.cjs <delivery>/scenarios.json
python <skill-dir>/scripts/render_scenarios.py <delivery>/scenarios.json
```

Skip the first command for directly authored pages. Capture resolves Playwright from the current working directory or `PLAYWRIGHT_MODULE`. A separate tooling directory may hold Playwright and Chromium; Node alone is insufficient. Scripts preserve existing outputs by default. Use `--overwrite` only after retaining wanted manual edits. They do not generate business judgments or narrative.

## Scenario JSON contract

Replace illustrative text with source-supported project content:

```json
{
  "title": "Business scenario comparison",
  "scope": "Current scope, evidence cutoff, and real or simulated material status.",
  "capability": {"browser_capture": true, "reason": "Local browser renders and captures the simulation."},
  "sources": [{"id": "A01", "label": "Business record", "path": "inputs/record.md", "nature": "Original project material; actual status retained"}],
  "scenes": [{
    "id": "S01", "title": "An operator completes a specific task",
    "status": "Before supported by evidence; after proposed for review",
    "functions": ["F01: candidate function"],
    "actor": "Main operator and next role",
    "trigger": "The event that creates the task",
    "starting_point": "Same object, cutoff, state, available and missing inputs",
    "pain": "The action where difficulty occurs and the resulting burden",
    "before": ["Obtain the material, review it, and record the response.", "Hand it to the next role; identify where work stops."],
    "after": ["Enter the input; show what the system reads and returns.", "Review, correct, or decide, then continue."],
    "result": "Where the final record/state is saved and who continues",
    "human": "What the named role still decides, approves, or executes",
    "exceptions": "Important exceptions and recovery",
    "change": "Work change, added review, and later measurement; no invented benefit",
    "questions": "Open conditions, or explain why none remain",
    "source_ids": ["A01"],
    "demo": "screens/S01.html",
    "result_required": true,
    "images": []
  }]
}
```

`demo` must be a real nonempty HTML file inside delivery, not the overview. `result_required` indicates whether a separate result capture is needed, usually for opening an original, generating a draft, or changing a process state. Before/after arrays follow real action order without a fixed count. IDs begin with a letter and contain letters, digits, hyphens, or underscores.

Source paths are real files/directories relative to JSON or HTTP(S) links. Sources may lie outside delivery; independent delivery needs the necessary originals or reachable locations. Scripts check local existence, not factual validity.

Legacy `mode: text/image` and `image_generation` are unsupported. With `browser_capture: false` still create pages and label missing captures. Same-version, verified browser screenshots may be reused with provenance.

## Optional UI structure

For `build_screens.py` add a `ui` object to each scene:

```json
{
  "product": "Operations workspace", "organization": "Example organization",
  "module": "Business module", "person": "Alex", "role": "Operator",
  "object": "CASE-01", "task": "Review this record",
  "basis": "Proposed workflow; simulation", "time": "Evidence cutoff",
  "navigation": ["Current module", "Processing history"],
  "states": {
    "before": {"title": "Original record", "subtitle": "Current entry", "blocks": [{"type": "facts", "title": "Record", "items": [{"label": "Status", "value": "Source-supported state"}]}]},
    "after": {"title": "Proposed review page", "subtitle": "Task workspace", "action": {"label": "View evidence", "target": "result"}, "blocks": [{"type": "facts", "title": "Review", "items": [{"label": "Evidence", "value": "A01"}]}]},
    "result": {"title": "Evidence", "subtitle": "Relevant original opened", "action": {"label": "Back", "target": "after"}, "blocks": [{"type": "document", "title": "Source excerpt", "paragraphs": ["Actual supporting excerpt or explicitly labeled paraphrase."]}]}
  }
}
```

Every block needs `type` and `title`. Optional `width`: `main` (8 columns), `narrow` (4), `wide` (12), otherwise 6. Choose widths for the task, not to fill a template.

| Type | Content |
|---|---|
| facts | `items: [{label, value}]`, optional item `full`/`emphasis` and block `note` |
| table | `columns: [names]` and `rows: [[cells]]` |
| document, text | `paragraphs: [text]` |
| messages | `items: [{from, text, time}]` |
| timeline | `items: [{title, text, state}]`; `state: wait` means pending |

Add custom review controls, sourced answers, or comparisons as needed. Retain [capture hooks](simulation-and-screenshots.md) for the bundled script or use custom browser actions.

## Capture records

After inspecting each image, copy its receipt into the scene's `images`, remove `scene_id`, and set `checked` truthfully:

```json
{
  "phase": "after", "status": "captured",
  "file": "images/S01-after.png", "page": "screens/S01.html",
  "viewport": {"width": 1600, "height": 1000, "device_scale_factor": 2},
  "caption": "The action and business state actually shown",
  "provenance": "Actual browser capture of local HTML/CSS simulation; not production",
  "checked": true
}
```

The script captures the system area, excluding the phase switcher, so pixel dimensions may be smaller than the full viewport. Use at most one entry per `before`, `after`, or `result`. `page` must equal `demo`; files must be actual PNG/JPEG/WebP inside delivery.

`reused` requires original provenance, page version, and review; illustrations are not screenshots. `unverified` or `checked: false` means pending review. Failure records use `status: failed` plus phase, caption, provenance, and reason, without invented image files.

## Status and checks

Overview exit 0 means required files/capture statuses are complete; 2 means missing/failed/unreviewed images but readable MD/HTML were still generated; 1 means structural/source/page errors or overwrite refusal. Capture exits 2 for failures, with details in its receipt. Exit status never replaces content/visual judgment.

Check MD relative image links, HTML image decoding, scene count/content, demo links, filtering/reset, navigation, zoom/close, narrow screens, and print layout. HTML embeds captures for offline reading. Share `screens/` for interaction and source originals as needed. Distinguish overview reading tools, scenario simulation, and complete prototypes.

## Configurable identity

`ui.product` and `ui.organization` use real or explicitly fictional project names. “Example organization” is not a default enterprise. Optional `ui.simulation_label` defaults to “Simulation · Not a production system.” A teaching case can say “Teaching simulation · Local demo”; it must not be empty or imply production. The label uses `textContent`, not interpreted HTML. The product initial is generic, not a supplier logo.
