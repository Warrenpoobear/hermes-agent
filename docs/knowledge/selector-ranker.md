# Selector / Ranker / Construction (Knowledge Reference)

<!--
SYNC PROVENANCE
  Source: Town skill `selector-ranker`
  Source maturity (per skill-maturity-metadata): STABLE (last reviewed 2026-06-22)
  Synced to Hermes: 2026-06-24 (manual, operator-approved, PR-gated)
  Sync owner: Darren Schulz (dschulz@wakerobin.co)
  Type: knowledge-layer reference (NOT an agent; no AGENT_REGISTRY.json entry, no cron, no authority)
  Batch: Town -> Hermes mapping pipeline.
  SCOPE NOTE: Only the STABLE "Framework Reference" section is synced. The source skill's
  volatile "Operational State" section (dated ruleset IDs, T1-T8 research status, snapshot
  metrics) is intentionally EXCLUDED — it goes stale and should be fetched live via MCP /
  the biotech-screener repo rather than mirrored here.
-->

## Purpose

Reference for the production two-stage selector/ranker architecture and EW Top-30 construction — how the screener turns scored tickers into an actionable ranked portfolio. This reference carries the **stable framework only**; volatile operational state (active ruleset ID, research-spec status, snapshot metrics) is excluded by design — fetch it live.

---

## Production Stack (v1.14.0)

```
Modules 1-5 (scoring)
  -> Decision Engine (L0 gates -> L2 overlays -> L4 tiers -> L3 sizing -> sort key)
  -> Selector Engine (B6: coinvest_score_z 100%)
  -> Ranker Engine (pairwise_minimal: 6 features, top-60 cohort, ordinal-only)
  -> Sort by final_score -> EW Top-30 -> rankings.csv
```

---

## Selector Engine

File: `selector_engine.py`

### B6 Selector (Production)

- v1.14.0: coinvest_score_z at 100% weight (coinvest-only)
- Prior (v1.13.0): coinvest 65% + inst_delta_z 35%
- inst_delta_z zeroed 2026-05-04 (ALERT: mean IC = -0.097 over 36 dates, two-frame confirmed)
- Reinstatement conditions documented in governance log

> Signal naming cross-reference (CON-1): Repo model docs and .docx files use legacy names `sponsorship_score_z` (= `coinvest_score_z`) and `momentum_delta_z` (= `inst_delta_z`). Same signals, different names. Current skill docs and production code use `coinvest_score_z` and `inst_delta_z`.

### Selector Validation

- Checklist v2 (2026-04-04): bootstrap +2.42pp/mo, 95% CI [1.25%, 3.70%], P(>0) = 99.99%
- LOSO: ROBUST across all dimensions
- Neither component survives standalone, but the bundle is real
- Sort anchor: `selector_score`

### What the Selector Learns

Coinvest selects WHICH 30 names enter the portfolio. It captures institutional co-investment conviction from elite biotech managers.

---

## Ranker Engine

File: `ranker_v2_pairwise.py`

### Pairwise Minimal Ranker (Production)

- 6 input features enter the ranker at runtime, but the deployed artifact stores only 2 non-zero trained weights (coinvest_score_z and financial_score) in `production_data/ranker_v2_model.json`. The other 4 features have near-zero coefficients but are retained for forward compatibility and diagnostic logging.
- Document discrepancy: repo model docs and the .docx Executive Overview describe a "2-feature" ranker (referencing the stored weight artifact). This reference describes "6 features" (the full runtime input vector). Both correct, different layers. The deployed artifact's `provenance` block is authoritative for production weights.

> OPEN ISSUE N1 (Run 8, 2026-05-25): `coinvest_score_z` deployed ranker weight = +0.02 (capped Family C live pilot, per model_documentation.md v1.7.2). Trained basis weight = +0.0613 (stored in artifact). The +0.02 cap reflects a deliberate live-pilot ceiling, not the trained coefficient. Cite +0.02 as the deployed weight in production context; +0.0613 only when describing the trained artifact.

- ECE = 0.129 (POOR calibration — confirms ordinal-only is correct)
- Top-60 cohort scope
- inst_delta_z zeroed in selector since v1.14.0 (2026-05-04), but remains active in ranker as a feature

> Fix applied 2026-05-16 (Code Review H3): Corrected "excluded from ranker since Spec 051" — inst_delta_z was zeroed in the SELECTOR, not the ranker. It remains an active ranker discriminator (NW-t = +3.32).

### Within-Top-30 Feature Roles

| Feature | Role | NW t-stat |
| --- | --- | --- |
| inst_delta_z | Dominant positive discriminator | +3.32 |
| financial_score | True negative penalty (stress-upside) | -3.41 |
| coinvest_score_z | Washes out within cohort | +0.49 |

### financial_score Sign Direction (RESOLVED, Spec 093)

- Weight: -0.0533 in `production_data/ranker_v2_model.json`
- Confirmed intentional: stress-upside thesis (Spec 074, reconfirmed Spec 093 2026-05-13)
- Classification: INTENTIONAL_STRESS_UPSIDE
- Negative weight means financially safe names are penalized (more catalytic, less safe names preferred)
- Raw components: 50% runway + 30% dilution + 20% liquidity (all directional: higher = better health)
- Rank-normalized within stage x size cohort (direction preserved)
- t-statistic significant (-3.41), persists across cohorts and regimes

---

## Construction

### EW Top-30

- Equal-weight, top 30 names by final_score
- K=30 validated by PIT sweep (stable K=25-35 plateau, net-of-cost peak)
- RW-EW delta = -0.09pp, t = -0.95 (rank-weighting does NOT help)

### Production Evidence

- True PIT backtest: +2.34pp/mo net-of-cost, t = 2.57, 69% hit rate, 67 monthly periods (Jun 2020 - Apr 2026)
- Bear/neutral alpha engine: Bear +3.37pp (75% hit), Neutral +6.23pp (93% hit), Bull -0.37pp (50% hit)
- Regime caveat: expect bounded underperformance in strong bull markets

---

## Decision Engine

File: `decision_engine.py`

### Pipeline Layers

| Layer | Purpose |
| --- | --- |
| L0 | Hard gates (liquidity, price, data quality) |
| L2 | Overlays (event_type_score as diagnostic) |
| L4 | Tier classification |
| L3 | Position sizing |

### EV/Sizing Severity Consumption (Spec 101, RESOLVED)

The L3 position sizing layer consumes `ev_severity_score` (from runway severity v1.1):

```
dilution_haircut = 0.35 * ev_severity_score
size_multiplier = max(0.40, 1.0 - 0.60 * ev_severity_score)
```

`ev_severity_score` is exported to `rankings.csv` and `SNAPSHOT_COLUMNS` (Spec 101, commits eaa4ea87 + cba4ee0f). `check_severity_formulas()` QA validation runs every snapshot.

---

## Dead Lanes (Do Not Reopen Without New Evidence)

| Lane | Status | Why |
| --- | --- | --- |
| Options surface-shape as ranker | DEAD | 50-month IC negative all horizons |
| Options-as-alpha (Spec 053) | CLOSED | 37 signals tested, ALL fail |
| Static execution features (Spec 054) | CLOSED | All noise/destructive |
| Clinical composites as ranker (Spec 055) | CLOSED | Negative across ALL slices |
| total_volume_z | DEAD | IC = -0.10 on PIT data |
| Always-on rank-weighting | NOT PROMOTED | RW-EW = -0.09pp |
| insider_exec_buy_value_90d | SHADOW ONLY | 1/5 Checklist v2 |
| aact_execution_score | SHADOW ONLY | 1/5 Checklist v2 |
| cal_alpha | REMOVED v1.12.0 | Confirmed no-op |
| Clinical sort signal | OFF | Insufficient IC |
| Fixed sleeve budgets | RETIRED | Primary construction damage (+153.6pp drag) |

---

## Promotion Governance

| Component | File |
| --- | --- |
| Manifest | `production_data/decision_rulesets/manifest.json` |
| Promotion Battery | `scripts/research/run_promotion_battery.py` |
| Promote Script | `scripts/promote_ruleset.py` (blocks unless battery PASS) |
| Health Monitor | `tools/ruleset_health_monitor.py` (post-promotion drift) |
| Rollback | `scripts/promote_ruleset.py --rollback --reason "..."` |

Drift detection: JSONL append per evaluation (idempotent on same-day reruns); consecutive WARN tracking by active ruleset ID; recommend rollback after sustained degradation.

---

## Source Files

| Component | File |
| --- | --- |
| Decision Engine | `decision_engine.py` |
| Selector Engine | `selector_engine.py` |
| Ranker v2 Pairwise | `ranker_v2_pairwise.py` |
| Ranker Legacy | `ranker_engine.py` |
| Main Orchestrator | `run_screen.py` |
| Ruleset Manifest | `production_data/decision_rulesets/manifest.json` |
| Promotion Battery | `scripts/research/run_promotion_battery.py` |
| Checklist v2 | `scripts/research/checklist_v2_rerun.py` |

---

> Operational state (active ruleset ID, T1-T8 ranker-alternatives research status, snapshot metrics, monitoring-spec review dates) is intentionally NOT mirrored here — it is volatile. Fetch it live via the biotech-screener repo / Hermes MCP when needed.
