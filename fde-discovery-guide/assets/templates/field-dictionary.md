# Field Dictionary

This dictionary explains the fields in the data actually obtained; it does not presume that every enterprise has the same tables or fields. Use one section per file/data object, recording the source asset ID, the version, the row granularity, and the unique key.

## [Object or file name]

- **Source**: [Asset and actual path].
- **What one row represents**: [A business case, a document line item, an event, an observed action, etc.].
- **Primary key and joins**: [Unique key, foreign keys, and one-to-many / many-to-many relationships].
- **Data snapshot and refresh**: [Export date, business period covered, how it is updated].

| Original field name | Business meaning | Type / unit / time zone | Status or value range | Meaning of null | Relations / statistical use |
| --- | --- | --- | --- | --- | --- |
| [Actual field] | [Do not substitute a literal translation of the field name for an explanation] | [Actual constraint] | [Known values] | [Unknown is not zero] | [Use] |

## Statuses and business ID conventions

Explain each actual ID prefix and status value. Event time, entry time, approval time, payment time, and the like must not be conflated. Keep observed facts separate from field meanings still to be confirmed.

## Data quality and mapping decisions

Record duplicates, missing values, invalid values, failed joins, mixed units, and the handling proposed, noting whether it has been confirmed. Any standardized field used in the analysis must map to a real original field with the conversion rule preserved.
