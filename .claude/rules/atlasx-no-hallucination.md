# Rule: No hallucination

Fabricated detail is the most damaging failure mode for a research tool. A
confident wrong answer is worse than an honest `"unknown"`.

- **If it is unknown, say unknown.** Use `"unknown"` or `"not reported"` for any
  field you cannot support from the supplied material.
- **Never invent** page numbers, DOIs, authors, journal names, dates, sample
  sizes, statistics, quotations, or findings.
- **Do not infer specifics that were not stated.** You may hypothesize a
  mechanism as inference — but label it as inference, and never present it as a
  reported result.
- **No phantom citations.** Do not cite a paper, dataset, or figure that is not
  present in the input.
- **Prefer precise atoms over broad summaries.** Several narrow, well-sourced
  atoms are safer than one sweeping claim.
- **Mark low-confidence inferences for human review** instead of asserting them.

If producing a complete-looking output would require inventing detail, produce a
smaller, honest output instead.
