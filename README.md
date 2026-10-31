# Veritalex

A personal Android reading app built one lesson at a time. Start with [the learning path](docs/LEARNING_PATH.md).

## Current checkpoint

The app displays a stateless Compose list of sample books. The titles and authors are real examples, but this screen does not fetch a catalogue, save books or open a reader. The activity passes sample data directly to `BooksScreen`.

Exactly three modules are active:

```text
:app → :feature:books → :core:designsystem
  └──────────────────→ :core:designsystem
```

`app` launches the screen, `feature:books` owns the sample model and UI, and `core:designsystem` supplies the existing theme, interface font and visual tokens. Networking, Room, Hilt, Paging, ViewModels, coroutine scaffolding and navigation are future lessons. There are no dormant copies of those modules in this checkout.

The first real product milestone is **browse → save → Library → relaunch offline**. The learner will implement it incrementally; this checkpoint establishes a small, readable starting point.

## Build and check

Use Temurin JDK 25 and Android SDK 37. The retained toolchain is AGP 9.5.0, Gradle 9.8.2 and Kotlin 2.4.21, with AGP's built-in Kotlin support. The app supports API 30+, targets SDK 37 and emits JVM 17 bytecode. The JDK running Gradle and the Android bytecode target serve different purposes.

Lifecycle runtime remains explicitly pinned to 2.11.0 so its bundled lint checks work with this toolchain. The Compose BOM does not manage Lifecycle versions.

From the repository root:

```sh
rtk proxy ./gradlew testDebugUnitTest :app:assembleDebug :app:assembleRelease :app:lintDebug
rtk proxy adb devices
rtk proxy ./gradlew :app:connectedDebugAndroidTest
```

The last command requires a running emulator or connected device. With several devices, set `ANDROID_SERIAL` to the intended serial before running it. Successful assembly checks compilation and packaging; the connected test checks the displayed sample screen. These commands describe the current checks, not a claim that future features are tested.

There is one activity launch test. Unit-test tasks currently have no business tests; add those with the first ViewModel or repository behavior. Connected tests are configured to leave the app installed. Use a dedicated emulator for testing.

## Design reference and recovery

The approved product and visual reference remains [.stitch/HANDOFF.md](.stitch/HANDOFF.md). Open [.stitch/index.html](.stitch/index.html) to browse it. Its reader, shelves, journal and account flows describe future work.

The complete source before this learning reset, including Room schemas, migrations and tests, is preserved on the local branch `codex/pre-reset-2026-10-30` at `9445e42`. Work continues on `codex/foundation-reset`. Earlier maintenance plans are historical records.

The sample app opens no existing database or preferences and performs no data migration or deletion. The Git checkpoint preserves source code and schemas, not device data; keep separate backups of any records you need.
