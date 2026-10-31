# Veritalex MVP wireflow

Stable IDs in [screens.json](screens.json) drive every state export. This is the base scenario transition map; the prototype resolves collection empties, selected identity, return context and operation recovery dynamically. Numbers match the boards. Home / Explore / Library are the primary destinations. Library contains Books / Shelves / Journal; Account & sync lives in Settings.

Loading completion, network failure and provider outcomes are simulated events outside the app frame. Empty and first-use scenarios can be selected from the prototype shell.

## Primary journeys

1. Guest reading: `auth-welcome` → `home-first` → `explore-browse` → `explore-results` → `book-new` → `book-saved` → `book-downloading` → `book-downloaded` → `reader-scroll`.
2. Reading and writing: `home-returning` → `reader-scroll` → `reader-selection` → `reader-highlight` → `journal-create` → `journal-view` → `reader-highlight`.
3. Organize: `library-books` → `library-actions` → `shelf-membership` → `book-reading`; or `shelf-detail` → `shelf-add-books` → `shelf-detail`. Shelf deletion preserves the saved books.
4. Optional account: `settings-main` → `sync-local` → `auth-loading` → `auth-import-preview` → `auth-importing` → `auth-import-complete` → `sync-conflict`.
5. Recovery: `explore-offline` → `explore-loading`; `book-download-failed` → `book-downloading`; `sync-failed` → `sync-syncing`. Local reading stays available.
6. Deletion: `account-details` → `account-delete-confirm` → `account-reauth` → `account-deleting` → `account-deleted`, with cancellation and failure routes.

## Every state and transition

### 01 · A little space to read · `auth-welcome`

Auth · base. [Wireframe](wireframes/auth-welcome.html) · [Light state design](polished/auth-welcome.html) · [Prototype](prototype.html#auth-welcome)

- Continue with Google (action) → 02 · `auth-loading`
- Continue as guest (action) → 08 · `home-first`

Annotation: Google is optional; guest mode has the complete local reading experience.

Annotation: No real provider sign-in occurs in the prototype.

### 02 · Connecting to Google · `auth-loading`

Auth · loading. [Wireframe](wireframes/auth-loading.html) · [Light state design](polished/auth-loading.html) · [Prototype](prototype.html#auth-loading)

- Cancel (action) → 03 · `auth-cancelled`
- Simulate sign-in success (event) → 05 · `auth-import-preview`
- Simulate sign-in failure (event) → 04 · `auth-error`
- Back (back) → 01 · `auth-welcome`

Annotation: External provider returns success, cancellation or recoverable error.

### 03 · You’re still welcome here · `auth-cancelled`

Auth · cancelled. [Wireframe](wireframes/auth-cancelled.html) · [Light state design](polished/auth-cancelled.html) · [Prototype](prototype.html#auth-cancelled)

- Try Google again (action) → 02 · `auth-loading`
- Continue as guest (action) → 08 · `home-first`
- Back (back) → 01 · `auth-welcome`

### 04 · Couldn’t sign in · `auth-error`

Auth · error. [Wireframe](wireframes/auth-error.html) · [Light state design](polished/auth-error.html) · [Prototype](prototype.html#auth-error)

- Try again (action) → 02 · `auth-loading`
- Continue as guest (action) → 08 · `home-first`
- Back (back) → 01 · `auth-welcome`

### 05 · Add guest reading? · `auth-import-preview`

Auth · base. [Wireframe](wireframes/auth-import-preview.html) · [Light state design](polished/auth-import-preview.html) · [Prototype](prototype.html#auth-import-preview)

- Add to account (action) → 06 · `auth-importing`
- Keep libraries separate (action) → 09 · `home-returning`
- Back (back) → 71 · `account-details`

Annotation: Deduplicate books by Gutenberg catalogue ID, never title.

Annotation: Keep journal entries and highlights by their persistent IDs. Retry must not duplicate imported records.

Annotation: Skip leaves the guest workspace available on this device.

### 06 · Adding your reading · `auth-importing`

Auth · progress. [Wireframe](wireframes/auth-importing.html) · [Light state design](polished/auth-importing.html) · [Prototype](prototype.html#auth-importing)

- Simulate import complete (event) → 07 · `auth-import-complete`
- Simulate import interrupted (event) → 83 · `sync-failed`
- Back (back) → 71 · `account-details`

### 07 · Guest reading added · `auth-import-complete`

Auth · success. [Wireframe](wireframes/auth-import-complete.html) · [Light state design](polished/auth-import-complete.html) · [Prototype](prototype.html#auth-import-complete)

- Choose reading position (action) → 86 · `sync-conflict`
- Back (back) → 09 · `home-returning`

### 08 · Home · `home-first`

Home · first-use. [Wireframe](wireframes/home-first.html) · [Light state design](polished/home-first.html) · [Prototype](prototype.html#home-first)

- Explore books (action) → 10 · `explore-browse`
- Pride and Prejudice (action) → 17 · `book-new`
- Frankenstein (action) → 17 · `book-new`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 09 · Home · `home-returning`

Home · base. [Wireframe](wireframes/home-returning.html) · [Light state design](polished/home-returning.html) · [Prototype](prototype.html#home-returning)

- Continue reading (action) → 53 · `reader-scroll`
- Saved on device (action) → 79 · `sync-local`
- Frankenstein (action) → 18 · `book-saved`
- Alice’s Adventures in Wonderland (action) → 18 · `book-saved`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 10 · Explore · `explore-browse`

Explore · base. [Wireframe](wireframes/explore-browse.html) · [Light state design](polished/explore-browse.html) · [Prototype](prototype.html#explore-browse)

- Search books (action) → 11 · `explore-search`
- Browse Fiction (action) → 12 · `explore-results`
- Pride and Prejudice (action) → 17 · `book-new`
- Frankenstein (action) → 17 · `book-new`
- Alice’s Adventures in Wonderland (action) → 17 · `book-new`
- Jane Eyre (action) → 17 · `book-new`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 11 · Search books · `explore-search`

Explore · base. [Wireframe](wireframes/explore-search.html) · [Light state design](polished/explore-search.html) · [Prototype](prototype.html#explore-search)

- Search for Austen (action) → 15 · `explore-loading`
- Clear recent searches (action) → 11 · `explore-search`
- Back (back) → 10 · `explore-browse`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

Annotation: Keyboard and IME search submit use the same action. Empty input keeps focus and shows no network error.

### 12 · Search results · `explore-results`

Explore · base. [Wireframe](wireframes/explore-results.html) · [Light state design](polished/explore-results.html) · [Prototype](prototype.html#explore-results)

- Edit search (action) → 11 · `explore-search`
- Filters (action) → 13 · `explore-filters`
- Pride and Prejudice (action) → 17 · `book-new`
- Simulate no matches (event) → 14 · `explore-empty`
- Simulate connection loss (event) → 16 · `explore-offline`
- Back (back) → 10 · `explore-browse`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 13 · Filter books · `explore-filters`

Explore · sheet. [Wireframe](wireframes/explore-filters.html) · [Light state design](polished/explore-filters.html) · [Prototype](prototype.html#explore-filters)

- Show results (action) → 12 · `explore-results`
- Reset filters (action) → 12 · `explore-results`
- Back (back) → 12 · `explore-results`

Annotation: Temporary filter choices are discarded by Back. Language/subject are catalogue metadata, not app preferences.

### 14 · No matching books · `explore-empty`

Explore · empty. [Wireframe](wireframes/explore-empty.html) · [Light state design](polished/explore-empty.html) · [Prototype](prototype.html#explore-empty)

- Clear filters (action) → 12 · `explore-results`
- Change search (action) → 11 · `explore-search`
- Back (back) → 10 · `explore-browse`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 15 · Searching the catalogue · `explore-loading`

Explore · loading. [Wireframe](wireframes/explore-loading.html) · [Light state design](polished/explore-loading.html) · [Prototype](prototype.html#explore-loading)

- Edit search (action) → 11 · `explore-search`
- Simulate results (event) → 12 · `explore-results`
- Simulate request failure (event) → 16 · `explore-offline`
- Back (back) → 11 · `explore-search`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 16 · Explore is offline · `explore-offline`

Explore · offline. [Wireframe](wireframes/explore-offline.html) · [Light state design](polished/explore-offline.html) · [Prototype](prototype.html#explore-offline)

- Try again (action) → 15 · `explore-loading`
- Open Library (action) → 28 · `library-downloaded`
- Back (back) → 10 · `explore-browse`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 17 · Book details · `book-new`

Book · base. [Wireframe](wireframes/book-new.html) · [Light state design](polished/book-new.html) · [Prototype](prototype.html#book-new)

- Want to read (action) → 18 · `book-saved`
- Download to read (action) → 20 · `book-downloading`
- Back (back) → 12 · `explore-results`

Annotation: No page count, publication date or aggregate rating is invented.

Annotation: Saving a book and downloading its text are distinct operations.

Annotation: Design reference: Project Gutenberg catalogue ID 1342. Catalogue IDs are data identity and stay outside book-detail app copy.

### 18 · Book details · `book-saved`

Book · saved. [Wireframe](wireframes/book-saved.html) · [Light state design](polished/book-saved.html) · [Prototype](prototype.html#book-saved)

- Download to read (action) → 20 · `book-downloading`
- Book actions (action) → 30 · `library-actions`
- Back (back) → 25 · `library-want`

Annotation: Design reference: Project Gutenberg catalogue ID 1342. Catalogue IDs are data identity and stay outside book-detail app copy.

### 19 · Book details · `book-reading`

Book · in-progress. [Wireframe](wireframes/book-reading.html) · [Light state design](polished/book-reading.html) · [Prototype](prototype.html#book-reading)

- Continue reading (action) → 53 · `reader-scroll`
- Open book journal (action) → 45 · `journal-book`
- Book actions (action) → 30 · `library-actions`
- Back (back) → 26 · `library-reading`

Annotation: Design reference: Project Gutenberg catalogue ID 1342. Catalogue IDs are data identity and stay outside book-detail app copy.

### 20 · Downloading book · `book-downloading`

Book · progress. [Wireframe](wireframes/book-downloading.html) · [Light state design](polished/book-downloading.html) · [Prototype](prototype.html#book-downloading)

- Cancel download (action) → 18 · `book-saved`
- Simulate download complete (event) → 22 · `book-downloaded`
- Simulate download failure (event) → 21 · `book-download-failed`
- Back (back) → 24 · `library-books`

### 21 · Download interrupted · `book-download-failed`

Book · error. [Wireframe](wireframes/book-download-failed.html) · [Light state design](polished/book-download-failed.html) · [Prototype](prototype.html#book-download-failed)

- Try download again (action) → 20 · `book-downloading`
- Manage storage (action) → 68 · `settings-storage`
- Back (back) → 18 · `book-saved`

### 22 · Ready to read · `book-downloaded`

Book · downloaded. [Wireframe](wireframes/book-downloaded.html) · [Light state design](polished/book-downloaded.html) · [Prototype](prototype.html#book-downloaded)

- Start reading (action) → 53 · `reader-scroll`
- Book actions (action) → 30 · `library-actions`
- Simulate unreadable text (event) → 23 · `book-unreadable`
- Back (back) → 28 · `library-downloaded`

Annotation: Design reference: Project Gutenberg catalogue ID 1342. Catalogue IDs are data identity and stay outside book-detail app copy.

### 23 · Book can’t be opened · `book-unreadable`

Book · error. [Wireframe](wireframes/book-unreadable.html) · [Light state design](polished/book-unreadable.html) · [Prototype](prototype.html#book-unreadable)

- Download again (action) → 20 · `book-downloading`
- Return to Library (action) → 24 · `library-books`
- Back (back) → 22 · `book-downloaded`

### 24 · Library · `library-books`

Library · base. [Wireframe](wireframes/library-books.html) · [Light state design](polished/library-books.html) · [Prototype](prototype.html#library-books)

- Choose a library filter (action) → 24 · `library-books`
- Want to read filter (action) → 25 · `library-want`
- Reading filter (action) → 26 · `library-reading`
- Finished filter (action) → 27 · `library-finished`
- Pride and Prejudice (action) → 19 · `book-reading`
- Frankenstein (action) → 18 · `book-saved`
- Alice’s Adventures in Wonderland (action) → 22 · `book-downloaded`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`
- Downloaded filter (action) → 28 · `library-downloaded`

### 25 · Library · `library-want`

Library · filtered. [Wireframe](wireframes/library-want.html) · [Light state design](polished/library-want.html) · [Prototype](prototype.html#library-want)

- Choose a library filter (action) → 24 · `library-books`
- Want to read filter (action) → 25 · `library-want`
- Reading filter (action) → 26 · `library-reading`
- Finished filter (action) → 27 · `library-finished`
- Downloaded filter (action) → 28 · `library-downloaded`
- Frankenstein (action) → 18 · `book-saved`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

### 26 · Library · `library-reading`

Library · filtered. [Wireframe](wireframes/library-reading.html) · [Light state design](polished/library-reading.html) · [Prototype](prototype.html#library-reading)

- Choose a library filter (action) → 24 · `library-books`
- Want to read filter (action) → 25 · `library-want`
- Reading filter (action) → 26 · `library-reading`
- Finished filter (action) → 27 · `library-finished`
- Downloaded filter (action) → 28 · `library-downloaded`
- Pride and Prejudice (action) → 19 · `book-reading`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

### 27 · Library · `library-finished`

Library · filtered. [Wireframe](wireframes/library-finished.html) · [Light state design](polished/library-finished.html) · [Prototype](prototype.html#library-finished)

- Choose a library filter (action) → 24 · `library-books`
- Want to read filter (action) → 25 · `library-want`
- Reading filter (action) → 26 · `library-reading`
- Finished filter (action) → 27 · `library-finished`
- Downloaded filter (action) → 28 · `library-downloaded`
- Alice’s Adventures in Wonderland (action) → 22 · `book-downloaded`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

### 28 · Library · `library-downloaded`

Library · filtered. [Wireframe](wireframes/library-downloaded.html) · [Light state design](polished/library-downloaded.html) · [Prototype](prototype.html#library-downloaded)

- Choose a library filter (action) → 24 · `library-books`
- Want to read filter (action) → 25 · `library-want`
- Reading filter (action) → 26 · `library-reading`
- Finished filter (action) → 27 · `library-finished`
- Downloaded filter (action) → 28 · `library-downloaded`
- Pride and Prejudice (action) → 19 · `book-reading`
- Alice’s Adventures in Wonderland (action) → 22 · `book-downloaded`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

### 29 · Library · `library-empty`

Library · empty. [Wireframe](wireframes/library-empty.html) · [Light state design](polished/library-empty.html) · [Prototype](prototype.html#library-empty)

- Explore books (action) → 10 · `explore-browse`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

### 30 · Book actions · `library-actions`

Library · sheet. [Wireframe](wireframes/library-actions.html) · [Light state design](polished/library-actions.html) · [Prototype](prototype.html#library-actions)

- Choose shelves (action) → 40 · `shelf-membership`
- Set private rating (action) → 32 · `library-rating`
- Open book journal (action) → 45 · `journal-book`
- Remove from library (action) → 31 · `library-remove`
- Back (back) → 19 · `book-reading`
- Mark Want to read (action) → 25 · `library-want`
- Mark Reading (action) → 26 · `library-reading`
- Mark Finished (action) → 27 · `library-finished`

Annotation: Status changes are local-first. Marking Finished does not delete downloaded text or notes.

### 31 · Remove this book? · `library-remove`

Library · dialog. [Wireframe](wireframes/library-remove.html) · [Light state design](polished/library-remove.html) · [Prototype](prototype.html#library-remove)

- Remove from library (action) → 36 · `library-after-removal`
- Keep book (action) → 24 · `library-books`
- Back (back) → 30 · `library-actions`

Annotation: Destructive label states its exact scope. Do not delete notes as a side effect of removing a library book.

### 32 · Your rating · `library-rating`

Library · sheet. [Wireframe](wireframes/library-rating.html) · [Light state design](polished/library-rating.html) · [Prototype](prototype.html#library-rating)

- Save rating (action) → 30 · `library-actions`
- Clear rating (action) → 30 · `library-actions`
- Back (back) → 30 · `library-actions`

### 33 · Library · `shelves-list`

Shelves · base. [Wireframe](wireframes/shelves-list.html) · [Light state design](polished/shelves-list.html) · [Prototype](prototype.html#shelves-list)

- New shelf (action) → 35 · `shelf-create`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`
- Open Classics (action) → 41 · `shelf-detail`
- Open Reading next (action) → 41 · `shelf-detail`

### 34 · Library · `shelves-empty`

Shelves · empty. [Wireframe](wireframes/shelves-empty.html) · [Light state design](polished/shelves-empty.html) · [Prototype](prototype.html#shelves-empty)

- New shelf (action) → 35 · `shelf-create`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

### 35 · Create shelf · `shelf-create`

Shelves · base. [Wireframe](wireframes/shelf-create.html) · [Light state design](polished/shelf-create.html) · [Prototype](prototype.html#shelf-create)

- Create shelf (action) → 42 · `shelf-detail-empty`
- Simulate duplicate name (event) → 37 · `shelf-name-error`
- Back (back) → 33 · `shelves-list`

### 36 · Library · `library-after-removal`

Library · after-removal. [Wireframe](wireframes/library-after-removal.html) · [Light state design](polished/library-after-removal.html) · [Prototype](prototype.html#library-after-removal)

- Frankenstein (action) → 18 · `book-saved`
- Alice’s Adventures in Wonderland (action) → 22 · `book-downloaded`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

Annotation: Removal changes only its confirmed scope; other saved data remains visible.

### 37 · Create shelf · `shelf-name-error`

Shelves · validation. [Wireframe](wireframes/shelf-name-error.html) · [Light state design](polished/shelf-name-error.html) · [Prototype](prototype.html#shelf-name-error)

- Save name (action) → 42 · `shelf-detail-empty`
- Open existing shelf (action) → 41 · `shelf-detail`
- Back (back) → 35 · `shelf-create`

### 38 · Rename shelf · `shelf-rename`

Shelves · base. [Wireframe](wireframes/shelf-rename.html) · [Light state design](polished/shelf-rename.html) · [Prototype](prototype.html#shelf-rename)

- Save name (action) → 41 · `shelf-detail`
- Back (back) → 41 · `shelf-detail`

### 39 · Delete this shelf? · `shelf-delete`

Shelves · dialog. [Wireframe](wireframes/shelf-delete.html) · [Light state design](polished/shelf-delete.html) · [Prototype](prototype.html#shelf-delete)

- Delete shelf (action) → 44 · `shelves-after-delete`
- Keep shelf (action) → 41 · `shelf-detail`
- Back (back) → 41 · `shelf-detail`

### 40 · Add to shelves · `shelf-membership`

Shelves · sheet. [Wireframe](wireframes/shelf-membership.html) · [Light state design](polished/shelf-membership.html) · [Prototype](prototype.html#shelf-membership)

- Create shelf (action) → 35 · `shelf-create`
- Save shelves (action) → 19 · `book-reading`
- Back (back) → 30 · `library-actions`

Annotation: A book may belong to multiple shelves. This changes membership only.

### 41 · Classics · `shelf-detail`

Shelves · base. [Wireframe](wireframes/shelf-detail.html) · [Light state design](polished/shelf-detail.html) · [Prototype](prototype.html#shelf-detail)

- Rename shelf (action) → 38 · `shelf-rename`
- Delete shelf (action) → 39 · `shelf-delete`
- Add books (action) → 87 · `shelf-add-books`
- Pride and Prejudice (action) → 19 · `book-reading`
- Frankenstein (action) → 18 · `book-saved`
- Back (back) → 33 · `shelves-list`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 42 · Classics to revisit · `shelf-detail-empty`

Shelves · empty. [Wireframe](wireframes/shelf-detail-empty.html) · [Light state design](polished/shelf-detail-empty.html) · [Prototype](prototype.html#shelf-detail-empty)

- Add books (action) → 87 · `shelf-add-books`
- Rename shelf (action) → 38 · `shelf-rename`
- Delete shelf (action) → 39 · `shelf-delete`
- Back (back) → 33 · `shelves-list`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`

### 43 · Library · `journal-all`

Journal · base. [Wireframe](wireframes/journal-all.html) · [Light state design](polished/journal-all.html) · [Prototype](prototype.html#journal-all)

- New entry (action) → 88 · `journal-book-picker`
- Read First impressions (action) → 48 · `journal-view`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

### 44 · Library · `shelves-after-delete`

Shelves · after-removal. [Wireframe](wireframes/shelves-after-delete.html) · [Light state design](polished/shelves-after-delete.html) · [Prototype](prototype.html#shelves-after-delete)

- View saved books (action) → 24 · `library-books`
- New shelf (action) → 35 · `shelf-create`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

Annotation: Removal changes only its confirmed scope; other saved data remains visible.

### 45 · Book journal · `journal-book`

Journal · base. [Wireframe](wireframes/journal-book.html) · [Light state design](polished/journal-book.html) · [Prototype](prototype.html#journal-book)

- New entry (action) → 49 · `journal-create`
- Read First impressions (action) → 48 · `journal-view`
- Back (back) → 19 · `book-reading`

### 46 · Library · `journal-empty`

Journal · empty. [Wireframe](wireframes/journal-empty.html) · [Light state design](polished/journal-empty.html) · [Prototype](prototype.html#journal-empty)

- New entry (action) → 88 · `journal-book-picker`
- Home (navigation) → 09 · `home-returning`
- Explore (navigation) → 10 · `explore-browse`
- Library (navigation) → 24 · `library-books`
- Settings (toolbar) → 65 · `settings-main`
- Books (tab) → 24 · `library-books`
- Shelves (tab) → 33 · `shelves-list`
- Journal (tab) → 43 · `journal-all`

### 47 · Book journal · `journal-book-empty`

Journal · empty. [Wireframe](wireframes/journal-book-empty.html) · [Light state design](polished/journal-book-empty.html) · [Prototype](prototype.html#journal-book-empty)

- New entry (action) → 49 · `journal-create`
- Back (back) → 19 · `book-reading`

### 48 · Journal entry · `journal-view`

Journal · base. [Wireframe](wireframes/journal-view.html) · [Light state design](polished/journal-view.html) · [Prototype](prototype.html#journal-view)

- Return to passage (action) → 58 · `reader-highlight`
- Edit entry (action) → 50 · `journal-edit`
- Delete entry (action) → 51 · `journal-delete`
- Back (back) → 43 · `journal-all`

Annotation: Chapter 18 excerpt verified against Gutenberg 1342. The 28% value is a prototype anchor; production uses a stable passage locator.

### 49 · New journal entry · `journal-create`

Journal · base. [Wireframe](wireframes/journal-create.html) · [Light state design](polished/journal-create.html) · [Prototype](prototype.html#journal-create)

- Save entry (action) → 48 · `journal-view`
- Back (back) → 52 · `journal-discard`
- Choose book (action) → 88 · `journal-book-picker`

Annotation: When started from Reader, selected text and its stable passage reference are attached. From Journal, choose a library book first.

### 50 · Edit journal entry · `journal-edit`

Journal · base. [Wireframe](wireframes/journal-edit.html) · [Light state design](polished/journal-edit.html) · [Prototype](prototype.html#journal-edit)

- Save changes (action) → 48 · `journal-view`
- Back (back) → 52 · `journal-discard`

### 51 · Delete this entry? · `journal-delete`

Journal · dialog. [Wireframe](wireframes/journal-delete.html) · [Light state design](polished/journal-delete.html) · [Prototype](prototype.html#journal-delete)

- Delete entry (action) → 46 · `journal-empty`
- Keep entry (action) → 48 · `journal-view`
- Back (back) → 48 · `journal-view`

### 52 · Discard your changes? · `journal-discard`

Journal · dialog. [Wireframe](wireframes/journal-discard.html) · [Light state design](polished/journal-discard.html) · [Prototype](prototype.html#journal-discard)

- Keep editing (action) → 50 · `journal-edit`
- Discard changes (action) → 43 · `journal-all`
- Back (back) → 50 · `journal-edit`

### 53 · Pride and Prejudice · `reader-scroll`

Reader · scroll. [Wireframe](wireframes/reader-scroll.html) · [Light state design](polished/reader-scroll.html) · [Prototype](prototype.html#reader-scroll)

- Hide controls (action) → 54 · `reader-immersive`
- Reading appearance (action) → 59 · `reader-appearance`
- Contents (action) → 60 · `reader-contents`
- Search in book (action) → 61 · `reader-search`
- Add bookmark (action) → 56 · `reader-bookmark`
- Select passage (action) → 57 · `reader-selection`
- Back (back) → 19 · `book-reading`
- Book journal (action) → 45 · `journal-book`

Annotation: Reader demo anchor: 28%, Chapter 18. Continuous scroll is the default.

Annotation: Tap prose to reveal/hide controls; no primary destination navigation appears in Reader.

### 54 · Pride and Prejudice · `reader-immersive`

Reader · immersive. [Wireframe](wireframes/reader-immersive.html) · [Light state design](polished/reader-immersive.html) · [Prototype](prototype.html#reader-immersive)

- Show controls (action) → 53 · `reader-scroll`
- Select passage (action) → 57 · `reader-selection`
- Back (back) → 19 · `book-reading`

Annotation: Reader demo anchor: 28%, Chapter 18. Continuous scroll is the default.

Annotation: Tap prose to reveal/hide controls; no primary destination navigation appears in Reader.

### 55 · Pride and Prejudice · `reader-paged`

Reader · paged. [Wireframe](wireframes/reader-paged.html) · [Light state design](polished/reader-paged.html) · [Prototype](prototype.html#reader-paged)

- Previous passage (action) → 55 · `reader-paged`
- Next passage (action) → 55 · `reader-paged`
- Reading appearance (action) → 59 · `reader-appearance`
- Contents (action) → 60 · `reader-contents`
- Add bookmark (action) → 56 · `reader-bookmark`
- Search in book (action) → 61 · `reader-search`
- Select passage (action) → 57 · `reader-selection`
- Back (back) → 19 · `book-reading`
- Simulate reaching the end (event) → 64 · `reader-finished`
- Book journal (action) → 45 · `journal-book`

Annotation: Reader demo anchor: 28%, Chapter 18. Continuous scroll is the default.

Annotation: Tap prose to reveal/hide controls; no primary destination navigation appears in Reader.

### 56 · Pride and Prejudice · `reader-bookmark`

Reader · bookmark. [Wireframe](wireframes/reader-bookmark.html) · [Light state design](polished/reader-bookmark.html) · [Prototype](prototype.html#reader-bookmark)

- Remove bookmark (action) → 53 · `reader-scroll`
- Reading appearance (action) → 59 · `reader-appearance`
- Contents (action) → 60 · `reader-contents`
- Search in book (action) → 61 · `reader-search`
- Select passage (action) → 57 · `reader-selection`
- Back (back) → 19 · `book-reading`
- Book journal (action) → 45 · `journal-book`

Annotation: Reader demo anchor: 28%, Chapter 18. Continuous scroll is the default.

Annotation: Tap prose to reveal/hide controls; no primary destination navigation appears in Reader.

### 57 · Pride and Prejudice · `reader-selection`

Reader · selection. [Wireframe](wireframes/reader-selection.html) · [Light state design](polished/reader-selection.html) · [Prototype](prototype.html#reader-selection)

- Highlight (action) → 58 · `reader-highlight`
- Add note (action) → 49 · `journal-create`
- Dismiss selection (action) → 53 · `reader-scroll`
- Back (back) → 53 · `reader-scroll`

Annotation: Reader demo anchor: 28%, Chapter 18. Continuous scroll is the default.

Annotation: Tap prose to reveal/hide controls; no primary destination navigation appears in Reader.

### 58 · Pride and Prejudice · `reader-highlight`

Reader · highlight. [Wireframe](wireframes/reader-highlight.html) · [Light state design](polished/reader-highlight.html) · [Prototype](prototype.html#reader-highlight)

- Add note (action) → 49 · `journal-create`
- Remove highlight (action) → 53 · `reader-scroll`
- Reading appearance (action) → 59 · `reader-appearance`
- Contents (action) → 60 · `reader-contents`
- Search in book (action) → 61 · `reader-search`
- Add bookmark (action) → 56 · `reader-bookmark`
- Back (back) → 19 · `book-reading`
- Book journal (action) → 45 · `journal-book`

Annotation: Reader demo anchor: 28%, Chapter 18. Continuous scroll is the default.

Annotation: Tap prose to reveal/hide controls; no primary destination navigation appears in Reader.

### 59 · Reading appearance · `reader-appearance`

Reader · sheet. [Wireframe](wireframes/reader-appearance.html) · [Light state design](polished/reader-appearance.html) · [Prototype](prototype.html#reader-appearance)

- Done (action) → 53 · `reader-scroll`
- Back (back) → 53 · `reader-scroll`

Annotation: Changing paper, text size or mode preserves the current passage, not a pixel offset.

Annotation: App theme remains independent from reader Light/Sepia/Dark paper.

Annotation: Font, size, line spacing, margins, paper and reading mode are editable. The simulated prototype carries these values and preserves its passage anchor.

### 60 · Contents · `reader-contents`

Reader · base. [Wireframe](wireframes/reader-contents.html) · [Light state design](polished/reader-contents.html) · [Prototype](prototype.html#reader-contents)

- Go to Chapter 18 (action) → 53 · `reader-scroll`
- Open bookmarked passage (action) → 56 · `reader-bookmark`
- Back (back) → 53 · `reader-scroll`

Annotation: This prototype opens the representative Chapter 18 passage; neighboring chapter rows are visible only. Production contents navigate every stored chapter locator.

### 61 · Search in book · `reader-search`

Reader · base. [Wireframe](wireframes/reader-search.html) · [Light state design](polished/reader-search.html) · [Prototype](prototype.html#reader-search)

- Search this book (action) → 62 · `reader-search-results`
- Simulate no matches (event) → 63 · `reader-search-empty`
- Back (back) → 53 · `reader-scroll`

### 62 · Search in book · `reader-search-results`

Reader · base. [Wireframe](wireframes/reader-search-results.html) · [Light state design](polished/reader-search-results.html) · [Prototype](prototype.html#reader-search-results)

- Edit in-book search (action) → 61 · `reader-search`
- Jump to matching passage (action) → 53 · `reader-scroll`
- Back (back) → 53 · `reader-scroll`

Annotation: No fabricated global result count; production displays results from the actual downloaded text.

### 63 · Search in book · `reader-search-empty`

Reader · empty. [Wireframe](wireframes/reader-search-empty.html) · [Light state design](polished/reader-search-empty.html) · [Prototype](prototype.html#reader-search-empty)

- Change search (action) → 61 · `reader-search`
- Back (back) → 53 · `reader-scroll`

### 64 · The end · `reader-finished`

Reader · completion. [Wireframe](wireframes/reader-finished.html) · [Light state design](polished/reader-finished.html) · [Prototype](prototype.html#reader-finished)

- Mark as finished (action) → 27 · `library-finished`
- Write a final thought (action) → 49 · `journal-create`
- Keep reading (action) → 53 · `reader-scroll`
- Back (back) → 53 · `reader-scroll`

Annotation: Reaching the end offers an explicit status change; it does not silently publish or rate anything.

### 65 · Settings · `settings-main`

Settings · base. [Wireframe](wireframes/settings-main.html) · [Light state design](polished/settings-main.html) · [Prototype](prototype.html#settings-main)

- Account & sync (action) → 79 · `sync-local`
- Appearance (action) → 66 · `settings-appearance`
- Reader defaults (action) → 67 · `settings-reader-defaults`
- Downloaded books (action) → 68 · `settings-storage`
- About Veritalex (action) → 70 · `settings-about`
- Back (back) → 09 · `home-returning`

### 66 · Appearance · `settings-appearance`

Settings · base. [Wireframe](wireframes/settings-appearance.html) · [Light state design](polished/settings-appearance.html) · [Prototype](prototype.html#settings-appearance)

- Save appearance (action) → 65 · `settings-main`
- Back (back) → 65 · `settings-main`

### 67 · Reader defaults · `settings-reader-defaults`

Settings · base. [Wireframe](wireframes/settings-reader-defaults.html) · [Light state design](polished/settings-reader-defaults.html) · [Prototype](prototype.html#settings-reader-defaults)

- Save reader defaults (action) → 65 · `settings-main`
- Back (back) → 65 · `settings-main`

Annotation: Font, size, line spacing, margins, paper and reading mode are editable. The simulated prototype carries these values and preserves its passage anchor.

### 68 · Downloaded books · `settings-storage`

Settings · base. [Wireframe](wireframes/settings-storage.html) · [Light state design](polished/settings-storage.html) · [Prototype](prototype.html#settings-storage)

- Remove downloaded text (action) → 69 · `settings-storage-confirm`
- Back (back) → 65 · `settings-main`

Annotation: Show storage bytes only after measuring files on the device.

### 69 · Remove downloaded text? · `settings-storage-confirm`

Settings · dialog. [Wireframe](wireframes/settings-storage-confirm.html) · [Light state design](polished/settings-storage-confirm.html) · [Prototype](prototype.html#settings-storage-confirm)

- Remove downloads (action) → 74 · `settings-storage-empty`
- Keep downloads (action) → 68 · `settings-storage`
- Back (back) → 68 · `settings-storage`

### 70 · About Veritalex · `settings-about`

Settings · base. [Wireframe](wireframes/settings-about.html) · [Light state design](polished/settings-about.html) · [Prototype](prototype.html#settings-about)

- Back (back) → 65 · `settings-main`

Annotation: The installed app supplies its build version. No version is fabricated in this design.

### 71 · Account & sync · `account-details`

Account · base. [Wireframe](wireframes/account-details.html) · [Light state design](polished/account-details.html) · [Prototype](prototype.html#account-details)

- View sync status (action) → 82 · `sync-current`
- Review guest reading (action) → 05 · `auth-import-preview`
- Sign out (action) → 72 · `account-signout-pending`
- Delete account (action) → 73 · `account-delete-confirm`
- Back (back) → 65 · `settings-main`

Annotation: Example email is a design placeholder. The account workspace and local guest workspace remain distinct.

### 72 · Before you sign out · `account-signout-pending`

Account · dialog. [Wireframe](wireframes/account-signout-pending.html) · [Light state design](polished/account-signout-pending.html) · [Prototype](prototype.html#account-signout-pending)

- Sync before signing out (action) → 81 · `sync-syncing`
- Sign out and keep on device (action) → 79 · `sync-local`
- Stay signed in (action) → 71 · `account-details`
- Back (back) → 71 · `account-details`

Annotation: Signing out never merges unsynced account records into the guest workspace.

Annotation: Device retention must be scoped to the signed-out account; the next matching sign-in can retry sync.

### 73 · Delete your account? · `account-delete-confirm`

Account · dialog. [Wireframe](wireframes/account-delete-confirm.html) · [Light state design](polished/account-delete-confirm.html) · [Prototype](prototype.html#account-delete-confirm)

- Continue to verification (action) → 75 · `account-reauth`
- Keep my account (action) → 71 · `account-details`
- Back (back) → 71 · `account-details`

### 74 · Downloaded books · `settings-storage-empty`

Settings · empty. [Wireframe](wireframes/settings-storage-empty.html) · [Light state design](polished/settings-storage-empty.html) · [Prototype](prototype.html#settings-storage-empty)

- Open Library (action) → 24 · `library-books`
- Back (back) → 65 · `settings-main`

Annotation: Removal changes only its confirmed scope; other saved data remains visible.

### 75 · Verify it’s you · `account-reauth`

Account · base. [Wireframe](wireframes/account-reauth.html) · [Light state design](polished/account-reauth.html) · [Prototype](prototype.html#account-reauth)

- Verify with Google (action) → 76 · `account-deleting`
- Cancel deletion (action) → 71 · `account-details`
- Simulate verification failure (event) → 77 · `account-delete-error`
- Back (back) → 71 · `account-details`

Annotation: Production reauthentication must confirm the same account and require fresh verification. Prototype buttons simulate this only.

### 76 · Deleting your account · `account-deleting`

Account · progress. [Wireframe](wireframes/account-deleting.html) · [Light state design](polished/account-deleting.html) · [Prototype](prototype.html#account-deleting)

- Simulate deletion complete (event) → 78 · `account-deleted`
- Simulate deletion failure (event) → 77 · `account-delete-error`
- Back (back) → 71 · `account-details`

Annotation: Do not present a success state until the service confirms deletion. Back may leave this screen but must not imply cancellation of an accepted deletion.

### 77 · Deletion wasn’t confirmed · `account-delete-error`

Account · error. [Wireframe](wireframes/account-delete-error.html) · [Light state design](polished/account-delete-error.html) · [Prototype](prototype.html#account-delete-error)

- Verify and try again (action) → 75 · `account-reauth`
- Return to account (action) → 71 · `account-details`
- Back (back) → 71 · `account-details`

### 78 · Account deleted · `account-deleted`

Account · success. [Wireframe](wireframes/account-deleted.html) · [Light state design](polished/account-deleted.html) · [Prototype](prototype.html#account-deleted)

- Open guest library (action) → 08 · `home-first`
- Back (back) → 08 · `home-first`

### 79 · Account & sync · `sync-local`

Sync · local. [Wireframe](wireframes/sync-local.html) · [Light state design](polished/sync-local.html) · [Prototype](prototype.html#sync-local)

- Sign in to sync (action) → 02 · `auth-loading`
- Open Library (action) → 24 · `library-books`
- Back (back) → 65 · `settings-main`

Annotation: Sync copy describes confirmed local or account state; reading remains available offline.

### 80 · Account & sync · `sync-waiting`

Sync · waiting. [Wireframe](wireframes/sync-waiting.html) · [Light state design](polished/sync-waiting.html) · [Prototype](prototype.html#sync-waiting)

- Try sync now (action) → 81 · `sync-syncing`
- Keep reading (action) → 53 · `reader-scroll`
- Back (back) → 65 · `settings-main`

Annotation: Sync copy describes confirmed local or account state; reading remains available offline.

### 81 · Account & sync · `sync-syncing`

Sync · syncing. [Wireframe](wireframes/sync-syncing.html) · [Light state design](polished/sync-syncing.html) · [Prototype](prototype.html#sync-syncing)

- Keep reading (action) → 53 · `reader-scroll`
- Simulate sync complete (event) → 82 · `sync-current`
- Simulate sync failure (event) → 83 · `sync-failed`
- Back (back) → 65 · `settings-main`

Annotation: Sync copy describes confirmed local or account state; reading remains available offline.

### 82 · Account & sync · `sync-current`

Sync · current. [Wireframe](wireframes/sync-current.html) · [Light state design](polished/sync-current.html) · [Prototype](prototype.html#sync-current)

- Account details (action) → 71 · `account-details`
- Open Library (action) → 24 · `library-books`
- Back (back) → 65 · `settings-main`

Annotation: Sync copy describes confirmed local or account state; reading remains available offline.

### 83 · Account & sync · `sync-failed`

Sync · failed. [Wireframe](wireframes/sync-failed.html) · [Light state design](polished/sync-failed.html) · [Prototype](prototype.html#sync-failed)

- Try again (action) → 81 · `sync-syncing`
- Keep reading (action) → 53 · `reader-scroll`
- Back (back) → 65 · `settings-main`

Annotation: Sync copy describes confirmed local or account state; reading remains available offline.

### 84 · Account & sync · `sync-expired`

Sync · expired. [Wireframe](wireframes/sync-expired.html) · [Light state design](polished/sync-expired.html) · [Prototype](prototype.html#sync-expired)

- Sign in again (action) → 02 · `auth-loading`
- Keep reading offline (action) → 53 · `reader-scroll`
- Back (back) → 65 · `settings-main`

Annotation: Sync copy describes confirmed local or account state; reading remains available offline.

### 85 · Account & sync · `sync-restoring`

Sync · restoring. [Wireframe](wireframes/sync-restoring.html) · [Light state design](polished/sync-restoring.html) · [Prototype](prototype.html#sync-restoring)

- Use local library (action) → 24 · `library-books`
- Simulate restore complete (event) → 82 · `sync-current`
- Simulate restore interrupted (event) → 83 · `sync-failed`
- Back (back) → 65 · `settings-main`

Annotation: Sync copy describes confirmed local or account state; reading remains available offline.

### 86 · Choose where to continue · `sync-conflict`

Sync · conflict. [Wireframe](wireframes/sync-conflict.html) · [Light state design](polished/sync-conflict.html) · [Prototype](prototype.html#sync-conflict)

- Use selected position (action) → 53 · `reader-scroll`
- Decide later (action) → 09 · `home-returning`
- Back (back) → 71 · `account-details`

Annotation: Compare stable passage locators and modified time. Do not resolve a meaningful conflict by choosing the larger percentage silently.

### 87 · Add books to shelf · `shelf-add-books`

Shelves · picker. [Wireframe](wireframes/shelf-add-books.html) · [Light state design](polished/shelf-add-books.html) · [Prototype](prototype.html#shelf-add-books)

- Add selected books (action) → 41 · `shelf-detail`
- Back (back) → 42 · `shelf-detail-empty`

Annotation: This direction selects multiple Library books for one shelf. The per-book Add to shelves sheet is a separate operation.

### 88 · Choose a book · `journal-book-picker`

Journal · picker. [Wireframe](wireframes/journal-book-picker.html) · [Light state design](polished/journal-book-picker.html) · [Prototype](prototype.html#journal-book-picker)

- Pride and Prejudice (action) → 49 · `journal-create`
- Frankenstein (action) → 49 · `journal-create`
- Alice’s Adventures in Wonderland (action) → 49 · `journal-create`
- Back (back) → 43 · `journal-all`

Annotation: A journal entry always has an explicit book context. Starting from a book or selected Reader passage already supplies it.

