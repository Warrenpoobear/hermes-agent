# Validation & Governance (Knowledge Reference)

<!--
SYNC PROVENANCE
  Source: Town skill `biotech-validation`
  Source maturity (per skill-maturity-metadata): STABLE (last reviewed 2026-06-16)
  Synced to Hermes: 2026-06-24 (manual, operator-approved, PR-gated)
  Sync owner: Darren Schulz (dschulz@wakerobin.co)
  Type: knowledge-layer reference (NOT an agent; no AGENT_REGISTRY.json entry, no cron, no authority)
  Batch: Town -> Hermes mapping pipeline (after financial-health PR #35, clinical-scoring PR #36).
  NOTE: Reference knowledge a SOUL.md may cite. It does not execute, mutate data, or write to .learnings/.
-->

## Purpose

Define the go/no-go gates, data quality checks, staleness windows, IC thresholds, and governance requirements every pipeline run must satisfy before producing output. Encodes Wake Robin's fail-closed philosophy: uncertain or stale data triggers exclusion, not graceful degradation.

## Preconditions

- Pipeline runs MUST have an explicit `as_of_date` parameter (never `datetime.now()`).
- All validation uses `Decimal` arithmetic where scores are involved.
- PIT cutoff: `source_date <= as_of_date - 1` (standard) or `source_date < as_of_date - 2` (strict mode).

---

## Gate 1: Point-in-Time (PIT) Enforcement

| Rule | Formula | Consequence |
| --- | --- | --- |
| Standard PIT | `source_date <= as_of_date - 1 day` | Data admitted |
| Strict PIT | `source_date < as_of_date - 2 days` | Extra buffer for intraday data |
| Lookahead | `age_days < 0` (future data) | Reject unconditionally |

Every record must pass PIT admissibility before entering any scoring module. No exceptions.

---

## Gate 2: Data Staleness (Phase-Dependent) — AUTHORITATIVE for all data-age decisions

### Financial Data

| Level | Age (days) | Penalty |
| --- | --- | --- |
| PASS | <= 60 | 1.0x |
| WARN | 60-90 | 1.0x |
| SOFT_GATE | 90-120 | 0.5x |
| HARD_GATE | > 120 | Exclude (0.0x) |

### Trial Data - Phase 3

| Level | Age (days) | Penalty |
| --- | --- | --- |
| PASS | <= 90 | 1.0x |
| WARN | 90-120 | 1.0x |
| SOFT_GATE | 120-180 | 0.6x |
| HARD_GATE | > 180 | Exclude |

### Trial Data - Phase 2

| Level | Age (days) | Penalty |
| --- | --- | --- |
| PASS | <= 180 | 1.0x |
| WARN | 180-270 | 1.0x |
| SOFT_GATE | 270-365 | 0.7x |
| HARD_GATE | > 365 | Exclude |

### Trial Data - Phase 1

| Level | Age (days) | Penalty |
| --- | --- | --- |
| PASS | <= 270 | 1.0x |
| WARN | 270-365 | 1.0x |
| SOFT_GATE | 365-545 | 0.8x |
| HARD_GATE | > 545 | Exclude |

### Market Data

| Level | Age (days) | Penalty |
| --- | --- | --- |
| PASS | <= 3 | 1.0x |
| WARN | 3-5 | 1.0x |
| SOFT_GATE | 5-10 | 0.3x |
| HARD_GATE | > 10 | Exclude |

### Short Interest Data (FINRA 2-week lag built in)

| Level | Age (days) | Penalty |
| --- | --- | --- |
| PASS | <= 20 | 1.0x |
| WARN | 20-30 | 1.0x |
| SOFT_GATE | 30-45 | 0.5x |
| HARD_GATE | > 45 | Exclude |

### 13F Holdings Data (45-day SEC filing lag)

| Level | Age (days) | Penalty |
| --- | --- | --- |
| PASS | <= 60 | 1.0x |
| WARN | 60-90 | 1.0x |
| SOFT_GATE | 90-135 | 0.4x |
| HARD_GATE | > 135 | Exclude |

SEC_13F_FILING_LAG_DAYS: 45 (built-in constant).

---

## Gate 3: Data Quality Hard Gates (non-temporal only)

> Fix applied 2026-05-16 (Code Review H2): Data-age thresholds removed from this gate (they conflicted with Gate 2). Gate 2 is authoritative for all data-age staleness decisions. Gate 3 holds only non-temporal quality gates.

| Gate | Threshold | Action |
| --- | --- | --- |
| Liquidity (ADV) | < $500,000/day | Exclude ticker |
| Price (penny stock) | < $5.00 | Exclude ticker |
| Market field coverage | < 80% fields present | Exclude ticker |
| Financial field coverage | < 50% fields present | Issue warning |

> Penny stock threshold note (W7): The $5.00 hard gate here is the production exclusion threshold. The financial-health skill's $2.00 penny stock penalty is a SECONDARY safeguard, unreachable at the current $5.00 gate. Both thresholds are intentional.

---

## Gate 4: Circuit Breakers

| Condition | Threshold | Action |
| --- | --- | --- |
| Records failing validation | > 20% | Log warning |
| Records failing validation | > 50% | Fail entire pipeline |
| Minimum records for check | < 10 | Skip circuit breaker check |

---

## Gate 5: Input Validation

| Validation | Rule |
| --- | --- |
| Ticker format | `^[A-Z]{1,5}$` |
| Minimum date | >= 1990-01-01 |
| Cash | Non-negative |
| Market cap | Positive |
| Maximum runway | <= 1200 months |
| Valid records % | >= 10% must pass |

---

## Gate 6: Score Bounds Validation

All scores must fall within [0, 100]: financial_score, clinical_score, catalyst_score, score_blended, composite_score. Any score outside [0, 100] is a pipeline error. Fail-closed.

---

## Gate 7: Weight Sum Validation

Module 5 component weights must sum to 1.0 within tolerance +/- 0.01. Weights outside tolerance are a configuration error. Fail-closed.

---

## Gate 8: Module Coverage Minimums

| Module | Minimum Coverage | Action if Below |
| --- | --- | --- |
| Module 2 (Financial) | 80% of universe | Warning |
| Module 3 (Catalyst) | 80% of universe | Warning |
| Module 4 (Clinical) | 80% of universe | Warning |

---

## Gate 9: Severity System

| Level | Meaning | Score Multiplier | Action |
| --- | --- | --- | --- |
| NONE | Healthy | 1.0 | Include |
| SEV1 | Caution | 0.90 | Include with flag |
| SEV2 | Warning | 0.50 | Include, soft gate |
| SEV3 | Critical | 0.00 | Exclude (hard gate) |

---

## Gate 10: Pipeline Health Status

| Component | Coverage Threshold | Status if Below |
| --- | --- | --- |
| catalyst_raw | 10% | DEGRADED |
| momentum | 0% | OPTIONAL |
| smart_money | 0% | OPTIONAL |
| market_data | 0% | OPTIONAL |

Run Status: OK (all met) / DEGRADED (optional components below threshold) / FAIL (catalyst pipeline < 5% with events).

---

## IC Quality Benchmarks

### Information Coefficient Thresholds

| Quality | IC Range | Action |
| --- | --- | --- |
| Excellent | IC > 0.05 | Deploy |
| Good | IC 0.03-0.05 | Use with confidence |
| Weak | IC 0.01-0.03 | Monitor |
| Noise | IC < 0.01 | Abandon signal |
| Negative | IC < 0 | Investigate inversion |

### IC Measurement Constants

| Constant | Value |
| --- | --- |
| MIN_OBS_IC | 10 |
| MIN_OBS_TSTAT | 20 |
| MIN_OBS_BOOTSTRAP | 30 |
| MIN_ROLLING_WINDOW | 12 weeks |
| BOOTSTRAP_ITERATIONS | 1000 |
| TSTAT_THRESHOLD_95 | 2.0 |
| TSTAT_THRESHOLD_99 | 2.58 |

### Forward Return Horizons

| Horizon | Trading Days |
| --- | --- |
| 1w | 5 |
| 2w | 10 |
| 1m | 20 |
| 1.5m | 30 |
| 3m | 60 |
| 4.5m | 90 |

### Market Cap Buckets (IC Analysis)

> Cross-reference note (W2): These IC-segmentation tiers differ from the financial-health liquidity scoring tiers. Both are intentional; always specify which system when citing.

| Bucket | Range |
| --- | --- |
| MICRO | < $300M |
| SMALL | $300M - $1B |
| MID | $1B - $5B |
| LARGE | > $5B |

---

## Regime Data Staleness Haircuts

| Data Age | Confidence Multiplier |
| --- | --- |
| <= 2 days | 1.00 |
| 3-5 days | 0.85 |
| 6-10 days | 0.65 |
| > 10 days | 0.00 (force UNKNOWN regime) |

---

## Production Hardening Limits

File size: JSON 100 MB, config 10 MB, checkpoint 50 MB. Timeouts: file read 60s, module execution 600s, full pipeline 3600s. Logging sanitization: 10 list items max, 200 chars max; blocked patterns include `api_key`, `password`, `secret`, `token`, `credential`, `ssn`, `account_number`, `cusip`.

---

## Determinism Enforcement

| Setting | Required Value |
| --- | --- |
| force_deterministic_timestamps | true |
| sort_output_keys | true |
| include_content_hashes | true |
| random_seed | 42 |

Rules: same inputs produce byte-identical outputs; sorted-key JSON; deterministic sort keys; SHA256 content hashes in every output; no external API calls during scoring; all timestamps from `as_of_date`.

---

## Governance Metadata Requirements

Every pipeline output MUST include a `_governance` block: `run_id`, `score_version`, `schema_version`, `parameters_hash`, `pit_cutoff`, `as_of_date`.

Audit stages: INIT, LOAD, ADAPT, FEATURES, RISK, SCORE, REPORT, FINAL. Status values: OK / FAIL / SKIP. Error codes: MISSING_INPUT, SCHEMA_MISMATCH, HASH_ERROR, PARAMS_MISSING, MAPPING_MISSING, VALIDATION_ERROR, UNKNOWN_ERROR.

---

## Enhancement Engine Confidence Thresholds

| Engine | Confidence Gate | Effect Below Gate |
| --- | --- | --- |
| PoS | 0.40 | PoS weight -> 0 |
| Momentum | 0.50 | Momentum not meaningful |
| Smart Money | 0.50 | Smart money signal excluded |
| Valuation | 0.40 | Valuation fallback to sector |

---

## Gate 11: Snapshot Content Collapse Guards (2026-05-08)

| Check | Threshold | Verdict |
| --- | --- | --- |
| coinvest_score_z SD | <= 0.10 | FAIL (selector signal flat) |
| catalyst_quality classification | < 90% classified among has_catalyst_signal=1 rows | FAIL |
| No has_catalyst_signal=1 rows | n/a | WARN |

Tool: `tools/verify_snapshot_integrity.py`. Runs after hash/manifest checks to catch silent degradation.

---

## Gate 12: Expectation Layer Coverage Gate (Spec 105)

QA file: `production_qa_check.py`. Hard-fails if market-expectation fields are missing or under-covered. Thresholds sourced from `FEATURE_COVERAGE_REQUIREMENTS`.

| Field | Required Coverage |
| --- | --- |
| `short_interest_pct` | 0.90 |
| `close_price` | 0.99 |
| `market_cap_mm` | 0.95 |
| `priced_move_pct` | 0.80 |
| `insider_net_buy_value_90d` | 0.30 (diagnostic only) |

---

## Diagnostic Fields Registry (Spec 104)

Fields tracked for observability but excluded from scoring/ranking/selection. Current: `insider_net_buy_value_90d` (DIAGNOSTIC ONLY).

Insider Model Isolation Guard (CRITICAL): `insider_net_buy_value_90d` must NOT enter the expectation model's `market_features` input. Guard via input exclusion (preferred), weight zeroing, or a drop guard. Never collapse blank (NaN) and zero (0.0) — different semantics. Promotion requires 20+ stable snapshots, >= 60% coverage, IC > 0 at p < 0.05, Checklist v2 pass, explicit written approval.

---

## Pre-Run Checklist

1. `as_of_date` explicitly provided
2. All input files exist and within size limits
3. PIT cutoff computed and logged
4. Schema versions match
5. Weight sums within tolerance
6. No `float` in scoring paths (only `Decimal`)
7. No `datetime.now()` calls
8. No `random` without explicit seed
9. Audit log writer initialized
10. Run ID deterministically generated

## Post-Run Checklist

1. All output scores within [0, 100]
2. Governance metadata present in every output
3. Content hashes match (determinism)
4. No SEV3 tickers in ranked output
5. Coverage metrics logged
6. Circuit breaker did not trip silently
7. Staleness penalties applied where required
8. Audit log complete (INIT through FINAL)

---

## Source Files

| Component | File |
| --- | --- |
| Data Quality Gates | `common/data_quality.py` |
| Staleness Gates | `common/staleness_gates.py` |
| PIT Enforcement | `common/pit_enforcement.py` |
| Input Validation | `common/input_validation.py` |
| Schema Validation | `common/schema_validation.py` |
| Production Hardening | `common/production_hardening.py` |
| IC Measurement | `backtest/ic_measurement.py` |
| Audit Log | `governance/audit_log.py` |
