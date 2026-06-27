# Self-Improvement Proposal

> **Status:** TEMPLATE — fill in all required fields below
> **Governance:** docs/TOWN_OPENCLAW_AGENT_FLOW_CONTRACT.md Section 5
> **Rules:** Proposals are documents, not implementations. No automatic application. No identity synthesis. No runtime state mutation. No skill promotion without explicit approval.

---

## Metadata

| Field | Value |
|---|---|
| **proposal_id** | `SIP-YYYY-MM-DD-NNN` |
| **created** | YYYY-MM-DDTHH:MM:SSZ |
| **proposer** | [agent name, skill name, or "operator"] |

---

## Problem

### Observed Problem

[What was observed. Be specific. One paragraph maximum.]

### Evidence

[Specific data, logs, outputs, or observations supporting the problem statement. Include timestamps, file paths, error messages, or metric values where available.]

### Related Failure Patterns

[Cross-reference entries from `docs/FAILURE_PATTERN_LIBRARY.md`. Use pattern IDs. If no related pattern exists, state "None — candidate for new pattern entry if recurrence >= 3."]

---

## Impact

### Affected Agents

[List specific agent names from AGENT_REGISTRY, or "none".]

### Affected Skills

[List specific skill names from `docs/skills/*` or `skills/openclaw/*`, or "none".]

### Affected Tools

[List specific MCP tools, CLI tools, or pipeline components, or "none".]

### Source of Truth Checked

[Which layer(s) from the flow contract Section 3 were consulted. Mark all that apply.]

- [ ] A: Runtime HERMES_AGENTS_DIR identity files
- [ ] B: AGENT_REGISTRY.json
- [ ] C: docs/skills/*
- [ ] D: skills/openclaw/* (routing hint only)
- [ ] E: Generated knowledge ledgers (summary only)

---

## Proposed Change

### Description

[Diff-style description of the proposed change. What exactly would be modified, added, or removed. Be precise enough that someone could implement this from the description alone.]

### Files to Touch

[Exact file paths that would be modified, created, or deleted.]

```
path/to/file1.md   — [create / modify / delete]
path/to/file2.json — [create / modify / delete]
```

---

## Risk Classification

| Dimension | Value | Notes |
|---|---|---|
| **behavior_change** | `yes` / `no` | Does this change how any agent, skill, or tool behaves? |
| **runtime_state_change** | `yes` / `no` | Does this write to runtime identity, config, cron, or MCP state? |
| **risk_class** | `SAFE` / `GATED` / `BLOCKED` | Per flow contract Section 4 and Section 7 |
| **approval_required** | `yes` / `no` | `yes` if risk_class is GATED or BLOCKED, or if behavior_change is `yes` |

### Risk class determination

[Explain why this risk class was assigned. Reference specific flow contract sections or Do-Not-Cross Boundaries.]

---

## Validation Plan

[How to verify the change works as intended. Include specific checks, tests, or observations. For docs-only changes, a review pass may suffice. For anything touching behavior, describe the validation steps concretely.]

---

## Rollback Plan

[How to revert if the change fails or produces unintended effects. Be specific: exact commands, file restores, or git reverts.]

---

## Non-Goals

[What this proposal explicitly does not do. Use this to draw clear boundaries and prevent scope creep. Include at minimum:]

- This proposal does not implement itself.
- This proposal does not synthesize identity from metadata.
- This proposal does not mutate runtime state.
- This proposal does not promote any skill without explicit approval.
- [Add task-specific non-goals here.]

---

## Operator Decision

> **This section is filled by the operator, not the proposer.**

| Field | Value |
|---|---|
| **decision** | `APPROVED` / `REJECTED` / `DEFERRED` |
| **decided_by** | [operator name] |
| **decided_at** | YYYY-MM-DDTHH:MM:SSZ |
| **conditions** | [any conditions on approval, or "none"] |
| **notes** | [operator notes, or "none"] |

---

## Promotion Eligibility

> **Only relevant if this proposal recommends promoting a prevention rule from the Failure Pattern Library into a skill or governance document.**

Per flow contract Section 6, promotion requires all gates to pass:

- [ ] `recurrence_count >= 3` in Failure Pattern Library
- [ ] Root cause is confirmed (not speculative)
- [ ] Affected skill/agent is specifically identified
- [ ] Proposed change is expressed as a precise diff
- [ ] Operator has explicitly approved the promotion

**Meeting the recurrence threshold justifies proposing promotion, not applying it.**

---

## Revision History

| Date | Author | Change |
|---|---|---|
| YYYY-MM-DD | [proposer] | Initial proposal |
