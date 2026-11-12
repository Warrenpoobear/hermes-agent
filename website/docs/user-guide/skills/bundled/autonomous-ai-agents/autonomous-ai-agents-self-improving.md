---
title: "Self Improving — Captures corrections and tiers memory for Hermes"
sidebar_label: "Self Improving"
description: "Captures corrections and tiers memory for Hermes"
---

{/* This page is auto-generated from the skill's SKILL.md by website/scripts/generate-skill-docs.py. Edit the source SKILL.md, not this page. */}

# Self Improving

Captures corrections and tiers memory for Hermes.

## Skill metadata

| | |
|---|---|
| Source | Bundled (installed by default) |
| Path | `skills/autonomous-ai-agents/self-improving` |
| Version | `1.0.0` |
| Author | Hermes Agent |
| License | MIT |
| Platforms | linux, macos, windows |
| Tags | `learning`, `memory`, `self-improvement`, `corrections` |

## Reference: full SKILL.md

:::info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
:::

# Self-Improving Skill

Structured learning capture with HOT/WARM/COLD tiers for Hermes file-based memory. Does not auto-sync with Town or the knowledge layer while the feedback protocol is frozen.

## When to Use

- The user corrects you or states a durable preference
- You finish significant work and want a self-reflection entry
- You are about to edit `.learnings/memory.md` or promote a pattern to HOT

## Prerequisites

- `.learnings/` directory (repo or `HERMES_HOME`)
- Hermes MCP or CLI audit: `self_improvement_snapshot(summary=True)` / `python -m tools.self_improvement_audit`
- Knowledge artifacts for reconciliation: `latest_state`, `held_spec_ledger`, `contradiction_ledger`

## How to Run

1. Session start: run the recursive loop in `references/recursive-improvement-loop.md`.
2. Log corrections to `.learnings/corrections.md` (append-only).
3. Before HOT edits: run `self_improvement_snapshot()` and apply only operator-approved changes.

## Quick Reference

| Tier | Path | Cap |
|------|------|-----|
| HOT | `memory.md` | 100 lines |
| WARM | `projects/*.md`, `domains/*.md` | 200 lines each |
| LOG | `corrections.md` | rolling log |

## Procedure

### Corrections (log immediately)

User says "no, use X not Y", "always do X", or similar → append to `corrections.md`:

```
CONTEXT: [task]
REFLECTION: [what went wrong]
LESSON: [what to do next time]
```

### Promotion (after 3× in 7 days)

Move durable lessons from corrections/WARM into HOT only after operator review and a clean audit snapshot.

### Self-reflection (after significant work)

```
CONTEXT: [task type]
REFLECTION: [outcome vs expectation]
LESSON: [change for next time]
```

## Pitfalls

- Never infer preferences from silence; confirm patterns after three occurrences.
- Do not exceed HOT cap — demote stale sections to WARM instead.
- Knowledge layer is operational truth; HOT is a bounded bootstrap summary.
- Do not store credentials or third-party confidential data in memory files.

## Verification

```bash
python -m tools.self_improvement_audit
python -m tools.self_improvement_audit --json
```

Expect `writes_allowed: false` and actionable `proposals` only (no automatic writes).
