# Architecture diagrams and presentation

## Align content first

Describe components, responsibilities, paths, deployment, authority, and recommendation status before creating editable sources. Existing choices remain valid; no node-by-node approval is required.

Provide at least one overview, adding execution, knowledge/model, deployment, or development-isolation views when useful. Do not prescribe four diagrams. Nodes explain role/technology; edges distinguish actual call/data directions, reads, writes, publication, and asynchronous delivery. Proposed services, external systems, humans, and resource states match the report.

Keep readable density through separate views, notes, or details rather than tiny text/decorative complexity. Do not mix SDK, deployment process, database, and business responsibility arbitrarily at one level.

## Standard and enhanced paths

New projects default to `diagram_profile: standard`: Mermaid, Graphviz, draw.io, or editable SVG appropriate to the environment, plus actual rendered PNG/SVG and consistency/readability records. Word embeds actual PNG/JPEG. Mermaid code without rendered/viewed output is incomplete. Interactive HTML is optional and must state actual capabilities.

Use `archify` when requested or continuing that contract. Retain its full enhanced requirements below. Missing Archify does not silently downgrade the contract; deliver partial work or record an explicitly scoped change to standard without claiming Archify completion. Both paths require actual visual review and clear directions, human roles, and boundaries. See [manifest roles](run-contract.md).

## Installed Archify

Locate its actual skill, read SKILL.md and the relevant/current schemas/examples. Follow its candidate, validate, deliver, visual-check, and export contracts. Some versions support this pattern:

```sh
node "$ARCHIFY_DIR/bin/archify.mjs" validate architecture specs/overview.json --quality showcase --json
node "$ARCHIFY_DIR/bin/archify.mjs" deliver architecture specs/overview.json public/overview.html --quality showcase --json
node "$ARCHIFY_DIR/bin/archify.mjs" visual-check public/overview.html --json
```

Verify current syntax first; these do not freeze future schemas/receipts. Distinguish structural validation, browser checks, and actual screenshot review. Basic validation is not showcase acceptance; automated measurements are not visual inspection.

Preserve successful deliver receipts and source/HTML hashes. Failed commands may leave old HTML; never present old captures as new success. Static images come from the final successful version and enter report/manifest. Use a separate A3 landscape page for dense printable diagrams without stretching; simple diagrams may fit A4.

## Interactive explanation

Reuse existing search, zoom, node details, theme, and relation tracing. A lightweight multiview portal must not alter accepted standalone HTML. Actual browser captures illustrate the presentation tool, not completed business software.

Check real desktop readability, overflow, and main interactions at the tool-required viewport. Do not remove permissions/domain conditions to fit the first screen.

## Serving

Standalone HTML normally opens locally. Start a presentation server only within actual requested scope. Explicit LAN/no-password requests already authorize that scope; another project's authorization does not transfer.

Serve a dedicated public folder containing selected HTML/images/required CSS/JS, never the project root. Internal conditions, originals, Word, credentials, and debug logs are excluded by default. Prepare a suitable presentation version for its audience if diagrams contain restricted detail.

The helper allowlists paths and rejects directory listing, unknown routes, escaping symlinks, and writes. Example `public-files.json`:

```json
["index.html", "overview.html", "exports/overview.png", "exports/overview.svg"]
```

```sh
python "$SKILL_DIR/scripts/serve_diagrams.py" --root "$RUN_DIR/architecture/public" --allowlist "$RUN_DIR/architecture/public-files.json" --host 127.0.0.1 --port 8925
```

Use `0.0.0.0` only for authorized LAN scope. Choose a free port without stopping unrelated services. Use a host-supported controlled background session, recording its PID/session and stop command; no hardcoded machine IP in portable scripts.

Verify localhost and current LAN-IP URLs as applicable, actual diagram/image responses, and 404 for nonallowlisted internal paths. Binding and accessing the LAN IP on this machine proves local routing, not access from another device; report the observed scope. Stop only this run's service and check its port release. This skill does not start a business backend automatically.

## Missing dependencies

Use actual standard tools when selected. If Archify is unavailable, preserve specs/text and state the missing dependency; Mermaid output cannot be labeled Archify. Missing static rendering/browser evidence remains an explicit gap. Successful partial artifacts remain useful without claiming the complete package.
