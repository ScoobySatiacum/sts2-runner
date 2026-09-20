# Ticket 05: Build the query and analysis layer for reporting and data science

## Goal

Create a reusable query layer that supports both operational reporting and broader data analysis on the persisted dataset.

## Scope

- Expose reusable read operations for run-level and aggregated data
- Support single-run and multi-run queries
- Provide a clean interface for Polars-based analysis
- Keep database reads separate from UI rendering

## Architectural requirement

This layer must work for both reporting and analysis without coupling to any specific presentation format.

## Proposed capabilities

- run lookup by run_id
- player summaries by run
- win/loss summaries by character
- choice frequency analysis
- relic distribution analysis
- map progression summaries
- aggregate trend analysis across many runs

## Data analysis approach

- Keep SQLite as the canonical storage layer.
- When analytical transforms are needed, use Polars DataFrames over query results.
- The query layer should return data ready for downstream use by reports and notebooks.

## Acceptance criteria

- The query layer can fetch a single run for report generation.
- The query layer can aggregate across all runs for dataset analysis.
- Query results can be converted to Polars without leaking DB logic into UI code.
- The presentation layers rely only on service methods, not direct SQL.

## Test-first approach

- Add failing tests for aggregate win/loss queries.
- Add failing tests for player-level summary queries.
- Add failing tests verifying a report query and an analysis query use the same data contract.

## Definition of done

- Query services exist for both reporting and analytics.
- Polars can be used on top of repository reads without reworking the schema.
- CLI and GUI presentation layers can consume the same query interfaces.
