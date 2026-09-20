# Ticket 04: Create the SQLite repository and migration layer

## Goal

Implement the persistence layer responsible for schema creation, table writes, incremental ingestion, and data validation.

## Scope

- Create and manage SQLite schema
- Write normalized rows to the correct tables
- Maintain a migration system for schema changes
- Skip duplicate ingest based on run_id
- Expose methods for inserting or replacing run data

## Responsibilities

The repository owns the behaviour below:

- open and close SQLite connections
- create tables if absent
- enforce idempotent inserts for existing run_id values
- validate required columns before insert
- map row groups to their corresponding tables
- support migration scripts for future schema evolution

## Data integrity requirements

- Each run_id must be unique within runs.
- Child tables must refer to a valid run_id.
- Player rows must refer to a valid run_id and player_id.
- New schema changes must be introduced through migrations, not by ad hoc edits to the live database.

## Acceptance criteria

- A fresh database can be created from the schema contract.
- A sample run can be inserted without manual SQL.
- Re-running ingestion for the same run_id does not duplicate the run.
- Child rows are inserted into the correct tables with stable identifiers.
- The repository can be used independently of the CLI and GUI layers.

## Test-first approach

- Add a failing test that creates an empty database and inserts a sample run.
- Add a failing test that verifies duplicate run_id values are not inserted twice.
- Add a failing test that validates an expected child table receives the relevant row payload.
- Add a failing test that checks the repository can replace or migrate schema safely.

## Definition of done

- The repository is the sole owner of SQLite access patterns.
- The parser does not construct SQL directly.
- The database layer is reusable by CLI and GUI code.
