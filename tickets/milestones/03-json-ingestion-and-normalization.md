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
