# Veritalex

A personal Android reading app and learning project. The native code currently provides the catalogue and saved-book foundation. The approved MVP design is in [.stitch/HANDOFF.md](.stitch/HANDOFF.md); open [.stitch/index.html](.stitch/index.html) to browse the design states.

## Build and check

Install Temurin JDK 25 LTS and Android SDK 37. The wrapper selects JDK 25 through `gradle/gradle-daemon-jvm.properties`; CI also installs current Temurin 25 and SDK 37. Use Android Studio Rabbit 2 (2026.2.2) or newer for AGP 9.5; the installed Studio is on that compatible line. No Firebase configuration is required.

```sh
./gradlew testDebugUnitTest :app:assembleDebug :app:lintDebug
./gradlew :app:assembleRelease
ANDROID_SERIAL=emulator-5554 ./gradlew :core:database:connectedDebugAndroidTest
```

Use the actual emulator serial from `adb devices` for the last command. Database instrumentation tests cover author/translator membership, repeated imports and preservation of version-1 records during migration. Network tests use a local HTTP server; they do not require Gutendex to be online.

## Maintenance decisions

The current stable baseline is AGP 9.5.0, Gradle 9.8.2, Kotlin 2.4.21, KSP 2.3.13, Hilt 2.60.1 and Temurin JDK 25 LTS (verified with 25.0.5). All modules compile against SDK 37; the app targets 37 and still supports API 30+. Kotlin uses AGP's built-in support and new DSL, with the documented root compiler override to 2.4.21. The legacy Kotlin Android plugin and DSL opt-outs are absent. See the [AGP 9.5 compatibility table](https://developer.android.com/build/releases/agp-9-5-0-release-notes?hl=en) and [built-in Kotlin migration guide](https://developer.android.com/build/migrate-to-built-in-kotlin).

Java/Kotlin bytecode stays at JVM 17 for Android compatibility; that is separate from the JDK used to run Gradle. Gradle's own embedded Kotlin version shown by `./gradlew --version` is also separate from the app compiler pinned in the version catalog.

Compose BOM 2026.09.00, Core 1.19.1, Lifecycle 2.11.0, Navigation 3 1.2.0, AndroidX Hilt Compose 1.4.0, Serialization 1.12.0, OkHttp 5.5.1 and Coil 3.6.3 replace the older compatibility pins. Coil includes its explicit OkHttp networking module; HTTP regression tests use MockWebServer 3. Direct versions were checked against official Maven release metadata. Existing Room, Paging, Retrofit, DataStore, Gson and JUnit dependencies were already on their current stable releases.

Unused Firebase analytics, the Google Services plugin, downloadable fonts, duplicate dependencies and stale generated theme variants were removed. The version catalog owns library versions; app bytecode targets JVM 17. Both the Gradle distribution and wrapper JAR were checked against official SHA-256 values.

## Design system and learning boundary

`:core:designsystem` implements the approved warm-paper and Night Material 3 roles, Roboto Flex interface typography, Literata prose/chapter styles, 4/16/28 dp cover/card/sheet shapes and 16/20 dp compact/regular gutters. Fonts and their OFL licenses ship with the app and work offline. `VeritalexTheme` follows device appearance; optional dynamic color remains available through its existing parameter. Use semantic Material roles in feature code.

The shell uses Home, Explore and Library, with Settings in the toolbar and a navigation rail on wider windows. Existing catalogue/saved-book UI is reused; there is no fabricated reading progress or sample saved collection. Missing covers have a typeset fallback. Loading failures offer retry.

Book details and save actions, a reader with independent paper settings, Library shelves/journal, and optional account/sync are still learning work. Settings currently only describes the actual system appearance behavior. The design gallery contains these future flows; it does not mean they are implemented in Android.

The version-2 Room migration preserves existing books and people. Version 1 never stored reliable author/translator memberships, so those are rebuilt from catalogue responses rather than guessed from unrelated IDs. It never clears the database or saved-book preferences.

## Verified on October 30, 2026

Debug and release APKs build on JDK 25.0.5; all 17 unit tests and 3 database instrumentation tests pass. Lint reports zero errors and zero warnings. Gradle configuration (`help`), the full task graph (`build --dry-run`) and resolved compiler checks passed: AGP’s bundled Kotlin dependency resolves to 2.4.21. The packaged APK confirms compile/target SDK 37.

Android 17 / API 37 verification used a 16 KB page-size emulator: actual network book covers loaded through Coil 3, tab/Settings/Back navigation and launcher-based process restoration worked, light/Night appearance and 200% text were checked, and a fresh cold launch survived 30 seconds with the same process resumed and no fresh crash recorded. Android Studio GUI sync and remote GitHub Actions were not automated.
