# Milestone 8: End-to-end validation and regression control

## Objective

Validate the full data flow from .run file to normalized SQLite storage to report generation and analysis. This milestone closes the refactor with a disciplined test and regression strategy.

## Scope

- Run the full pytest suite for relevant components.
- Validate the ingestion path, storage, query, CLI, and GUI integration.
- Check for hidden coupling and regressions introduced by the refactor.
- Confirm that the system remains easy to extend.

## Design constraints

- All milestones must be validated before proceeding to the next engineering increment.
- No major refactor step should rely solely on manual inspection.
- Test coverage should include the end-to-end user flow from raw file to output.

## Acceptance criteria

- The full project pipeline can ingest real sample run files and produce queryable output.
- The CLI and GUI consume the same underlying services.
- Reports and analysis outputs are consistent with the underlying database.
- The test suite is green for the refactor scope.

## Execution checklist

### Preconditions

- [ ] Confirm Milestones 1 through 7 have documented completion evidence.
- [ ] Identify the supported end-to-end workflows that must not regress.
- [ ] Confirm representative sample data is available and safe to use in tests.

### Integration validation

- [ ] Test raw `.run` file ingestion into a temporary SQLite database.
- [ ] Test querying a single imported run.
- [ ] Test aggregate analysis across multiple imported runs.
- [ ] Test CLI output from the imported database.
- [ ] Test GUI responses from the same imported database.
- [ ] Verify CLI and GUI results agree for the same query.
- [ ] Verify repeated ingestion does not duplicate data.
- [ ] Verify a failed import does not leave partial rows.
- [ ] Verify the package remains importable without starting either presentation layer.

### Quality gates

- [ ] Run the focused integration tests.
- [ ] Run the complete pytest suite.
- [ ] Run Ruff check and format check.
- [ ] Build the package with uv.
- [ ] Review public API docstrings and changed documentation.
- [ ] Review the final diff for unrelated changes or generated artifacts.

### Documentation and completion evidence

- [ ] Record the end-to-end commands and results in development status.
- [ ] Record any remaining test gaps and their rationale.
- [ ] Update the engineering plan if integration testing changed an architectural decision.
- [ ] Mark the milestone complete only when the full supported workflow is reproducible from a clean environment.

## Example pytest cases

```python
# tests/test_end_to_end.py

def test_pipeline_ingests_run_and_generates_report(tmp_path):
    db_path = tmp_path / "runs.db"
    ingest_runs("tests/samples", db_path)

    summary = build_run_summary(db_path)

    assert summary is not None
    assert len(summary["runs"]) > 0
```

## Definition of done

The milestone is complete when the end-to-end workflow is verified and the project is stable enough to continue with future feature work without breaking the architecture.
