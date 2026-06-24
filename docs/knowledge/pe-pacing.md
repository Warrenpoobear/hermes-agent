# PE Pacing (Knowledge Reference)

<!--
SYNC PROVENANCE
  Source: Town skill `pe-pacing`
  Source maturity (per skill-maturity-metadata): STABLE
  Synced to Hermes: 2026-06-24 (manual, operator-approved, PR-gated)
  Sync owner: Darren Schulz (dschulz@wakerobin.co)
  Type: knowledge-layer reference (NOT an agent; no AGENT_REGISTRY.json entry, no cron, no authority)
  Batch: Town -> Hermes mapping pipeline.
  NOTE: Reference knowledge a SOUL.md may cite. Source repo for this domain is
  Warrenpoobear/asset-allocation (separate from the agent runtime repo).
-->

## Purpose

Reference for the private equity pacing model within the Wake Robin Liquidity Architecture. Covers the Takahashi-Alexander deterministic model, STAIRS market-coupled adapter, capital call obligations, and workbook reconciliation with configurable gates.

---

## Takahashi-Alexander Model

File: `src/aa_model/pe/ta_model.py`. Deterministic PE cash-flow projection used as the canonical PE engine.

### Default Parameters (pinned in `configs/pe_pacing.yaml`)

| Parameter | Default | Description |
| --- | --- | --- |
| lifetime_years | 12 | Total fund life |
| commitment_period_years | 4 | Capital call window |
| rate_of_contribution | [0.25, 0.30, 0.25, 0.20] | Year-by-year call schedule (sums to 1.0) |
| bow | 2.5 | Distribution curve shape |
| yield_pct | 0.0 | Current yield |
| growth_pct | 0.13 | NAV growth rate |

### Golden CSV Regression Test

`tests/golden/ta_single_fund.csv` generated from a single fund: $100M commitment, 2024Q1 vintage, default params, 48 quarters. Regression test asserts byte-equality.

### Ledger Integration

PE flows on the quarterly ledger follow canonical ordering:

1. `pe_call` - capital deployed (negative amount)
2. `pe_distribution` - capital returned (positive amount)
3. `pe_nav_mark` - NAV growth + yield (positive amount)

PE buckets are illiquid and DO NOT participate in rebalancing (Phase 8 liquidity overlay).

---

## STAIRS Adapter

File: `src/aa_model/pe/stairs_adapter.py`. Market-state-coupled PE pacing — adjusts commitment timing and distribution pace based on public market conditions. Design locked at `993a751`. Implementation blocked until tests + invariants drafted.

---

## Capital Call Obligation Bridge (Phase 19)

File: `src/aa_model/pe/call_obligation.py`. Bridges PE pacing model projections to actual capital call obligations from the cash-flow workbook.

### Source Precedence

When workbook and model disagree: default = workbook-classified line wins (model-derived projection is cross-check); override = configurable per obligation source via reconciliation gates.

### Obligation Sources (Canonical Taxonomy)

| Source | Description |
| --- | --- |
| explicit_config | Manually configured obligations |
| cashflow_workbook | From Cashflow Modeling v7.xlsx |
| pe_pacing_model | TA or STAIRS model output |
| investment_summary | From Investment Summary workbook |
| synthetic_fixture | Test fixtures |

---

## Workbook Reconciliation (Phase 20)

File: `src/aa_model/pe/call_reconciliation.py`. Compares model-projected PE calls against workbook capital-call lines per quarter per fund. Per-quarter, per-source output: model-projected call amount, workbook-classified call amount, delta (absolute and percentage), reconciliation verdict.

---

## Configurable Reconciliation Gates (Phase 21)

File: `src/aa_model/pe/reconciliation_gates.py`. Four-tier gate classification:

| Gate Level | Behavior |
| --- | --- |
| advisory | Log only, no blocking |
| warning | Log + surface in report |
| requires_override | Block unless operator explicitly overrides |
| hard_fail | Block unconditionally, fail the run |

Gate thresholds are configurable per obligation type and per fund.

---

## PE Sleeve Policy

From `configs/base.yaml`: `pe.sleeve_target_pct` = 0.25 (25% of total portfolio); `pe.scope` = [buyout]. Supported sub-strategies: buyout, venture, growth, infra, re, pc.

### Illiquidity Overlay (Phase 8)

The liquidity overlay (`allocation/liquidity_overlay.py`) enforces that PE buckets are structurally illiquid: PE NAV is marked but NOT available for rebalancing; liquid NAV residual (public_equity, public_bond, cash) absorbs all rebalancing. This prevents the model from treating PE NAV as spendable liquidity.

---

## Phase 23: PE Real-Data Commitment Input Layer

Design locked at `f81ff43`. Implementation pending. Purpose: replace synthetic PE commitment fixtures with real fund commitment data ingested from the Investment Summary workbook.

---

## Key Constraints

1. TA model is NOT behind an adapter in Phase 1 — it is the canonical implementation
2. STAIRS is optional, wrapped behind adapter interface
3. PE flows must follow canonical intra-quarter ordering on the ledger
4. PE call obligations carry provenance from the canonical source taxonomy
5. Reconciliation gates are configurable but default to workbook-wins precedence
6. All PE projections are deterministic (seeded RNG from base.yaml)

---

## Source Files

| Component | File |
| --- | --- |
| TA Model | `src/aa_model/pe/ta_model.py` |
| TA Adapter | `src/aa_model/pe/ta_adapter.py` |
| STAIRS Adapter | `src/aa_model/pe/stairs_adapter.py` |
| PE Pacing | `src/aa_model/pe/pacing.py` |
| Call Obligation | `src/aa_model/pe/call_obligation.py` |
| Call Reconciliation | `src/aa_model/pe/call_reconciliation.py` |
| Reconciliation Gates | `src/aa_model/pe/reconciliation_gates.py` |
| PE Factory | `src/aa_model/pe/factory.py` |
| PE Config | `configs/pe_pacing.yaml` |
| Golden CSV | `tests/golden/ta_single_fund.csv` |
