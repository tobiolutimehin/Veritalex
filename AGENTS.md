# Repository workflow

- Prefix shell commands with `rtk`; use `rtk proxy` for commands without a dedicated wrapper. See `/Users/tobiolutimehin/.codex/RTK.md`.
- Inspect Git status before work and again before finishing. Preserve changes owned by the user or another chat.
- Once requested work is complete and verified, create focused local commits for that work by default. Do not leave your completed changes uncommitted. Do not push unless requested.
- Stage only the task's changes. Keep concurrent feature work out of unrelated commits, including unrelated hunks in shared files.
- Keep intentional design sources, screenshots, handoff documents and review evidence tracked. Ignore generated caches, build output and local distribution archives. Untrack already-ignored local artifacts when appropriate, preserving local copies.
- Do not hide unfinished work with ignore rules, assume-unchanged, skip-worktree, stashing, resets or deletion. If other work remains dirty, identify its scope accurately.
- Prefer `gh` and CLI tools for GitHub work. Use browser automation only when the required action has no suitable CLI or API.

## Current library documentation

Use Context7 MCP for library, framework, SDK, API, CLI and cloud-service questions, including configuration, migration and library-specific debugging. Read `/Users/tobiolutimehin/.agents/skills/context7-mcp/SKILL.md` when applying this workflow.

1. Start with `resolve-library-id`, unless the user supplied an exact Context7 library ID.
2. Prefer an exact, relevant official source with reputable, current documentation; use a version-specific ID when needed.
3. Call `query-docs` with the selected ID and a focused question. Query separate concepts separately.
4. Base the answer or implementation on the fetched documentation. If unavailable, state that and use official documentation as a fallback.

Context7 is unnecessary for general programming concepts, local scripts, business-logic debugging, refactoring or code review that does not ask about a library API.
