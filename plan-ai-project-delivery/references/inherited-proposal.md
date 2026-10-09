# Write from user estimates or an existing delivery proposal

Use when the user supplies price/time estimates or designates a historical proposal/workbook. Both modes still read business assets, readiness handoff/originals, and final technical design. This mode additionally inherits commercial estimates in Word, MD, PDF, spreadsheets, or calculation files; the agent extracts them without requiring user-created JSON. Preserve the selected plan, examine changes, and improve the report instead of automatically rebuilding the whole estimate.

## Adoption and analysis boundaries

“Use a similar project as a reference” permits re-estimation; “use this price and duration” or “improve this proposal” uses this path. The explicitly selected version takes priority over a later-dated unrelated file. A writing baseline is not customer approval or a signed contract.

Read the selected report/workbook and current business/design inputs in full. Extract scope/exclusions, personnel/reservation, packages/stages, pilot/support, price/tax/payment, development API/third-party fees, production/equipment boundaries, assumptions, and validity. Retain file/location, original review status, and adoption reason. Inherit the coherent set, not one price mixed with another version's dates/samples/support/API.

Identify unchanged scope, real changes, conflicts, and missing detail. Explain feasibility, cooperation, and acceptance without turning added prose into services. For material conflicts still deliver a conditional report under the original baseline plus affected items/options. Recalculate only explicitly authorized changes without overwriting the adopted baseline.

With only price/duration, preserve that granularity and identify missing costs/daily hours. Do not reverse-invent activities, rates, or model calls to hit a target. Reconcile available arithmetic/capacity/payments/dependencies using the original method; do not force historical data into the new estimator. Weekly checks are weekly, not daily validation.

Adopted API budgets remain funding reserves with original usage/price dates, not guaranteed consumption or caps. Without usage detail do not fabricate requests. Regenerating a document neither renews quote validity nor constitutes fresh vendor pricing. Internal cost/margin stays internal.

## Partial user estimates without a prior report

Save the conversation's supplied terms as a project input with date, provider role, meaning, and status. This can be a source without an existing proposal. “Write using this price/time” is a designated baseline; “try to fit this budget/time” is a feasibility target, not proven feasibility.

Inherit only supplied fields and use business/design inputs to add phases, scope, human/agent work, acceptance, and cost boundaries. Label any new estimate as this run's assumption with basis. Do not copy an example API allowance/rate/margin. Report conflicts rather than reverse-engineering false worksheets. Internal records may honestly consist of known basis, missing detail, and added assumptions instead of claiming detailed costing.

## Freeze the baseline

Prepare `work/baseline-input.json` as a numerical/source index, not a second estimator:

```json
{
  "adoption_instruction": "The user's instruction identifying the version and permitted changes",
  "sources": [{"id": "proposal", "path": "inputs/adopted-proposal.md", "title": "Delivery proposal", "status": "Pending customer review"}],
  "facts": {
    "service_price": {"value": "100000.00", "display": "100,000.00", "unit": "CNY excluding tax", "source_id": "proposal", "locator": "Service quotation section", "visibility": "client", "status": "adopted_estimate"}
  },
  "scope_review": {"conclusion": "Actual comparison conclusion", "changes": [], "conflicts": [], "missing_details": []},
  "checks": []
}
```

Values illustrate structure, not a default quote. Facts retain consequential adopted values; visibility is client/internal, status adopted_estimate/confirmed/provisional. Display changes separators/precision without changing value. Source paths are relative to this input root. Original models/results/decisions may be sources; read-only snapshots preserve them.

Declare available arithmetic checks, e.g. `{"label":"Service line total","operation":"sum","inputs":["part_a","part_b"],"expected":"service_price","tolerance":"0.01"}`. Operations: sum, product, difference (two inputs), percentage (first/second × 100). Arithmetic checks do not prove credible estimates or correct extraction.

```sh
python scripts/inherit_baseline.py adopt --input work/baseline-input.json --source-root INPUT_ROOT --output output/v001
python scripts/inherit_baseline.py check --root output/v001
python scripts/inherit_baseline.py render --root output/v001 --template internal/report-source.md --output client/report.md
```

Adopt writes baseline.json, baseline-check.json, manifest, and internal original snapshots and refuses existing versions. Use tokens such as `{{baseline.service_price}}`; internal facts cannot enter client via tokens. Follow [report writing](report-writing.md)/[delivery contract](delivery-contract.md), reconciling key numbers to originals. Render binds report, values, and hashes but cannot judge every handwritten number. Appendices use this baseline, not new-estimate results.

Follow [Word delivery](word-delivery.md). Delivery checks recognize inheritance without requiring historical workbooks to contain new model fields. Customer report/acceptance/assumptions and internal cost/assumptions are still required; missing cost detail is stated honestly. Explain what was inherited, newly analyzed, and unresolved.
