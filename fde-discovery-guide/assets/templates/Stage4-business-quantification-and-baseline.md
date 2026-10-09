# Stage 4: Business Quantification and Baseline Establishment

## 1. Quantification goal and evaluation scope

State which identified problems need quantifying and why these metrics can serve as a reference for future improvement. Do not assume that all current elapsed time or effort can be eliminated by AI. Keep the data period, observation cutoff, sample/population, and business boundary consistent across this round.

## 2. Metric definitions

Reference the metric definition card for each metric, stating its business meaning, unit, numerator and denominator, start and end events, completion condition, and data source. Avoid giving only a metric name and a formula, leaving the reason for choosing it invisible.

## 3. System data and on-site observation

- **System export**: show the role and system the file came from, a preview of the actual data, the field mapping, the joins, and the check results, keeping the business counts before and after filtering.
- **On-site shadowing**: show the person observed, the task, the start/pause/resume/end points, and the actual effort; distinguish live timing, after-the-fact backfill, and spoken estimates.
- **Data conditions**: state the missing values, duplicates, unfinished cases, time and unit problems, and the handling adopted; items whose materials were never obtained remain not measured.

## 4. Computation process and results

For each metric, state the concrete formula and one traceable example, linking to the input version, the script, the actual run, and the result file. Count system history and on-site observation samples separately; never stitch a denominator across samples.

## 5. Per-metric analysis

### [Metric ID and name]

- **Baseline result**: [The actually computed value, unit, sample size, scope, and period.]
- **Chart and detail**: [The chart generated from the result, with links to source and detail.]
- **Analytical conclusion**: [Explain the specific burden and the evidence for its cause; explicitly hold back any attribution the data cannot support.]
- **Use in later evaluation**: [The definition and observation conditions that must be kept for a future comparison, and the benefits that cannot be inferred directly.]

Repeat the structure above for every metric. Finally, summarize the conclusions sufficient to support a priority judgment together with the measurements still missing; do not let one summary table replace the per-metric analysis.
