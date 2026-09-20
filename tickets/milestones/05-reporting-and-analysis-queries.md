# Milestone 5: Reporting and analysis queries

## Objective

Create the query layer that supports both operational reporting and broader data analysis. The query layer is the boundary between the canonical database and the presentation layer.

## Scope

- Create read operations for single-run summaries.
- Create aggregate queries for broader analysis across all runs.
- Support conversion to Polars DataFrames for dataset-level transformations.
- Keep SQL access inside the library layer and out of the presentation code.

## Design constraints

- The same query services should be usable by both CLI and GUI components.
- SQL should not be embedded in the reporting or API layers.
- Polars should be used for tabular analysis, not as the storage model.

## Example query categories

- run lookup by run_id
- win/loss by character
- relic distribution across runs
- room progression or act summaries
- aggregate choice distributions
- trend analysis across run history

## Acceptance criteria

- The query layer can fetch a single run for report generation.
- The query layer can aggregate over the full dataset for analysis.
- Query results can be converted to Polars DataFrames without leaking database logic into the presentation layer.

## Execution checklist

### Preconditions

- [ ] Confirm the repository exposes stable read access and returns predictable database records.
- [ ] Define the report and analysis questions before writing SQL.
- [ ] Identify which results are single-run reports and which are dataset aggregates.

### Implementation

- [ ] Implement a query for one run by `run_id`.
- [ ] Implement a query for run summaries and related child records.
- [ ] Implement win/loss aggregates by character.
- [ ] Implement relic, card, map, and choice aggregate queries that match available data.
- [ ] Keep SQL statements inside query modules or repository read methods.
- [ ] Define stable result shapes for CLI and GUI consumers.
- [ ] Implement conversion from query results to Polars DataFrames at the analysis boundary.
- [ ] Handle empty datasets without raising presentation-layer errors.
- [ ] Document query ordering and null behavior.

### Tests and validation

- [ ] Write failing tests for every public query before implementation.
- [ ] Test single-run results against known sample data.
- [ ] Test aggregate results across win, loss, and multiplayer samples.
- [ ] Test empty database behavior.
- [ ] Test Polars column names and data types at the analysis boundary.
- [ ] Run focused query tests, the full pytest suite, and Ruff.

### Documentation and completion evidence

- [ ] Document supported report and analysis query contracts.
- [ ] Record the first analysis result and any interpretation limits in private learning notes.
- [ ] Update development status with query coverage and validation evidence.
- [ ] Mark the milestone complete only when both CLI and GUI can consume the same query services.

## Example pytest cases

```python
# tests/test_queries.py

def test_query_returns_run_summary(repo):
    summary = repo.get_run_summary("abc123")

    assert summary["run_id"] == "abc123"
    assert "win" in summary


def test_analysis_query_returns_character_distribution(repo):
    df = repo.get_character_win_rate_df()

    assert "character" in df.columns
    assert "win_rate" in df.columns
```

## Definition of done

This milestone is complete when both single-run reports and multi-run analysis can be generated through the same library-level read API. 
