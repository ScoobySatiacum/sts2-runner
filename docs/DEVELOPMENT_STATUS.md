# Development status

Last updated: 2026-09-20

## Current branch

The `M01` branch is the current working branch for Milestone 1. It was created from the `refactor` branch and is intended to hold the package-foundation work until the milestone is complete.

## Git status snapshot

At the beginning of the Milestone 1 work, the repository reported:

```text
## M01
```

The branch is being used for the first implementation milestone. Inspect `git status --short --branch` before each work session and preserve unrelated user changes.

The current validation baseline is 14 passing legacy parser tests plus 2 intentionally failing Milestone 1 package-boundary tests. The failing tests identify the first implementation targets: `sts2.parse.loader`, `sts2.storage.sqlite_repository`, `sts2.queries.run_queries`, and the CLI/GUI public exports.

Task-level progress is tracked in GitHub Issues. The local milestone checklist provides the task IDs and completion evidence; it is not a duplicate status board.

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

The following worktree items were already present during this pass and were preserved without modification:

- `.obsidian/`
- `tests/test_package_boundries.py`

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

## Current milestone

Milestone 1 is package foundations and public contracts. Its executable checklist is in [M01-package-foundations.md](../tickets/milestones/M01-package-foundations.md). Active work is tracked in GitHub Issues using task IDs such as `M01-T01`.

## Next implementation step

Complete the Milestone 1 preconditions, package-structure tasks, focused tests, and documentation evidence. Keep the work test-first, preserve the current parser regression coverage, and update this status file only for milestone-level decisions, blockers, and validation evidence. GitHub Issues hold the task-level progress.
