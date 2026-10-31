---
name: Veritalex Reading Refined
colors:
  primary: "#895021"
  on-primary: "#FFFFFF"
  surface: "#FFF8F3"
  on-surface: "#241A14"
  on-surface-variant: "#55483D"
  primary-container: "#FFDCBF"
  on-primary-container: "#2D1606"
  outline: "#857468"
---

# Design System: Veritalex - Reading, Refined
Project ID: 6233788376335662642. Approved MVP design, October 30 2026.

## 1. Visual Theme and Atmosphere
A calm, personal Android reading room. Refine the existing Figma design: warm paper, amber-brown accents, book-cover shelves and a clear Continue reading. Strict Material 3 / Material You. Simple, readable, deliberate. No marketing hero, decorative dashboard metrics, glass effects, gradients, giant display typography or social feed. Real native Android components and generous whitespace. Use only three primary destinations: Home, Explore, Library. Settings is a toolbar action. Library contains Books, Shelves, Journal.

## 2. Color Palette and Roles
Brand seed #895021. Light primary #895021, on-primary #FFFFFF, primary-container #FFDCBF, on-primary-container #2D1606. Warm paper surface #FFF8F3, surface-container-low #FCF1E8, surface-container #F5E9DF, surface-container-high #EEE1D5. Ink on-surface #241A14, on-surface-variant #55483D. Outline #857468, outline-variant #D7C3B4. Secondary #6F5B4B, secondary-container #F9DDC5. Tertiary #5D633D, tertiary-container #E1E8B8. Error #BA1A1A, error-container #FFDAD6. Highlights #F6E5A8 with ink text.
Dark companion: surface #19120D, containers #231A14/#2D231C/#382D25, on-surface #F0DFD6, muted #D6C3B7, primary #FFB77F, on-primary #4E2600, primary-container #6D3A0D, outline #9F8D83.
Use semantic Material roles, never cover-derived app themes. App appearance follows system, offers brand/dynamic color; reader paper Light/Sepia/Dark is independently selectable. No text with insufficient contrast.

## 3. Typography Rules
Roboto Flex for ALL app interface, headings and labels. Literata only for actual book prose and meaningful short book excerpts. UI titles 24/32 medium, section titles 20/28 medium, title text 16/24 medium, body 16/24 regular, supporting text 14/20, labels 14/20 medium. Reader prose 19/32 regular by default; book chapter heading 26/34. Prefer short sentence-case labels. No ornamental serifs on interface headings. Reflow for large fonts. Full book titles available on detail screens.

## 4. Component Stylings
Material 3 filled/tonal/text buttons; pill main action, minimum 48dp targets. Icon buttons have 48dp bounds. Navigation bar uses labelled destinations and a selected tonal pill. Search bars, filter chips, segmented controls, dropdown menus, bottom sheets, dialogs, switches, sliders and snackbars follow native Material behavior.
Cards softly rounded 16dp, sheets/dialogs 28dp; book covers 4dp preserve portrait ratio about 2:3. Flat tonal grouping; shadows only transient overlays. Avoid card-in-card layouts. Prefer natural cover grids, readable list rows and generous section spacing. Primary actions have clear verbs. One primary action per decision.
Reusable components: ContinueReading, BookCoverCard, BookListRow, ReadingStatusChip, DownloadState, SyncStatusRow, ShelfRow, JournalEntry, ReaderToolbar, ReaderAppearanceSheet, AccountEntry, EmptyState, RetryState.
Book imagery must use actual Gutenberg covers or dignified typeset fallback covers with correct book/author. No unrelated stock images. Books: Pride and Prejudice / Jane Austen / 1342; Frankenstein / Mary Shelley / 84; Alice's Adventures in Wonderland / Lewis Carroll / 11; Jane Eyre / Charlotte Bronte / 1260.
Ratings are private user data. No invented community ratings, publication dates, total pages, personalized recommendations or modern paid novels.

## 5. Layout Principles
Android phone baseline 412x915, validate down to 360dp. Edge-to-edge with safe status/navigation insets; content gutters 20dp (16dp compact), spacing 4/8/12/16/24/32dp. Top bars about 64dp, bottom navigation about 80dp plus system inset. Reader hides destination navigation; distraction-free text, controls on tap. Continuous scroll default with page mode option. Preserve passage when appearance changes.
Tablet: navigation rail and intentional list/detail panes. Reader centered measure 60-70 characters, optional contents pane. No giant stretched phone.
Guest data stays on device; Google sign-in is optional. Cloud status is factual: Saved on device, Waiting to sync, Syncing, Up to date, Sign in to sync, Couldn't sync. Reading remains usable offline. Separate account and guest workspaces. Never show backend implementation terms in app copy.

## 6. Clarity and interaction rules
Content and state lead the routine screens. On book details, place the current reading/download state and one prominent next action before summary/source metadata: Download to read, Start reading, or Continue reading. Keep saving for later separate from downloading. Library membership and passage bookmarks use distinct symbols.

Home leads with the current book; Library and Journal prioritize content rows and useful filters. Use one clear creation entry point. Shelf overflow opens Rename and Delete choices. Journal passage navigation belongs with an entry that has a real locator. Keep main navigation, tabs, and consequential action labels visible; familiar toolbar icons have accessible names and state. Every interactive control keeps a minimum 48dp target.

Supporting text supplies current values, consequences or recovery. Remove paraphrases, repeated headings, duplicate populated-state discovery actions and explanations of absent features. Preserve explicit import, pending-write sign-out, deletion and reading-position choice information. Reader prose and personal writing are content, not explanatory copy to shorten. The clarity revision is reviewed at revisions/clarity-v1/index.html.
