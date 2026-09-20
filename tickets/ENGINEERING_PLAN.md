## Engineering plan for the refactor

I have incorporated the decisions you confirmed:

- SQLite remains the canonical persistence layer
- The database must preserve all data from each run file in a normalized 1:1 schema
- The redesign should be broader and done in phases
- Reporting and data analysis are both first-class outputs
- The package should be library-first and reusable
- The UI should be split into two separate presentation layers
- The CLI should support saved output to file
- The GUI should be web-based with FastAPI, not Django
- pytest and TDD are mandatory
- Ruff is the required formatter and linter: 300-character lines, tab indentation with width 4, single quotes, and no magic trailing commas
- hatch-vcs derives package versions from Git tags; bumpver is not required
- the `refactor` branch is the working branch until the refactor is complete

The work is tracked in Obsidian-ready markdown tickets under:
- [tickets/README.md](README.md)
- [tickets/01-foundation-package-structure.md](01-foundation-package-structure.md)
- [tickets/02-normalized-db-schema.md](02-normalized-db-schema.md)
- [tickets/03-ingestion-parser.md](03-ingestion-parser.md)
- [tickets/04-sqlite-repository.md](04-sqlite-repository.md)
- [tickets/05-analysis-query-layer.md](05-analysis-query-layer.md)
- [tickets/06-cli-presentation-layer.md](06-cli-presentation-layer.md)
- [tickets/07-gui-presentation-layer.md](07-gui-presentation-layer.md)
- [tickets/08-test-strategy-and-tdd.md](08-test-strategy-and-tdd.md)

---

## Architecture direction

The refactor should move the project from a monolithic parser to a layered library with explicit boundaries:

- Ingestion layer: parse raw .run files into canonical row data
- Normalization layer: flatten nested structures into stable logical records
- Storage layer: write to SQLite with a normalized schema
- Query layer: expose reusable reports and analysis operations
- CLI layer: read from the library and emit saved output
- GUI layer: read from the same library and render web pages
- Analysis layer: use Polars for dataset-level transformation when required

This keeps the system maintainable while allowing all presentation layers to share the same domain logic.

---

## Phase plan

### Phase 1: Foundation and package contracts

Purpose:
- establish the reusable package structure
- define dependency direction
- prevent the UI and CLI from leaking into storage logic

Tasks:
1. Create the package layout under the src/sts2 tree for models, parsing, storage, queries, reports, CLI, and GUI.
2. Define the public interfaces for ingestion, persistence, and reporting.
3. Set a rule that all UIs consume the library layer, not the database layer directly.
4. Document the package dependency direction and responsibilities.

Deliverable:
- a clean library boundary with no parsing logic embedded in the UI

---

### Phase 2: Normalized schema and 1:1 representation

Purpose:
- preserve every relevant field from the raw .run file in SQLite
- remove lossy flattening from the database design

Tasks:
1. Map each top-level JSON section to a table or table family.
2. Define run-level, player-level, relic-level, map-level, modifier-level, choice-level, and nested property tables.
3. Use explicit foreign keys such as run_id, player_id, act_id, and choice_id.
4. Keep the schema normalized rather than storing entire objects as opaque JSON.
5. Decide which nested values are row-based versus value-based to maximize analysis without losing fidelity.

Deliverable:
- a normalized schema contract that defines how each .run file is represented 1:1 in SQLite

---

### Phase 3: Parse and normalize .run files

Purpose:
- replace the current monolithic parsing logic with explicit ingestion and normalization steps

Tasks:
1. Build a raw file loader that reads the .run JSON.
2. Validate the structure and required metadata fields.
3. Extract run metadata, player data, relic data, map history, and modifiers into explicit record collections.
4. Convert nested arrays into row-based outputs suitable for database insertion.
5. Ensure every row set includes stable identifiers needed to rebuild relationships later.

Deliverable:
- reusable parse output objects or row collections that are independent of SQLite and the UI

---

### Phase 4: SQLite repository and migration layer

Purpose:
- own all database lifecycle concerns
- enforce the schema and idempotent ingestion

Tasks:
1. Create the database schema from the contract.
2. Add repository methods for insert, replace, and batch ingest.
3. Enforce run_id uniqueness and skip duplicate imports.
4. Add migration support so the schema can evolve without breaking the codebase.
5. Validate that the repository is the only component allowed to write database rows.

Deliverable:
- a clear persistence layer with versioned schema management

---

### Phase 5: Reporting and analysis query layer

Purpose:
- build a reusable query service that works for both reporting and analysis

Tasks:
1. Add run-level query methods for single-run summaries.
2. Add aggregate queries for win/loss, character distribution, relic trends, map progression, and other data points.
3. Define a conversion pipeline from SQLite result sets to Polars DataFrames for analysis.
4. Keep all SQL access inside query services, not inside presentation code.
5. Make the query layer usable by the CLI and the GUI without duplication.

Deliverable:
- a single source of truth for reporting and analytical queries

---

### Phase 6: CLI presentation layer

Purpose:
- provide scriptable, saved-output reporting for terminal users

Tasks:
1. Build a command layer that can ingest runs, query summaries, and export reports.
2. Support saved output formats such as plain text, CSV, JSON, and Markdown.
3. Make commands composable so a user can run a small subset of the library as needed.
4. Keep the CLI deliberately thin and not responsible for parsing or database logic.

Deliverable:
- a stable command-line interface that can generate saved reports without a GUI

---

### Phase 7: GUI presentation layer using FastAPI

Purpose:
- provide a separate interactive reporting interface without coupling to the storage logic

Tasks:
1. Create a FastAPI application that serves report pages and JSON endpoints.
2. Expose endpoints for run detail, aggregate report views, and analysis summaries.
3. Keep all business logic in the library and query services.
4. Keep the web layer presentation-only: request input, process output, render results.
5. Prefer FastAPI because it gives a clean API layer, typed request/response handling, and easy future extension.

Deliverable:
- a browser-based reporting interface that uses the same business logic as the CLI

---

### Phase 8: pytest-first regression and quality gates

Purpose:
- protect the refactor through disciplined TDD and regression testing

Tasks:
1. For each ticket, write failing tests before implementation.
2. Cover:
   - parsing behaviour
   - storage behaviour
   - query behaviour
   - CLI output
   - API responses
3. Run the focused test set before merging each refactor milestone.
4. Add a small set of integration tests to validate the end-to-end flow from .run file to SQLite to report.

Deliverable:
- a reliable test suite and a disciplined engineering workflow

---

## TDD requirements for this project

The TDD workflow should be mandatory for the refactor:

1. Write a failing test for the desired behaviour.
2. Implement only the code required to satisfy that behaviour.
3. Refactor the code while preserving the test contract.
4. Repeat for each phase.

This matters particularly because the project is being restructured across several layers. Without test-first development, the schema changes and package boundaries are likely to drift.

---

## Interface design

### CLI
The CLI should be used for:
- importing runs
- generating saved reports
- exporting exports to file
- automation in scripts and pipelines

It should focus on operational and file-based use cases.

### GUI
The GUI should be used for:
- interactive exploration
- charts
- web-based report browsing
- user-driven filtering and analysis

It should be a presentation layer over the same underlying query services and storage model.

This split gives you a clean separation between scriptability and interactivity.

---

## Recommended implementation order

The order should be:

1. Foundation package structure
2. Normalized schema contract
3. Parser and normalizer
4. Repository and migration layer
5. Query layer
6. CLI
7. FastAPI GUI
8. Regression and polish

This order reduces risk because the data contract is defined before the library becomes too large.

---

## Final recommendation

The strongest design for this project is:

- SQLite as the durable, canonical datastore
- a normalized schema that preserves all source data
- a library-first architecture with explicit layers
- Polars only at the analysis boundary
- FastAPI as the GUI layer
- CLI output for saved reports
- pytest-driven development across all major milestones
- Ruff-enforced formatting and linting documented in [CONTRIBUTING.md](../CONTRIBUTING.md)
- Git-tag-based automatic versioning through hatch-vcs
- cross-platform build instructions for macOS, Debian Linux, and Windows

This gives you a maintainable system that supports both operational reporting and deeper data analysis without sacrificing fidelity to the raw run files.

The Obsidian tracking set has already been created and organized under [tickets/README.md](README.md). If you want, the next step can be to turn this into a milestone-by-milestone execution checklist with example pytest test cases and a proposed package directory tree.
