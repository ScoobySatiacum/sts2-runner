# Contributing to sts2-runner

This guide describes the development workflow for current and future contributors. The project is being refactored on the `refactor` branch into a library-first package with SQLite persistence, separate CLI and FastAPI presentation layers, and test-driven development.

## Development prerequisites

Install:

- Python 3.12 or newer
- uv
- Git

The project uses a `src/` layout and uv-managed dependencies. Do not rely on a globally installed copy of the package when developing.

```bash
uv sync --dev
uv run pytest
```

Run commands with `uv run` so they use the project environment:

```bash
uv run pytest
uv run python -m pytest tests
```

## Branch and worktree workflow

The `refactor` branch is the working branch for the current redesign. Start from an up-to-date branch and inspect the worktree before editing:

```bash
git status --short --branch
git branch --show-current
git pull --ff-only
```

Keep commits focused on one milestone or bounded change. Do not commit generated environments, database files, build output, or local run data.

Commit `uv.lock` when dependency resolution changes. It is the reproducibility record for the uv environment and binary build inputs.

## GitHub task workflow

GitHub Issues are the active task tracker. Before starting work:

1. Select one unchecked task from the relevant milestone file.
2. Create or select the matching GitHub Issue using the task template.
3. Use the task ID in the issue title, branch name, and commit messages.
4. Assign the issue to the matching GitHub Milestone.
5. Open a pull request using the repository template and link the issue with `Closes #123`.

Use one issue for one bounded outcome. Keep architecture decisions in `tickets/decisions/` and personal learning notes in the ignored `docs/learning/` directory. Do not copy GitHub issue status into `docs/DEVELOPMENT_STATUS.md`; that file records only milestone-level decisions, blockers, and validation evidence.

## Engineering boundaries

Changes should preserve these ownership boundaries:

- parsing loads and validates raw `.run` data
- normalization maps nested data into canonical records
- storage owns SQLite schema and writes
- queries own reusable read operations
- analysis owns Polars transformations
- reports shape reusable report data
- CLI and GUI layers present library results without reimplementing domain logic

New public modules, classes, functions, and service entry points require docstrings. Use Google-style docstrings consistently.

## Test-driven workflow

Each refactor ticket follows this sequence:

1. Write a focused failing pytest for the desired behavior.
2. Implement the smallest change that satisfies the test.
3. Refactor while keeping the test contract green.
4. Run the focused test and then the broader suite.
5. Update the relevant ticket or documentation when the contract changes.

The focused test command is:

```bash
uv run pytest tests/path/to/test_file.py::test_name
```

The full suite is:

```bash
uv run pytest
```

## Ruff policy

Ruff is the required Python formatter and linter. Its configuration is in `pyproject.toml`.

The enforced style is:

- maximum line length: 300 characters
- indentation: tabs
- indentation width: 4
- string quotes: single quotes
- magic trailing commas: disabled so parameters stay on one line when the 300-character limit allows it
- `W191`: disabled because it conflicts with the required tab indentation

Check code before opening a pull request:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
```

Apply the formatter when appropriate:

```bash
uv run ruff format src tests
uv run ruff check --fix src tests
```

Ruff is the source of truth for formatting. Do not add another formatter with different quote or indentation settings.

## Versioning

The project uses `hatch-vcs`, not `bumpver`, for automatic version discovery. `hatch-vcs` derives the built package version from Git tags and the repository state. This keeps the release history and package metadata connected without maintaining a duplicated version string in source files.

Use semantic version tags with a `v` prefix:

- `v0.1.0` for the first compatible release
- increment MAJOR for incompatible public API changes
- increment MINOR for backwards-compatible features
- increment PATCH for backwards-compatible fixes

Before tagging a release:

```bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv build
```

Create the tag from the reviewed release commit and rebuild:

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
uv build
```

The resulting artifacts are written to `dist/` and should contain the tag version. Do not commit the artifacts. Future CI can build and publish when a version tag is pushed.

`bumpver` remains a possible alternative if the project later needs to edit versions in multiple tracked files, but it is unnecessary while Git tags are the authoritative release markers.

## Documentation expectations

Update documentation when changing:

- package structure or dependency direction
- the SQLite schema or migration contract
- CLI commands or output formats
- API routes or response contracts
- build, release, or supported-platform behavior

The primary planning documents are:

- [docs/DEVELOPMENT_SETUP.md](docs/DEVELOPMENT_SETUP.md)
- [docs/DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md)
- [tickets/ENGINEERING_PLAN.md](tickets/ENGINEERING_PLAN.md)
- [tickets/TECHNICAL_SPECIFICATION.md](tickets/TECHNICAL_SPECIFICATION.md)
- [tickets/README.md](tickets/README.md)

## Pull request checklist

Before requesting review, confirm:

- the change is on the correct milestone branch
- focused tests pass
- the full test suite passes when the change crosses a boundary
- Ruff check passes
- Ruff format check passes for changed Python files
- public APIs have docstrings
- documentation and tickets reflect changed behavior
- no generated files, credentials, local databases, or run samples were added
- the worktree status is understood and unrelated changes were preserved
