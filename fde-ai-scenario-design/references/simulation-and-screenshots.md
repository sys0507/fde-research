# Simulated interfaces and browser screenshots

## Define the action behind each image

Identify the operator, task, object, common starting point, and information cutoff. Then identify the original medium, proposed information/actions, and concrete result after the main action. Text and images together express input, action, feedback, and handoff.

The before-screen shows source-supported forms, files, messages, or lists. Use side-by-side windows or successive pages for multiple media. Do not present manually assembled conclusions as an existing automatic panel. If the original layout is unknown, reconstruct the business medium and explain that in the simulation shell/caption.

The after-screen uses consistent navigation, identity, titles, and primary-action placement. Choose structure by task: sourced question answering, original plus checklist for review, differences for correction, lists for plans/queues, stateful records for execution. AI is part of the assistance, not a mandatory label on every page.

## Make it usable software

A reasonable starting point is a 1600×1000 logical desktop viewport at pixel ratio 2; adapt to the project and keep before/after equal. Suggested sizes: body 13–15 px, helper labels 11–12 px, titles 22–28 px. Use restrained neutral backgrounds, one primary color, clear borders, and consistent state colors.

Keep identity, current module, object, key fields, and main action visible. Show only relevant and authorized information. Put teaching commentary, assumptions, and comparison summaries in captions or outside the business panel. Avoid decorative illustrations, fictional charts, and inert controls presented as implemented services. Density follows the task; split evidence/result pages instead of making text unreadable.

The [HTML/CSS template](../assets/screen-template.html) is an editable starting point, not a universal UI standard. Add task-specific components or implement directly.

## Results follow an actual local action

Perform the after-screen's main action before capturing the result. “View plan source” opens the plan and status; “Save correction draft” creates a draft retaining the original version. A generic toast or heading change is insufficient.

Local teaching data/state is enough; enterprise interfaces are not required. Keep future assumptions visible and simulated success separate from real approval. Preserve the person/object; another role's subsequent action is not the current operator's result.

## Authenticity and review

Use an available browser tool or Node.js/Playwright. Without one, deliver source HTML with capture and visual review pending. Do not replace captures with image generation. Diagnose module/browser/path/page failures and repair specifically.

Record scene ID, phase, relative page, viewport/pixel ratio, method, and checked status for each screenshot, for example `images/S08-before.png`, `S08-after.png`, and `S08-result.png`. Actually inspect key text, numbers, layout, buttons, and states before marking checked; automation cannot perform that judgment on your behalf.

Markdown embeds separate before/after/result images for report layout. HTML may compare side by side, enlarge images, and link to simulations. Embedded images support offline reading, but working demonstrations still need `screens/` and dependencies.

## Capture-script page contract

When using the bundled script, pages accept `?state=before|after|result`, expose current phase in `body[data-state]`, identify the system area with `[data-capture-root]`, the main action with `[data-primary]`, and changing business content with `#blocks`. The after-screen's main action reaches result. The script checks state transition, changed content, horizontal overflow, and runtime errors.

Custom pages may preserve these hooks or use task-specific browser operations. Hooks serve automation and are not business-interface content.
