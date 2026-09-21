# ADR-002: GitHub as task tracking system

- Status: accepted
- Date: 2026-09-20
- Related milestones: all

## Context

The project needs task tracking that works for both a human contributor and AI-assisted development. Markdown is useful for durable plans and Obsidian notes, but active task state should not be duplicated across multiple local documents.

## Decision

Use GitHub Issues and GitHub Milestones for active task tracking. Use stable task IDs such as `M01-T07` in issue titles, branches, commits, and pull requests. Keep Markdown milestone files for scope, dependencies, checklists, decisions, and completion evidence.

## Alternatives considered

- Use only Markdown checkboxes.
- Use a separate project-management application.
- Use GitHub Issues without a durable local milestone specification.

The selected approach keeps active state collaborative while preserving the technical plan in version control.

## Consequences

- GitHub access is required to see current task state.
- The repository must keep issue links and milestone files aligned.
- Local documents should not duplicate issue status.
- Pull requests should close or reference task issues explicitly.
