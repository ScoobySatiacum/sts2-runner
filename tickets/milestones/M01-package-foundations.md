# Milestone 1: Package foundations and public contracts

## Objective

Establish the library structure and the architectural boundaries that will guide the rest of the refactor. This milestone defines the package layout and clarifies the dependency direction between parsing, storage, query logic, and presentation.

## Scope

- Create the project package structure under src/sts2.
- Separate concerns into domain, parse, storage, query, analysis, report, CLI, and GUI layers.
- Define the public interfaces used by ingestion, persistence, and reporting services.
- Ensure that the package can be imported and used independently of the CLI and GUI layers.

## Design constraints

- The project must remain library-first.
- Database access must not be performed directly from presentation code.
- The CLI and GUI must consume the library services rather than reimplement business logic.
- The package structure must support future extension without creating tight coupling between subsystems.

## Proposed package layout

```text
src/
  sts2/
    __init__.py
    domain/
    parse/
    storage/
    queries/
    analysis/
    reports/
    cli/
    gui/
    services/
```

## How to work through M01

Treat each unchecked item as one small reviewable change. Before editing, write down the boundary being created and the test that will prove it exists. After editing, run the narrowest relevant test first, then the complete suite when the item changes shared package structure.

For example, a task that defines a loader contract should produce one public interface and one focused import or behavior test:

```python
# src/sts2/parse/loader.py
from pathlib import Path
from typing import Protocol


class RunFileLoader(Protocol):
    """Load one raw .run file without opening a database."""

    def load(self, path: Path) -> dict:
        """Return the decoded source payload for ``path``."""
```

```python
# tests/test_package_boundaries.py
from sts2.parse.loader import RunFileLoader


def test_loader_is_a_public_parse_boundary():
    assert RunFileLoader is not None
```

The example is a contract illustration, not a demand to use `Protocol` or `dict` as the final type. The important result is that parsing has a named public boundary and no SQLite dependency.

## Boundary examples

### Allowed dependency direction

```text
domain <- parse <- services <- cli
domain <- storage <- queries <- services <- gui
```

The arrows show that higher-level orchestration may use lower-level library services. Presentation modules may call services, but they should not import `sqlite3`, construct schemas, or parse `.run` JSON directly.

### A boundary test that catches a shortcut

```python
from pathlib import Path


def test_gui_does_not_import_sqlite():
    source = Path("src/sts2/gui/app.py").read_text()

    assert "import sqlite3" not in source
    assert "from sqlite3" not in source
```

An AST-based import check may replace this string check when the boundary is implemented. The test should fail if presentation code starts owning persistence.

### Public contracts should not expose pandas

The planned library boundary should exchange domain records or row collections rather than requiring callers to understand the legacy `dict[str, pandas.DataFrame]` shape:

```python
class RunNormalizer(Protocol):
    """Convert a loaded run into named normalized row groups."""

    def normalize(self, payload: dict) -> dict[str, list[dict]]:
        """Return storage-ready rows without opening a database."""
```

The existing parser may continue using pandas internally during the transition. M01 only establishes that new public interfaces do not make pandas a required caller-facing contract.

## Suggested task loop

For each task:

1. Read the linked architecture or decision document.
2. Add or update the smallest focused test that expresses the boundary.
3. Make the smallest implementation or documentation change that satisfies the test.
4. Run the focused test and record the command and result.
5. Run the full suite before closing a task that changes imports or public APIs.
6. Link the commit or pull request to the matching GitHub issue.

Example validation commands:

```bash
uv run pytest tests/test_package_boundries.py -q
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
```

## Acceptance criteria

- The project package can be imported from Python without needing to start the CLI or GUI.
- The core library modules expose clear service entry points.
- The package structure reflects the intended ownership boundaries.
- The architecture documentation describes the direction of dependency flow.

## Execution checklist

### Preconditions

- [x] **M01-T01** Confirm the working branch is the milestone branch for this work.
- [x] **M01-T02** Confirm the current test suite passes before making changes.
- [x] **M01-T03** Read the package layout and dependency-direction requirements in the technical specification.
- [x] **M01-T04** Record any existing uncommitted changes before editing files.

### Package structure

- [x] **M01-T05** Create the required package directories under `src/sts2`.
- [x] **M01-T06** Add `__init__.py` files to every importable package directory.
- [ ] **M01-T07** Add a module-level docstring to each new package module.
- [ ] **M01-T08** Add public exports for the parse, storage, query, CLI, and GUI entry points.
- [ ] **M01-T09** Add a smoke test that imports the core package without starting a presentation layer.
- [ ] **M01-T10** Keep CLI modules limited to argument parsing and service invocation.
- [ ] **M01-T11** Keep GUI modules limited to request handling and presentation formatting.
- [ ] **M01-T12** Add a test that detects direct SQLite imports in CLI and GUI modules.
- [ ] **M01-T13** Define the first public loader interface.
- [ ] **M01-T14** Define the first public normalizer interface.
- [ ] **M01-T15** Define the first public repository interface.
- [ ] **M01-T16** Define the first public query interface.
- [ ] **M01-T17** Define the service composition boundary used by CLI and GUI callers.
- [ ] **M01-T18** Keep new public contracts independent of pandas DataFrame implementation details.
- [ ] **M01-T19** Add a contract example showing normalized row groups as plain Python data.

### Tests and validation

- [ ] **M01-T20** Add core package import tests before implementing the corresponding imports.
- [ ] **M01-T21** Add CLI and GUI separation tests.
- [ ] **M01-T22** Add a test for the public service entry points.
- [ ] **M01-T23** Run the focused package-boundary test file.
- [ ] **M01-T24** Run the complete existing regression suite.
- [ ] **M01-T25** Run Ruff check on every changed Python file.
- [ ] **M01-T26** Run Ruff format check on every changed Python file.
- [ ] **M01-T27** Inspect the import graph for presentation-to-storage shortcuts.
- [ ] **M01-T28** Record focused and complete validation results in the issue or pull request.

### Documentation and completion evidence

- [ ] **M01-T29** Document the dependency direction in the architecture documentation.
- [ ] **M01-T30** Document the public boundary examples for a new contributor.
- [ ] **M01-T31** Record package-layout decisions in the private learning notes.
- [ ] **M01-T32** Update `docs/DEVELOPMENT_STATUS.md` with completed work and validation commands.
- [ ] **M01-T33** Review every M01 acceptance criterion against implementation evidence.
- [ ] **M01-T34** Mark M01 complete only when all acceptance criteria and checklist items are satisfied.

## Example pytest cases

```python
# tests/test_package_boundaries.py

def test_core_package_imports():
    from sts2.parse.loader import RunFileLoader
    from sts2.storage.sqlite_repository import SqliteRunRepository
    from sts2.queries.run_queries import RunQueries

    assert RunFileLoader is not None
    assert SqliteRunRepository is not None
    assert RunQueries is not None


def test_cli_and_gui_are_separate_layers():
    import sts2.cli as cli
    import sts2.gui as gui

    assert hasattr(cli, "ingest")
    assert hasattr(gui, "app")
```

## Definition of done

The milestone is complete when the package structure is in place and the library boundary is clear enough for the next phase to proceed without architectural rework.
