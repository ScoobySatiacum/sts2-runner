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

## Execution checklist

### Preconditions

- [ ] Confirm the schema contract and normalized row groups are approved.
- [ ] Confirm the repository is the only component responsible for SQLite writes.
- [ ] Use a temporary database for repository tests.

### Implementation

- [ ] Implement database creation from the schema contract.
- [ ] Enable SQLite foreign-key enforcement for every connection.
- [ ] Implement an explicit schema version table or equivalent migration marker.
- [ ] Implement migrations as ordered, repeatable operations.
- [ ] Implement insertion for the parent `runs` row.
- [ ] Implement insertion for each child row group.
- [ ] Wrap one run import in a transaction.
- [ ] Enforce `run_id` uniqueness at the database level.
- [ ] Define the duplicate-import result and expose it to callers.
- [ ] Roll back the full import when a child-row insert fails.
- [ ] Keep connection lifecycle and SQL statements inside the repository module.

### Tests and validation

- [ ] Write failing repository tests before implementing writes.
- [ ] Test database creation and schema version initialization.
- [ ] Test parent and child inserts with foreign keys enabled.
- [ ] Test duplicate `run_id` behavior.
- [ ] Test transaction rollback after an insertion failure.
- [ ] Test migration from the previous schema version.
- [ ] Run focused repository tests, the full pytest suite, and Ruff.

### Documentation and completion evidence

- [ ] Document repository methods and transaction behavior.
- [ ] Document migration ordering and upgrade expectations.
- [ ] Record the first persistence failure and its resolution in private learning notes.
- [ ] Update development status with schema and transaction validation evidence.
- [ ] Mark the milestone complete only when all SQLite writes pass through the repository.

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
