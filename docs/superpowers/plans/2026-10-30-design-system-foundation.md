# Design system foundation implementation plan

**Goal:** Make the approved visual vocabulary usable and teachable in the existing three modules.

**Architecture:** MaterialTheme owns app color, type and shape. Additional packages contain only shared layout tokens, independent reader styles, focused component defaults and a debug gallery. Features keep their data and callbacks; sample fixtures and gallery state do not enter component APIs.

**Toolchain:** Retain AGP 9.5.0, Kotlin 2.4.21, BOM 2026.09.00 (resolved Compose 1.12.1 / Material3 1.4.0). No Styles alpha dependency.

- [x] Verify official guidance with Context7 for Material extensions, variable fonts, accessibility and component state behavior.
- [x] Finish `theme/`: appearance inputs, audited semantic colors, explicit full UI type scale, independent reader paper/type/selection and shared spacing/layout tokens. Recover only the licensed Android Literata asset from the archived source.
- [x] Add `components/`: role-based action variants with loading protection, labeled icon action, fields/search, flat card, cover/list row, status/progress and empty/retry presentation. Keep chips, selection controls, overlays and snackbars as direct Material usage where defaults suffice.
- [x] Add meaningful action-state, paper independence and color contrast checks; use preview/device checks for visual defaults.
- [x] Add `gallery/` under designsystem debug sources and a debug-only activity entry in app. Show all roles, states, type, spacing, radii, reader papers and direct Material examples with local demo state.
- [x] Adopt book rows and shared tokens in `BooksScreen`; retain stateless sample-only behavior and long-text/empty/large-type previews.
- [x] Write `docs/DESIGN_SYSTEM.md` with decisions, semantic usage, copyable examples, source links and verification evidence. Update README and learning path.
- [x] Run debug/release assembly, lint, unit and connected tests; inspect narrow/200%/dark/tablet renderings and restore temporary emulator configuration.

The owner has already approved the design and authorized implementation in the current checkout. Preserve the two pre-existing `.idea` changes and all `.stitch` files. No new modules, persistence, navigation framework, product flows, commits or publishing.
