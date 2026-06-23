# Hermes Desktop Build Fix — Dependency Version Mismatch

**Date:** 2026-06-23  
**Status:** RESOLVED  
**Commits:** `fda98e38a`, `0e9718d2e`, `fe3e8de60`

---

## Symptom

`npm run build --workspace apps/desktop` failed during the Vite/Rolldown JS bundle phase with unresolved imports:

```
@assistant-ui/react imports tapClientLookup, tapClientResource
from @assistant-ui/store — symbols not found in installed version
```

The error appeared downstream of a successful `npm install`, native dep staging, and TypeScript compilation. The Electron mirror message that accompanied the failure was a red herring — the Electron binary download was a separate background step; the blocking step was the Vite module graph resolution.

---

## Root Cause

After the `eb2b0ec4c` upstream merge (`upstream/main` → local `main`), the root `package.json` had:

```json
"overrides": {
  "@assistant-ui/store": "0.2.13"
}
```

`@assistant-ui/react@0.12.28` (the version in `apps/desktop`) imports `tapClientLookup` and `tapClientResource` from `@assistant-ui/store`. These symbols were introduced in `@assistant-ui/store@0.2.20` (tagged `store-0.2-compat`). The override pinned the store to `0.2.13`, which pre-dates those exports.

Secondary cause: `@assistant-ui/react@0.12.28` also had two renamed export references from the 0.17 upstream that broke TypeScript compilation:
- `COMPLETION_DRAWER_ROW_CLASS` removed from `completion-drawer` exports
- `setThreadScrolledUp` removed; replacement is `setThreadAtBottom` (inverted semantics)

---

## Fix Applied

### Step 1 — Resolve TS renamed-export errors (`fda98e38a`)

- `apps/desktop/src/app/chat/composer/skin-slash-popover.tsx`: inline `ROW_BASE_CLASS` locally instead of importing `COMPLETION_DRAWER_ROW_CLASS`
- `apps/desktop/src/components/assistant-ui/thread-virtualizer.tsx`: replace `setThreadScrolledUp(true)` with `setThreadAtBottom(false)` (inverted semantics)

### Step 2 — Upgrade store override (`0e9718d2e`)

Updated `package.json` overrides:

```json
// before
"@assistant-ui/store": "0.2.13"

// after
"@assistant-ui/store": "0.2.20"
```

Regenerated `package-lock.json` to reflect the upgraded resolution. `@assistant-ui/react@0.12.28` requires `@assistant-ui/store@^0.2.9`; `0.2.20` satisfies this and exports both required symbols.

### Step 3 — Remove spurious direct dep (`fe3e8de60`)

The `npm install` invocation in Step 2 also added `@assistant-ui/store: ^0.2.20` to root `dependencies`, which conflicts with the override (npm@10 EOVERRIDE: cannot override a direct dependency). Removed the direct dep; kept only the override pin.

---

## Verification

```
@assistant-ui/store@0.2.20 exports:
  tapClientLookup   ✓
  tapClientResource ✓
  tapClientList     ✓
  tapAssistantClientRef ✓
  (21 total exports)

npm ls @assistant-ui/react @assistant-ui/store --workspaces:
  hermes@0.17.0 → @assistant-ui/react@0.12.28
    @assistant-ui/store@0.2.20 overridden  ✓ (no EOVERRIDE)

npm run build --workspace apps/desktop:
  ✓ 11,796 modules transformed
  ✓ built in 8.27s
  ✓ assert-dist-built: dist/index.html + assets present
```

---

## What Was NOT Done

- No Electron mirror change (not the root cause)
- No `npm audit fix`
- No node_modules patching
- No vendor/shim of missing exports
- No upstream merge
- No generated build artifacts committed (`apps/desktop/build/` is gitignored)

---

## Version Alignment Reference

| Package | Required by | Constraint | Resolved |
|---|---|---|---|
| `@assistant-ui/store` | `@assistant-ui/react@0.12.28` | `^0.2.9` | `0.2.20` (override) |
| `@assistant-ui/store` | `@assistant-ui/core@0.1.17` | `^0.2.9` | `0.2.20` (deduped) |
| `@assistant-ui/react` | `apps/desktop` | `^0.12.28` | `0.12.28` |
