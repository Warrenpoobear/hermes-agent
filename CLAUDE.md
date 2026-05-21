# CLAUDE.md — Hermes Agent Fleet

## Project Identity
Multi-agent system for biotech investment monitoring and operational automation.
Maintained by Wake Robin's Director of Investments. Production fleet runs on OpenClaw runtime.

## Agent Fleet
- 30 total agents per `agents/AGENT_REGISTRY.json` (authoritative source, schema v1.0)
- 27 active, 1 suppressed (bioshort_watch), 1 retired (company_news_ingest), 1 shadow (shadow_watch)
- Never hardcode agent counts — always source from AGENT_REGISTRY.json with a dated citation

## Authority Levels
```
observe_only < observe_and_propose < write_artifacts < mutate_data < mutate_config
```
Only `crt_resolution_watcher` holds `mutate_data` (writes to catalyst resolution tables under orchestrator supervision).
No agent may modify production weights without traversing the full multi-gate promotion path.

## Model Configuration
- **Primary**: Llama 3.3 70B Instruct Turbo (Together AI) — all agents default
- **Fallback**: Anthropic Claude SDK (for Claude-specific models)
- **Routing**: "llama" models -> Together API (OpenAI-compatible), "claude" -> Anthropic SDK
- **Previous**: OpenRouter (out of credits as of 2026-05-13)

## Inference Parameters
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Temperature | 0.2 | Governance determinism |
| Frequency penalty | 0.1 | Reduce repetition loops |
| Top_p | 0.95 | Tighter nucleus sampling |
| Repetition penalty | 1.2 | Anti-loop guard |
| API timeout | 2400s | Together cold-start variance (8-12s spikes) |
| Retry strategy | Exponential backoff | 500ms-8000ms delays |
| Compression threshold | 0.5 | Less aggressive for 131K context |

## Llama-Specific Prompting Rules
- IF/THEN chains instead of open-ended reasoning
- Step numbering for multi-step workflows
- Schema-first output format — define output structure before requesting content
- No inferred data; report missing fields explicitly
- Never say "some" or "several" — use specific counts or "unknown"

## Uncertainty Handling (All Agents)
- Missing artifacts -> RED or FAIL (never GUESS)
- Confidence < 0.7 -> escalate to operator
- Missing drift data -> FAIL (not infer)
- Boundary/ambiguous cases -> WARN or ALERT (conservative)
- Unreachable agent status -> MEDIUM severity (not healthy)
- Missing last_run -> anomalous (not healthy)

## Three-Lane Routing
| Lane | Purpose | Tools |
|------|---------|-------|
| A — Deterministic | Production pipeline, cron | Scripts, static checks only |
| B — Cheap Monitoring | Fleet health, anomaly detection | Low-risk agents (observe_only) |
| C — Manual Engineering | Architecture changes, spec work | Claude Code, human review |

No cron job may depend on a gateway token.
Terminal agents (e.g., ops_supervisor) are intentionally unsupervised and do not carry HEARTBEAT.md.

## Monitoring Stack
| Layer | Tool | Purpose |
|-------|------|---------|
| Heartbeat | `tools/agent_heartbeat_checks.py` | Per-agent health |
| Supervisor | `agents/ops_supervisor/supervisor.py` | Fleet-wide anomaly classification |
| Post-snapshot | `tools/run_post_snapshot_supervisor.py` | Post-pipeline task orchestration |
| Sentinel | `tools/agent_supervisor_sentinel.py` | Final watchdog |
| Gateway | `~/.hermes/monitor_together_latency.py` | Latency trends, alerts on <80% success or >5s avg |

## Anomaly Classification
| Classification | Severity | Meaning |
|----------------|----------|---------|
| new | ORANGE | First occurrence |
| carried | YELLOW | Same anomaly seen yesterday (exact text match) |
| resolved | GREEN | Previously seen, now gone |

## Herald Pipeline
Done predicate requires BOTH:
- `data/press_releases/deduped/deduped_{date}.jsonl`
- `data/press_releases/classified/classified_{date}.jsonl`

If classification failed but dedupe exists, next supervisor run retries classification.

## OpenClaw Runtime
- Gateway: 127.0.0.1:18789, loopback only, auth via setup token
- Workspace per agent: `agents/{agent_name}/` with SOUL.md, TOOLS.md, HEARTBEAT.md
- Status: maintenance-only as of mid-May 2026 (stable, no new features expected)
- Migration path: `hermes claw migrate` available but NOT approved — Tier 4 governance decision

## Key References
- Agent fleet documentation: `agents/AGENTS.md` (46KB)
- Contributor guide: `CONTRIBUTING.md` (28KB)
- Agent registry: `agents/AGENT_REGISTRY.json`
- Governance policy: see biotech-screener `governance/AGENT_ROUTING_POLICY.md`
- Ops routing: `docs/ops/hermes_openclaw_routing_policy.md`

## Commands
```bash
# Docker
docker compose build
docker compose up -d

# Agent health
python tools/agent_heartbeat_checks.py
python agents/ops_supervisor/supervisor.py

# Gateway monitoring
python ~/.hermes/monitor_together_latency.py
```

## Do Not
- Do not reactivate bioshort_watch LLM
- Do not modify production weights without full promotion path
- Do not hardcode agent counts (source from AGENT_REGISTRY.json)
- Do not let any cron job depend on a gateway token
- Do not adopt Hermes runtime without Tier 4 governance review
- Do not allow self-evolving skill loops without version control and review
