# Learning foundation reset

**Goal:** Give the owner a small, runnable Android project they can understand before adding app behavior.

**Approved direction:** The architecture review and the owner's request authorize a staged reset. Five modules remain the eventual data-and-persistence target; the first learning checkpoint has only three active modules. No dormant data modules or placeholder frameworks are included.

**Recovery:** The full pre-reset source is committed at `9445e42` on `codex/pre-reset-2026-10-30`. Work continues on `codex/foundation-reset`. Nothing is pushed. Keep `.stitch` as a product reference. Do not uninstall the app, clear device data, or delete existing database files.

## Starting checkpoint

- `app`: activity, app theme, and an explicit call into the books feature.
- `feature:books`: a small book model, clearly named sample catalogue, and a stateless Compose list with realistic light/dark previews.
- `core:designsystem`: the existing Material colors, interface font, shapes, and theme.
- A native launch smoke test verifies the actual activity displays the sample catalogue.
- No networking, database opening, saving, navigation, ViewModel, Hilt, paging, or coroutine scaffolding in this checkpoint. These are separate learning milestones.
- Keep application ID, SDK levels, bytecode targets, Gradle/AGP/Kotlin versions, launcher resources, and bundled font licenses.

## Execution

- [x] Preserve tracked and untracked source in a recovery commit and label its branch.
- [x] Add `app/src/androidTest/java/com/veritalex/CatalogueSmokeTest.kt`; run it against the old app and confirm the sample-catalogue assertion fails.
- [x] Replace `feature:home` with `feature:books`; implement `Book.kt`, `SampleCatalogue.kt`, `BooksScreen.kt`, feature strings, and a minimal Android library build.
- [x] Simplify `app/MainActivity.kt` and `app/build.gradle.kts`; remove Hilt application/registration and old app navigation.
- [x] Remove the old data, database, network, datastore, navigation, and home source from the active checkout after confirming the recovery branch contains it.
- [x] Remove unused design-system components/icons/reader typography; keep the current theme and interface font.
- [x] Reduce `settings.gradle.kts`, root plugin declarations, and `libs.versions.toml` to dependencies used by the three modules. Ignore nested `build/` directories.
- [x] Delete arithmetic and package-name template tests. Keep one actual activity smoke test.
- [x] Replace the outdated README, add `docs/LEARNING_PATH.md`, and annotate earlier plans as historical.
- [x] Build debug and release, run lint and the launch smoke test, inspect the screen in light/dark and at large text, and review the final dependency graph and diff.

## Completion checks

```sh
rtk proxy ./gradlew testDebugUnitTest :app:assembleDebug :app:assembleRelease :app:lintDebug --console=plain
rtk proxy ./gradlew :app:connectedDebugAndroidTest --console=plain
rtk proxy ./gradlew projects --console=plain
```

Expected: successful builds, zero lint errors/warnings, one passing activity smoke test, and exactly the three named Android modules. There is deliberately no unit-testable business logic yet, and no template tests inflate the reported count.

The learning guide must explain the current source path, the difference between modules and packages, Kotlin/Compose foundations, later coroutine ownership and cancellation, when data/database modules are introduced, and completion criteria for the first durable save/offline workflow.

## Verification record

- Clean debug/release builds, UI-test APK assembly, and unit-test task configuration succeeded. There are no unit tests yet because this checkpoint has no business logic.
- The activity smoke test failed against the old app because the sample-catalogue label was absent, then passed on the reset app: 1 test, 0 failures, 0 errors on an API 35 emulator.
- Final debug/release assembly and lint passed after adding a paper background to the previews. Lint reports 0 issues.
- Removing old direct dependencies exposed Lifecycle 2.9.4's incompatible lint checks. Restoring the existing 2.11.0 runtime pin across the UI modules fixed the warning; no lint checks were suppressed.
- AGP's initial connected-test cleanup removed its installed APK from the dedicated emulator. The supported `android.injected.androidTest.leaveApksInstalledAfterRun` option is now enabled; a subsequent test passed and both app/test packages remained installed. No physical device was used.
- Inspected light appearance and dark appearance with 200% text: all sample titles/authors remain readable without clipping. Restored font scale 1.0 and light appearance afterward.
- Independent specification and code-quality reviews approved the reset; the minor preview-background issue was corrected.
- Confirmed `.stitch`, the wrapper and Gradle daemon JVM configuration are unchanged from the recovery checkpoint. All removed tracked source paths exist in that checkpoint.
- Android Studio GUI sync and remote GitHub Actions were not run. The current command-line build and local emulator checks passed.
