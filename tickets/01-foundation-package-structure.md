# Ticket 01: Establish the library package structure and architectural contracts

## Goal

Create a library-style package structure so that the project can be composed into reusable parts without requiring a single monolithic execution path.

## Scope

- Define the Python package layout under src/sts2/
- Separate parsing, models, storage, querying, reporting, and presentation concerns
- Establish a stable dependency direction
- Document the public interfaces and their responsibilities

## Proposed package layout

- src/sts2/
  - __init__.py
  - models/
    - run.py
    - player.py
    - map_point.py
    - choice.py
    - modifier.py
  - parse/
    - loader.py
    - normalizer.py
    - schema_contract.py
  - storage/
    - sqlite_repository.py
    - migrations.py
    - schema.py
  - queries/
    - run_queries.py
    - analysis_queries.py
  - reports/
    - report_service.py
    - export_service.py
  - cli/
    - __init__.py
    - ingest.py
    - report.py
  - gui/
    - api/
    - templates/
    - static/
    - views.py

## Design constraints

- The package must support composition of multiple components into a complete workflow.
- The storage layer must be independent of the UI layer.
- The query layer must be independent of the parser.
- All user interfaces must consume the same library interfaces rather than reach into parsing internals.

## Implementation notes

- Use dataclasses or Pydantic-style internal models for canonical row data.
- Avoid exposing pandas objects as the primary internal contract.
- Keep a clear boundary between raw parse output and persisted database rows.
- Use SQLite as the storage source of truth, while allowing temporary Polars DataFrames for analysis.

## Acceptance criteria

- The package has distinct modules for ingestion, storage, querying, and presentation.
- No code path depends on CLI or GUI code for basic ingestion or storage operations.
- The package can be imported and used in tests without requiring UI startup.
- The public interfaces are documented in a minimal architecture note.

## Test-first approach

- Add a failing test establishing the package import contract.
- Add a failing test proving the core service boundaries are importable and independent.
- Add a failing test asserting that the repository layer does not depend on CLI code.

## Definition of done

- The package structure exists and matches the planned responsibilities.
- The architecture README or developer note reflects the dependency direction.
- The next tickets can be executed without reworking the package shape.
