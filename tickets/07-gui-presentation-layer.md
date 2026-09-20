# Ticket 07: Build the GUI presentation layer using FastAPI or Flask

## Goal

Create a separate GUI presentation layer for interactive reporting, while keeping the business logic in the library.

## Scope

- Choose either FastAPI or Flask as the web presentation stack
- Expose HTTP endpoints for report generation and analysis
- Provide a browser-based interface for viewing run summaries and cross-run analysis
- Keep the GUI separate from the storage and parsing layers

## Requirements

- No Django usage.
- The GUI must consume the library query services rather than direct SQLite access.
- The user interface must be optional and not required for core ingestion or analysis.
- The current codebase should remain library-first.

## Preferred stack

Use FastAPI if the project wants a clean typed API and modern docs. Use Flask if the team prefers lower deployment complexity. The implementation should be chosen based on maintainability and deployment simplicity.

## Proposed routes

- GET /runs
- GET /runs/{run_id}
- GET /reports/summary
- GET /analysis/character-win-rates
- GET /analysis/common-relics

## Acceptance criteria

- The GUI can render a summary report for a selected run.
- The GUI can render aggregate analytics over the full dataset.
- The backend uses the same query layer as the CLI.
- The GUI is optional and does not change the library’s portability.

## Test-first approach

- Add failing tests for the HTTP report endpoints.
- Add failing tests for invalid run_id and missing data handling.
- Add failing tests for a successful aggregate analysis response.

## Definition of done

- The GUI can be run separately from the CLI.
- The front-end is clearly separated from the domain logic.
- Both presentation layers share the same data contracts and service interfaces.
