# Learning Veritalex

Start by understanding the screen already in the app. Then introduce one new concept when a working feature needs it. The aim is to build and explain a small reading app yourself.

## What the three modules mean

A **module** is a separately configured build unit with its own dependencies. A **package** organizes related source files inside a module. A **library** supplies code that a module depends on, such as Compose Material 3. A new package does not require a new Gradle module, and using a library does not require wrapping it in an interface.

| Module | Owns now | Why it exists |
| --- | --- | --- |
| `:app` | Activity and screen assembly | The runnable Android application. |
| `:feature:books` | `Book`, `SampleCatalogue`, `BooksScreen` | A small feature boundary you can read end to end. |
| `:core:designsystem` | Theme, UI/reader fonts, colors, shapes, spacing and shared controls | A reusable visual vocabulary shared by the activity and feature. |

This is a learning choice, not a rule that every Android app needs three modules. Android's [modularization guide](https://developer.android.com/topic/modularization) explains the costs and benefits of boundaries. For now, organize new concepts in packages before adding modules.

## Read the source in this order

1. Read [MainActivity.kt](../app/src/main/java/com/veritalex/MainActivity.kt). Trace how Android launches the activity, applies the theme and passes sample data into `BooksScreen`.
2. Read [Book.kt](../feature/books/src/main/java/com/veritalex/feature/books/Book.kt) and [SampleCatalogue.kt](../feature/books/src/main/java/com/veritalex/feature/books/SampleCatalogue.kt). Identify the model fields and the sample values.
3. Read [BooksScreen.kt](../feature/books/src/main/java/com/veritalex/feature/books/BooksScreen.kt). Follow a list item from its `Book` argument to the title and author on screen, then inspect its previews.
4. Read [the theme](../core/designsystem/src/main/java/com/veritalex/core/designsystem/theme/Theme.kt), followed by its color and typography definitions. Change a semantic role and find where it appears.
5. Read [settings.gradle.kts](../settings.gradle.kts), the three module build files and [libs.versions.toml](../gradle/libs.versions.toml). Draw which module depends on which, and distinguish project dependencies from external libraries.

You should be able to describe the current execution path without opening the old implementation or a future architecture plan.

The [native design-system guide](DESIGN_SYSTEM.md) explains what the visual roles mean and how to select them. Open the debug **Veritalex UI gallery** to compare actions, fields, shapes, type and independent reader papers. Its remembered demo state is not application architecture or persisted settings. Use its examples without introducing a ViewModel or new module just to render a control.

For a new screen preview, add `@VeritalexPreviews` to a parameterless composable and wrap its sample content in `VeritalexTheme` plus Surface/Scaffold. It supplies six standard configurations from one shared definition. Use the focused Theme/LargeText/Tablet annotations when fewer views are sufficient; see [the preview examples](DESIGN_SYSTEM.md#shared-preview-annotations).

## 1. Kotlin through the book model

**Exercise:** Add one sample book, rename a field in a small local experiment, and use `copy` to produce an updated value. Try a nullable author in that experiment and decide how the UI should describe an unknown author. Keep the actual checkpoint's `Book(id: Int, title: String, author: String)` simple until a requirement calls for changing it.

Learn what a data class supplies, how nullability changes the caller's responsibilities, and how `map` and `filter` transform collections. `val` prevents reassignment of a reference; it does not make the referenced object or every nested value immutable. A read-only `List` interface also does not prove that no other owner can mutate the underlying collection.

**Done when:** You can predict the effect of `val`, `var`, `copy` and a nullable property, and display an empty sample list without an exception.

## 2. Stateless Compose and layout

**Exercise:** Adjust the book row using Material typography and semantic colors. Preview an empty list, a long title, a long author name, light and dark appearance, and larger text. Test the installed screen with a narrow window and TalkBack.

`BooksScreen` receives the books it renders. Keep loading, storage and sample creation outside the composable. When a real action arrives, pass an event callback to the caller. State ownership can then grow from this explicit input/output relationship; see the official [state hoisting guidance](https://developer.android.com/develop/ui/compose/state-hoisting).

**Done when:** Text remains readable without overlap, scrolling works, content is described sensibly to accessibility services, and a preview can render the screen without an activity, network or database. Use meaningful labels and a minimum 48 dp touch target for any controls you add.

## 3. Screen state and a fake repository

**Exercise:** Introduce a ViewModel when the screen gains behavior worth retaining, such as loading a catalogue and retrying a failure. Start with a fake repository returning a small fixed list. Constructor injection can be written by hand.

Follow unidirectional data flow: the screen renders state and sends events; the owner handles events and produces new state. Cover loading, content, empty and error states. A sealed interface or a small state data class is enough; choose whichever makes valid states easiest to express. The [architecture recommendations](https://developer.android.com/topic/architecture/recommendations) explain the roles of ViewModels, repositories and observable UI state.

**Done when:** The composable has no data-loading decisions, a fake failure can be retried, and a focused ViewModel test verifies an actual state transition. Explain why the ViewModel was added before adding another layer.

## 4. Coroutines and Flow with a purpose

**Exercise:** Make the fake load suspend, then cancel an in-flight request and trigger a retry. Introduce Flow only when values change over time. Practice observing it in a lifecycle-aware way from the screen.

Keep work in an owned scope and let cancellation propagate. Turn expected failures into useful UI state; avoid broad catches that swallow cancellation. Use a test dispatcher and controlled fake behavior to verify loading, failure, retry and cancellation without real delays. Follow the official [coroutines best practices](https://developer.android.com/kotlin/coroutines/coroutines-best-practices).

Use `viewModelScope` for work owned by a ViewModel. `suspend` permits suspension; it does not automatically run work on a background thread. Put dispatcher switching where an implementation performs blocking work, rather than wrapping every repository call in `Dispatchers.IO`.

**Done when:** Work stops with its owner, replacing a request does not show a stale result, and tests control time and outcomes. You can explain the difference between a suspending operation and a stream of updates.

At this point, introduce `:core:data` when repository behavior needs a boundary outside the UI feature. Move shared book models there when both persistence/data code and the feature need them. Do not make the data layer depend on the UI module.

## 5. Durable saving with Room

**Exercise:** Add explicit save and remove operations, backed by Room. Repeating Save must keep the book saved. Show saved books in a simple Library view and observe changes from the database. Start with the sample catalogue so network behavior cannot hide storage mistakes.

Introduce `:core:database` for entities, DAOs, database creation and schema history. Keep repository coordination and model mapping in `:core:data`. Persist a stable book ID and the metadata needed to display saved books offline. Test a round trip, repeated saves and removal; add a tested migration when a later schema change requires one.

Use a new development database name for these exercises. Before opening the pre-reset database, recover its schema history from `codex/pre-reset-2026-10-30` and test an upgrade from version 2. Do not reuse that database name with a fresh version-1 schema or destructive migration.

**Done when:** Saving a book, closing the process and reopening the app preserves it without connectivity. Removing it updates Library, and a write failure does not produce a success message.

The target now has five modules:

```text
:app → :feature:books → :core:data → :core:database
  └──────────────────→ :core:designsystem ← :feature:books
```

These modules are introduced by their lessons; empty placeholders are not needed at the first checkpoint.

## 6. Real catalogue loading, then paging

**Exercise:** Replace the fake catalogue load with a real request while keeping the same UI contract. Parse a small response, map transport models to app models, and implement an explicit refresh. Keep saved metadata durable even if refresh fails. Put HTTP code in a `network` package inside `:core:data` first.

Test request parameters and response/error handling against a local HTTP server. Exercise offline mode, malformed responses and retry. Add Paging only after a real list needs incremental loading; first understand page keys, list ordering, refresh and end-of-list behavior with a small implementation.

**Done when:** A refresh updates catalogue content, offline saved books remain visible, failures offer recovery, and tests do not depend on the public service being available. Pagination is a separate follow-up with its own observable need and tests.

## 7. Navigation when a second screen needs it

**Exercise:** Add book details, carrying the selected book's stable ID. Start with explicit destination registration in `app` and callbacks from the feature. Keep navigation decisions out of individual list rows.

This lesson can happen as soon as the Library or detail view needs separate destinations. Choose one navigation approach and learn it through a two-screen flow. Add more stacks or shared navigation modules only when an actual interaction requires them.

**Done when:** Selecting different books opens the correct detail, Back returns to the previous context, and recreation preserves the destination and selected identity.

The first product milestone is complete when a person can **browse → save → Library → relaunch offline**. Check that sequence on a device; passing isolated tests alone does not establish the complete flow.

## 8. A reader after the library works

**Exercise:** Download readable public-domain text, open it and persist a stable passage locator. Treat saving a book, downloading its text and reading it as different operations. Start with scrolling and one text format before contents, search, highlights or pagination.

**Done when:** A downloaded book opens offline, its position survives relaunch, and changing text size preserves the passage. Failed downloads can be retried without losing saved status or progress.

Use [.stitch/HANDOFF.md](../.stitch/HANDOFF.md) as the product reference. Shelves, journal, advanced reader controls and optional account/sync remain later lessons. Introduce a reader feature module when its code has a clear responsibility worth isolating.

## A small mentor workflow

Pick one visible behavior, explain the intended change in your own words, implement it, and verify it before moving on. Ask for a hint or a review of your attempt before asking an assistant to write the whole feature. After each lesson, explain where state lives, what can fail and how you know it works.

A useful assistant request is: “Review this save operation for idempotence and failure handling. Explain the smallest fix; do not add modules or libraries.” Ask for current official documentation when learning a library API.

No step requires MVI scaffolding, one-use use cases, a `core:domain` module, convention plugins, a DI framework or a library swap. Add an abstraction when you can name the repeated problem it solves. Keep working code and meaningful tests as checkpoints; keep future designs separate from claims about implemented behavior.
