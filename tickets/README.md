# Sts2 Runner Engineering Plan

This directory tracks the phased refactor of the project into a library-style package with clear boundaries, a normalized SQLite schema, and distinct presentation layers for CLI and GUI use.

## Objectives

- Preserve all data from each .run file in SQLite in a normalized 1:1 form.
- Keep SQLite as the persistence layer for the canonical dataset.
- Split responsibilities into reusable library components.
- Support both reporting and data analysis through the same underlying domain model.
- Provide two distinct user-facing presentation layers:
  - CLI reporting that can be saved to file.
  - GUI reporting using a web application based on FastAPI or Flask.
- Use pytest and TDD throughout the engineering plan.

## Architectural principles

1. SQLite is authoritative storage.
2. Parsing, normalization, persistence, analysis, and presentation are separate layers.
3. The library exposes composable services, not a single monolithic runner.
4. The schema captures every raw field from each run file without lossy transformation.
5. Polars is used for analytical transforms after data is loaded from SQLite.
6. The database schema is versioned and migration-aware.
7. Each task is implemented in a test-first workflow.

## Execution phases

- Phase 1: package structure and contracts
- Phase 2: normalized schema and ingestion contract
- Phase 3: persistence and repository layer
- Phase 4: query and analysis layer
- Phase 5: CLI presentation layer
- Phase 6: GUI presentation layer
- Phase 7: integration, regression, and release readiness

## Ticket index

- [01-foundation-package-structure.md](01-foundation-package-structure.md)
- [02-normalized-db-schema.md](02-normalized-db-schema.md)
- [03-ingestion-parser.md](03-ingestion-parser.md)
- [04-sqlite-repository.md](04-sqlite-repository.md)
- [05-analysis-query-layer.md](05-analysis-query-layer.md)
- [06-cli-presentation-layer.md](06-cli-presentation-layer.md)
- [07-gui-presentation-layer.md](07-gui-presentation-layer.md)
- [08-test-strategy-and-tdd.md](08-test-strategy-and-tdd.md)

## Dependencies and sequencing

The work is intentionally staged. The first two tickets define the architecture and schema model that all later work depends on. The remaining tickets can be executed in parallel once the contracts are stable, but they should still be validated against the same underlying schema and test suite.
