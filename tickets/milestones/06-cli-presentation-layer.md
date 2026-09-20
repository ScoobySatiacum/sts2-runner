# Milestone 6: CLI presentation layer

## Objective

Provide a CLI interface for running imports, generating summaries, and exporting saved output. The CLI is intended for automation, scripting, and file-based reporting.

## Scope

- Add CLI commands for import and report operations.
- Support saved output to plain text, CSV, JSON, or Markdown.
- Keep the CLI thin and presentation-focused.
- Reuse the library query and repository services.

## Design constraints

- The CLI must not contain data model logic.
- It must not directly construct the SQLite schema or inspect raw JSON beyond argument validation.
- All operational logic must be delegated to the library layer.

## Acceptance criteria

- The CLI can ingest runs from a directory and write into SQLite.
- The CLI can generate a saved report in a file.
- The CLI can use the same queries that the GUI uses.
- Output is deterministic and suitable for automation.

## Example pytest cases

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
    result = runner.invoke(
        cli,
        ["report", "summary", "--db", "instance/runs.db", "--output", str(output_path)],
    )

    assert result.exit_code == 0
    assert output_path.exists()
```

## Definition of done

This milestone is complete when the CLI offers file-based reporting and import workflows without duplicating the business logic of the library.
