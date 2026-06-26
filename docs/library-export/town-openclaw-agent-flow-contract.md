# Town/OpenClaw Agent Flow Contract

> **Status:** ACTIVE — read-only governance document
> **Created:** 2026-05-25
> **Author:** Darren Schulz (operator)
> **Scope:** Documentation only. No runtime behavior changes, no gateway changes, no MCP config changes, no AGENT_REGISTRY edits, no skills/openclaw edits, no SOUL/HEARTBEAT/history/identity synthesis, no cron changes, no automation, no commits unless approved.

---

## 1. Current State

### 1.1 Repository

Hermes repo (`hermes-agent`) is clean and current. Architecture freeze lifts post-h20d (~May 26, 2026). No pending PRs that touch agent identity, MCP config, or runtime behavior.

### 1.2 MCP Tool Surface

The Hermes MCP server exposes the following **read-only** context tools to Town/Cursor:

| Tool | Purpose |
|---|---|
| `town_brief` | Structured system summary for Town integration |
| `fleet_context_snapshot` | Point-in-time agent fleet state |
| `agent_health_summary` | Per-agent health and last-run status |
| `knowledge_query` | Query knowledge ledgers |
| `skills_list` / `skills_read` | Enumerate and read skill documents |
| `agents_list` / `agents_get` | Enumerate and read agent metadata |
| `knowledge_read` | Read specific knowledge entries |
| `learnings_read` | Read self-improvement learnings |

All tools are read-only. No MCP tool writes to runtime state, agent config, cron, or identity files.

### 1.3 OpenClaw Wrapper Skills

`skills/openclaw/*` are **shallow wrapper skills** that provide routing hints to the OpenClaw agent orchestrator. They are **not behavioral truth**. They describe what an agent *can be asked to do*, not what the agent *is* or *how it behaves*. Behavioral truth lives in runtime identity files and production code.

### 1.4 Agent Registry

`/workspace/agents` and `AGENT_REGISTRY.json` are **registry-side metadata only**. They record which agents exist, their declared capabilities, and their configuration parameters. They do not define runtime identity or behavioral contracts.

### 1.5 Runtime Identity

Runtime SOUL, HEARTBEAT, and identity validation require the real local `HERMES_AGENTS_DIR` path. This directory contains the authoritative identity files for each agent. Identity synthesis from registry metadata, wrapper skills, or knowledge ledgers is **explicitly prohibited** — see Section 7.

### 1.6 Seven-Layer Identity Stack

The seven-layer identity stack (SOUL -> HEARTBEAT -> capabilities -> tools -> knowledge -> history -> context) is conceptually approved but **implementation-blocked** until the runtime identity source (`HERMES_AGENTS_DIR`) is verified and a provenance-safe write policy exists for each layer.

---

## 2. Flow Model

All Town/OpenClaw/Cursor interactions with Hermes follow this **read-only flow**:

```
User or Cursor request
  → Cursor rule or command
    → Hermes MCP context tools (read-only)
      → town_brief / fleet_context_snapshot / agent_health_summary / knowledge_query
        → OpenClaw wrapper skill as routing hint only
          → proposed action (document, not execute)
            → operator approval (explicit, not inferred)
              → implementation (separate step, separate approval)
```

### Key constraints

- **No step bypasses operator approval.** A proposed action is a document, not an execution.
- **OpenClaw wrappers route, they do not authorize.** A wrapper skill that says "agent X handles task Y" is a routing hint. It does not grant permission to modify agent X.
- **MCP tools observe, they do not mutate.** Every MCP tool in the current surface is read-only. If a write-capable MCP tool is added in the future, it must go through the Do-Not-Cross Boundaries (Section 7) approval process.
- **Implementation is always a separate step.** The flow ends at "proposed action" unless the operator explicitly approves implementation.

---

## 3. Source-of-Truth Hierarchy

When conflicting information exists across layers, precedence follows this order:

| Priority | Source | Authority |
|---|---|---|
| **A** | Runtime `HERMES_AGENTS_DIR` identity files (once verified) | Authoritative for agent identity, SOUL, HEARTBEAT |
| **B** | `AGENT_REGISTRY.json` | Authoritative for registered agent metadata (name, type, schedule) |
| **C** | `docs/skills/*` | Authoritative for documented skill behavior and methodology |
| **D** | `skills/openclaw/*` | Lightweight routing wrappers only — not behavioral truth |
| **E** | Generated knowledge ledgers | Summaries and derived data — not authority |

### Explicit prohibitions

- **Do not synthesize identity from registry metadata.** The registry records what agents exist. It does not define what they are.
- **Do not treat OpenClaw wrappers as behavioral truth.** Wrappers describe routing. Behavior is defined by runtime identity files and production code.
- **Do not persist ACTIVE_CONTEXT as durable memory.** ACTIVE_CONTEXT is ephemeral session state. It must not be written to knowledge ledgers, identity files, or any persistent store without an explicit provenance policy.
- **Do not write HISTORY_MAP or HISTORY_NEW until an append/provenance policy exists.** History entries require a defined schema, provenance chain, and retention policy before any writes are permitted.

---

## 4. Agent Handoff Rules

For any Town/OpenClaw task that touches Hermes agents, skills, or infrastructure, the following preflight sequence is **required**:

### 4.1 Preflight Checklist

1. **Identify target agent or skill.** Name the specific agent, skill, or tool the task concerns.
2. **Read relevant skill/context.** Use MCP tools (`skills_read`, `knowledge_query`, `agents_get`) to load current state.
3. **Check agent health.** Use `agent_health_summary` to verify the target agent is not in a degraded or error state.
4. **Check Failure Pattern Library.** Read `docs/FAILURE_PATTERN_LIBRARY.md` for known failure modes related to the target.
5. **Classify the action.** Every action falls into exactly one category:

| Category | Description | Approval Required |
|---|---|---|
| `docs` | Documentation changes only | No (but review encouraged) |
| `proposal` | Self-improvement proposal, design doc, or spec | No (but must follow template) |
| `test` | Validation, smoke check, read-only diagnostic | No |
| `runtime` | Changes to agent behavior, identity, config, cron | **Yes — explicit operator approval** |
| `production` | Changes to model, ranker, selector, sizing, KG, pipeline | **Yes — explicit operator approval** |

6. **Stop if gated or blocked.** If the action touches any item in the Do-Not-Cross Boundaries (Section 7), stop and report the classification. Do not proceed without explicit approval.

### 4.2 Handoff Report

Every preflight produces a handoff report containing:

- Target agent/skill
- Source-of-truth consulted (which layer from Section 3)
- Relevant known failure patterns
- Health warnings (if any)
- Risk class: `SAFE` / `GATED` / `BLOCKED`
- Proposed next action
- Exact files that would be touched

---

## 5. Self-Improvement Loop

Self-improvement operates in **proposal-only mode**. No automatic application. No runtime mutation. No identity synthesis.

### 5.1 Loop Structure

```
observe
  → classify failure or opportunity
    → search Failure Pattern Library (docs/FAILURE_PATTERN_LIBRARY.md)
      → search knowledge/learnings (MCP: knowledge_query, learnings_read)
        → propose bounded improvement
          → attach risk classification
            → operator approval
              → implementation in separate step
```

### 5.2 Proposal Requirements

Every self-improvement proposal must include all fields defined in `docs/templates/SELF_IMPROVEMENT_PROPOSAL.md`:

| Field | Required | Description |
|---|---|---|
| `proposal_id` | Yes | Unique identifier (format: `SIP-YYYY-MM-DD-NNN`) |
| `created` | Yes | ISO 8601 timestamp |
| `proposer` | Yes | Agent, skill, or operator that originated the proposal |
| `observed_problem` | Yes | What was observed |
| `evidence` | Yes | Specific data, logs, or outputs supporting the observation |
| `related_failure_patterns` | Yes | Cross-reference to FAILURE_PATTERN_LIBRARY entries |
| `affected_agents` | Yes | Which agents are impacted |
| `affected_skills` | Yes | Which skills are impacted |
| `affected_tools` | Yes | Which tools or MCP endpoints are impacted |
| `source_of_truth_checked` | Yes | Which layer(s) from Section 3 were consulted |
| `proposed_change` | Yes | Diff-style description of the proposed change |
| `files_to_touch` | Yes | Exact file paths |
| `behavior_change` | Yes | `yes` or `no` |
| `runtime_state_change` | Yes | `yes` or `no` |
| `risk_class` | Yes | `SAFE` / `GATED` / `BLOCKED` |
| `approval_required` | Yes | `yes` or `no` |
| `validation_plan` | Yes | How to verify the change works |
| `rollback_plan` | Yes | How to revert if the change fails |
| `non_goals` | Yes | What the proposal explicitly does not do |
| `operator_decision` | No | Filled by operator: `APPROVED` / `REJECTED` / `DEFERRED` |

### 5.3 Constraints

- Proposals are documents, not implementations.
- No automatic application of proposals.
- No identity synthesis in proposals.
- No runtime state mutation from proposals.
- No skill promotion without explicit approval (see Section 6).
- A proposal with `behavior_change: yes` or `runtime_state_change: yes` is automatically `GATED` or `BLOCKED`.

---

## 6. Promotion Gates

A prevention rule may be promoted from `docs/FAILURE_PATTERN_LIBRARY.md` into an active skill or governance document **only** when all of the following conditions are met:

| Gate | Requirement |
|---|---|
| **Recurrence** | `recurrence_count >= 3` in the Failure Pattern Library |
| **Root cause** | Root cause is confirmed (not speculative) |
| **Target identified** | Affected skill or agent is specifically identified |
| **Diff-only** | Proposed change is expressed as a precise diff, not a narrative |
| **Operator approval** | Operator has explicitly approved the promotion |

### Explicit prohibitions

- **No automatic promotion.** Meeting the recurrence threshold justifies *proposing* promotion, not *applying* it.
- **No narrative-based promotion.** "We should probably update X" is not a promotion. A promotion is a diff.
- **No promotion without rollback.** Every promotion must include a rollback path.

---

## 7. Do-Not-Cross Boundaries

The following actions are **blocked without explicit operator approval**. No agent, skill, command, or automation may perform these actions autonomously:

| Boundary | Scope |
|---|---|
| `AGENT_REGISTRY.json` edits | Adding, removing, or modifying agent entries |
| `skills/openclaw/*` edits | Modifying wrapper skill content or adding new wrappers |
| MCP config changes | Adding, removing, or modifying MCP tools or server config |
| Gateway/platform changes | Hermes gateway routing, API endpoints, auth config |
| Cron changes | Adding, removing, or modifying cron schedules |
| Runtime identity files | Any write to `HERMES_AGENTS_DIR` identity files (SOUL, HEARTBEAT, etc.) |
| SOUL/HEARTBEAT/HISTORY writes | Any write to identity, heartbeat, or history layers |
| Production model changes | model, ranker, selector, sizing, KG, alpha-affecting parameters |
| Codegraph Hermes registration | Registering or modifying Hermes in external dependency graphs |

### Escalation

If a task requires crossing any boundary:

1. Stop execution.
2. Report the boundary that would be crossed.
3. Describe the proposed action as a diff.
4. Wait for explicit operator approval.
5. Implement in a separate step after approval.

---

## 8. Recommended Cursor Commands

Copy-paste command templates for common governed workflows.

### 8.1 Run Town Agent Context Preflight

```
Before doing anything with Hermes agents:
1. Read docs/TOWN_OPENCLAW_AGENT_FLOW_CONTRACT.md
2. Read docs/FAILURE_PATTERN_LIBRARY.md
3. Use MCP tools: fleet_context_snapshot, agent_health_summary, town_brief
4. Identify the target agent/skill
5. Classify the action: docs / proposal / test / runtime / production
6. Report: target, sources consulted, failure patterns, health, risk class, proposed action, files to touch
7. Stop before edits unless I explicitly approve.
```

### 8.2 Draft Self-Improvement Proposal

```
I want to draft a self-improvement proposal.
1. Read docs/TOWN_OPENCLAW_AGENT_FLOW_CONTRACT.md Section 5
2. Read docs/templates/SELF_IMPROVEMENT_PROPOSAL.md
3. Read docs/FAILURE_PATTERN_LIBRARY.md for related patterns
4. Use MCP: knowledge_query, learnings_read for relevant context
5. Fill out the template with all required fields
6. Classify risk: SAFE / GATED / BLOCKED
7. Return the completed proposal for my review. Do not apply it.
```

### 8.3 Check Failure Pattern Before Investigation

```
Before investigating this issue:
1. Read docs/FAILURE_PATTERN_LIBRARY.md
2. Search for entries matching [DESCRIBE ISSUE]
3. If a matching pattern exists, report: pattern ID, root cause, prevention rule, recurrence count
4. If no match, note this as a potential new pattern to catalog after investigation
5. Proceed with investigation using the flow contract (Section 2).
```

### 8.4 Classify OpenClaw Wrapper vs Runtime Truth

```
For [AGENT/SKILL NAME]:
1. Read skills/openclaw/[relevant wrapper] — note this is routing hint only
2. Use MCP: agents_get for registry metadata
3. Check if HERMES_AGENTS_DIR identity files are accessible for this agent
4. Report:
   - Wrapper says: [summary]
   - Registry says: [summary]
   - Runtime identity: [verified / not accessible / not yet verified]
   - Source-of-truth hierarchy position: [A/B/C/D/E per Section 3]
5. Do not synthesize identity from metadata. Report what each layer says independently.
```

### 8.5 Prepare Guarded Skill Promotion Proposal

```
I want to evaluate promoting a prevention rule to a skill.
1. Read docs/TOWN_OPENCLAW_AGENT_FLOW_CONTRACT.md Section 6 (Promotion Gates)
2. Read docs/FAILURE_PATTERN_LIBRARY.md entry for [PATTERN ID]
3. Check all promotion gates:
   - recurrence_count >= 3?
   - root cause confirmed?
   - affected skill/agent identified?
   - proposed change is diff-only?
4. If all gates pass, draft the promotion as a diff
5. If any gate fails, report which gate(s) failed and what's needed
6. Do not apply the promotion. Return the proposal for my approval.
```

---

## Revision History

| Date | Author | Change |
|---|---|---|
| 2026-05-25 | Darren Schulz | Initial version — contract created |
