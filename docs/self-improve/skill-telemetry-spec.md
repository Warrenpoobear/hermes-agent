# Skill Execution Telemetry & Efficacy Spec (proposal)

**Status:** PROPOSAL / NOT IMPLEMENTED
**Author:** Town assistant (staged for Cursor-side implementation)
**Date:** 2026-06-24
**Scope:** Tier 0 — docs/skills/learnings + advisory logging only. NO production scoring, ranker, selector, sizing, or cron change. This spec adds observability; it does not change agent behavior or routing.

---

## Why

Today the self-improvement loop promotes lessons on intuition, not evidence. `self-improving` Rule 12 (promotion checklist) defines two gates — "Operator verdict >= 3 helpful" and "7+ days observation" — that are **inert** until skill-loading sessions actually emit telemetry. This spec defines that telemetry so the loop can answer: *which skills are worth keeping, patching, or trimming?*

It is the prerequisite that turns "we believe self-learning helps coding" into a measurable claim.

## Non-goals

- Does NOT auto-route agents to skills based on telemetry (needs observation period + operator sign-off — separate change).
- Does NOT auto-merge skill patches (Rule 11 FENCE still binds; `pattern_to_skillpatch.py` proposes, humans approve).
- Does NOT log prompt contents, portfolio data, PII, or credentials (see Privacy below).

---

## What each skill-loading agent session logs

One record per skill load per session, appended to a JSONL telemetry log (`artifacts/skills_telemetry/{YYYY-MM}.jsonl`).

| Field | Type | Notes |
| --- | --- | --- |
| `skill_name` | str | The skill loaded (e.g. `openclaw-cron-scheduler-debug`) |
| `execution_id` | str | Deterministic session/run id |
| `loaded_at` | ISO-8601 | Derived from `as_of_date`/run clock, never wall-clock guesses |
| `agent` | str | Which agent loaded it (e.g. `herald`, `fleet_steward`) |
| `outcome` | enum | `success` \| `fail` \| `partial` \| `unknown` |
| `latency_ms` | int | Optional; session duration where meaningful |
| `operator_verdict` | enum\|null | `helpful` \| `unhelpful` \| null (operator-supplied, async) |
| `pattern_key` | str\|null | If the session resolved a known failure-pattern, its key |

Logging is **append-only and advisory** — no agent decision branches on it at write time.

## Monthly report

`tools/skills_telemetry_report.py` (to be authored) reads the JSONL and emits `artifacts/skills_telemetry/report_{YYYY-MM}.md`:

- **Patch candidates:** skills with `>= 5` executions AND `< 80%` success rate.
- **Trim/demote candidates:** skills with `0` loads in 30 days (dead weight in the context budget).
- **High-confidence:** skills with `>= 5` executions AND `>= 95%` success (stable; safe to leave).
- **Operator-verdict roll-up:** count of `helpful`/`unhelpful` per skill (feeds Rule 12 "operator verdict >= 3" gate).

The report is the forcing function for the monthly loop review. It proposes; it does not act.

## Privacy / governance

- Log field allow-list only (the table above). Never log prompt bodies, file contents, tickers, holdings, or secrets — reuse the existing logging sanitization block (`api_key`, `password`, `secret`, `token`, `credential`, `ssn`, `account_number`, `cusip`).
- Determinism: timestamps from run clock, sorted JSONL keys, no `datetime.now()` in any path that feeds an artifact hash.
- The two stalled-loop outages (F-2026-005 Herald, F-2026-006 CI) cannot have efficacy measured until their recovery is confirmed from the host — telemetry on an unconfirmed fix measures nothing.

## Wiring sequence (operator-gated)

1. Land this spec (doc-only).
2. Author `skills_telemetry` logger as advisory append-only; wire into the skill-load path behind a flag (default ON for logging, no behavior change).
3. Accumulate `>= 5` executions per skill before citing any rate.
4. Author the monthly report; review first output with operator.
5. Only after that: consider activating Rule 12's telemetry-dependent gates.
