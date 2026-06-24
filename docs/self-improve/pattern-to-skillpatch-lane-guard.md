# pattern_to_skillpatch.py — Lane-Refusal Guard (spec stub)

**Status:** PROPOSAL / NOT IMPLEMENTED
**Author:** Town assistant (staged for Cursor-side implementation)
**Date:** 2026-06-24
**Scope:** Tier 0 — governance guard on the patch-draft generator. Does NOT change scoring, ranker, selector, sizing, or cron. Prevents research/scoring findings from being silently promoted into production skills.

---

## Why

`self-improving` Rule 12 and Rule 10 require that signal/scoring/research findings (size confound, portfolio drag, ranker weights) go through a governance **Spec + ablation**, never into a production skill via the self-improvement loop. `pattern_to_skillpatch.py` is the tool that drafts skill patches from recurring patterns — it is the exact chokepoint where a mis-laned research lesson could leak into `screener_ops` or a scoring skill. This guard makes the refusal mechanical, not a matter of reviewer vigilance.

## Required metadata on every promotable entry

Each `.learnings/LEARNINGS.md` entry and each `failure-patterns` entry carries:

- `Area:` one of `hermes_ops` | `data_pipeline` | `research` | `portfolio`
- `Promotion-lane:` one of `skill` | `spec` | `none`

## Guard behavior (the stub)

When `pattern_to_skillpatch.py` iterates candidate entries, it MUST:

1. **Refuse `Promotion-lane: spec`.** Skip the entry, do not emit a skill-patch draft, and write a one-line reason to the run report:
   `REFUSED <pattern_key>: Promotion-lane=spec — route to projects/biotech_screener.md + governance Spec, not a skill patch.`
2. **Refuse `Promotion-lane: none`.** Skip silently-promotable noise; log `SKIPPED <pattern_key>: Promotion-lane=none`.
3. **Refuse missing/invalid lane.** Fail-closed: if `Promotion-lane` is absent or not in the enum, treat as `spec` (most conservative) and refuse with `REFUSED <pattern_key>: lane missing — fail-closed to spec`.
4. **Refuse `Area: research|portfolio` regardless of lane.** These areas never patch a production skill directly; belt-and-suspenders against a mis-tagged `Promotion-lane: skill` on a research finding.
5. **Allow** only `Promotion-lane: skill` AND `Area in {hermes_ops, data_pipeline}` AND recurrence gate met (per Rule 12) to produce a draft in `artifacts/skill_patch_drafts/`.

Drafts are still operator-reviewed before any `SKILL.md` edit (Rule 11 FENCE). The guard narrows *what can even be drafted*; it does not auto-apply anything.

## Pseudocode

```python
ALLOWED_AREAS = {"hermes_ops", "data_pipeline"}
VALID_LANES = {"skill", "spec", "none"}

def lane_allows_skill_patch(entry) -> tuple[bool, str]:
    lane = entry.get("Promotion-lane")
    area = entry.get("Area")
    if lane not in VALID_LANES:
        return False, f"REFUSED {entry.pattern_key}: lane missing — fail-closed to spec"
    if lane == "spec":
        return False, f"REFUSED {entry.pattern_key}: Promotion-lane=spec — route to Spec, not skill"
    if lane == "none":
        return False, f"SKIPPED {entry.pattern_key}: Promotion-lane=none"
    if area not in ALLOWED_AREAS:
        return False, f"REFUSED {entry.pattern_key}: Area={area} never patches a production skill"
    return True, f"OK {entry.pattern_key}: eligible for draft"
```

## Test expectations (for `tests/test_pattern_to_skillpatch_lane.py`)

- `Promotion-lane: spec` → refused, no draft emitted, reason logged.
- `Promotion-lane: none` → skipped.
- Missing lane → refused (fail-closed).
- `Area: research` + `Promotion-lane: skill` (mis-tagged) → refused.
- `Area: hermes_ops` + `Promotion-lane: skill` + recurrence met → draft emitted.
