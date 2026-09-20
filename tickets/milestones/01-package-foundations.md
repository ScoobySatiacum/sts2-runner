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

## Acceptance criteria

- The project package can be imported from Python without needing to start the CLI or GUI.
- The core library modules expose clear service entry points.
- The package structure reflects the intended ownership boundaries.
- The architecture documentation describes the direction of dependency flow.

## Execution checklist

### Preconditions

- [ ] Confirm the working branch is the milestone branch for this work.
- [ ] Confirm the current test suite passes before making changes.
- [ ] Read the package layout and dependency-direction requirements in the technical specification.
- [ ] Record any existing uncommitted changes before editing files.

### Package structure

- [ ] Create the required package directories under `src/sts2`.
- [ ] Add `__init__.py` files to every importable package directory.
- [ ] Add module-level docstrings to new public modules.
- [ ] Keep CLI and GUI modules separate from the core library modules.
- [ ] Keep database imports out of CLI and GUI modules except through service interfaces.
- [ ] Define the first public interfaces for loading, normalization, persistence, and querying.
- [ ] Keep the interfaces independent of pandas DataFrame implementation details.

### Tests and validation

- [ ] Add the package-boundary tests before implementing the corresponding imports.
- [ ] Run the focused package-boundary tests.
- [ ] Run the complete existing regression suite.
- [ ] Run Ruff on every changed Python file.
- [ ] Inspect the import graph for presentation-to-storage shortcuts.

### Documentation and completion evidence

- [ ] Document the dependency direction in the architecture documentation.
- [ ] Record any package-layout decisions in the private learning notes.
- [ ] Update `docs/DEVELOPMENT_STATUS.md` with the completed work and validation commands.
- [ ] Mark this milestone complete only when all acceptance criteria and checklist items are satisfied.

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
