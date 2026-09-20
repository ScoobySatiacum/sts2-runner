# Milestone 9: Cross-platform binary packaging

## Objective

Define and implement the build process required to produce executable binaries for macOS, Debian Linux, and Windows. This milestone ensures that the project can be distributed as a native executable, not only as a Python package or source tree.

## Scope

- Add a packaging tool configuration for native binary builds.
- Prefer PyInstaller as the default tool for the CLI binary.
- Define the build commands and expected outputs for each target platform.
- Verify the packaged binary runs successfully with a smoke test.

## Design constraints

- The build system must be repeatable and versioned.
- The application logic must remain separate from packaging details.
- Generated build artifacts must not be committed to source control.
- The project must remain usable through uv for local development while also supporting binary distribution.

## Recommended approach

Use PyInstaller for the CLI application because it is straightforward for a Python console tool and supports the cross-platform requirement.

Example build command:

```bash
uv add --dev pyinstaller
uv run pyinstaller --name sts2-runner --onefile --console src/sts2/cli/__main__.py
```

## Platform-specific expectations

- macOS: produce a single-file executable or .app package for the target architecture
- Debian Linux: produce a standalone executable or Debian package if desired
- Windows: produce a .exe binary with the same CLI contract

## Acceptance criteria

- The project can generate a standalone binary for the CLI entry point.
- The build is captured in project documentation and can be repeated.
- The binary responds to `--help` or equivalent smoke checks without requiring a source checkout.
- Packaging does not change the underlying library architecture.

## Example smoke test

```bash
./dist/sts2-runner --help
```

## Definition of done

This milestone is complete when the project has a repeatable binary build path for all required target platforms and the build process is documented in the project setup documentation.
