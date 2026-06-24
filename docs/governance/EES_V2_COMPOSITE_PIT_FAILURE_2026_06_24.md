# EES v2 Composite PIT Failure Governance Memo

**Date:** 2026-06-24
**Status:** Diagnostic governance artifact only
**Production boundary:** No production scoring, selector, sizing, eligibility, portfolio construction, or `run_screen.py` wiring changes.
**Freeze state:** Active; not lifted by this memo or by any diagnostic script in this branch.

## Executive verdict

The current `ees_v2_score` composite must remain frozen. The short-horizon Phase 3 shadow monitor can continue to collect evidence, but it is not sufficient to lift the freeze because the strict long-history PIT backtest indicates that the current composite is negative over the 2020-2026 PIT panel.

The 5d monitor is encouraging but not decisive. It has met its observation gate, but the 20d monitor remains unobservable until sufficient forward-return rows complete. Even if the 20d monitor later passes, it cannot override the long-history PIT failure without a redesigned composite that clears a pre-declared PIT promotion bar.

## Evidence basis to preserve/reference

The remediation workstream should preserve or reference the following evidence classes when present in the operator environment:

- Strict PIT EES v2 backtest: `artifacts/research/ees_v2_pit_backtest_<date>.json`.
- Daily/Phase 3 EES shadow-monitor outputs.
- Attribution outputs, including `artifacts/audit/ees_v2_phase3_attribution_report_2026-06-23.md`.

This repository snapshot currently contains the Phase 3 attribution report but does not include the full PIT JSON outputs in `artifacts/research`; the diagnostic script added in this branch can regenerate research-only outputs when the PIT snapshots, prices, and trial records are available.

## Required governance statements

- The current `ees_v2_score` has negative PIT IC over 2020-2026 according to the operator-provided strict PIT synthesis.
- Freeze remains active.
- The 20d shadow monitor is still useful for forward evidence, but it is insufficient by itself for freeze lift.
- `trap_overlay_score` and `base_rate_gap_score` are candidates for removal or sign flip.
- `conditional_gap_score`, `conditional_misprice_score`, `conditional_base_rate`, and `conditional_expected_move` are candidate positive components.

## Candidate remediation direction

The diagnostic branch tests reconstructed composites only. It does not promote or wire any variant into production. The diagnostic variants are:

1. `positive_components_equal_weight`
2. `positive_components_ic_weighted`
3. `original_minus_trap_overlay`
4. `original_minus_base_rate_gap`
5. `original_minus_both`
6. `sign_flip_trap_and_base_rate_gap`

## Pre-declared pass bar

A reconstructed composite is only a promotion candidate if all of the following hold:

- 21d, 42d, and 63d IC are all positive.
- At least two horizons have Newey-West `t >= 2.0`.
- No single ticker contributes more than 25% of total IC contribution.
- The result survives priced-move-only and full-panel subsamples.
- No look-ahead or live-universe dependency is detected.

Passing this bar does **not** lift the freeze. It only makes a variant eligible for human review and a separate production-change proposal.

## Operational controls

- No live data fetches.
- Use existing PIT snapshots/prices/trial records only.
- Write research artifacts only under `artifacts/research`.
- Do not mutate `production_data`, `data/snapshots`, `run_screen.py`, ranker/scoring code, selector code, sizing code, or portfolio construction.
- Keep daily production outputs unchanged.

## Governance verdict

`FREEZE_REMAINS_ACTIVE` until a reconstructed composite clears the pre-declared PIT bar, is independently reviewed, and is promoted through a separate production-governance PR.
