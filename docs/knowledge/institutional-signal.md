# Institutional Signal (Knowledge Reference)

<!--
SYNC PROVENANCE
  Source: Town skill `institutional-signal`
  Source maturity (per skill-maturity-metadata): STABLE but HIGH-CHURN (14-day SLA, live 13F/VRDN state)
  Synced to Hermes: 2026-06-24 (manual, operator-approved, PR-gated)
  Sync owner: Darren Schulz (dschulz@wakerobin.co)
  Type: knowledge-layer reference (NOT an agent; no AGENT_REGISTRY.json entry, no cron, no authority)
  Batch: Town -> Hermes mapping pipeline.
  NOTE: Reference knowledge a SOUL.md may cite. It does not execute, mutate data, or write to .learnings/.
-->

> **LIVE-STATE WARNING — framework only.**
> This reference carries ONLY the stable Framework Reference (Section 1) of the source skill.
> The source skill's Section 2 "Operational State" — 13F filing-cycle status, the VRDN PDUFA
> countdown, per-quarter holdings snapshots, accession numbers, cohort-quarantine verdicts, and
> near-term coinvest watch — is **intentionally EXCLUDED** because it goes stale within days.
> Do NOT add point-in-time 13F state to this file. For current institutional state, fetch live
> from `production_data/institutional_summary.json`, the cohort-quarantine tool output, or the
> Town institutional-signal skill — never from this static copy.

## Purpose

Reference for the 13F institutional signal pipeline — from SEC EDGAR filing ingestion through the `coinvest_score_z` production signal and cohort quarantine governance. This is the dominant selector signal (100% weight in v1.14.0).

---

## Architecture Overview

```
SEC EDGAR 13F-HR filings
  -> warm_13f_cache.py (per-CIK PIT cache dirs)
  -> build_institutional_summary.py (canonical summary)
  -> coinvest_score_z (selector signal, 100% weight v1.14.0)
  -> inst_delta_z (governance-controlled; active in ranker only as of v1.14.0)
```

---

## Manager Registry

File: `production_data/manager_registry.json`. Never edit directly — use `tools/onboard_manager.py`. Derive the manager count dynamically from this file; never hardcode it.

### Tiers

| Tier | Description | Signal Weight |
| --- | --- | --- |
| elite_core | Highest-conviction biotech-focused managers | Full weight |
| conditional | Broader institutional managers with biotech exposure | Reduced weight |

Tier 1 (highest conviction, per operator preference): Fairmount Funds, Deep Track Capital, Logos Capital.

### Onboarding Flow

```bash
python tools/onboard_manager.py \
  --cik 1802528 \
  --name "Fairmount Funds Management" \
  --aum-b 1.3 \
  --style concentrated_clinical_stage \
  --tier elite_core \
  --notes "..."
```

One-shot flow: registry append -> backfill across every existing PIT dir (lookback=40, approx 10y) -> warm current as-of date -> run `tools/test_manager_integration.py` (6/6 gate). Partial reruns: `--skip-registry`, `--skip-backfill`, `--skip-current`, `--skip-test`.

---

## coinvest_score_z

The production selector signal. Measures institutional co-investment conviction across elite biotech managers.

### Key Properties

- Drives 100% of selector weight (v1.14.0, coinvest-only after inst_delta_z demotion)
- Correlation with final_score: rho = +0.882 (double-count concern, documented in T1 ranker anatomy)
- Checklist v2: 3/5 standalone, but bundle (with inst_delta) is 5/5
- Collapse guard: SD floor = 0.10 (below this, snapshot integrity check FAILs)

### Data Flow

1. PIT cache: `data/caches/sec_13f/PIT/{YYYY-MM-DD}/` per manager
2. Canonical summary: `production_data/institutional_summary.json`
3. Delta computation: `institutional_summary_delta.json` (pre vs post refresh)
4. Score: z-scored across eligible universe per snapshot

---

## inst_delta_z

Quarter-over-quarter change in institutional holdings. Measures whether smart money is accumulating or distributing.

- Reinstatement requires IC recovery evidence documented in governance log
- When active, contributes to ranker (dominant positive discriminator, NW-t = +3.32)
- When zeroed, selector runs on coinvest_score_z alone
- Current zeroed/active status is volatile — fetch live, do not assume from this file

---

## insider_net_buy_value_90d (Spec 104, Diagnostic Only)

Form 4-derived insider buying signal over a trailing 90-day window.

### Status: DIAGNOSTIC ONLY

- Listed in `DIAGNOSTIC_FIELDS`, NOT in `ALPHA_FEATURE_REGISTRY`
- Tracked/exported for observability; does NOT enter scoring model, ranker, or selector
- Does NOT affect ranks, actions, or position sizing

### Blank vs. Zero Semantics (CRITICAL)

| Value | Meaning |
| --- | --- |
| NaN / None / blank | Not fetched, no Form 4 coverage for this ticker |
| 0.0 | Fetched successfully, no insider buy activity in 90-day window |

Never collapse blank and zero. Never impute zero for missing or blank for zero.

### Expectation Model Isolation Guard (Spec 104, R4a)

The expectation model has an `insider_net_buy_z` weight that activates silently if `insider_net_buy_value_90d` flows into `market_features`. Spec 104 requires an explicit guard: runtime assertion that the field is NOT in `market_features`, or weight zeroing, or a pre-inference drop guard.

### Promotion Criteria (future, not current build)

Requires ALL of: 20+ stable snapshots with >= 60% non-null coverage, blank/zero integrity verified, IC > 0 at p < 0.05, Checklist v2 battery pass, explicit written approval.

---

## 13F Refresh Cycle

SEC 13F filings have a 45-day lag from quarter-end. Filings typically cluster in the final 3 business days before the deadline.

### Pre-Refresh Readiness (`tools/prep_13f_refresh.py`)

5 guards, all must PASS:

| Guard | Check |
| --- | --- |
| 1 | Most recent snapshot has valid institutional_summary_delta.json |
| 2 | coinvest_score_z has healthy variance (SD > 0.10) |
| 3 | PIT cache has entries within 3 days of today |
| 4 | SEC EDGAR endpoint is reachable |
| 5 | Dry-run: build_institutional_summary() produces valid output (>=80% coverage) |

Writes baseline artifact: `artifacts/13f_pre_refresh_baseline_{date}.json`

### Cohort Quarantine (`tools/check_13f_cohort_quarantine.py`)

Run after new filings land. Compares pre-refresh vs post-refresh snapshots.

Sections: A (manager-level diff), B (coverage diff), C (per-ticker score diff), D (top-30 churn / Jaccard).

| Verdict | Meaning | Action |
| --- | --- | --- |
| CLEAN | Normal refresh, minimal churn | Proceed |
| QUARANTINE | Significant score/rank disruption | Hold for review |
| PRODUCER_AUDIT_REQUIRED | Anomalous coverage or manager changes | Deep investigation |

Telegram alerting on QUARANTINE/PRODUCER_AUDIT_REQUIRED (suppressible with `--no-alert`).

### Contamination Window

After adding new managers, a contamination window opens (typically 20 trading days). IC measurements during this window are flagged contaminated and excluded from clean IC calculations.

---

## Data Provenance Rules

- Holdings truth source: `production_data/institutional_summary.json` is canonical
- CUSIP-first, not issuer-first: always reason from CUSIP -> canonical ticker
- Raw EDGAR XML is debug-only: never build narratives from raw filing parses
- If raw count != summary count: investigate the summary pipeline first

---

## Key Biotech 13F Filers to Track

Per operator preference: Fairmount Funds, Deep Track Capital, Logos Capital. Also monitor BioPharm IQ Twitter (https://twitter.com/BioPharmIQ).

---

## Source Files

| Component | File |
| --- | --- |
| Manager Onboarding | `tools/onboard_manager.py` |
| 13F Cache Warmer | `tools/warm_13f_cache.py` |
| Institutional Summary Builder | `build_institutional_summary.py` |
| 13F Refresh Readiness | `tools/prep_13f_refresh.py` |
| Cohort Quarantine | `tools/check_13f_cohort_quarantine.py` |
| Snapshot Collapse Guards | `tools/verify_snapshot_integrity.py` |
| Manager Registry | `production_data/manager_registry.json` |
| Institutional Summary | `production_data/institutional_summary.json` |
