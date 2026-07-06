# Rule: Source provenance

Every extraction must be traceable back to its source. Provenance is not
optional metadata — it is what separates a knowledge atom from a hallucination.

- **Every knowledge atom carries a source trace**: a file path, chunk/section
  reference, page number when genuinely available, DOI, or citation.
- **Never invent provenance.** If a DOI, page number, author, year, or journal
  is not present in the supplied material, record `"unknown"` or
  `"not reported"`. Do not fabricate a plausible-looking identifier.
- **Preserve links and DOIs for verification** so a human can check the original.
- **Duplicate and missing-field detection.** Flag duplicate sources and missing
  citation fields rather than silently guessing them.
- **Chunk-level traceability.** When text is chunked, keep enough reference
  (section, page, or chunk id) that a reader can locate the passage.
- **Do not misrepresent the source.** Extraction summarizes and structures; it
  must not distort, replace, or overstate the original.

If provenance cannot be established, mark the atom as requiring human review
rather than presenting it as verified.
