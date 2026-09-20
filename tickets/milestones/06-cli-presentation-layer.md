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

## Execution checklist

### Preconditions

- [ ] Confirm ingest, repository, and query service interfaces are stable.
- [ ] Choose the CLI framework and document the choice.
- [ ] Define command names, arguments, exit codes, and output formats before implementation.

### Implementation

- [ ] Add a package entry point for the CLI.
- [ ] Implement an ingest command that delegates to the ingestion service.
- [ ] Implement a single-run report command.
- [ ] Implement an aggregate report or analysis command.
- [ ] Implement output destinations for stdout and files.
- [ ] Implement JSON, CSV, Markdown, or text serialization according to the defined contract.
- [ ] Return nonzero exit codes for invalid paths, invalid arguments, and service failures.
- [ ] Keep SQL, parsing, and business rules out of command functions.
- [ ] Ensure output is deterministic for the same database state.

### Tests and validation

- [ ] Write failing CLI invocation tests before implementing commands.
- [ ] Test help output and invalid arguments.
- [ ] Test ingest against a temporary database.
- [ ] Test report output to stdout and a file.
- [ ] Test each supported serialization format.
- [ ] Test failure exit codes and useful error messages.
- [ ] Run focused CLI tests, the full pytest suite, and Ruff.

### Documentation and completion evidence

- [ ] Document every command, option, output format, and exit code.
- [ ] Add at least one copyable CLI workflow to the contributor guide.
- [ ] Record CLI design lessons in private learning notes.
- [ ] Update development status with command and validation evidence.
- [ ] Mark the milestone complete only when the CLI uses library services exclusively.

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
