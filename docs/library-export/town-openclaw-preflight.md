---
description: "Town/OpenClaw agent context preflight — collect context and classify risk before any Hermes agent task"
---

# Town/OpenClaw Preflight

Before performing any Hermes, OpenClaw, or Town agent task, run this preflight to collect context and classify whether the task is safe, gated, or blocked.

**Scope:** Read-only context collection and risk classification. No runtime behavior changes. No MCP config changes. No AGENT_REGISTRY edits. No skills/openclaw edits. No automation. No commits unless approved.

---

## Step 1 — Load Governance Context

Read the following documents in full before proceeding:

1. `docs/TOWN_OPENCLAW_AGENT_FLOW_CONTRACT.md` — the governing flow contract
2. `docs/FAILURE_PATTERN_LIBRARY.md` — known failure modes and prevention rules

If either file is missing or unreadable, stop and report the gap.

---

## Step 2 — Collect MCP Context

Use available Hermes MCP tools to gather current system state. Run whichever of the following are available:

| Tool | Purpose |
|---|---|
| `fleet_context_snapshot` | Current agent fleet state |
| `agent_health_summary` | Per-agent health and last-run status |
| `town_brief` | Structured system summary |
| `skills_list` / `skills_read` | Enumerate skills; read specific skill if relevant to the task |
| `agents_list` / `agents_get` | Enumerate agents; read specific agent metadata if relevant |
| `knowledge_query` | Query knowledge ledgers for relevant context |

If MCP tools are not available (e.g., Hermes MCP server is not running), note this in the report and proceed with document-only context.

---

## Step 3 — Classify What the Request Touches

Determine which layer(s) of the system the request affects. A request may touch multiple layers.

| Layer | Examples | Risk |
|---|---|---|
| **Docs only** | Markdown files in `docs/`, templates, READMEs | SAFE |
| **Wrapper skill** | Files in `skills/openclaw/*` | GATED |
| **Registry** | `AGENT_REGISTRY.json`, `/workspace/agents` | GATED |
| **Runtime identity** | `HERMES_AGENTS_DIR` files: SOUL, HEARTBEAT, identity | BLOCKED |
| **MCP config** | MCP server config, tool definitions, endpoint routing | BLOCKED |
| **Gateway** | Hermes gateway routing, API endpoints, auth | BLOCKED |
| **Cron** | Cron schedules, agent triggers, timer config | BLOCKED |
| **Production code** | Pipeline steps, data processing, API integrations | GATED |
| **Model/ranker/selector/sizing/KG** | Scoring models, ranker weights, selector logic, knowledge graph | BLOCKED |

### Risk classification rules

- **SAFE:** Task touches only docs, templates, or proposals. No approval required (review encouraged).
- **GATED:** Task touches wrapper skills, registry, or production code. Requires explicit operator approval before implementation.
- **BLOCKED:** Task touches runtime identity, MCP config, gateway, cron, or model/ranker/selector/sizing/KG. Must not proceed without explicit operator approval. Report the boundary and stop.

---

## Step 4 — Check for Known Failure Patterns

Search `docs/FAILURE_PATTERN_LIBRARY.md` for entries matching the current task:

- Does the task resemble a previously cataloged failure mode?
- Is the target agent/skill listed in any failure pattern's `affected_agents` or `affected_skills`?
- Are there active prevention rules that apply?

If a match is found, include the pattern ID, root cause, and prevention rule in the report.

---

## Step 5 — Produce Preflight Report

Return a structured report with all of the following fields:

```
## Preflight Report

**Request:** [one-sentence summary of what was asked]

**Target agent/skill:** [name, or "none" if docs-only]

**Source-of-truth consulted:**
- [ ] A: Runtime HERMES_AGENTS_DIR identity files
- [ ] B: AGENT_REGISTRY.json
- [ ] C: docs/skills/*
- [ ] D: skills/openclaw/* (routing hint only)
- [ ] E: Generated knowledge ledgers (summary only)

**MCP context collected:**
- fleet_context_snapshot: [available/unavailable — key findings]
- agent_health_summary: [available/unavailable — key findings]
- town_brief: [available/unavailable — key findings]
- Other tools used: [list]

**Relevant known failure patterns:**
- [pattern ID and summary, or "none found"]

**Health warnings:**
- [any degraded agents, stale data, or system issues, or "none"]

**Layers touched:**
- [list each layer from Step 3 that applies]

**Risk class:** SAFE / GATED / BLOCKED

**Proposed next action:**
- [specific description of what would be done]

**Files that would be touched:**
- [exact file paths, or "none — read-only task"]

**Boundaries crossed:**
- [list any Do-Not-Cross Boundaries from flow contract Section 7, or "none"]
```

---

## Step 6 — Stop Before Edits

**Do not make any changes unless the user explicitly approves after reviewing the preflight report.**

- If risk class is SAFE: present the report and proposed action. Wait for approval.
- If risk class is GATED: present the report, highlight the gated boundary, and wait for explicit approval.
- If risk class is BLOCKED: present the report, explain which boundary is blocked, and do not proceed. The user must explicitly approve crossing the boundary.

---

## Reference

- Flow contract: `docs/TOWN_OPENCLAW_AGENT_FLOW_CONTRACT.md`
- Failure patterns: `docs/FAILURE_PATTERN_LIBRARY.md`
- Self-improvement template: `docs/templates/SELF_IMPROVEMENT_PROPOSAL.md`
- Source-of-truth hierarchy: Flow contract Section 3
- Do-Not-Cross Boundaries: Flow contract Section 7
