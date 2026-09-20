# Ticket 06: Build the CLI presentation layer for saved file output

## Goal

Deliver a CLI that exposes the project library in a user-friendly, scriptable form and supports saved output to a file.

## Scope

- Provide commands for importing .run files into SQLite
- Provide commands for querying run summaries
- Provide commands for exporting reports to file
- Support plain text, CSV, JSON, and optionally Markdown output

## Requirements

- The CLI must be a thin presentation layer over the library.
- It must not contain data model logic.
- It must support file output for automation or documentation workflows.
- It must be testable separately from the GUI.

## Proposed commands

- sts2 ingest <input-dir> --db <path>
- sts2 report run --run-id <id>
- sts2 report summary --db <path>
- sts2 export --format csv|json|md --output <path>

## Acceptance criteria

- The CLI can execute a complete import workflow from a directory of .run files.
- It can render a run summary and persist the output to a file.
- It can invoke the same query layer used by the GUI.
- Each command has pytest coverage for valid and invalid use cases.

## Test-first approach

- Add failing tests for CLI argument parsing.
- Add failing tests for file-output generation.
- Add failing tests for invalid database and missing run_id inputs.

## Definition of done

- The CLI is stable and scriptable.
- Output can be saved to file without requiring a GUI.
- The CLI layer does not duplicate any database logic.
