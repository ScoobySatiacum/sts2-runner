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

## Execution checklist

### Preconditions

- [ ] Confirm the CLI entry point and `--help` behavior are stable.
- [ ] Confirm the package builds successfully with `uv build`.
- [ ] Decide which CPU architectures and artifact formats are required for the first release.

### Implementation

- [ ] Add PyInstaller to the development dependency group.
- [ ] Define the PyInstaller configuration without moving packaging logic into library modules.
- [ ] Build a macOS executable on each supported macOS architecture.
- [ ] Build a Debian Linux executable in a Debian-compatible environment.
- [ ] Build a Windows `.exe` in a Windows environment.
- [ ] Include package resources required by the CLI.
- [ ] Name artifacts using the project name, version, operating system, and architecture.
- [ ] Keep `build/`, `dist/`, and generated spec files out of source control.
- [ ] Add CI or documented local commands for each target platform.

### Tests and validation

- [ ] Run each generated binary with `--help`.
- [ ] Run a minimal ingest or report smoke test for each target platform.
- [ ] Verify the executable does not require a source checkout or active virtual environment.
- [ ] Verify the artifact version matches the Git tag.
- [ ] Record platform-specific limitations and missing-resource failures.

### Documentation and completion evidence

- [ ] Document build prerequisites and commands for all target platforms.
- [ ] Document artifact naming, release storage, and checksum expectations.
- [ ] Record packaging lessons in private learning notes.
- [ ] Update development status with artifact and smoke-test evidence.
- [ ] Mark the milestone complete only when each required platform has a repeatable build.

## Example smoke test

```bash
./dist/sts2-runner --help
```

## Definition of done

This milestone is complete when the project has a repeatable binary build path for all required target platforms and the build process is documented in the project setup documentation.
