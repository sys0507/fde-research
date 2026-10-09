# Baseline Calculation Run Record

Run ID: [content]; case: [content]; status: [not started / running / succeeded / failed / cancelled]; start and end time: [content].

## Snapshot of inputs and definitions

| Input asset ID | File relative path / version / hash | Encoding and how confirmed | Original row count | Filtered and included counts this run | Related metrics |
| --- | --- | --- | --- | --- | --- |
| [Actual input] | [Recorded at execution time] | [e.g. GBK; source statement / file declaration / sample check; "n/a" for binary formats] | [Actual] | [Actual] | [Metric ID and definition version] |

Record the field mapping, deduplication, missing values, unfinished business, time zone/unit handling, and join cardinality handling; keep zero denominators separate from unmeasured values. The counts before and after cleaning must be comparable — do not save only the final result.

## Execution method

- **Script**: [Actual relative file path].
- **Environment and dependencies**: [Actual versions or an installable dependency file].
- **Recompute command**: [A genuinely runnable command with the case directory as the working directory, containing no machine absolute paths].
- **Output path**: [This run's directory].
- **Limits**: [Actual configuration such as execution timeout and memory].

## Results and charts

Register the actual value tables, result JSON/CSV, charts, and sanity checks only after a successful run; label each chart's metric, input version, and sample. On a failed run, keep the error and the direction for fixing it; never fill the table with expected values.

## Analysis documents and update impact

Record which documents and report versions use this run's results; mark them as pending recomputation when an input or a definition changes. Keep the necessary parts of old successful results and error information, and ensure the export contains no host credentials, no raw run logs, and no content from other cases.
