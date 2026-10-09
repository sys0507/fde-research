# Metric Definition Card

Fill out one card per metric; the metric ID stays stable across documents and runs, and a change of formula creates a new definition version.

- **Metric ID, name, and definition version**: [content].
- **Business question it answers**: [Related problem ID and why it is worth measuring].
- **Meaning and unit**: [Ratio / cases / hours / person-minutes / currency amount, etc.].
- **Population, sample, and observation period**: [Selection method, start and end, cutoff point, statistical granularity].
- **Numerator**: [Which records meeting which condition; for a non-ratio metric, write "not applicable" and give the computed item].
- **Denominator**: [Which business enters the population; an empty denominator shows as "not applicable," never as 0%].
- **Formula, start/end events, and aggregation**: [Sum / mean / median / percentile, etc., with the time definition and the business calendar].
- **Data source and field mapping**: [Actual asset ID, columns, join keys, version].
- **Inclusion, exclusion, deduplication, and missing-value rules**: [State the reasons and the items pending confirmation].
- **How unfinished business is handled**: [Listed separately / observation window, etc.; never treated as completed].
- **Overlap and additivity**: [Whether categories are mutually exclusive and whether the parts can be summed].
- **Use and limits of interpretation**: [How it will be compared in future, and what it currently cannot prove].
- **Confirmation record**: [User confirmation time / an explicit existing policy basis / pending verification; never pass an automated step off as human confirmation].
