# AGENTS.md

A data parser for Slay the Spire 2 run saves -> sqlite database, plus a small report/graphing script. Single-package repo (`sts2`), no app/server.

## Commands

- Run tests: `.venv/bin/python -m pytest tests` (repo has a committed `.venv`, Python 3.14).
- Single test: `.venv/bin/python -m pytest tests/sts2/test_sts_run_parser.py::test_parse_players_win`.
- Parse runs into the DB: `.venv/bin/python -m sts2.sts_run_parser <dir-of-.run-files> --db instance/sts2_runs.db` (argparse CLI; skips run_ids already in the DB).
- No lint, typecheck, or formatter config exists. `pyproject.toml` has no dev tooling.

## Package layout

- src-layout: the importable package is `src/sts2`, installed *editable* into `.venv` (hatchling). Tests do `from sts2.sts_run_parser import StsRunParser`. Don't move files into a top-level `sts2/` dir.
- `src/sts2/sts_run_parser.py` is the core: normalizes a `.run` JSON file into a dict of pandas DataFrames (`self.dfs`) and loads them into sqlite via `load_to_db()`. `run_id` = the file stem, used as the identity column across all tables (including `runs`).
- `src/sts2/sts_run_reporter.py` is a standalone streamlit/matplotlib/plotly script, half-formed and not wired into the parser.

## Gotchas

- **Schema file** is `sts2_run_db_schema.sql` (repo root, misspelling "schmea" was fixed). The parser derives its path from `__file__`, so it's portable — don't hardcode an absolute path to it.
- **Dotted table names are intentional** (e.g. `props.ints`, `props.strings` come from the `self.dfs` keys). But the parser renames dotted **column** names to underscores before writing (`load_to_db`), and the committed schema is regenerated to match — so no dotted columns should appear in the DB.
- **Add a table to the schema when adding a new df**: `load_to_db` only creates tables that exist in `self.dfs`; the schema pre-defines the stable full set (26 tables). Regenerate it from a clean DB dump (`pandas.io.sql.get_schema`) if you change the output shape.
- **Incremental runs**: `main()` skips runs whose `run_id` (file stem) is already in `runs`, keyed on `run_id` (not `start_time`, which is not unique across multiplayer runs).
- **Hardcoded absolute path**: `sts_run_reporter.py` still connects to the author's absolute `instance/sts2_runs.db` path. Don't rely on it being portable.
- **Dependencies are declared** in `pyproject.toml` (`pandas`, `tqdm`, `streamlit`, `matplotlib`, `plotly`, `Pillow`), but they also live in the committed `.venv` (Python 3.14).
- DB `instance/sts2_runs.db` and test/sample run data (`tests/samples/*.run`, `resources/`) are gitignored. The committed test suite is green (14 pass).
