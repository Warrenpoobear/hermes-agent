# Screener Ops & Governance (Knowledge Reference)

<!--
SYNC PROVENANCE
  Source: Town skill `screener-ops`
  Source maturity (per skill-maturity-metadata): STABLE but HIGH-CHURN (7-day SLA, live CI/Herald/fleet state)
  Synced to Hermes: 2026-06-24 (manual, operator-approved, PR-gated)
  Sync owner: Darren Schulz (dschulz@wakerobin.co)
  Type: knowledge-layer reference (NOT an agent; no AGENT_REGISTRY.json entry, no cron, no authority)
  Batch: Town -> Hermes mapping pipeline.
  NOTE: Reference knowledge a SOUL.md may cite. It does not execute, mutate data, or write to .learnings/.
-->

> **LIVE-STATE WARNING — framework only.**
> This reference carries ONLY the stable Framework Reference (Section 1) of the source skill.
> The source skill's Section 2 "Operational State" — active ruleset ID, CI red day-count,
> Herald outage duration, agent-fleet counts, KG phase status, infrastructure host details,
> and dated sync snapshots — is **intentionally EXCLUDED** because it goes stale within days.
> This Hermes repo is itself the source of truth for fleet/CI/infra state: fetch it live via
> the Hermes MCP knowledge layer (`knowledge_read(artifact="latest_state")`,
> `held_spec_ledger`, `operator_brief`) and `agents/AGENT_REGISTRY.json` — never from this
> static copy. Do NOT hardcode agent counts here.

## Purpose

Reference for daily production operations, the Hermes knowledge layer, agent fleet monitoring, and the spec/governance lifecycle that governs all changes to the biotech screener.

---

## Daily Production Pipeline

Runner: `tools/run_daily_production.py` (13-step orchestrator). Cron: 5:30 PM ET weekdays + `@reboot` catch-up for missed runs.

### Pipeline Steps (in order)

1. Price refresh
2. Cache warm (including FDA)
3. Screen (with `--inputs-manifest write`)
4. Audit
5. Gates
6. Manifest + promotion
7. Drift report
8. Action packet
9. Shadow portfolio
10. Trade plan
11. Portfolio report
12. Readiness scorecard
13. Ops digest + PIT backfill (optional)

Key rule: always warm 8-K cache BEFORE running screen.

Pipeline timeout: 6000s (100 min) to cover worst-case AACT + tail steps.

> Monday timeout rule (origin: failure F-2026-004): Monday runs ingest the weekend AACT batch and are the longest of the week — the binding case for this timeout. Keep dedicated monitoring on Monday pipeline duration; validate ANY future timeout change against the trailing 4-week Monday duration distribution, not a single run. Treat a Monday run approaching the timeout as an ALERT even when mid-week runs finish comfortably.

---

## Hermes Knowledge Layer (Spec 089)

Generator: `tools/build_hermes_knowledge_layer.py`. Repo-native "ops brain" that continuously answers: current operational state; what changed since last good state; what is held/blocked/awaiting first-fire validation; what contradictions exist; the next allowed operator action; what is explicitly not allowed.

### Four Layers

| Layer | Purpose | Output |
| --- | --- | --- |
| Capture | Read-only from specs, artifacts, registry, git, cron | Raw state |
| Normalize | Structured ledgers | `artifacts/ops/knowledge_layer/` |
| Reason | Drift, contradiction, missed-run detection | Alerts |
| Deliver | Operator briefs | Daily/weekly summaries |

### Output Artifacts

| Artifact | Location |
| --- | --- |
| Latest state | `artifacts/ops/knowledge_layer/latest_state.{json,md}` |
| Held spec ledger | `artifacts/ops/held_spec_ledger/latest.{json,md}` |
| First fire ledger | `artifacts/ops/first_fire_ledger/latest.{json,md}` |
| Contradiction ledger | `artifacts/ops/contradiction_ledger/latest.md` |
| Operator briefs | `artifacts/ops/operator_brief/daily/YYYY-MM-DD.md` |

---

## Town-Hermes Bridge (Spec 090)

Module: `common/operator_delivery.py`. Routes Hermes Knowledge Layer events to Town via email trigger. Town does NOT control Hermes.

```
Hermes job completes
  -> write ledger artifact (repo)
  -> send_operator_event(channel="town", ...)
    -> structured email to TOWN_EMAIL (djschulz@gmail.com)
    -> Town routine triggers on [Hermes] subject prefix
    -> Town creates task / DMs operator
```

What Town is NOT: not a scheduler/cron controller; not a repo mutator or spec approver; not allowed to reactivate bioshort_watch LLM; not the authoritative source for any production state.

---

## OpenClaw Agent Fleet

### Agent Registry

File: `agents/AGENT_REGISTRY.json` (schema v1.0). Source the agent count dynamically from this file and cite `governance/agent_governance.md` with a dated reference — do NOT hardcode counts (documents have historically shown conflicting counts).

Authority levels: observe_only, observe_and_propose, write_artifacts, mutate_data, mutate_config. Only crt_resolution_watcher holds mutate_data authority (writes to catalyst resolution tables under orchestrator supervision). No agent holds mutate_config (operator-only).

### Model Configuration

- Primary model: DeepSeek v4 flash (Together AI) — all agents default to this
- Fallback: Anthropic Claude SDK (for Claude-specific models)
- Auto-routing: "deepseek" models -> Together API (OpenAI-compatible), "claude" -> Anthropic SDK

### Inference Tuning (DeepSeek v4-optimized)

| Parameter | Value | Rationale |
| --- | --- | --- |
| Temperature | 0.2 | Stronger governance determinism |
| Frequency penalty | 0.1 | Reduce repetition loops |
| Top_p | 0.95 | Tighter nucleus sampling |
| Repetition penalty | 1.2 | Anti-loop guard |
| API timeout | 2400s | DeepSeek inference variance (do not reduce below 2400s) |
| Retry strategy | Exponential backoff | 500ms-8000ms delays |
| Compression threshold | 0.5 | Less aggressive for 131K context |

### Uncertainty Handling (all agents)

- ops_supervisor: missing artifacts -> RED (not GUESS); confidence < 0.7 -> escalate
- sentinel: missing drift -> FAIL; boundary cases -> WARN; ambiguous rollback -> both commands
- data_auditor: missing snapshot -> FAIL; specific ticker counts (not "some")
- ic_health_monitor: missing dashboard -> UNKNOWN; threshold boundaries -> ALERT (conservative)
- fleet_steward: unreachable status -> MEDIUM; missing last_run -> anomalous (not healthy)

### Monitoring Layers

| Layer | Tool | Purpose |
| --- | --- | --- |
| Heartbeat | `tools/agent_heartbeat_checks.py` | Per-agent health |
| Supervisor | `agents/ops_supervisor/supervisor.py` | Fleet-wide anomaly classification |
| Post-snapshot | `tools/run_post_snapshot_supervisor.py` | Post-pipeline task orchestration |
| Sentinel | `tools/agent_supervisor_sentinel.py` | Final watchdog |

### Anomaly Classification

| Classification | Severity | Meaning |
| --- | --- | --- |
| new | ORANGE | First occurrence |
| carried | YELLOW | Same anomaly seen yesterday (exact text match) |
| resolved | GREEN | Previously seen, now gone |

Terminal agents (e.g., ops_supervisor) are intentionally unsupervised and do not carry HEARTBEAT.md.

### Herald Pipeline

Done predicate requires BOTH deduped AND classified JSONL: `data/press_releases/deduped/deduped_{date}.jsonl` and `data/press_releases/classified/classified_{date}.jsonl`. If classification failed but dedupe exists, the next supervisor run retries classification.

---

## SOUL.md / Ruleset System

SOUL.md: per-agent operating manual defining boundaries, tools, and heartbeat checks. Located in each agent workspace under `agents/{name}/SOUL.md`.

Ruleset Health Monitor (`tools/ruleset_health_monitor.py`): JSONL history grows with each new evaluation date (idempotent on same-day reruns); tracks consecutive WARN days by active ruleset ID; recommends rollback after sustained degradation.

---

## Governance Artifacts

- `governance/AGENT_ROUTING_POLICY.md`: Tier 0-4 routing policy classifying every part of the codebase by governance sensitivity. The policy itself is Tier 4; changes require a memo, not a direct edit.
- `governance/STATUS.md`: enforcement status.
- `governance/HASH_ROTATIONS.md`: required landing zone for any Tier 3 production-hash rotation. Each entry: old hash, new hash, effective date, affected surface, reason, downstream impact, reviewer.

### Operational Routing (three execution lanes)

- Lane A (Deterministic Production): No LLM. Scripts, cron, tests only.
- Lane B (Cheap Monitoring): File/JSON checks first. LLM on anomaly only via run_agent_direct.py.
- Lane C (High-Token Manual): Manual sessions for synthesis, audits, refactoring. No autonomous cron.

Critical constraint: no cron job may depend on a gateway token.

---

## Spec Lifecycle

### Spec States

| State | Meaning |
| --- | --- |
| DRAFT | Under development |
| IN PROGRESS | Active work, phased |
| HELD | Blocked on dependency |
| RESOLVED | All acceptance criteria met |
| SUPERSEDED / MITIGATED | Failure modes neutralized via different route |
| CLOSED | Formally closed |

Specs are numbered sequentially. Each has acceptance criteria with explicit section references, phase gates (A/B/C/D typical), blocking dependencies, and closure memos in `artifacts/audit/`.

### Held-Spec Ledger

Tracks all specs that are held/blocked with: what is held and why, first-fire validation status, alert deadlines, next operator action. (Fetch the live ledger via MCP — do not mirror its contents here.)

---

## Expectation Layer Coverage Gate (Spec 105)

QA file: `production_qa_check.py`. Production pipeline hard-fails if market-expectation fields are missing or under-covered in `rankings.csv`. Thresholds sourced from `FEATURE_COVERAGE_REQUIREMENTS` (single source of truth — do NOT hardcode coverage floors).

| Field | Required Coverage | Source |
| --- | --- | --- |
| `short_interest_pct` | 0.90 | Market data provider |
| `close_price` | 0.99 | Market data provider |
| `market_cap_mm` | 0.95 | Market data provider |
| `priced_move_pct` | 0.80 | Derived (catalyst pricing model) |
| `insider_net_buy_value_90d` | 0.30 | Form 4 (diagnostic only) |

Runs every pipeline execution at Step 5 (Gates). Hard fail if any required field is missing or below its per-field threshold. The expectation model must consume these columns from `rankings.csv`, not a parallel source.

---

## Export Contract Registry (Spec 101)

Tracks which computed fields are exported to CSV and snapshots. Runway Severity export (v1.1): `runway_severity_score`, `ev_severity_score`, `runway_buffer_months`, `financing_truth_gate`, `dilution_haircut`, `size_multiplier`, `severity_bucket`, `severity_notes`. `check_severity_formulas()` QA validation runs on every snapshot; validates finiteness before formula checks; fails explicitly on blank/NaN/Inf.

Derived field contracts (all non-null rows):

```
dilution_haircut == 0.35 * ev_severity_score       (tolerance 1e-6)
size_multiplier == max(0.40, 1 - 0.60 * ev_severity_score)  (tolerance 1e-6)
```

---

## Diagnostic Fields Registry (Spec 104)

Current diagnostic field: `insider_net_buy_value_90d` (DIAGNOSTIC ONLY). Must NOT enter the expectation model's `market_features` input (the `insider_net_buy_z` weight activates silently if it flows upstream). Guard via input exclusion (preferred), weight zeroing, or a pre-inference drop guard. Never collapse blank (NaN) and zero (0.0). Promotion requires 20+ stable snapshots, >= 60% coverage, IC > 0 at p < 0.05, Checklist v2 pass, explicit written approval.

---

## Backfill Tooling (Spec 102)

Research-enablement tooling for backfilling expectation fields into historical snapshots. Target fields: `short_interest_pct`, `close_price`, `market_cap_mm`, `priced_move_pct` (required); `insider_net_buy_value_90d` (optional). Default additive-only (`recompute=False`); original ranks/actions preserved. Every backfill emits a structured manifest; `_backfill_version` metadata column added (null for originals). Research scripts must filter on `_backfill_version` to avoid silent pre/post mixing.

---

## Source Files

| Component | File |
| --- | --- |
| Daily Production Runner | `tools/run_daily_production.py` |
| Knowledge Layer Builder | `tools/build_hermes_knowledge_layer.py` |
| Operator Delivery | `common/operator_delivery.py` |
| Agent Heartbeat Checks | `tools/agent_heartbeat_checks.py` |
| Ops Supervisor | `agents/ops_supervisor/supervisor.py` |
| Post-Snapshot Supervisor | `tools/run_post_snapshot_supervisor.py` |
| Ruleset Health Monitor | `tools/ruleset_health_monitor.py` |
| Ops Digest Builder | `tools/build_ops_digest.py` |
| Readiness Scorecard | `tools/weekly_readiness_scorecard.py` |
| Cron Wrapper | `tools/cron_daily_production.sh` |
