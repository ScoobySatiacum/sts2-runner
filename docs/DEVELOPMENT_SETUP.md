# Development setup and repository hygiene

This document captures the project’s working conventions for git hygiene, uv-based project management, and documentation standards. It is intended for both the human maintainer and any AI-assisted contributors working on the repo.

## 1. Clean starting point for the git repository

The goal is to produce a working repository that is easy to reason about, easy to review, and easy to reset when the project refactor begins.

### Step 1: Back up the current repository state

Before rewriting any history, back up the repository locally.

```bash
git status
git remote -v
git branch -vv
cp -a . ../sts2-runner-backup
```

If the repo is already on a remote, confirm that the current branch is the one you want to rewrite before making any destructive changes.

### Step 2: Review the working tree and remove generated artifacts

Remove local-only generated files before starting a clean base.

```bash
git status --short
rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info
find . -type d -name __pycache__ -prune -exec rm -rf {} +
```

Do not delete files that are part of the real project. Keep only source, tests, documentation, and explicit project configuration.

### Step 3: Choose the clean reset strategy

There are two common options.

#### Option A: Keep the current branch and rewrite history

This is the least disruptive option if the repo has not yet been shared widely.

```bash
git checkout main
git reset --soft $(git rev-list --max-parents=0 HEAD)
git add -A
git commit -m "Initial clean project state"
```

This clears the current branch to a single root commit while retaining the working tree contents.

#### Option B: Create a fresh orphan branch

This is the safest way to create a clean starting point if the project should be restarted around a clean history.

```bash
git checkout --orphan clean-start
git rm -rf --cached .
git add -A
git commit -m "Initial clean project state"
```

This gives a branch with a fresh commit history while preserving the project files.

### Step 4: Reconnect the repo to the remote carefully

If the repository has already been published, do not force-push until the branch state is reviewed.

```bash
git remote -v
git push --set-upstream origin clean-start
```

If you are replacing an existing branch history, use a force push only after confirmation:

```bash
git push --force-with-lease origin main
```

### Step 5: Keep the repo clean going forward

Use these conventions:

- do not commit generated files or local environment artifacts
- keep configuration in version control
- keep one branch per refactor milestone or feature
- keep commit messages focused and descriptive

---

## 2. Converting the project to uv

The project should use uv for dependency management and project execution. uv is used to create the environment, install dependencies, and run the project with a standard Python project layout.

### Step 1: Install uv

If uv is not installed, install it from the official uv installer.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then confirm the version:

```bash
uv --version
```

### Step 2: Define the project as a uv-managed package

The project should use a src-layout package and a modern pyproject.toml configuration. The current project already has a src-layout import path under src/sts2, so the migration should preserve that shape.

The minimum practical structure is:

```toml
[project]
name = "sts2-runner"
dynamic = ["version"]
description = "Slay the Spire 2 run parser and reporting toolkit"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
  "pandas",
  "polars",
  "tqdm",
  "streamlit",
  "matplotlib",
  "plotly",
  "pillow",
  "fastapi",
  "uvicorn",
  "pytest",
]

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.uv]
package = true

[tool.hatch.version]
source = "vcs"
```

If the project is being created from scratch, a more standard uv flow is:

```bash
uv init --package --src
```

If the project already exists, keep the src layout and replace or update the pyproject.toml file to match the uv-managed standard.

### Step 3: Sync the environment with uv

```bash
uv sync --dev
```

This creates the project environment and installs the declared dependencies.

### Step 4: Run commands through uv

Use uv to run all project commands consistently.

```bash
uv run pytest
uv run python -m pytest tests
uv run python -m sts2
```

This keeps the dependency and environment management consistent across contributors and automation.

### Step 5: Keep the environment clean

Use these conventions:

- keep runtime and dev dependencies explicitly declared in pyproject.toml
- avoid relying on a manually managed global Python install
- prefer `uv run ...` instead of activating a local virtualenv manually when possible
- commit only project configuration, not local environment files

---

## 3. Documentation and autodoc standards

This project is intended to be both human-readable and AI-friendly. The design is library-first and should remain maintainable as the codebase grows.

### Required documentation standard

All public modules, classes, functions, and service entry points should include docstrings. This is required for later autodoc generation and for keeping the project understandable to both engineers and AI assistants.

Use one of these conventions consistently:

- Google style docstrings
- NumPy style docstrings

Google style is usually simpler for a project of this size.

Example:

```python
class RunFileLoader:
    """Load and validate a Slay the Spire 2 .run file.

    Args:
        path: Path to the raw .run file.

    Returns:
        A validated run payload ready for normalization.
    """
```

### Documentation expectations for the refactor

At the end of the refactor effort, the project should include:

- module-level docstrings for all public modules
- class docstrings for all public service classes
- function docstrings for public entry points and reusable query functions
- descriptive comments only when they clarify non-obvious behaviour
- no reliance on comments as a substitute for docstrings

### Why this matters

This project is meant to be extended by multiple contributors and to support automation. Good docstrings make the project easier to:

- review with AI assistants
- generate technical documentation later via autodoc
- maintain consistent public interfaces
- reduce drift during refactors

---

## 4. Ruff formatting and linting

Ruff is the required formatter and linter for Python changes. The project configuration lives in `pyproject.toml` and defines these conventions:

- maximum line length: 300 characters
- indentation: tabs with an indentation width of 4
- string quote style: single quotes
- magic trailing commas: disabled so parameters stay on one line when the 300-character limit allows it
- `W191`: disabled because it rejects the tab indentation style required by this project

Run Ruff through uv:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
```

To apply formatting locally:

```bash
uv run ruff format src tests
```

To apply safe lint fixes:

```bash
uv run ruff check --fix src tests
```

Do not use a separate formatter with a conflicting indentation or quote policy. Ruff is the source of truth for Python formatting.

---

## 5. Documentation workflow for AI-assisted work

When AI assistance is used, it should be treated as a tool for review and acceleration, not as a substitute for engineering judgement.

Required behaviour:

- keep the project scope focused on the current milestone
- preserve the architectural boundaries described in the technical specification
- write or update documentation whenever the project structure or workflow changes
- add or extend docstrings when new public components are added
- make sure the project remains reviewable and traceable in the git history

---

## 6. Versioning and release workflow

The project uses `hatch-vcs` for automatic version discovery. The version is derived from Git tags during builds, so the Git tag and the built package version cannot drift because of a manually duplicated version field in `pyproject.toml`.

`bumpver` is not the preferred default for this repository. It is useful when a project intentionally stores a version string in one or more source files and wants a command to edit those files. This project already has Git as its release history, and Hatchling is already the build backend, so `hatch-vcs` is the smaller and more reliable integration.

### Development versions

When there is no release tag at the current commit, `hatch-vcs` generates a development version from the repository state. This is suitable for local builds and pre-release testing.

### Release versions

Create an annotated semantic-version tag after the release commit has passed its tests:

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
uv build
```

The generated wheel and source archive under `dist/` should contain version `0.1.0`. Build artifacts are ignored and should not be committed.

### Versioning rules

- use `MAJOR.MINOR.PATCH` semantic versions
- increment MAJOR for incompatible public API changes
- increment MINOR for backwards-compatible features
- increment PATCH for backwards-compatible fixes
- use a `v` prefix for Git tags, such as `v0.2.0`
- create release tags only from reviewed commits on the intended release branch

For future automation, CI can run tests, build the package, verify the artifact version, and publish when a version tag is pushed. The initial refactor does not need a release bot before the package and CLI contracts stabilize.

---

## 7. Cross-platform build and distribution strategy

The project must be executable as a native binary on macOS, Debian Linux, and Windows. The build strategy should be defined as part of the engineering plan rather than added as a late workaround.

### Build goal

The project must be able to produce an executable artifact for each target platform without requiring the end user to install Python or the project dependencies manually.

### Recommended approach

Use PyInstaller as the primary packaging tool, with one build configuration per target platform. This is the simplest and most reliable path for a Python CLI application that is not a web app or a full desktop framework.

### Install PyInstaller in the project environment

```bash
uv add --dev pyinstaller
```

### Example PyInstaller command

```bash
uv run pyinstaller \
  --name sts2-runner \
  --onefile \
  --console \
  --collect-all sts2 \
  src/sts2/cli/__main__.py
```

This produces a single-file executable that can be distributed as a binary build.

### Cross-platform build matrix

Use separate CI or local build steps for each platform:

- macOS: build a `.app` or single-file binary for Intel or Apple Silicon as required
- Debian Linux: build a standalone executable or packaged `.deb` if a system package is desired
- Windows: build a `.exe` using the Windows environment and package it as a standalone binary

### Build process responsibilities

The build workflow should:

- use the uv-managed environment for dependency resolution
- build from a clean environment on each target platform
- produce a reproducible artifact name and version from the project metadata
- place the output in a `dist/` or `build/` directory and keep the generated artifacts out of source control
- verify that the generated binary runs successfully before release

### Optional packaging alternatives

PyInstaller is the default recommendation for the CLI binary. If a more managed distribution flow is needed later, the project may also support:

- a `pipx`-based install flow
- a Debian package workflow for Linux
- a Windows installer using a packaging tool such as NSIS or WiX
- a signed macOS app distribution path if desktop packaging becomes necessary

### Build verification

The project should include a build verification test or smoke workflow that runs the packaged binary in a minimal example, such as:

```bash
./dist/sts2-runner --help
```

This confirms that the packaged artifact still loads the project and responds to the CLI interface.

---

## 8. Minimum project hygiene checklist

Before a refactor is considered ready for review, confirm the following:

- git history is clean or intentionally rewritten
- uv is managing the environment and dependencies
- pyproject.toml is the source of truth for project metadata
- pytest is the test runner
- public modules are documented with docstrings
- the tickets and milestones reflect the current scope and documentation standards
- the project has a clear build and packaging plan for macOS, Debian Linux, and Windows
