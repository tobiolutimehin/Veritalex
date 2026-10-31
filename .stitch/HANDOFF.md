# Veritalex MVP design handoff

The package describes a personal Android reading app. Home, Explore and Library are the three primary destinations. Library contains Books, Shelves and Journal. Account & sync is reached through the Settings toolbar action. The approved visual rules live in [DESIGN.md](DESIGN.md).

Open [index.html](index.html) for the browsable state gallery, [prototype.html](prototype.html) for the simulated walkthrough and [WIREFLOW.md](WIREFLOW.md) for the base scenario transition map. [screens.json](screens.json) is the stable-ID source of truth. Every manifest state has a standalone grayscale wireframe and a companion light state design. Bespoke Stitch reference screens are indexed separately from those complete state designs.

## Navigation and state ownership

- Preserve the selected primary destination and Library tab when returning from a detail screen. System Back closes an overlay before leaving its parent; Reader Back returns to the book. Empty/error screens keep their valid navigation and recovery paths.
- Guest and signed-in account workspaces remain separate. Optional Google sign-in never gates reading. A cancelled provider sheet leaves local data unchanged. Errors offer retry and guest access.
- Primary navigation never appears inside Reader. Tap prose reveals or hides its controls. Continuous scroll is the default; paged mode is an explicit setting.
- Base scenario routes, Back and simulated completion/failure events are declared in the manifest. The prototype resolves the actual destination using the selected book/shelf, active workspace, collection empties, invoking destination, reader mode and interrupted operation. The shell exposes loading outcomes without placing test controls in the app interface. Some first-use and empty scenarios are selected directly from the shell.

## Data and account behavior

Guest records stay on the device. Sign-in offers a preview before adding any guest records to an account. Match books by Project Gutenberg catalogue ID, not title. Deduplicate journal entries and highlights by persistent record IDs; preserve their book IDs, timestamps and passage locators. Retrying an interrupted addition must be idempotent. Skipping the preview leaves the guest workspace available.

Account data restored to a new device includes saved books, shelves, private ratings, notes, highlights and reading positions. Downloaded book text is device-specific and is downloaded separately. Local reading stays usable while restoration or sync is pending.

Use factual status copy: Saved on device, Waiting to sync, Syncing, Up to date, Couldn’t sync, and Sign in to sync. Failed or expired authentication never implies that local edits were lost. The conflict state offers device and account positions explicitly; it does not silently pick the greater percentage. Store a stable text locator plus modification time; percentages are display values.

Before signing out with pending edits, offer sync, cancellation, or sign-out while retaining unsynced records for that same account on this device. Retained account records must not become guest records. The next matching account sign-in may retry them.

Deleting an account requires an explicit scope explanation, fresh verification of the same Google account, progress and confirmed success. A network/verification failure must not show a success message. Deletion covers the account’s library, shelves, ratings, reading positions, journal and highlights and removes downloaded account text on this device. Separate guest records are preserved. Navigation away from an accepted deletion must not pretend to cancel it.

## Books, downloads and shelves

The catalogue examples are real public-domain entries: 1342, Pride and Prejudice by Jane Austen; 84, Frankenstein by Mary Shelley; 11, Alice’s Adventures in Wonderland by Lewis Carroll; 1260, Jane Eyre by Charlotte Brontë. Covers are dignified typeset fallbacks, never unrelated imagery. No total pages, aggregate ratings, publication dates or recommendation claims are invented.

Saving a book, downloading text and reading it are distinct states. Book details cover new, saved, reading, downloading, failed, downloaded and unreadable text. Cancellation/failure keeps the saved book. An unreadable file offers a fresh download without deleting notes or reading progress. A downloaded filter means text actually exists on that device.

Reading status is Want to read, Reading or Finished. Ratings belong only to the current user. Marking Finished is explicit; it does not rate or publish anything. Download removal preserves saved books, journal, highlights, reading positions and shelf memberships.

A book may belong to several shelves. Creating and renaming validate nonblank, unique names. Deleting a shelf removes only the shelf and its memberships; every book stays in Library. Removing a book from Library removes its memberships and downloaded text, while preserving personal writing and its passage references. The destructive confirmation spells out this scope.

Add books from a shelf opens a multi-book Library picker. Add to shelves from a book opens a multi-shelf picker. These are separate directions and preserve the selected shelf/book identity.

## Journal and reading

Journal has all-book and per-book views, distinct empty states, entry detail, creation, editing, deletion and unsaved-change confirmation. An entry can include a selected quote and a stable passage reference. Return to passage reopens the associated book and locator. Deleting an entry keeps its book, position and any separately saved highlight.

Starting an entry from the all-book Journal first opens a book-context picker. Starting within a book or from selected Reader text already supplies its book. If its downloaded text has been removed, Return to passage offers download before resuming the saved locator.

Reader states include visible controls, immersive scroll, paged reading, appearance, contents/bookmarks, in-book search/results/empty, bookmark confirmation, text selection, highlight and end-of-book. Font, text size, line spacing, margins, paper and reading mode have explicit controls. Production preserves the passage across these changes. The app theme and reader Light/Sepia/Dark paper remain independent, with complete foreground/background palettes for each paper choice.

The demonstration anchor is Pride and Prejudice, Chapter 18, 28%. Prose and the short selected quote are verified against [Project Gutenberg 1342, Chapter XVIII](https://www.gutenberg.org/cache/epub/1342/pg1342.txt). The percentage is an illustrative anchor, not an asserted chapter boundary. Search snippets represent the downloaded-text interaction; the design deliberately avoids a fabricated global match count.

## Visual and accessibility requirements

Phone baseline is 412 × 915 dp; the generated frame reflows at 360 dp. App UI uses Roboto Flex; only book prose, excerpts and quotes use Literata. Light state exports embed the supplied font assets as data URIs. Grayscale wireframes use sans/serif system fallbacks. Native Android implementation must use semantic Material 3 roles, system insets, labelled navigation, 48 dp touch targets and scalable text. No decorative marketing typography belongs in the interface.

Sheets/dialogs show parent context behind them. The embedded interactive prototype uses native HTML `dialog.showModal()`, Escape cancellation and safe cancellation focus. Static boards show the same state without top-layer behavior so every phone can be viewed together. The prototype shell supplies labels, screen selection and simulated events outside the app frame. Respect reduced motion, keyboard focus and accessible input labels.

Tablet and dark-theme bespoke references, when available, are indexed in metadata. The complete manifest-based state exports are light phone designs; they do not substitute for native tablet behavior. The production tablet uses a navigation rail and intentional list/detail panes; Reader centers its prose measure rather than stretching a phone layout.

## Rebuild and verify

From the repository root:

```sh
rtk proxy python3 .stitch/scripts/build_package.py
rtk proxy python3 .stitch/scripts/build_package.py --check
rtk proxy python3 .stitch/scripts/build_package.py --check --test-prototype
rtk proxy python3 -m http.server 4175 --bind 127.0.0.1 --directory .stitch
```

Then open `http://localhost:4175/index.html`. No framework, build server, package installation or backend is required. The optional prototype regression command uses Node's built-in VM to verify owned-book routing, idempotent saves and duplicate-shelf identity. The generator reads the manifest and optional [metadata.json](metadata.json), emits all self-contained phone/board HTML and rebuilds the gallery and prototype. Run it again after adding Stitch exports to metadata. The audit verifies stable IDs, manifest targets, complete state/board coverage and local link integrity. Browser layout/interaction checks are separate from structural checks.

## Prototype limits and implementation boundaries

This is a reviewable design package. It performs no real sign-in, deletion, network catalogue search, download, storage or sync. A small in-memory simulation carries separate guest/account collections, edited journal drafts, shelf membership, private ratings, status, appearance, bookmarks/highlights and selected reading position between screens. It retains pending sync and interrupted-operation intent. Reloading or choosing a new scenario resets that simulation; the standalone state exports remain static review artifacts.

Reader interactions use representative Pride and Prejudice passages, including a short verified Chapter 19 excerpt when the account’s 31% position is selected. Neighboring contents rows are visual context, and paged Next switches between two sample passage anchors; it does not advance a full book. Other catalogue detail selections retain their actual title, author and subjects; the Reader remains the explicit Pride and Prejudice demo. These limits are declared in the prototype shell, outside the app flow. This simulation is not a native Android implementation or a persistent app data layer.

No goals, reminders, social feed, payments, audio or user-imported books are in this MVP. No Android source is changed by this package generator.

## Browser verification and exports

The final package includes 14 light phone references, 7 Night references, and 4 tablet references generated in Stitch. Some references include approved final content, attribution and typography refinements; their local HTML and PNGs are the handoff versions. Complete state designs and boards are self-contained; raw bespoke Stitch HTML may load its original CDN styles or fonts, while PNGs work offline.

Browser QA uses Playwright and an installed Chromium/Chrome. Run `node .stitch/scripts/render_package.mjs audit`, `flows`, `large-text`, `boards`, or `gallery` with the localhost server above running. Set `VERITALEX_BASE_URL` for a different server URL, `VERITALEX_CHROME` for a browser executable, and `VERITALEX_PLAYWRIGHT` for a module path when needed. The renderer discovers the bundled runtime on this workstation as a fallback. Audit failures return a nonzero exit code. Generated QA JSON and screenshots are in `qa/`.

Rebuild reference metadata with Python 3.11+ using `python3.11 .stitch/scripts/index_exports.py`, then rebuild the gallery. Upload receipts preserve remote IDs and hashes; `publish_boards.py` resumes identical saved batches. The transfer utility reads the existing Stitch connection in memory and does not include credentials in this package.
