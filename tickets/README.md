# Sts2 Runner Tracking

Active task tracking is managed through GitHub Issues and GitHub Milestones. This directory contains the durable roadmap, technical specification, milestone checklists, and architecture decision records.

The older ticket files are retained under [archive/](archive/) for historical reference and are not active work items.

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

## Canonical documents

- [ROADMAP.md](ROADMAP.md)
- [TECHNICAL_SPECIFICATION.md](TECHNICAL_SPECIFICATION.md)
- [ENGINEERING_PLAN.md](ENGINEERING_PLAN.md)
- [milestones/README.md](milestones/README.md)
- [decisions/](decisions/)

## Dependencies and sequencing

The work is intentionally staged. M01 and M02 define the architecture and schema model that later work depends on. Each active GitHub Issue should reference one task ID from the corresponding milestone checklist.
