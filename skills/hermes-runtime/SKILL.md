---
name: hermes-runtime
description: 'Hermes/OpenClaw agent runtime architecture: session lifecycle, skill document loading, tool execution pipeline, exec allowlist, cron job management, Docker deployment, API gateway routing (Together AI/Anthropic), model routing, agent fleet configuration, monitoring stack, the Town-Hermes runtime bridge, and the loop architecture reference (turn-based/goal-based/time-based/proactive loops mapped to Hermes primitives). Use whenever the user asks about how Hermes sessions run, cron scheduling, agent authority levels, loop design, or runtime configuration.'
---

# Hermes Runtime

**Status:** DRAFT / NOT ACTIVE
**Created:** 2026-05-18

## Purpose

Encode the Hermes/OpenClaw agent runtime mechanics -- how sessions start, how tools execute, how cron jobs fire, and how the infrastructure is configured. The screener-ops skill covers *what* the fleet does; the openclaw-agent-optimize skill covers *how to tune* it; this skill covers the runtime machinery itself.

---

## Repo Context

**Repo:** `Warrenpoobear/hermes-agent`
**Version:** v0.14.0 (latest release, upgraded 2026-05-24)
**Key files:**
- `cli.py` (683KB) -- Main CLI entry point
- `AGENTS.md` (69KB) -- Agent fleet documentation
- `CONTRIBUTING.md` (46KB) -- Contributor guide
- `SECURITY.md` (7KB) -- Security advisory handling
- `hermes_constants.py` (13KB) -- Runtime constants
- `batch_runner.py` (57KB) -- Batch execution engine

---

## Session Lifecycle

### Session Start

1. **Config load:** Read `cli-config.yaml` (or equivalent) for model routing, API keys, tool permissions
2. **Skill loading:** Load SKILL.md files from configured skill directories. Skills are Markdown files created after 5+ tool calls in prior sessions.
3. **Memory load:** Load `.learnings/memory.md` (HOT tier, <=100 lines) first, then namespace-specific files on demand
4. **Agent bootstrap:** Load per-agent `SOUL.md` and `AGENTS.md` configuration
5. **Tool registration:** Register available tools based on agent authority level
6. **Session ready:** Agent begins processing

### Session End

1. **Skill creation check:** If 5+ tool calls were made, evaluate whether a new skill document should be created
2. **Memory update:** Write any corrections or learnings to `.learnings/` files
3. **Artifact output:** Write results to designated output paths
4. **Heartbeat update:** Update `HEARTBEAT.md` with session completion timestamp

---

## Model Routing

### API Configuration (as of May 2026)

| Model Pattern | API Gateway | Notes |
| --- | --- | --- |
| `deepseek*` | Together AI (OpenAI-compatible) | Primary for all agents |
| `claude*` | Anthropic SDK | Fallback for Claude-specific models |
| Previous | Llama 3.3 70B (2026-05-13 to 2026-05-20), OpenRouter (out of credits 2026-05-13) |

### Primary Model

**DeepSeek v4 flash** (Together AI) -- all agents default to this (switched 2026-05-20).

### Inference Parameters (DeepSeek v4-optimized)

| Parameter | Value | Rationale |
| --- | --- | --- |
| Temperature | 0.2 | Stronger governance determinism |
| Frequency penalty | 0.1 | Reduce repetition loops |
| Top_p | 0.95 | Tighter nucleus sampling |
| Repetition penalty | 1.2 | Anti-loop guard |
| API timeout | 2400s | Together can spike 8-12s cold start |
| Retry strategy | Exponential backoff | 500ms-8000ms delays |
| Compression threshold | 0.5 | Less aggressive for 131K context window |

### Gateway Monitoring

- `~/.hermes/monitor_together_latency.py` tracks latency trends
- Alerts on success rate < 80% or avg latency > 5s
- Logs to `together_latency.log`

---

## Cron Job Management

### Production Cron Schedule

| Job | Time (ET) | Frequency | Notes |
| --- | --- | --- | --- |
| Daily production pipeline | 5:30 PM | Weekdays | 13-step orchestrator |
| @reboot catch-up | On boot | -- | Catches missed runs after sleep/restart |
| Universe maintenance | 10:00 AM | Weekdays | Fixed race condition (was running before rankings.csv existed) |

### Cron Infrastructure

- **Environment:** WSL2 on Windows host
- **Sleep-cliff risk:** Windows host suspend kills crons silently
- **Stopgap:** `powercfg /change standby-timeout-ac 0` (disable sleep)
- **Missed cron signature:** 24-48h gap in `data/snapshots/`
- **Planned migration:** $15/mo Linux VPS (DigitalOcean / Hetzner). No timeline set.

### Critical Constraint

No cron job may depend on a gateway token (from operational routing policy, Lane A).

---

## Tool Execution Pipeline

### Authority Levels

| Level | What It Can Do | Who Has It |
| --- | --- | --- |
| observe_only | Read files, check status | Most monitoring agents |
| observe_and_propose | Read + suggest changes | Analysis agents |
| write_artifacts | Write to artifacts/ | Report generators |
| mutate_data | Write to data/ directories | Only `crt_resolution_watcher` |
| mutate_config | Modify configuration | No agent (operator only) |

### Exec Allowlist

The tool execution pipeline has an exec allowlist that controls which shell commands agents can run. Known bypass vectors (from Texas A&M taxonomy, 470 advisories):
- Line continuation bypass
- Busybox multiplexing
- GNU long-option abbreviation
- These compose into a complete unauthenticated RCE path from LLM tool call to host process

### Execution Lanes (Operational Routing Policy)

| Lane | Description | LLM Usage | Cron Allowed |
| --- | --- | --- | --- |
| A (Deterministic Production) | Scripts, cron, tests only | None | Yes |
| B (Cheap Monitoring) | File/JSON checks first, LLM on anomaly only | Anomaly-triggered | Yes (via `run_agent_direct.py`) |
| C (High-Token Manual) | Synthesis, audits, refactoring | Full | No (manual sessions only) |

---

## Docker Deployment

### Files

- `Dockerfile` (4.3KB) -- Multi-stage build
- `docker-compose.yml` (3.1KB) -- Service composition
- `docker/` -- Additional Docker configuration

### Current Status

Docker deployment is available but the production environment runs on WSL2, not Docker. Docker is primarily used for reproducible development environments.

---

## Agent Fleet Configuration

### Agent Count (Authoritative: agent_governance.md)

30 total agents:
- 27 active
- 1 suppressed (bioshort_watch)
- 1 retired (company_news_ingest)
- 1 shadow (shadow_watch)



**Citation rule (origin: failure F-2026-008, NC):** Agent count is a moving target — it has appeared as 17 / 26 / 27 / 28 / 30 across documents. Always source it from `agent_governance.md` with a **dated** reference (e.g. "30 agents per agent_governance.md, 2026-05-17"). Never hardcode a bare count elsewhere; write "see agent_governance.md for current count" instead. The same dated-citation discipline applies to any count that drifts as the fleet changes (active vs. suppressed vs. retired vs. shadow).

### Per-Agent Configuration

Each agent has:
- `SOUL.md` -- Operating manual defining boundaries, tools, heartbeat checks
- `AGENTS.md` entry -- Fleet-wide documentation
- Authority level from registry
- Structured prompting conventions (IF/THEN chains, step numbering, schema-first output)

### Uncertainty Handling (Per-Agent Rules)

| Agent | Missing Data Response | Confidence Rule |
| --- | --- | --- |
| ops_supervisor | RED (not GUESS) | < 0.7 -> escalate |
| sentinel | FAIL | Boundary cases -> WARN |
| data_auditor | FAIL | Specific counts, not "some" |
| ic_health_monitor | UNKNOWN | Threshold boundaries -> ALERT (conservative) |
| fleet_steward | MEDIUM | Missing last_run -> anomalous (not healthy) |

---

## Monitoring Stack

| Layer | Tool | Purpose |
| --- | --- | --- |
| Heartbeat | `tools/agent_heartbeat_checks.py` | Per-agent health (HEARTBEAT.md) |
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

---

## Town-Hermes Bridge (Runtime Side)

From the Hermes side, the bridge works via `common/operator_delivery.py`:

```
Hermes job completes
  -> write ledger artifact (repo)
  -> send_operator_event(channel="town", ...)
    -> structured email to djschulz@gmail.com
    -> Town routine triggers on [Hermes] subject prefix
```

**Phase A** (dry-run mode, `OPERATOR_DELIVERY_DRY_RUN=1`): Complete.
**Phase B** (live delivery): Not yet started.

---

## Hermes Link

**Version:** v0.6.5
**Package:** `@hermespilot/link` (npm)
**Mode:** Paired, relay-connected

### Install Location

| Component | Path |
| --- | --- |
| Binary | `~/.npm-global/bin/hermeslink` |
| Package source | `~/.npm-global/lib/node_modules/@hermespilot/link/dist/cli/index.js` |
| Runtime data | `~/.hermeslink/` (config, staging dir, conversations) |
| Local API port | 52379 |

`~/.npm-global/bin` is in PATH globally, so `hermeslink` works as a command from anywhere.

### Purpose

Bridges Hermes agent fleet with external surfaces (Town, Cursor). Provides:
- Local API relay on port 52379
- Paired mode connection to relay service
- Conversation staging and routing

---



## Loop Architecture (External Reference)

**Source:** Anthropic, "Getting started with loops" (Claude Code team), published 2026-06-30 — https://claude.com/blog/getting-started-with-loops
**Status:** Reference framework only. Documents Anthropic's loop taxonomy and maps it onto existing Hermes primitives. Does NOT authorize new automations, cron jobs, or agent-authority changes. Any promotion of a Hermes loop to a new autonomy mode is a separate governance decision.

Anthropic defines a **loop** as an agent repeating cycles of work until a stop condition is met. Four types, ordered by how much you hand off:

| Loop type | You hand off | Use it when | Claude Code primitive | Hermes equivalent |
| --- | --- | --- | --- | --- |
| Turn-based | The check (human verifies each turn) | Exploring or deciding | Custom verification skills | Manual Lane C session (operator is the verifier) |
| Goal-based | The stop condition | You know what "done" looks like | `/goal` | No native equivalent — closest is a script-driven pass/fail gate in Lane A |
| Time-based | The trigger | Work happens on a schedule, outside the project | `/loop`, `/schedule` | Cron schedule (Lane A/B), `@reboot` catch-up |
| Proactive | The prompt | Work is recurring and well-defined | All of the above + dynamic workflows | Full production pipeline + supervisor/sentinel stack |

### Key mechanics

- **`/goal` — separate-evaluator pattern (most transferable).** After each turn, Claude Code sends the stop condition plus the transcript to a separate small/fast model (Haiku by default) that judges "are we there yet?" and returns yes/no with a reason. On "no," the reason becomes the next instruction; on "yes," the goal auto-clears and the run stops. The agent that did the work is *not* the one that decides it is done. This mirrors Hermes's own separation of terminal agents (ops_supervisor, sentinel) from the agents they judge — the evaluator/executor split is a governance principle, not just an implementation detail.
- **`/loop`** — re-runs a prompt on an interval (min 1 minute) or self-paced; runs on the local machine; needs an open session; stopped with `Esc`. Analogous to Hermes weekday crons but session-bound rather than headless.
- **`/schedule`** — runs on Anthropic's cloud (min 1-hour interval); no open session required; stops on schedule end. Closest to a headless VPS cron (the planned Hermes migration target).

### Stop-condition and token discipline

- Give every loop **a budget and a verifier.** Imprecise goal conditions burn tokens for little output — success/evaluation criteria must be explicit and checkable.
- Recommended maturation path: start watched (`/loop`) -> graduate to a verified stop condition (`/goal`) once you trust the verifier -> move durable ones to `/schedule` once you trust the budget.
- This reinforces existing Hermes constraints: fail-closed on stale/uncertain data, observe-only defaults, and no promotion of prep-only agents to live automations without explicit approval. The loop taxonomy is a design vocabulary for reasoning about *which* autonomy mode a given Hermes job belongs in — it does not relax any freeze boundary.

---

## Troubleshooting Quick Reference

| Symptom | Likely Cause | First Check |
| --- | --- | --- |
| Agent STALE (no heartbeat > 48h) | Cron missed or agent crashed | `crontab -l`, check `together_latency.log` |
| Preflight timeout | Agent startup > 20s (was 10s, fixed 2026-05-24) | Check `tools/agent_preflight.py` |
| Pipeline timeout | AACT Monday batch or API latency | Check pipeline step that timed out |
| Herald DARK | Classification pipeline broken or dedupe failed | Check for `deduped_{date}.jsonl` file |
| CI RED | Test failure or dependency issue | Check GitHub Actions, PR #285 status |
| Together API errors | Rate limit or service outage | Check `monitor_together_latency.py` output |
| Sleep-cliff miss | Windows host suspended | Check `data/snapshots/` for gap |
