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
