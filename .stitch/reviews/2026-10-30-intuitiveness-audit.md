# Veritalex: clarity and interaction audit

October 30, 2026. Three independent reviewers examined information hierarchy, content design, and interaction/accessibility. The lead reconciled their findings against the approved handoff and screen manifest. This is a heuristic review and a proposed refinement direction; it does not claim user-tested improvements. Existing designs and Android source were not changed by this review.

## Recommended direction

Keep the warm Material 3 identity, Roboto Flex interface, Literata reading text, and existing navigation. Let book content, current state, and recognizable controls carry more of the interface. Remove repeated instructions and competing actions while retaining short labels that help someone predict a result.

Reduce visual and decision burden before reducing words. An unexplained icon, hidden action, or ambiguous state can require more thought than a short button label. User writing and actual book prose are content, not copy to shorten.

Three approaches were considered:

- **Focused refinement — recommended:** align actions with state, remove redundant copy, and consolidate secondary controls. This preserves the established product while addressing observed friction.
- **Copy edits alone:** quick, but leaves competing actions and inconsistent destinations unresolved.
- **Broad icon-only redesign:** reduces visible words but introduces recognition and discovery risks. Reserve icon-only actions for familiar toolbar controls.

## Priorities and evidence

### 1. Make reading actions consistent with the book's state

The [Book Details reference](../designs/book-details.png) presents **Read book**, **Save to library**, **Download**, and **Share** together. The manifest already separates download, saved status, and readiness to read. These sources should agree before the next design pass.

Use a compact book identity → reading/download state → next-action group. Before text is present, show **Download to read**; when available, **Start reading**; after starting, **Continue reading**. Saving for later remains an explicit secondary action, separate from downloading. Use different symbols for library membership and a passage bookmark; both currently use a bookmark shape. Keep progress near the reading action. Put About and source metadata below it; organization and occasional actions belong in a real menu. Remove the reference's Share control from this MVP pass because no sharing flow is defined in the manifest.

Affected IDs: `book-new`, `book-saved`, `book-downloading`, `book-download-failed`, `book-downloaded`, `book-reading`. Preserve recovery, offline availability, and status behavior; the changes concern presentation and hierarchy.

### 2. Give returning Home and Explore distinct, clear purposes

The [Home reference](../designs/home.png) repeats Continue reading in its section heading and button. The manifest adds decorative welcome text and repeated local-storage reassurance. Lead with the current book and its reading action, followed by saved books. Keep routine sync status compact and give a recoverable problem visible explanation and action. Evaluate discovery on returning Home as a secondary section, without duplicating a large Explore call to action.

The [Explore reference](../designs/explore.png) places promotional copy and six large explained subject tiles before catalogue rows. Put search directly below the app bar, then compact subject choices and actual books. Remove subject mini-definitions and explanatory text about features that are absent. Do not call catalogue subjects “shelves,” because personal Shelves already has a distinct meaning.

Affected IDs: `home-first`, `home-returning`, `explore-browse`, `explore-results`. Preserve useful first-use guidance, empty/error recovery, title/author search, subjects, and content attribution.

### 3. Let Library and Journal be easy to scan

The [Journal reference](../designs/journal.png) repeats a Reading journal heading beneath the selected Journal tab and places **Return to passage** on every entry. Use the existing manifest model: selecting an entry opens its detail; passage navigation lives there when a valid locator exists. Keep a single prominent **New entry** action. Preserve personal text, quotations, book identity, and useful passage references. The tradeoff is one additional tap for passage navigation from the list.

In populated Library, remove the large **Explore more books** call to action that repeats main navigation. Remove the reference's Sort/layout controls from this pass because they have no defined manifest flow. Choose a compact, consistent presentation for status, progress, and device download availability. Counts and private ratings should earn space through usefulness; avoid stacking several badges that communicate the same state. A clearly labeled discovery action still belongs in the empty Library state.

Affected IDs: `library-books`, `library-empty`, `journal-all`, `journal-view`. The reference's Frankenstein note shows passage navigation without a visible locator; verify its record before offering that action. A missing visible chapter does not prove that a locator is absent.

### 4. Make collection management match its affordance

In `shelf-detail`, **Shelf options / Rename or delete this shelf** currently opens Rename directly, while Delete is a separate action below the books. Replace this mismatch with an actual toolbar overflow containing **Rename** and **Delete**. Keep **Add books** visible. On the Shelves list, remove repeated collection explanation and give **New shelf** enough room for a readable label.

Affected IDs: `shelves-list`, `shelf-detail`, `shelf-rename`, `shelf-delete`. Deleting a shelf still keeps every book in Library, and the confirmation must say so. Management becomes one tap deeper; the main collection view becomes clearer.

### 5. Keep routine settings concise and consequential choices explicit

Settings subtitles sometimes paraphrase their labels. Keep useful current values and consequences; remove repeated definitions. Account & sync repeats healthy sync status through a heading, timestamp, inventory, and explanatory paragraph. One compact status is sufficient for routine success. A visible labeled retry remains appropriate for failure.

Import, pending changes at sign-out, deletion, and conflicting positions need clear choices. Compress repeated framing, not the information required to understand what will happen. Preserve account identity, import preview/deduplication, separate workspaces, local retention, irreversible deletion scope, verification, recovery, and deliberate position selection.

The import reference and manifest currently use different example counts; resolve fixtures before finalizing copy. The conflict reference says **Your other device**, while the manifest correctly says **Account**. Do not imply knowledge of a specific second device.

## Concrete copy examples

| Context | Current presentation | Proposed refinement |
| --- | --- | --- |
| Returning Home | Welcome back / A quiet moment for your next chapter | Lead with current book and Continue reading. |
| Journal | Selected Journal tab + Reading journal heading | Keep the tab; use the space for entries and controls. |
| Wallpaper colors | Use wallpaper colors + Personalize with your device colors | Keep the label; remove its paraphrase. |
| Reading settings | Keep screen awake while reading + Prevent display sleep during continuous reading | Keep screen awake, within the Reading group. |
| Healthy account sync | Up to date + Last synced just now + synced inventory | Up to date · Just now; retain device-specific download information where useful. |
| Import | Several headings explaining combination | Add guest reading?; account identity, actual preview, concise consequences. Actions: Add to account / Keep libraries separate. |
| Position conflict | Reading position + Where would you like to continue? + repeated instruction | Choose where to continue; labeled device/account positions; Your journal and highlights are kept either way. |

These are proposals, not replacement source strings. Validate state, account scope, and actual counts before applying them.

## Shared interaction rules

- Keep **Home, Explore, Library** and **Books, Shelves, Journal** labeled and in their existing locations.
- Familiar toolbar actions such as Back, Close, Search, Settings, and More can use icons with accessible names. Bookmark must expose selected state and the resulting add/remove action. Every interactive target retains at least 48 dp of effective space.
- Keep result-oriented labels for reading, downloading, saving, importing, sign-in, creation, retry, and destructive decisions when the icon alone would be ambiguous. “Ghost” describes text-button appearance; it does not mean removing the label.
- Give each decision group one clearly emphasized next action. Secondary controls can remain visible without competing emphasis. A menu must open a menu and contain the actions its label promises.
- Use supporting text for new information: current values, storage location, scope, consequences, or recovery. Avoid sentences that merely restate a heading or control label.
- Use one stable vocabulary for saved library membership, reading status, downloaded device text, and account sync. These are distinct states.
- Keep Reader tools discoverable. The existing labeled Contents, Appearance, Search, and Notes controls provide useful cues; there is no need to strip their labels automatically. Reconcile Notes with the Journal terminology and give any retained control a defined destination. Use one consistent toolbar across references and states. Hide/show controls by tapping prose, with an accessible equivalent. The prototype's passage-selection helper provides gesture/keyboard simulation and is not evidence that native Reader needs a permanent Select passage button.
- Preserve complete choices in Reader Appearance. Group paper, type, size/spacing/margins, and mode so they remain reachable; avoid fixed footers covering controls on small screens or enlarged text. Reader paper stays independent of app appearance.

Android's [accessibility defaults](https://developer.android.com/develop/ui/compose/accessibility/api-defaults) support the target-size and accessible-name requirements. This review did not conduct a fresh native TalkBack or device usability test.

## Suggested next design pass

Start with **returning Home, state-specific Book Details, Library Books, and Journal**. These establish reusable action, status, row, and copy patterns. Compare current and revised versions side by side before carrying the chosen patterns into the remaining states, dark examples, and tablet layouts. Keep the existing stable screen IDs and reconcile bespoke references with manifest behavior.

Validate with short tasks: resume a book; save one without downloading; download it for offline reading; find and edit a note; return to its passage; rename a shelf; recover from failed sync; distinguish account reading from guest reading. Check correct first action, hesitation, wrong turns, and backtracking. Word count is not a usability measure. Actual task observation is needed to establish whether the revisions help.

Source package: [design rules](../DESIGN.md), [handoff](../HANDOFF.md), [screen manifest](../screens.json), and the reference HTML/PNG in `../designs/`. The prototype shell and engineering annotations were excluded from product-copy findings. The parallel native design-system implementation was left untouched.
