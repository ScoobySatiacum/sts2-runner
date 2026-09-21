# Ticket 03: Build the ingestion and normalization pipeline from .run files

## Goal

Implement a robust parse pipeline that reads raw .run files and converts them into normalized domain objects ready for database persistence.

## Scope

- Read raw JSON from .run files
- Validate format and required top-level sections
- Normalize nested lists and dictionaries into stable row data
- Assign stable identifiers such as run_id, player_id, and event identifiers
- Expose parsing results as reusable data structures

## Architectural requirement

The parse layer must not own database creation or CLI reporting logic. Its job is to convert raw input to normalized records.

## Proposed flow

1. Load raw JSON from file.
2. Validate the structure.
3. Create a RunEnvelope or equivalent model.
4. Extract run metadata.
5. Extract players and nested player data.
6. Extract map history and room data.
7. Extract choice records, modifiers, and other aggregated object arrays.
8. Produce row collections ready for repository insertion.

## Output contract

The parser should return a collection of row groups or table payloads, such as:

- run_rows
- player_rows
- relic_rows
- map_point_rows
- room_rows
- choice_rows
- modifier_rows

This output should be explicit and testable.

## Acceptance criteria

- A sample .run file can be parsed without writing to SQLite.
- All nested collections identified in the schema contract are emitted as row collections.
- Each output row contains the run_id and all other identifiers needed for relational consistency.
- The parser does not depend on the DB layer or the UI layer.

## Test-first approach

- Add a failing test that parses a known win sample and verifies required run metadata is present.
- Add a failing test for a multiplayer sample to ensure player rows and associated identifiers are preserved.
- Add a failing test for nested choice data to ensure rows are emitted for the choice tables.
- Add a failing test for a loss sample to ensure the parser preserves loss-specific data.

## Definition of done

- The parser produces explicit normalized row payloads.
- The output contract matches the schema contract.
- The repository layer can insert the parsed rows without additional data-shaping logic.
