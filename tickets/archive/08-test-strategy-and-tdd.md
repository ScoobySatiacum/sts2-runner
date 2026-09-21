# Ticket 08: Define the engineering test strategy and TDD workflow

## Goal

Ensure the project is developed in a disciplined test-first way, with clear regression protection across parsing, storage, analysis, and UI layers.

## Scope

- Establish pytest-based testing strategy
- Define the expected test split between unit, integration, and API tests
- Ensure all new features are introduced with failing tests first
- Validate the library and presentation layers independently

## Required test categories

- Unit tests for parsing and normalization logic
- Integration tests for repository insertion and schema correctness
- Query tests for reporting and analysis functions
- CLI tests for command-line flows and file output
- API tests for GUI backend endpoints

## TDD workflow

1. Write a failing test for a required behaviour.
2. Implement only the minimal code needed to satisfy the test.
3. Refactor while preserving the test contract.
4. Repeat for each feature or bug fix.

## Acceptance criteria

- No task is implemented without a corresponding failing test first.
- The test suite is deterministic and run with pytest.
- Each layer has targeted tests appropriate to that layer.
- Regression safety is maintained across refactor milestones.

## Definition of done

- All major services and commands are covered by pytest tests.
- The test execution workflow is documented for contributors.
- The refactor can proceed in small, validated increments without breaking the wider project.
