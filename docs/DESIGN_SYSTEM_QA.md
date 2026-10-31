# Native foundation verification

Verified October 30, 2026 on the dedicated **VeritalexMaintenance** Android 15/API 35 arm64 emulator. This verifies the current sample and debug gallery, not future product flows.

## Automated verification

- Debug and release APK assembly passed.
- Debug lint passed for all three modules: no issues found.
- Two JVM contrast tests passed. These exercise many foreground/background pairs in the actual light/dark Material schemes and all reader papers, selections and highlights; they do not simply assert token hex values.
- Seven connected checks passed in the initial foundation verification: sample launch; every button variant’s labels/targets and activation while ready/disabled/loading; labeled icon actions and busy protection; specific field error semantics and search clearing; long book/action text without layout overflow at 200% in a 280dp content measure; independent reader paper with light/dark/dynamic app inputs; gallery theme controls, dark status-bar icon contrast, dialog cancellation, native sheet Back dismissal and visible snackbar feedback.
- The gallery interaction test also passed with actual Android font scale **2.0** and a **320dp** window. The full seven-test final run used restored phone defaults.
- Release DEX inspection confirms the gallery package and debug activity are absent. The normal release sample activity remains unchanged in purpose.
- `git diff --check` passed. The `.stitch` package and active module list were not modified. Existing IDE edits were left alone, including a further `.idea/gradle.xml` change that appeared during the session.

Foundation verification command:

```sh
rtk proxy ./gradlew :app:connectedDebugAndroidTest testDebugUnitTest :app:assembleDebug :app:assembleRelease :app:lintDebug :core:designsystem:lintDebug :feature:books:lintDebug --console=plain
```

Additional narrow-device overlay check:

```sh
rtk proxy ./gradlew :app:connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.class=com.veritalex.GalleryInteractionTest --console=plain
```

Gradle's local reports are under `app/build/reports/androidTests/connected/debug/`, each module’s `build/reports/lint-results-debug.html`, and `core/designsystem/build/reports/tests/testDebugUnitTest/`. Initial connected XML reported 7 tests, 0 failures, 0 errors, 0 skipped. JVM XML reported 2 tests, 0 failures, 0 errors, 0 skipped. The retained JDK/test tooling emits an upstream protobuf `sun.misc.Unsafe` warning; it did not fail those checks and required no dependency upgrade.

## Native visual checks

| Configuration | What was inspected | Evidence |
| --- | --- | --- |
| Phone, about 412dp, light, 100% | Warm semantic palette, readable interface type, native selected controls and safe insets | [Light gallery](qa/design-system/gallery-light.png) |
| 320dp, dark, actual 200% fonts | Full book metadata reflow, readable sample label, cover ellipsis and safe bounds | [Sample catalogue](qa/design-system/books-narrow-200-dark.png) |
| 320dp, dark, actual 200% fonts | Growing pill buttons, retained labels, distinct disabled/loading presentation | [Action states](qa/design-system/actions-narrow-200-dark.png) |
| 840dp tablet window, light, 100% | Two-column gallery, deliberate section gaps and native action states | [Tablet brand](qa/design-system/gallery-tablet-light.png) |
| 840dp tablet window, dynamic, 100% | Wallpaper palette replaces Material roles while type/spacing remain consistent | [Tablet dynamic](qa/design-system/gallery-tablet-dynamic.png) |
| Dark app with system Light, phone, 100% | Literata prose, independently light/sepia/dark paper and selection/highlight specimens; correct system icon contrast | [Reader specimens](qa/design-system/reader-dark-app.png) |

Tablet validation used a resized emulator window, not a separate physical tablet. At 420dpi, the normal display was 1080×2400px; narrow was 840×2100px; tablet was 2205×2625px. Density was not changed. Font scale was restored to 1.0, size override reset, and system night mode restored to No. No app data or database was deleted. Screenshots show scroll positions: partial content at the viewport edge is scrollable, not a fixed-height text layout.

Visual review found and corrected three issues: thumbnail text spilling at enlarged sizes (now constrained with deliberate ellipsis, full metadata outside); busy actions resembling disabled actions (now legible resting colors with disabled activation); and dark gallery system icons following the system’s light setting (now synchronized by the activity). The overlay regression test also exposed a snackbar below the viewport; its host now belongs to the Scaffold.

## Independent review and shared previews

Three independent reviewers inspected the existing source, connected callers, approved design, documentation and verification artifacts. Their A grade means no remaining material code findings for this learning checkpoint; it does not certify every device, IDE or future feature.

| Review | Final grade | Evidence and outcome |
| --- | --- | --- |
| Theme, type and tokens | A | Approved token values match; surface text contrast, true variable-font axes/licenses, theme selection and independent reader papers verified. No findings. |
| Controls and accessibility | A after correction | Found progress label/range on separate accessibility nodes. A device regression failed before the fix and passed afterward for both determinate and indeterminate modes. The native indicator now owns its label and range, with no duplicate label stop. Reviewer rechecked code, regression assertions and passing focused XML. No remaining findings. |
| Shared preview API | A | Checked all declarations/callers, supported nested multipreview behavior, binary retention, theme wrapping and release dependency isolation. Compiled class metadata confirms retained presets and consumer annotations. No findings. |

The shared `preview/VeritalexPreviews.kt` supplies three focused pairs and a six-view aggregate. Existing catalogue and gallery previews now use these presets. Light/dark modes are explicit, including both narrow 200% and tablet variants. The preview artifact is compile-only and the renderer is debug-only; release SDK dependency metadata contains neither `ui-tooling` nor `ui-tooling-preview`. No module, framework or toolchain version was added.

Android Studio’s preview panel was not visually operated during this follow-up. The definitions compile across the module boundary, their nested annotations survive in class files, and the configurations follow the [official multipreview guidance](https://developer.android.com/develop/ui/compose/tooling/previews). Native emulator evidence above remains separate from IDE rendering. See [usage examples](DESIGN_SYSTEM.md#shared-preview-annotations).

The follow-up progress regression passed on API 35: one test with zero failures/errors/skips. The controls reviewer inspected the passing focused XML before temporary files became unavailable. A subsequent whole-suite run competed with another app’s instrumentation on the shared emulator and lost its Compose activity hierarchies; that run is inconclusive and its report replaced the earlier connected report. A separate temporary read-only AVD was prepared, but the emulator processes became unavailable before the isolated rerun began. No eight-test whole-suite pass is claimed. Debug/release builds, lint and contrast checks were rerun successfully without further device setup. No original AVD or app data was deleted.

## Remaining limits

Automated semantics checks do not replace listening with TalkBack or testing a physical keyboard. Manual TalkBack, screen-reader traversal, physical devices, other locales/RTL, API 30 dynamic fallback, API 37 runtime, foldables and an actual tablet were not exercised. Reduced motion uses native Compose/Material behavior; there is no custom motion, and a device-level reduced-motion matrix was not run. Preview definitions compile, while screenshots here are actual emulator renders rather than Android Studio preview exports.

The sample remains sample-only. Gallery controls and overlays have disposable demo state; they do not fetch, save, search a service, remove books, persist settings or implement a reader. Recheck the relevant accessibility and window configurations when real features introduce behavior.
