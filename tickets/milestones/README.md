# Milestones

This folder contains a decomposed view of the project execution plan for the sts2-runner refactor. Each milestone describes a bounded engineering increment, the required scope, the acceptance criteria, example pytest cases, and an execution checklist.

## How to use a milestone

Work through the checklist from top to bottom. A human or AI contributor should:

1. Confirm the preconditions before editing.
2. Complete implementation items one at a time.
3. Add or update tests before declaring behavior complete.
4. Run the stated validation commands.
5. Record decisions and evidence in the milestone ticket and development status.
6. Mark the milestone complete only when its definition of done is demonstrably true.

Checklist items are intentionally small enough to become individual commits, pull-request tasks, or AI prompts. When a checklist item reveals a new design decision, pause implementation and document the decision before continuing.

## Canonical tracking rule

GitHub Issues are the task tracker and source of truth for active work. Each issue should reference one stable task ID such as `M01-T03` and one milestone such as `M01`.

These Markdown milestone files are the durable engineering plan. They define scope, dependencies, checklist order, acceptance criteria, and completion evidence. They are not a second task board.

## Milestone index

- [M01-package-foundations.md](M01-package-foundations.md)
- [M02-schema-contract.md](M02-schema-contract.md)
- [M03-json-ingestion-and-normalization.md](M03-json-ingestion-and-normalization.md)
- [M04-sqlite-repository-and-migrations.md](M04-sqlite-repository-and-migrations.md)
- [M05-reporting-and-analysis-queries.md](M05-reporting-and-analysis-queries.md)
- [M06-cli-presentation-layer.md](M06-cli-presentation-layer.md)
- [M07-fastapi-gui-layer.md](M07-fastapi-gui-layer.md)
- [M08-end-to-end-validation-and-regression.md](M08-end-to-end-validation-and-regression.md)
- [M09-cross-platform-binary-packaging.md](M09-cross-platform-binary-packaging.md)
- [M10-autodoc-and-documentation.md](M10-autodoc-and-documentation.md)

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

## GitHub workflow

1. Create or select the GitHub Issue for one task ID.
2. Add the issue to the matching GitHub Milestone, such as `M01 Package Foundations`.
3. Link the issue to the relevant checklist item in the milestone file.
4. Implement the issue on a branch named `M01-T##-short-description`.
5. Open a pull request using the repository template and link it with `Closes #123`.
6. Close the issue only after the pull request and validation evidence are complete.

Use GitHub labels for workflow state and concern, for example `milestone`, `bug`, `architecture`, `documentation`, `testing`, and `blocked`. Do not create a separate local status board that duplicates GitHub issue state.
