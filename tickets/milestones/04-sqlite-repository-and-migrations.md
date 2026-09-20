# Milestone 4: SQLite repository and migration behaviour

## Objective

Create the persistence layer that writes the normalized row groups into SQLite and manages the schema lifecycle. This milestone ensures that the database remains the canonical source of truth and that ingestion is repeatable and safe.

## Scope

- Create or validate the SQLite schema from the schema contract.
- Insert normalized rows into the correct table families.
- Enforce run_id uniqueness and duplicate protection.
- Provide migration support for future schema changes.

## Design constraints

- The repository is the only component allowed to write to SQLite.
- Parsing and presentation code must not issue direct SQL statements.
- Duplicate imports must be prevented by design.
- The repository must support future migration-aware evolution of the schema.

## Acceptance criteria

- A new SQLite database can be created from the schema contract.
- A sample run can be inserted without manual SQL.
- Re-running ingestion for the same run_id does not create duplicate records.
- Child rows are inserted into the correct related tables.

## Example pytest cases

```python
# tests/test_sqlite_repository.py

def test_repository_creates_database_and_inserts_run(tmp_path):
    db_path = tmp_path / "runs.db"
    repo = SqliteRunRepository(db_path)

    run_rows = [{"run_id": "abc123", "win": 1, "character": "IRONCLAD"}]
    repo.insert_runs(run_rows)

    assert db_path.exists()
    assert repo.get_run_count() == 1


def test_repository_skips_duplicate_run_id(tmp_path):
    db_path = tmp_path / "runs.db"
    repo = SqliteRunRepository(db_path)

    repo.insert_runs([{"run_id": "abc123", "win": 1}])
    repo.insert_runs([{"run_id": "abc123", "win": 1}])

    assert repo.get_run_count() == 1
```

## Definition of done

This milestone is complete when the repository owns all SQLite write operations and can safely create or migrate the schema without additional parsing logic.
