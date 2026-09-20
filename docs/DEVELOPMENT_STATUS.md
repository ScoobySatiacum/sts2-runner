# Development status

Last updated: 2026-09-20

## Current branch

The `refactor` branch is the working branch for the project redesign. It tracks `origin/refactor` and will hold the implementation work until the refactor is complete or a milestone-specific branch strategy is adopted.

## Git status snapshot

At the beginning of this documentation and tooling pass, the repository reported:

```text
## refactor...origin/refactor
 M pyproject.toml
```

The existing `pyproject.toml` change is the planned uv/package metadata migration. This pass extends that configuration with Ruff, explicit Hatch package selection, and Git-tag-based versioning. The files changed by this pass should remain visible in `git status` for review; they have not been committed automatically.

Generated files and local environments remain excluded from source control, including `.venv`, caches, build output, distribution output, and local SQLite data. `uv.lock` is the exception: it is an intentional, tracked reproducibility file for this package and its binary builds.

## Project phase

The project is at the transition from planning to implementation.

Completed planning work:

- layered library-first architecture defined
- SQLite selected as the canonical persistence layer
- normalized 1:1 data representation required
- Polars selected for analysis after SQLite reads
- CLI and FastAPI presentation layers separated
- pytest and TDD made mandatory
- cross-platform binary packaging planned
- autodoc-friendly public API documentation required
- uv-based project workflow documented
- Ruff style policy documented
- Git-tag-based automatic versioning selected

Not yet implemented:

- the new package boundary and service modules
- the parser and normalization split
- the repository and migration layer
- the reusable query and analysis services
- the CLI presentation layer
- the FastAPI GUI layer
- the PyInstaller build workflow
- the final public API documentation pass

## Current tooling decisions

- package manager and runner: uv
- build backend: Hatchling
- version source: hatch-vcs and Git tags
- formatter and linter: Ruff
- line length: 300 characters
- indentation: tabs with width 4
- quote style: single quotes
- magic trailing commas: disabled
- persistence: SQLite
- tests: pytest

## Next implementation step

Begin the first implementation milestone with package foundations and public contracts. Keep the work test-first, preserve the current parser regression coverage, and update this status file when a milestone changes from planned to implemented.
