# Current stable Android toolchain migration

> Historical record, superseded by the October 30, 2026 learning reset. The active starting point is [the learning path](../../LEARNING_PATH.md). This plan records the pre-reset implementation, preserved on local branch `codex/pre-reset-2026-10-30` at `9445e42`; its feature and validation claims do not describe the current three-module sample checkpoint. See [README](../../../README.md) for the retained toolchain.

The user approved completing the fresh-app baseline. Continue in the existing working tree and preserve the earlier cleanup/theme/navigation work. Keep feature scope unchanged and leave the mixed working tree uncommitted.

- [x] Confirm the prior baseline builds/tests pass; snapshot existing files before migration.
- [x] Verify stable releases through official repositories and use Context7 plus vendor migration documentation.
- [x] Migrate to AGP 9.5.0 with built-in Kotlin 2.4.21 and its new DSL, Gradle 9.8.2, JDK 25 LTS, and SDK/target 37. Remove the legacy Kotlin Android plugin and redundant compiler target blocks; keep Android bytecode compatibility at JVM 17.
- [x] Upgrade Hilt/KSP together and verify compilation/code generation and unit tests.
- [x] Upgrade current stable AndroidX, Compose, serialization and OkHttp dependencies; migrate Coil to 3 with its network module. Verify HTTP tests and image loading.
- [x] Verify Gradle configuration tasks, debug/release builds, unit tests, lint, database migrations and emulator startup/navigation on API 37.
- [x] Update README and CI to describe the resulting versions, verification and any remaining limitations.

Gradle distribution/JAR and downloaded JDK checksums must match vendor metadata. No legacy built-in-Kotlin or DSL opt-out flags, no new feature implementation, and no destructive database changes are part of this migration.

Actual Gradle CLI configuration and task-graph checks passed; GUI IDE sync was not driven. All 17 unit tests, 3 API-37 database tests, debug/release builds and zero-warning lint passed. The Android 17 16 KB emulator verified image loading, navigation, theme/font scaling and clean 30-second startup. Wrapper JAR SHA-256: `3b8a25775a69158b5ad2b1d17a80a88dc7b40a352a73eb27d06c612a7ce68e98`.
Process restoration after a background kill also retained Settings in Library and returned to Library on Back. The installed Android Studio build is on the AGP-9.5-compatible Rabbit 2 line; GUI sync was not automated.
