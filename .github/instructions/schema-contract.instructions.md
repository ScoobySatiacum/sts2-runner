---
name: schema-contract
description: "Use when designing, reviewing, or implementing the SQLite schema, JSON-to-relational mappings, migrations, or related parser and repository tests."
applyTo: "**/*schema*.sql, **/M02-schema-contract.md, **/src/sts2/parse/**, **/src/sts2/storage/**"
---

# Schema and Mapping Guidance

- Read [M02-schema-contract.md](../../tickets/milestones/M02-schema-contract.md), [TECHNICAL_SPECIFICATION.md](../../tickets/TECHNICAL_SPECIFICATION.md), and [ADR-001-library-boundaries.md](../../tickets/decisions/ADR-001-library-boundaries.md) before changing the data contract.
- Compare the current legacy behavior with the planned normalized contract. Do not silently treat the existing DataFrame shape or SQL file as the final architecture.
- Inspect all representative files under `tests/samples/` before deciding that a field, collection, or relationship is universal.
- Preserve source data and ordering. Arrays need an explicit ordinal; nested dictionaries need a lossless key/value or property representation; unknown and version-dependent values need a documented preservation path.
- Put `run_id` on every run-owned table. Give repeated child entities stable parent-aware identifiers and make parent relationships explicit with foreign keys where SQLite supports them.
- Define nullability, empty collection behavior, SQLite types, uniqueness, and duplicate semantics as part of the contract rather than leaving them implicit in parser code.
- Keep schema creation, migrations, and SQLite writes inside the storage boundary. Parsing should emit explicit normalized rows without opening a database; CLI and GUI code should consume services instead of issuing SQL.
- Add focused contract tests before implementation changes. Cover single-player and multiplayer samples, optional or empty sections, ordering, foreign-key enforcement, and representative unknown values.
- Validate with the narrowest relevant pytest target first, then the full test suite and `uv run ruff check src tests` when Python files change.
- Link to the existing milestone and technical documents instead of duplicating their full content in new instructions.
