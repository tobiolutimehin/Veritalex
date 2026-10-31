# Veritalex foundation refresh

> Historical record, superseded by the October 30, 2026 learning reset. The active starting point is [the learning path](../../LEARNING_PATH.md). This plan records the pre-reset implementation, preserved on local branch `codex/pre-reset-2026-10-30` at `9445e42`; its feature and validation claims do not describe the current three-module sample checkpoint. See [README](../../../README.md) for the retained toolchain.

The earlier conservative toolchain pins below are superseded by [the current-toolchain migration](2026-10-30-current-toolchain.md), approved and completed later the same day.

**Goal:** Make the existing learning project runnable with stable dependencies and apply the approved `.stitch/DESIGN.md` system without implementing the MVP.

**Scope:** Preserve the existing modules and unfinished Navigation 3 migration. Keep SDK 36 and the current minimum/target SDK. Use AGP 8.13.2, Gradle 8.14.6, JDK 17, Kotlin 2.3.21 and a compatible stable AndroidX set. Defer AGP 9 and SDK 37. Keep all changes uncommitted because the starting working tree contains user edits in the same files.

- [x] Inspect the working tree, build the baseline, and reproduce startup on an emulator.
- [x] Update the wrapper and compiler/processor group; run debug build and unit tests.
- [x] Update compatible stable libraries, align Compose/Paging versions, remove unused dependency declarations, and remove unused Firebase setup from local/CI builds.
- [x] Fix navigation construction, route registration and ViewModel scope. Preserve destination state across recreation and Back navigation. Verify with focused navigation tests and emulator launch.
- [x] Replace stale generated theme output with approved light/Night Material roles, bundled UI/reading fonts, shapes and reader typography. Retain dynamic-color support.
- [x] Apply these roles to the existing shell/components; remove fake book state and unsupported recommendation claims. Home, Explore and Library are primary destinations; Settings is a toolbar action. Reuse existing catalogue/saved-book UI; leave reader/account/sync/shelves/journal implementation for the owner.
- [x] Run module unit tests, debug/release build checks and Android lint. Check phone light/dark, large text, destination changes and recreation on an emulator, including a fresh 30-second startup survival check.
- [x] Document the exact commands, compatibility pins, validation and remaining feature boundaries.

The approved visual and product spec remains `.stitch/HANDOFF.md`, `.stitch/DESIGN.md` and `.stitch/DESIGN-DARK.md`; this task does not change those designs. Tests focus on crash-prone navigation and any data-loading bug fixed during maintenance. Visual token-only changes use build, lint and emulator review.

Room author/translator membership was also repaired with explicit junction tables, a tested version-1-to-2 migration, and exported schema history. Existing records are preserved. Final validation is recorded in README.md.
