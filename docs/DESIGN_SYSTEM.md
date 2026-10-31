# Veritalex’s native visual vocabulary

The foundation implements the approved warm Material 3 reading room. It supplies visual building blocks; the running app remains a stateless sample catalogue. Library, reader, account and sync flows in the design package are future work. The three modules remain `app → feature:books → core:designsystem`, with app also depending on designsystem.

## Start here

Apply `VeritalexTheme` at the application boundary. Features use `MaterialTheme.colorScheme`, `.typography`, `.shapes`, `VeritalexSpacing` and `VeritalexLayout`. Keep data and action ownership in the caller.

```kotlin
VeritalexTheme(
    appearance = AppAppearance.System,
    colorSource = AppColorSource.Brand,
) {
    Surface {
        Column(
            Modifier.padding(VeritalexLayout.gutter),
            verticalArrangement = Arrangement.spacedBy(VeritalexSpacing.medium),
        ) {
            Text("Books", style = MaterialTheme.typography.titleLarge)
            BookListRow("Pride and Prejudice", "Jane Austen")
        }
    }
}
```

`Surface` supplies a matching foreground/background. A theme alone does not paint a screen; use Surface or Scaffold. The activity’s Scaffold handles safe system insets once and passes consumed padding to the feature. Avoid adding the same status/navigation padding again inside the screen.

Window chrome belongs to the activity. If an appearance overrides the system, update status/navigation icon contrast there too. The debug gallery reports its actual surface brightness to its activity, which updates SystemBarStyle; choosing Dark while Android is light still gives readable system icons.

## Where to change a value

All theme files are in `core/designsystem/src/main/java/com/veritalex/core/designsystem/theme/`.

| Change | Source |
| --- | --- |
| Brand light/dark semantic colors | `Color.kt` |
| System/light/dark and brand/dynamic input | `Theme.kt` |
| All interface styles and variable-font weights | `Type.kt` |
| Cover, card, dialog and sheet radii | `Shape.kt` |
| Shared gaps, touch targets and content measures | `Tokens.kt` |
| Window-dependent gutter | `core/designsystem/src/main/res/values/dimens.xml` and `values-w400dp/dimens.xml` |
| Reader paper, prose, selection and highlight | `ReaderTheme.kt` |
| Action/field/book/feedback defaults | Adjacent `components/` package |
| Disposable demo state and fixtures | `core/designsystem/src/debug/…/gallery/` |
| Shared preview configurations | `core/designsystem/src/main/java/com/veritalex/core/designsystem/preview/VeritalexPreviews.kt` |

Use packages before adding modules. Add a token for a repeated visual decision, not every possible number. Material already owns color, type and shape: do not build parallel versions of those systems. A feature-specific measurement can stay in that feature.

## Color means a role

`onX` is the foreground intended to be read on `X`. Pair `primary/onPrimary` and `primaryContainer/onPrimaryContainer`; sharing part of a name does not make other foreground/background combinations readable.

| Role | Meaning and use |
| --- | --- |
| `primary` / `onPrimary` | Most prominent action and its label. Brand seed `#895021`; one primary action per decision. |
| `primaryContainer` / `onPrimaryContainer` | Softer accent grouping and typeset cover fallback. |
| Secondary and its container/on roles | Supporting emphasis; tonal buttons use the secondary container pair. |
| Tertiary and its container/on roles | Occasional complementary emphasis, such as a labeled reading status. Not an automatic synonym for success. |
| `surface` / `onSurface` | Canvas and ordinary text. Light `#FFF8F3/#241A14`; dark `#19120D/#F0DFD6`. |
| `onSurfaceVariant` | Supporting metadata on surfaces; not disabled text. |
| `surfaceContainerLowest/Low/(base)/High/Highest` | Tonal separation for groups and overlays. Quiet cards use Low; let native overlays use their defaults. Avoid five levels of nested cards. |
| `surfaceBright` / `surfaceDim` | Material surface variants available to native controls. |
| `outline` | Visible input/control boundary. |
| `outlineVariant` | Quiet divider; not the only boundary of a control that needs stronger contrast. |
| `error` / `onError` | Error or confirmed destructive emphasis, accompanied by explicit copy. |
| `errorContainer` / `onErrorContainer` | Larger error surface and its foreground. |
| `inverseSurface` / `inverseOnSurface` / `inversePrimary` | Inverted feedback surfaces, text and actions, including native snackbars. |
| `scrim` | Native modal backdrop; let the component apply its opacity. |
| `surfaceTint` | Material tonal elevation tint, matched to primary. |
| Accent `Fixed`, `FixedDim`, `onFixed`, `onFixedVariant` roles | Material accent roles that stay fixed across brand light/dark. Explicitly supplied to prevent default purple roles leaking into the palette. Prefer ordinary component roles first. |

`background/onBackground` and `surfaceVariant` remain supplied for compatibility. New layouts use surface/container roles. Never derive the app theme from a cover or infer saved/download/sync state from color.

`AppAppearance.System` follows Android light/dark; Light and Dark provide explicit inputs for a future settings owner. Brand is the default approved palette. Dynamic uses native wallpaper-derived Material schemes on Android 12/API 31+, with brand fallback on API 30. Dynamic changes Material colors, including native component colors and fallback covers. It does not change fonts, spacing, shapes or reader paper. No preferences or settings feature is implemented.

## Interface typography

Roboto Flex is used for every interface heading, label, book title, author and control. Choose by meaning instead of changing font sizes in each feature. All Material roles exist, but ordinary screens use the compact approved hierarchy.

| Material role | Size / line height (sp) | Weight | Use |
| --- | --- | --- | --- |
| displayLarge | 57 / 64 | Regular | Reserved Material role; no current product use. |
| displayMedium | 45 / 52 | Regular | Reserved; no marketing/dashboard heading. |
| displaySmall | 36 / 44 | Regular | Reserved; no current product use. |
| headlineLarge | 32 / 40 | Regular | Exceptional large heading only with a demonstrated need. |
| headlineMedium | 28 / 36 | Regular | Exceptional hierarchy, not the normal screen title. |
| headlineSmall | 24 / 32 | Medium | Available Material heading; prefer titleLarge for screen titles. |
| titleLarge | 24 / 32 | Medium | Screen title/dialog heading. |
| titleMedium | 20 / 28 | Medium | Section heading. |
| titleSmall | 16 / 24 | Medium | Book/row title. |
| bodyLarge | 16 / 24 | Regular | Interface body/explanations. |
| bodyMedium | 14 / 20 | Regular | Author and supporting metadata. |
| bodySmall | 12 / 16 | Regular | Minor metadata; never the only important instruction. |
| labelLarge | 14 / 20 | Medium | Actions and prominent labels. |
| labelMedium | 12 / 16 | Medium | Compact native labels and fallback cover text. |
| labelSmall | 11 / 16 | Medium | Supplementary labels; full book metadata also appears outside covers. |

Material baseline roles retain standard tracking. Custom roles use their declared styles. Text uses sp and reflows: do not set fixed heights on text-bearing fields, rows, chips or buttons to match a screenshot.

### Reader paper and typography

Literata is only for actual book prose, chapter headings and meaningful excerpts. `ReaderTypography.prose` is 19/32 regular; chapter is 26/34 medium. `ReadingPreview` is a selectable specimen, not a full reader or saved-position owner.

```kotlin
ReaderTheme(ReaderPaper.Sepia) {
    ReadingPreview(chapter = "Chapter 1", passage = passage)
}
```

Light, Sepia and Dark each supply `background`, `text`, `supportingText`, `selection`, `selectionHandle`, `highlight`, and `onHighlight`. Selection keeps the normal prose foreground: `text` must work on paper and selection backgrounds. ReaderTheme provides native selection colors. Saved highlights use highlight/onHighlight; selection is a different role. Reader paper stays independent of app light/dark and wallpaper. A future reader owns the selected paper and persistence.

Both fonts are bundled Android TrueType variable fonts, not WOFF2 assets. Roboto Flex explicitly maps 400/500/600/700 `wght` axes; Literata maps 400/500. Matching weight and the actual variable axis are both specified. Other axes keep upstream defaults. API 30 minimum supports these fonts. Font licenses ship under `assets/font-licenses/`. Only the Literata TTF/license were recovered from the archived source; no old implementation was restored.

## Spacing, shape, elevation and motion

| Token | dp | Use |
| --- | --- | --- |
| `VeritalexSpacing.extraSmall` | 4 | Closely related text. |
| small | 8 | Icon/label and compact gaps. |
| compact | 12 | Related controls. |
| medium | 16 | Row gaps and internal grouping. |
| large | 24 | Section content and generous padding. |
| extraLarge | 32 | Between sections. |
| `VeritalexLayout.gutter` | 16 below 400dp; 20 otherwise | Window-dependent content padding. |
| minimumTouchTarget | 48 | Minimum effective interactive bounds, never a maximum height. |
| contentMaxWidth | 720 | Centered sample list measure on wider windows. |
| readerMaxWidth | 680 | Prose specimen upper bound; future reader settings can narrow it. |
| listCoverWidth | 64 | List cover with 2:3 ratio. |

Material shapes are deliberate: extraSmall 4dp for covers, small 8dp for compact surfaces, medium 16dp for cards/fields, large 24dp when needed, extraLarge 28dp for native sheets/dialogs. Main actions use native pills. Consistency does not mean giving a cover and a dialog the same radius.

`VeritalexCard` is a flat surfaceContainerLow group. Avoid nested cards/decorative shadows. Native overlays own transient elevation, scrims and motion. There are no custom animations or unused motion/elevation abstractions. Compose/Material use the system animation duration scale; future custom motion must respect it too. Feedback remains understandable without animation.

## Actions and states

```kotlin
VeritalexButton("Save book", onSave, loading = saving, enabled = canSave)
VeritalexButton("Try again", onRetry, style = ActionStyle.Secondary)
VeritalexButton("View details", onDetails, style = ActionStyle.Outlined)
VeritalexButton("Cancel", onCancel, style = ActionStyle.Ghost)
```

| ActionStyle | Meaning |
| --- | --- |
| Primary | Filled; main positive action in a decision. |
| Secondary | Tonal; supporting action with visible emphasis. |
| Outlined | Visible alternative, boundary and low fill emphasis. |
| Ghost | Native Material text button; quiet/cancel action with transparent resting fill and native focus/ripple/pressed behavior. |
| Destructive | Error-colored filled confirmation with explicit destructive scope. Not every Remove menu item needs this emphasis. |

Disabled uses native disabled colors and blocks activation. Loading retains the visible label, adds a spinner and accessible “In progress” state, and blocks activation. A busy otherwise-enabled action keeps resting colors for legibility; a disabled action stays disabled even if loading is also true. Spinner semantics are cleared because the labeled control announces its state.

The owner sets loading promptly when work starts and clears it on success/failure. Components own no jobs and do not guarantee request idempotence. Do not replace a label with an unlabeled spinner. Destructive confirmation, cancellation and error handling belong to the feature.

`VeritalexIconButton(label, onClick) { Icon(…, contentDescription = null) }` requires a meaningful accessible label and has at least 48×48dp bounds. The icon is decorative because its parent supplies the label. It supports the same enabled/loading rules. Use a native tooltip when an icon needs discoverability, especially with mouse/stylus input.

## Fields, selection, books and feedback

```kotlin
VeritalexTextField(
    value = shelfName, onValueChange = onShelfNameChanged,
    label = "Shelf name", error = validationMessage,
)
VeritalexSearchField(query, onQueryChanged, onSearch, label = "Search books")
VeritalexMessage("Couldn’t load books", "Check your connection and try again.") {
    VeritalexButton("Retry", onRetry, style = ActionStyle.Secondary)
}
```

Fields retain native editing, keyboard, focus and selection, with 16dp shape. Error copy replaces supporting text, describes recovery and exposes the specific error to accessibility. Validation stays outside. These small stateless wrappers use supported value/onValueChange APIs; no ViewModel is required just to render them. Inline search supplies Search IME and a labeled clear action. Use native SearchBar directly when a feature needs expanded suggestions/results.

Use Material FilterChip, Switch, Checkbox, RadioButton, Slider, menus, ListItem and HorizontalDivider directly: themed defaults need no renamed wrappers. Keep at least 48dp effective targets. For labeled selection rows, put toggle/select on the parent with the correct role, set the child callback to null, and put radio choices in selectableGroup(). Keep visible selection; do not communicate it only with text color. The debug gallery shows these patterns.

BookCoverFallback is a 2:3, 4dp typeset fallback with supplied title/author. Small cover text can truncate; full metadata must also appear beside/below it. BookListRow does this, reflows full titles/authors and merges semantics without announcing a cover twice. It has no fake click action. Use VeritalexCard for intentional grouping, not around every list row. These components load no images and do not depend on the feature’s Book model.

VeritalexProgress combines factual copy with native progress semantics. Its visible label names the native indicator, so accessibility receives the label and range as one progress node without a duplicate text stop. Pass null for indeterminate or a fraction for determinate progress. Use labels such as “Downloading text · 28%” only when true. Keep non-interactive statuses as text/tonal surfaces, not chips with empty callbacks. No download/sync state is inferred here.

Use native AlertDialog, ModalBottomSheet, SnackbarHost and SnackbarHostState directly. The theme supplies shapes/colors; Material retains dismissal, scrim, focus and gestures. The owner decides whether dismissal is permitted during work. Keep recovery reachable after snackbars disappear and handle real undo/failure explicitly. Gallery overlays mutate no app data.

## Review the gallery and checks

Build debug and open the **Veritalex UI gallery** launcher icon:

```sh
rtk proxy ./gradlew :app:installDebug
rtk proxy adb shell am start -n com.veritalex/.DesignSystemGalleryActivity
```

It exists only in debug sources. Use System/Light/Dark, Brand/Dynamic and the Inspect section menu. The adaptive grid shows multiple columns on tablet windows. Local demo choices are not preferences. Previews cover light/dark, 320dp at 200%, and 840dp tablet; BooksScreen also previews empty and long metadata. Check real device font settings too: Android scaling can differ from a preview’s linear scale.

### Shared preview annotations

Use one annotation for the normal screen review set:

```kotlin
import com.veritalex.core.designsystem.preview.VeritalexPreviews

@VeritalexPreviews
@Composable
private fun BooksPreview() {
    VeritalexTheme {
        Surface { BooksScreen(books = SampleCatalogue.books) }
    }
}
```

`@VeritalexPreviews` expands to six independent configurations. Use a focused set when the full set adds no useful information:

| Annotation | Configurations |
| --- | --- |
| `VeritalexThemePreviews` | 412×915dp phone, light and dark, 100% text. |
| `VeritalexLargeTextPreviews` | 320×800dp narrow window, light and dark, 200% text. |
| `VeritalexTabletPreviews` | 840×1000dp tablet window, light and dark, 100% text. |
| `VeritalexPreviews` | All six above, grouped by theme, large text and tablet in the preview panel. |

For example, use `@VeritalexLargeTextPreviews` for a long-title fixture, `@VeritalexThemePreviews` for an empty-state fixture, and both on a component that needs four phone checks. Combining annotations adds their configurations; it does not multiply every size/theme/font combination. Avoid adding a focused set alongside `VeritalexPreviews`, since the full set already includes it.

The annotations configure the preview environment, not the composable’s content. Keep `VeritalexTheme` and a Surface/Scaffold in the preview function, pass realistic fixtures, and keep callbacks local/no-op. No network, repository, activity or ViewModel is needed. The main gallery already applies its own theme/Scaffold, so its preview just calls `DesignSystemGallery()`.

Change shared dimensions, font scale, names or groups in `preview/VeritalexPreviews.kt`, rather than copying raw `@Preview` declarations into feature files. Each annotation has binary retention and supports both functions and other annotations, so the presets remain visible to tooling across the existing module boundary. Modules that define previews keep `compileOnly(libs.ui.tooling.preview)` and `debugImplementation(libs.ui.tooling)`; the renderer stays out of release dependencies. No new module or preview framework is introduced.

The built-in `@PreviewDynamicColors` can be used separately for a future dynamic-color specimen, with `VeritalexTheme(colorSource = AppColorSource.Dynamic)`. Merely selecting wallpaper in an annotation does not switch a brand theme to dynamic color. The native gallery remains the current interactive dynamic-color check.

```sh
rtk proxy ./gradlew testDebugUnitTest :app:assembleDebug :app:assembleRelease :app:lintDebug :core:designsystem:lintDebug :feature:books:lintDebug
rtk proxy ./gradlew :app:connectedDebugAndroidTest
```

Unit tests verify actual semantic color mappings: 4.5:1 for active normal text; 3:1 for field boundaries and selection handles. Coverage includes brand light/dark surfaces, accent/container/error/fixed pairs and every reader paper/selection/highlight pair. Disabled states and decorative dividers do not use active-text contrast requirements. Review rendered wallpaper schemes when using dynamic color.

Connected tests cover the sample screen, all action variants’ activation/labels/targets while enabled, disabled and loading, icon semantics, field recovery errors/search clear, labeled determinate/indeterminate progress, long metadata/actions at 200% in a 280dp content measure, and paper independence across light/dark/dynamic inputs. Actual device evidence and limitations live in [DESIGN_SYSTEM_QA.md](DESIGN_SYSTEM_QA.md).

Before feature changes, review narrow windows, long translated text, 200% fonts, dark/dynamic, keyboard/TalkBack, safe insets and wider windows. Avoid fixed text heights and verify behavior as well as appearance.

Accessibility starts with this shared foundation: native Material interaction/semantics, tested color pairs, readable type, growing layouts, labeled states and minimum targets. Reuse these defaults instead of rechecking every shared contract in every feature. Keep later checks focused on what a screen introduces—its labels, reading order, content, new state transitions or a layout constraint. Add a regression for a concrete defect; do not build a new testing framework or repeat the whole device matrix for a routine styling change.

## Current API decision and sources

Verified October 30, 2026 with Context7’s official Android docs and the Gradle graph. BOM 2026.09.00 resolves Compose 1.12.1 and Material 3 1.4.0. No toolchain/general dependency upgrade. Tests use the current JUnit4 v2 rule factory.

Google’s [Styles update](https://developer.android.com/develop/ui/compose/styles/styles-update), updated October 26, says visual property definitions are moving to design-system layers, initial docs/skill were temporarily withdrawn, and Styles remains experimental in Compose 1.13. The installed June skill describes an earlier API. This foundation uses supported MaterialTheme and small Material wrappers, with no alpha dependency or obsolete Styles syntax. Re-evaluate when the new API and appropriate stable dependencies are available; retain the visual vocabulary.

- [Custom MaterialTheme extensions and wrappers](https://developer.android.com/develop/ui/compose/designsystems/custom)
- [Material 3 and dynamic color](https://developer.android.com/develop/ui/compose/designsystems/material3)
- [Bundled/variable fonts](https://developer.android.com/develop/ui/compose/text/fonts)
- [Accessibility defaults/targets](https://developer.android.com/develop/ui/compose/accessibility/api-defaults) and [semantics/errors](https://developer.android.com/develop/ui/compose/accessibility/semantics)
- [Buttons](https://developer.android.com/develop/ui/compose/components/button), [search](https://developer.android.com/develop/ui/compose/components/search-bar), [radio groups](https://developer.android.com/develop/ui/compose/components/radio-button)
- [Dialogs](https://developer.android.com/develop/ui/compose/components/dialog), [sheets](https://developer.android.com/develop/ui/compose/components/bottom-sheets), [snackbars](https://developer.android.com/develop/ui/compose/components/snackbar)
- [UI test v2 APIs](https://developer.android.com/reference/kotlin/androidx/compose/ui/test/junit4/v2/package-summary)
- [Custom multipreview annotations and combinations](https://developer.android.com/develop/ui/compose/tooling/previews)
- Approved [light](../.stitch/DESIGN.md), [dark](../.stitch/DESIGN-DARK.md), [tokens](../.stitch/tokens.json) and [handoff](../.stitch/HANDOFF.md). Future flows there are design references, not implemented behavior.
