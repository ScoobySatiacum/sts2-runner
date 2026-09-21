# ADR-001: Library-first package boundaries

- Status: accepted
- Date: 2026-09-20
- Related milestones: M01, M03, M04, M05, M06, M07

## Context

The original implementation combines file parsing, data transformation, SQLite writes, and reporting concerns. The refactor must support reusable library behavior, a CLI, and a FastAPI GUI without duplicating business logic.

## Decision

Use a library-first architecture with separate parsing, normalization, storage, query, analysis, report, CLI, GUI, and service boundaries. Presentation layers call library services and do not own SQL, schema creation, or raw-file parsing.

## Alternatives considered

- Keep a single parser class and add more methods.
- Allow CLI and GUI modules to query SQLite directly.
- Use a single framework to own ingestion and presentation.

These alternatives make reuse and testing harder by coupling responsibilities that change for different reasons.

## Consequences

- More modules and contracts must be maintained.
- Each layer can be tested independently.
- The same query and service behavior can support CLI and GUI consumers.
- Changes to storage or presentation are less likely to force a parser rewrite.
