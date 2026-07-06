# Source Routing Architecture

AtlasX Discovery Notebook introduces source routing so general documents can be
processed without forcing every source through a research-paper pipeline.

Routing is deterministic first. It does not require an LLM.

## Routes

- `research`
- `general`
- `learning`
- `strategic_brief`
- `source_collection`
- `unknown`

## Source Kinds

- `research_article`
- `thesis_dissertation`
- `literature_review`
- `report_whitepaper`
- `book_chapter`
- `essay`
- `policy_document`
- `legal_document`
- `curriculum_lesson`
- `transcript`
- `meeting_notes`
- `website_article`
- `general_document`
- `unknown`

## Signals

The router considers:

- `metadata.source_type`
- `metadata.tags`
- DOI presence
- journal presence
- abstract presence
- `route_hint`
- filename and title keywords
- text structure and headings

Research signals include DOI, journal, abstract, methods, results, discussion,
study, sample, participants, findings, statistically significant, literature
review, experiment, clinical, in vitro, in vivo, and dataset.

Learning signals include learning objectives, lesson, chapter, quiz, students
will, key terms, and curriculum.

Strategic brief signals include policy, strategy, stakeholder, recommendation,
risk, implementation, budget, operations, proposal, and decision.

The general route is the fallback when no specialized route threshold is met.

