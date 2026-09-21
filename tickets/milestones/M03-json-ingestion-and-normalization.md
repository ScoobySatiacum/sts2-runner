# Milestone 3: JSON ingestion and normalization

## Objective

Build the ingestion pipeline that reads raw .run files and converts them into explicit normalized row payloads ready for persistence. This milestone separates the parsing concern from the database concern.

## Scope

- Read raw JSON from the .run files.
- Validate the structure and top-level sections.
- Extract run metadata and nested collections.
- Normalize nested lists and dicts into row-based outputs.
- Assign stable identifiers such as run_id, player_id, and choice_id.

## Design constraints

- The parser must not own the SQLite schema or database lifecycle.
- The output of the parser should be explicit and testable.
- The normalization phase must preserve all relevant raw data and not collapse it into a lossy summary model.

## Proposed flow

1. Load the JSON file.
2. Validate the file format and required sections.
3. Build a run model instance.
4. Extract nested records into row groups.
5. Emit normalized payloads for persistence.

## Acceptance criteria

- A sample .run file can be parsed without writing to SQLite.
- A row collection is returned for each logical table family.
- The parser assigns consistent identifiers to all child rows.
- No essential source data is silently dropped.

## Execution checklist

### Preconditions

- [ ] Confirm the schema contract identifies every row group required from the source data.
- [ ] Select representative win, loss, and multiplayer samples for parser tests.
- [ ] Confirm parsing code has no SQLite imports.

### Implementation

- [ ] Implement a loader that reads one `.run` file and returns a raw payload.
- [ ] Add clear exceptions for missing files, invalid JSON, and unsupported top-level shapes.
- [ ] Validate required metadata without rejecting valid optional fields.
- [ ] Implement a canonical run envelope with the source `run_id`.
- [ ] Normalize each top-level scalar section into its defined row group.
- [ ] Normalize each nested list into child rows with stable parent identifiers.
- [ ] Preserve source array order in an explicit ordinal column.
- [ ] Preserve unknown or uninterpreted values according to the schema contract.
- [ ] Ensure normalization is deterministic for the same input file.
- [ ] Return parse output without opening or writing a database.

### Tests and validation

- [ ] Write failing loader tests before implementing loader behavior.
- [ ] Test valid win, loss, and multiplayer samples.
- [ ] Test malformed JSON and missing required sections.
- [ ] Test empty and optional nested collections.
- [ ] Test stable identifiers and source ordering.
- [ ] Test that parsing does not create or modify a SQLite database.
- [ ] Run focused parser tests, the full pytest suite, and Ruff.

### Documentation and completion evidence

- [ ] Document the raw payload, canonical envelope, and normalized row-group contracts.
- [ ] Record any source-data assumptions in the private learning notes.
- [ ] Update development status with sample coverage and validation results.
- [ ] Mark the milestone complete only when repository code can consume the parse output directly.

## Example pytest cases

```python
# tests/test_run_loader.py
from pathlib import Path


def test_load_run_file_returns_run_envelope():
    path = Path("tests/samples/win.run")
    run = load_run_file(path)

    assert run.run_id == "win"
    assert run.players is not None
    assert run.map_point_history is not None


def test_normalizer_creates_player_and_map_row_groups():
    run = load_run_file(Path("tests/samples/win.run"))
    rows = normalize_run(run)

    assert "players" in rows
    assert "map_points" in rows
    assert len(rows["players"]) > 0
```

## Definition of done

This milestone is complete when the parse output is explicit, stable, and directly usable by the repository layer without additional transformation logic.
