# Milestones

This folder contains a decomposed view of the project execution plan for the sts2-runner refactor. Each milestone describes a bounded engineering increment, the required scope, the acceptance criteria, and example pytest cases.

## Milestone index

- [01-package-foundations.md](01-package-foundations.md)
- [02-schema-contract.md](02-schema-contract.md)
- [03-json-ingestion-and-normalization.md](03-json-ingestion-and-normalization.md)
- [04-sqlite-repository-and-migrations.md](04-sqlite-repository-and-migrations.md)
- [05-reporting-and-analysis-queries.md](05-reporting-and-analysis-queries.md)
- [06-cli-presentation-layer.md](06-cli-presentation-layer.md)
- [07-fastapi-gui-layer.md](07-fastapi-gui-layer.md)
- [08-end-to-end-validation-and-regression.md](08-end-to-end-validation-and-regression.md)
- [09-cross-platform-binary-packaging.md](09-cross-platform-binary-packaging.md)
- [10-autodoc-and-documentation.md](10-autodoc-and-documentation.md)

## Execution order

The milestones are intentionally ordered to preserve a safe build sequence. Each milestone depends on the contracts and decisions established by the earlier milestones.

1. Package foundations and public contracts
2. Schema contract and data mapping design
3. Raw JSON ingestion and normalization
4. SQLite repository and migration behaviour
5. Reporting and analysis queries
6. CLI presentation layer
7. FastAPI GUI layer
8. End-to-end validation and regression
9. Cross-platform binary packaging
10. Autodocumentation and final documentation pass

## Relationship to the specification

The main specification remains in [../TECHNICAL_SPECIFICATION.md](../TECHNICAL_SPECIFICATION.md). This milestone folder is intended to make the plan easier to track and execute in smaller, reviewable chunks.
