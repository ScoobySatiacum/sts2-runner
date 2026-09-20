# Technical specification: sts2-runner refactor to a layered, SQLite-first library

## 1. Purpose

This specification defines the planned refactor of the project from a single monolithic parser into a reusable library with clear ownership boundaries. The goal is to preserve all data from each Slay the Spire 2 .run file in a normalized SQLite database, while supporting both reporting and data analysis in a maintainable way.

The design must support the following outcomes:

- SQLite remains the canonical storage layer.
- Every relevant field from each .run file is represented in the database in a normalized 1:1 form.
- The project is organized as a library-style package, not as a single script.
- The system supports two presentation layers:
  - a CLI layer that can generate saved output to files
  - a web GUI layer built with FastAPI
- The project uses pytest and follows TDD throughout development.
- Data analysis is supported using Polars at the query/analysis layer, without making Polars the persistence model.

---

## 2. Scope

### In scope

- Ingesting raw .run files
- Parsing and normalizing JSON into explicit row models
- Persisting all normalized data to SQLite
- Querying data for reporting and analysis
- Exposing a CLI interface for saved file output
- Exposing a FastAPI GUI for interactive report viewing
- Maintaining reproducible tests with pytest

### Out of scope

- Django usage
- A single monolithic object that handles parsing, persistence, query logic, and presentation
- Using SQLite as a shortcut for lossy or denormalized storage
- Building a UI before the database contract and query layer are stable

---

## 3. Decision summary

The following design decisions are fixed for this project:

1. SQLite is the authoritative storage layer.
2. The database schema must preserve all data from the run file in a normalized, relational form.
3. The system must be organized as a reusable library package.
4. Reporting and analysis are both first-class concerns.
5. The library exposes composable services that can be combined by the CLI and GUI layers.
6. The CLI is for scriptable output and file export.
7. The GUI is for interactive reports and analysis in a browser.
8. FastAPI is the preferred GUI framework.
9. Polars is used for analytical transformations after data has been loaded from SQLite.
10. All work must use pytest and TDD.
11. Public code must be documented with docstrings to support autodoc generation and AI-assisted code review.
12. The refactor must include a final documentation pass before sign-off.
13. The project must be buildable as a native executable on macOS, Debian Linux, and Windows.
14. PyInstaller or an equivalent packaging solution must be included as part of the final engineering plan.
15. Ruff is the required formatter and linter, with a 300-character line limit, tab indentation of width 4, single quotes, and no magic trailing commas.
16. Package versions must be derived automatically from Git tags through hatch-vcs; a manually duplicated version field is not required.

---

## 4. Architectural principles

### 4.1 Separation of concerns

Each subsystem owns a single responsibility:

- parsing: convert raw JSON into canonical domain records
- normalization: flatten nested objects and arrays into logical record types
- persistence: create schema and load rows into SQLite
- querying: provide reusable read operations for reports and analysis
- CLI: expose saved-output workflows
- GUI: expose interactive presentation logic

### 4.2 Library-first design

The library layer must be usable independently of the presentation concerns. The CLI and GUI should call into the library, not reimplement database logic or parsing logic.

### 4.3 Canonical data model

The project should not treat a dict of DataFrames as the domain contract. A dict of DataFrames is a storage-oriented convenience but is not a stable architecture boundary. The canonical shape should be explicit row groups or domain objects that map cleanly to the database schema.

### 4.4 Database fidelity

The database must not discard source data simply to make the data easier to query. The schema must reflect source structure first and reporting convenience second.

---

## 5. Proposed package layout

The package should be organized as follows:

```text
src/
  sts2/
    __init__.py
    domain/
      __init__.py
      run.py
      player.py
      relic.py
      map_point.py
      room.py
      choice.py
      modifier.py
      models.py
    parse/
      __init__.py
      loader.py
      normalizer.py
      schema_contract.py
      exceptions.py
    storage/
      __init__.py
      sqlite_repository.py
      migrations.py
      schema.py
      sql_helpers.py
    queries/
      __init__.py
      run_queries.py
      analysis_queries.py
      report_queries.py
    analysis/
      __init__.py
      polars_pipeline.py
      aggregations.py
    reports/
      __init__.py
      report_service.py
      exporters.py
    cli/
      __init__.py
      __main__.py
      ingest.py
      report.py
      export.py
    gui/
      __init__.py
      app.py
      routes/
        __init__.py
        runs.py
        reports.py
        analysis.py
      templates/
      static/
    services/
      __init__.py
      ingest_service.py
      report_service.py
      analysis_service.py
    compat/
      __init__.py
      legacy_adapter.py
```

### Notes on the package tree

- The domain layer contains the concepts that represent a run, a player, a map record, and related nested entities.
- The parse layer contains JSON loading and normalization only.
- The storage layer owns the SQLite schema and write operations.
- The queries layer owns read operations and result shaping.
- The analysis layer owns Polars-based transformations.
- The reports layer owns persisted and rendered reports.
- The CLI and GUI are presentation interfaces only.

---

## 6. Data model and schema strategy

### 6.1 Canonical storage model

The canonical storage model is SQLite with a normalized relational schema. A single run is represented by a set of related tables, connected by keys such as:

- run_id
- player_id
- act_id
- room_id
- choice_id
- modifier_id

### 6.2 Database principles

- Use one table for run metadata.
- Use separate tables for nested collections such as players, relics, rooms, choices, and modifiers.
- Keep parent/child relationships explicit.
- Do not collapse nested run structures into one giant table.
- Use migration scripts to evolve the schema over time.

### 6.3 What counts as a normalized 1:1 representation

For every top-level section of the raw JSON, there must be a corresponding table family in SQLite. Examples:

- runs: one row per run
- players: one row per player
- player_relics: one row per relic attached to a player
- map_points: one row per map point record
- map_rooms: one row per room in map history
- player_stats: one row per stat snapshot related to a player
- modifiers: one row per modifier on a run
- card_choices: one row per card choice event
- relic_choices: one row per relic choice event
- nested property records: one row per flattened property element attached to a parent record

The schema must be built to support later analysis without loss of information.

---

## 7. Documentation and autodoc requirements

The project is intended to be both human-readable and AI-friendly. Documentation is not a final step to be added later; it is a required part of the engineering work.

### 7.1 Public API documentation

Every public module, class, function, and service entry point must include a docstring. This is required so that future documentation generation tools can produce a consistent API reference without manual cleanup.

The project should use a consistent style for docstrings, preferably Google style, for readability and compatibility with common autodoc tooling.

Example:

```python
class RunFileLoader:
    """Load and validate a Slay the Spire 2 run file.

    Args:
        path: Path to the raw .run file.

    Returns:
        A validated run payload ready for normalization.
    """
```

### 7.2 Documentation expectations by phase

At the end of the refactor effort, the following should be true:

- all public modules have module-level docstrings
- all public classes have class docstrings
- all public functions and service methods have function docstrings
- private helpers may include concise comments only when the logic is not self-evident
- comments are not a substitute for docstrings

### 7.3 AI-assisted review and scope control

Because a human will work on the implementation and an AI assistant will help with review, documentation, and maintenance, the project must remain readable to both humans and automation. Clear docstrings, concise architecture notes, and stable task tracking reduce the risk of scope drift and make the project easier to review.

---

## 8. Milestone execution checklist

The implementation should proceed in ordered milestones. Each milestone should be treated as an independent engineering increment with test-first validation.

### Milestone 1: package foundations and public contracts

Tasks:

- create the project package structure under src/sts2
- define the import boundaries between domains, parse, storage, queries, CLI, and GUI
- establish a public service contract for ingest, repository, and query operations
- write the initial failing tests for importability and package boundary enforcement

Example pytest cases:

```python
# tests/test_package_boundaries.py

def test_core_package_imports():
    from sts2.parse.loader import RunFileLoader
    from sts2.storage.sqlite_repository import SqliteRunRepository
    from sts2.queries.run_queries import RunQueries

    assert RunFileLoader is not None
    assert SqliteRunRepository is not None
    assert RunQueries is not None


def test_cli_does_not_import_gui_modules():
    import sts2.cli as cli
    import sts2.gui as gui

    assert hasattr(cli, "ingest")
    assert hasattr(gui, "app")
```

Acceptance criteria:

- the package is importable
- the dependency direction is explicit
- no CLI or GUI code is required to load a run into the library

---

### Milestone 2: schema contract and data mapping design

Tasks:

- define the canonical table layout
- document the relationship model for run, player, room, choice, and modifier entities
- define how nested arrays and dictionaries are mapped into child tables
- define the schema versioning strategy

Example pytest cases:

```python
# tests/test_schema_contract.py

def test_run_schema_has_required_core_tables():
    schema = build_schema_contract()

    assert "runs" in schema.tables
    assert "players" in schema.tables
    assert "player_relics" in schema.tables
    assert "map_points" in schema.tables


def test_table_foreign_keys_are_defined():
    schema = build_schema_contract()

    assert schema.table("player_relics").foreign_key("run_id") == "runs.run_id"
    assert schema.table("players").foreign_key("run_id") == "runs.run_id"
```

Acceptance criteria:

- the schema contract is final enough to drive implementation
- all nested data categories are mapped to explicit table families
- foreign key relationships are defined before database code is written

---

### Milestone 3: raw JSON ingestion and normalization

Tasks:

- create the loader for raw .run files
- define the run model and nested record data structures
- transform nested objects into explicit row payloads
- assign stable identifiers such as run_id, player_id, and choice_id

Example pytest cases:

```python
# tests/test_run_loader.py
from pathlib import Path


def test_load_run_file_returns_run_envelope():
    path = Path("tests/samples/win.run")
    run = load_run_file(path)

    assert run.run_id == "win"
    assert run.players is not None
    assert run.map_point_history is not None


def test_normalizer_creates_player_and_map_row_groups():
    run = load_run_file(Path("tests/samples/win.run"))
    rows = normalize_run(run)

    assert "players" in rows
    assert "map_points" in rows
    assert len(rows["players"]) > 0
```

Acceptance criteria:

- raw JSON can be parsed without database access
- nested structures are flattened into stable row payloads
- run identity is assigned consistently

---

### Milestone 4: SQLite repository and migration behaviour

Tasks:

- create SQLite schema from the schema contract
- implement repository insert methods for each table family
- enforce deduplication by run_id
- add migration utilities for future schema evolution

Example pytest cases:

```python
# tests/test_sqlite_repository.py

def test_repository_creates_database_and_inserts_run(tmp_path):
    db_path = tmp_path / "runs.db"
    repo = SqliteRunRepository(db_path)

    run_rows = [{"run_id": "abc123", "win": 1, "character": "IRONCLAD"}]
    repo.insert_runs(run_rows)

    assert db_path.exists()
    assert repo.get_run_count() == 1


def test_repository_skips_duplicate_run_id(tmp_path):
    db_path = tmp_path / "runs.db"
    repo = SqliteRunRepository(db_path)

    repo.insert_runs([{"run_id": "abc123", "win": 1}])
    repo.insert_runs([{"run_id": "abc123", "win": 1}])

    assert repo.get_run_count() == 1
```

Acceptance criteria:

- a new database can be created from the schema contract
- duplicate run_id ingestion is prevented
- child row sets are inserted consistently into their table families

---

### Milestone 5: reporting queries and analysis queries

Tasks:

- create query methods for run-level and aggregate data access
- support single-run reporting and multi-run analysis
- allow conversion to Polars DataFrames for analysis workflows
- keep SQL outside the presentation layer

Example pytest cases:

```python
# tests/test_queries.py

def test_query_returns_run_summary(repo):
    summary = repo.get_run_summary("abc123")

    assert summary["run_id"] == "abc123"
    assert "win" in summary


def test_analysis_query_returns_character_distribution(repo):
    df = repo.get_character_win_rate_df()

    assert "character" in df.columns
    assert "win_rate" in df.columns
```

Acceptance criteria:

- the same underlying query layer can support both report generation and analytics
- data is available in a shape that can be passed to Polars for analysis

---

### Milestone 6: CLI for saved output

Tasks:

- create a CLI facade over the library services
- support import, report, and export commands
- implement text and file-based output
- make CLI output deterministic and scriptable

Example pytest cases:

```python
# tests/test_cli.py
from click.testing import CliRunner


def test_cli_ingest_command_runs(tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["ingest", "tests/samples", "--db", str(tmp_path / "runs.db")])

    assert result.exit_code == 0


def test_cli_report_outputs_file(tmp_path):
    runner = CliRunner()
    output_path = tmp_path / "summary.txt"
    result = runner.invoke(cli, ["report", "summary", "--db", "instance/runs.db", "--output", str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()
```

Acceptance criteria:

- CLI activities are separate from parsing and persistence logic
- saved file output works without a GUI
- commands are testable with local fixtures

---

### Milestone 7: FastAPI GUI layer

Tasks:

- create a FastAPI app wrapper around the query layer
- expose report and analysis endpoints
- design endpoints for run detail and aggregate views
- keep the API layer presentation-focused only

Example pytest cases:

```python
# tests/test_gui_api.py
from fastapi.testclient import TestClient


def test_run_detail_endpoint_returns_200(client):
    response = client.get("/runs/abc123")

    assert response.status_code == 200
    assert "run_id" in response.json()


def test_summary_endpoint_returns_aggregate_data(client):
    response = client.get("/reports/summary")

    assert response.status_code == 200
    assert "totals" in response.json()
```

Acceptance criteria:

- the GUI consumes the same library query layer as the CLI
- the GUI does not contain raw database access logic
- report endpoints are testable with FastAPI client fixtures

---

### Milestone 8: end-to-end validation and final quality gates

Tasks:

- validate the full data flow from .run file to SQLite to report
- ensure all major components work together without hidden coupling
- verify CLI output matches the API data model expectations
- run the full pytest suite before sign-off

Example pytest cases:

```python
# tests/test_end_to_end.py

def test_pipeline_ingests_run_and_generates_report(tmp_path):
    db_path = tmp_path / "runs.db"
    ingest_runs("tests/samples", db_path)

    summary = build_run_summary(db_path)

    assert summary is not None
    assert len(summary["runs"]) > 0
```

Acceptance criteria:

- all layers operate with the same contract
- final end-to-end validation succeeds
- the project is ready for the next release or experimentation cycle

---

### Milestone 9: cross-platform binary packaging

Tasks:

- add the build tooling for generating native executables
- select PyInstaller as the default packaging method for the CLI binary
- define the build commands for macOS, Debian Linux, and Windows
- verify the generated executable still runs successfully in a smoke-test workflow
- keep the packaging configuration separate from the application logic

Example build commands:

```bash
uv add --dev pyinstaller
uv run pyinstaller --name sts2-runner --onefile --console src/sts2/cli/__main__.py
```

Acceptance criteria:

- the project can generate a standalone binary for each target platform
- the CLI entry point remains the same across build targets
- the packaging workflow is captured in project documentation and build instructions

---

### Milestone 10: autodocumentation and final documentation pass

Tasks:

- review all public modules, classes, and functions for docstrings
- ensure the architecture, workflow, and API contracts are documented in a maintainable manner
- confirm that the project documentation supports future autodoc generation
- perform a final scope review to confirm that the implementation remains aligned with the technical specification

Required outputs:

- fully documented public API
- a final review of the docs and tickets
- a clear statement of the architecture and the design intent for future maintainers

Acceptance criteria:

- all public API surfaces have docstrings
- the docs and milestone set are aligned with the implemented code
- future contributors can generate a documentation site without major cleanup work

---

## 9. TDD policy

The implementation of this specification must follow a strict TDD policy:

1. A failing test is written before the implementation.
2. The implementation is minimized to satisfy the test.
3. The code is refactored only after the behaviour is green.
4. The test suite is run for the relevant milestone before moving to the next one.

This policy applies to database code, parser code, CLI code, and API code equally.

---

## 11. Non-functional requirements

### 9.1 Maintainability

The project architecture must be understandable to a mid-level Python engineer within one working session. The code should have clean boundaries and a small number of dependencies between subsystems.

### 9.2 Extensibility

New run metadata fields or new report types must be added without reworking the whole parser. The design should support new table families and new query methods without invasive changes.

### 9.3 Reliability

The ingest pipeline must not silently lose data. Duplicate run imports must be prevented, and migration behaviour must be explicit and testable.

### 9.4 Observability

It must be easy to inspect what was imported, what failed to import, and how many rows were inserted for each table family.

---

## 12. Definition of done for the refactor

The refactor is complete when all of the following are true:

- all .run file data is represented in the SQLite database in normalized form
- the project is organized as a library-style package
- CLI and GUI layers both consume the same library services
- queries support both reporting and analysis
- Polars is used only where analytical transformation is required
- all major milestones have pytest tests written in TDD order
- the project is maintainable and extensible for future data additions

---

## 13. Recommended next engineering step

The first implementation step should be Milestone 1 and Milestone 2 together, because they define the package boundary and the database contract before any parser or repository code is written. This reduces the chances of rework later.

Once those milestones are green, the project can continue with the parser, repository, query layer, and then the CLI and API presentation layers.
