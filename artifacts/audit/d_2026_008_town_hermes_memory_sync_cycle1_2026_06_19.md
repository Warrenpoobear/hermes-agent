# D-2026-008 — Town -> Hermes/Cursor Manual Memory-Sync Cycle #1

- **Date:** 2026-06-19
- **Component:** town-hermes-feedback (Channel 1: Memory Sync) / self-improving (Rule 2, tiered storage)
- **Status:** ACTIVE
- **Authoring:** Town assistant, operator-mediated (Darren Schulz)
- **Related PR:** #28 (`.learnings/memory.md` freshness)

## Decision

Execute manual Town -> Hermes/Cursor memory-sync **cycle #1** — a reviewed, operator-mediated commit of HOT-memory freshness edits. No automation wired.

## Rationale

Post-h20d feedback-protocol sequence requires: (1) pilot governance decision logging, (2) pilot weekly manual memory sync, then (3) automated export only after **two clean manual cycles + operator approval**. This cycle executes step (2) and is itself recorded under step (1). Town has no write path to the Hermes runtime, so sync is a reviewed manual commit (branch + operator-merged PR), not a wired export.

## Evidence

- Town-Hermes Feedback Protocol (Channels 1-3; DRAFT/NOT ACTIVE; priority 5 of 7).
- self-improving tiered-storage mapping: Town global <-> `.learnings/memory.md` HOT (<=100-line cap).
- Governance decision 2026-05-22 (freeze until h20d = 2026-05-26, now elapsed).
- Memory-scope convention 2026-06-04 (operational state stays WARM / routine-scoped).
- Repo inspection 2026-06-19: existing `.learnings/memory.md` is live and current; `.cursorrules` + 9 `.cursor/rules/*.mdc` already cover governance; `artifacts/ops/` is a cron-managed NTFS junction; `latest_state.md` stale (generated 2026-05-25).

## What was committed (PR #28)

1. `Priority firms` -> `Tier 1 managers` (Fairmount / Deep Track / Logos) — terminology convention.
2. Town-Hermes Feedback Protocol line -> post-h20d status (manual reviewed sync only; automated export gated).

## Held back — not silently resolved (per knowledge-learnings.mdc contradiction rule)

- **Spec 100** status (Town: resolved @ `2faa88e6`; file/ledger: blocked) — governed by `held_spec_ledger`.
- **Architecture Freeze** status (file + `latest_state.md`: still "ACTIVE through ~2026-05-26").
- Root cause: knowledge-layer artifacts stale (pre-h20d). Recommend `tools/build_hermes_knowledge_layer.py` regen before reconciling, then a follow-up commit.

## Scope excluded

SEC dedup accession ledgers, daily pipeline delivery logs, per-run scan narratives (remain WARM, routine-scoped). Town-only UI guide skills NOT exported. No new `.cursor/rules` file (already covered). No write into `artifacts/ops/` (cron junction).

## Revisit conditions

After cycle #2 completes cleanly, re-evaluate advancing to step (3) automated export. Revisit immediately if any synced item is found to contain operational/dedup state (scope violation) or if `memory.md` exceeds the 100-line cap after merge.

## Related

- Spec 090 (Hermes -> Town email path)
- Governance decision 2026-05-22 (protocol freeze)
- Memory-scope convention 2026-06-04
- Town decision-audit-trail catalog (D-2026-001 .. D-2026-007)

## Cycle ledger (toward the two-clean-cycles gate)

| Cycle | Date | Items committed | Clean? | Notes |
|---|---|---|---|---|
| #1 | 2026-06-19 | memory.md freshness (PR #28), this record | PENDING (merge + verify) | First manual sync since freeze elapsed |
| #2 | — | — | — | Required before considering automated export |
