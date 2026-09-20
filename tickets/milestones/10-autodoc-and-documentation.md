# Milestone 10: Autodocumentation and final documentation pass

## Objective

Complete the project documentation pass so the library remains maintainable, reviewable, and suitable for automated documentation generation. This milestone is intentionally placed at the end of the refactor to avoid documentation drift during earlier implementation work.

## Scope

- Review all public modules, classes, and functions for docstrings.
- Confirm the package architecture and responsibilities are documented clearly.
- Ensure the project is suitable for autodoc generation.
- Update the supporting developer documentation for the current project state.

## Design constraints

- Documentation is part of the implementation, not a final cleanup step.
- Docstrings should be specific and useful to both humans and automation.
- Comments are acceptable only where they remove genuine ambiguity; they are not a substitute for docstrings.
- The final project state must remain understandable to a human maintainer and an AI assistant working within the same repo.

## Acceptance criteria

- Every public module has a module docstring.
- Every public class has a class docstring.
- Every public function and service entry point has a function docstring.
- The project documentation reflects the final architecture and the current workflow.
- The project is ready for future autodoc or MkDocs/Sphinx-style documentation generation.

## Execution checklist

### Preconditions

- [ ] Confirm the final public package layout is stable.
- [ ] Identify every public module, class, function, service, CLI command, and API route.
- [ ] Select the autodoc tool or document why generation is intentionally deferred.

### Documentation implementation

- [ ] Add module docstrings to every public module.
- [ ] Add class docstrings to every public class.
- [ ] Add function docstrings to every public function and service entry point.
- [ ] Document parameters, return values, raised exceptions, and side effects where applicable.
- [ ] Document public CLI commands and API response contracts.
- [ ] Remove stale examples that no longer match the implementation.
- [ ] Keep comments limited to non-obvious implementation decisions.
- [ ] Add or update generated-documentation configuration if selected.

### Tests and validation

- [ ] Run the complete pytest suite.
- [ ] Run Ruff check and format check.
- [ ] Build the package with uv.
- [ ] Run the documentation tool or a docstring coverage check.
- [ ] Review links and code examples for accuracy.
- [ ] Review the public API from a new-contributor perspective.

### Documentation and completion evidence

- [ ] Update the contributor guide and development setup instructions.
- [ ] Record documentation lessons in private learning notes.
- [ ] Update development status with the final documentation validation.
- [ ] Mark the milestone complete only when a new contributor can understand and exercise the public API without source-code archaeology.

## Example documentation standard

```python
class RunFileLoader:
    """Load and validate a Slay the Spire 2 run file.

    Args:
        path: Path to the raw .run file.

    Returns:
        A validated run payload ready for normalization.
    """
```

## Definition of done

This milestone is complete when the codebase is clearly documented, the architecture is stable, and the project is ready for automated documentation generation without requiring a large cleanup effort.
