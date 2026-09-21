# sts2-runner roadmap

This is the canonical roadmap for the refactor. GitHub Issues track task-level progress; this file tracks milestone order, dependencies, and release-level outcomes.

## Milestones

| Milestone | Outcome | GitHub tracking |
| --- | --- | --- |
| M01 | Package foundations and public contracts | GitHub Milestone: `M01 Package Foundations` |
| M02 | Normalized SQLite schema contract | GitHub Milestone: `M02 Schema Contract` |
| M03 | JSON ingestion and normalization | GitHub Milestone: `M03 Ingestion` |
| M04 | SQLite repository and migrations | GitHub Milestone: `M04 Persistence` |
| M05 | Reporting and analysis queries | GitHub Milestone: `M05 Query and Analysis` |
| M06 | CLI presentation layer | GitHub Milestone: `M06 CLI` |
| M07 | FastAPI GUI layer | GitHub Milestone: `M07 GUI` |
| M08 | End-to-end validation and regression | GitHub Milestone: `M08 Integration` |
| M09 | Cross-platform binary packaging | GitHub Milestone: `M09 Packaging` |
| M10 | Autodocumentation and final documentation pass | GitHub Milestone: `M10 Documentation` |

## Operating rules

- Create one GitHub Issue per bounded task, not one issue for an entire milestone.
- Use task IDs such as `M01-T07` in issue titles, branch names, commits, and pull requests.
- Assign every issue to exactly one GitHub Milestone.
- Use this roadmap for sequence and dependency decisions; use GitHub for active state.
- Use the matching file in `tickets/milestones/` for technical scope, checklist order, and completion evidence.
- Record durable architectural decisions in `tickets/decisions/`.
- Record personal learning notes only in the ignored `docs/learning/` directory.

## Current focus

The current implementation branch is `M01`. The first active task is the next unchecked item in [M01-package-foundations.md](milestones/M01-package-foundations.md). Existing package-boundary tests currently define the first red test surface.

## Completion rule

A milestone is complete when all linked GitHub Issues are closed, all checklist items are checked, the milestone validation commands pass, and the completion evidence is recorded in the milestone file and development status.
