# HOT-tier Memory — DEM Fleet (Wake Robin Biotech Screener)
# Cap: 100 lines. Loaded every session. Do not exceed.
# Last updated: 2026-06-24
# Source repo: C:\Projects\biotech_screener\biotech-screener\

---

## System Identity

- **Project**: Wake Robin Capital — institutional biotech investment screener
- **Decision Engine**: Two-stage selector/ranker → EW Top-30 output
- **Production pipeline**: 13-step daily cron, 5:30 PM ET
- **Governance**: CCFT (Canonical, Complete, Frozen, Timestamped). All outputs deterministic.

---

## Active Ruleset

- **Ruleset**: v1.14.0 (`8887576e`) — coinvest-only selector, pairwise_minimal ranker
- **Sort anchor**: selector_score (coinvest_score_z 100%)
- **inst_delta_z**: ZEROED in selector since 2026-05-04 (mean_ic=-0.097, two-frame confirmed)
- **Model fleet**: `deepseek/deepseek-v4-flash:free` (migrated 2026-05-20, all 27 active agents)
- **Pinned in**: `run_screen.py` AND `run_phase2_snapshot_delta.py` (must stay in sync)

---

## Architecture Freeze

- **Status**: ACTIVE through ~2026-05-26 (h20d checkpoint)
- **h20d decision**: May 26. Evidence collected. All 5 Path A conditions met as of 2026-05-22.
- **Expected outcome**: Path A (freeze lift), June 1 KG deployment + ranker shadow start
- **No changes allowed**: no enforcement logic, scoring, or ranking changes until freeze lifts

---

## 13F Cohort Status

- **Q1 2026**: CLEARED as of 2026-05-19 (Jaccard 0.875, 42/48 managers, all gates PASS)
- **Tier 1 managers**: Fairmount, Deep Track, Logos — all filed 2026-05-15
- **Key positions**: VRDN (FM 14.04% + DT 5.30%), ORKA coinvest (FM + DT)
- **Next cycle**: Q2 2026, deadline ~2026-08-14

---

## Active Blockers / Held Specs

- **Spec 100** (ranker IC tooling): blocked by architecture freeze, implement post-May-26
- **Spec 095** (IC scope bug): CURRENT_TOOLS_CONFLATED — all composite_score IC claims invalid
- **score_rank_pct**: SPEC_REQUIRED — WARN streak (mean_ic=-0.0119, hit_rate=28.95%)
- **Spec 087 B2**: UNBLOCKED (B1b formally closed 2026-05-14), dashboard envelope ready to draft
- **Spec 088 Phase B**: HELD — pending Spec 087 full closure
- **KG Phase 2 Step 5**: blocked until freeze lifts (June 1 target)

---

## Governance Rules (Always Active)

- North star: backtests produce evidence only — never change production weights without governance
- No agent may modify production weights without full multi-gate promotion path
- Tier 4 changes (architecture, signal promotion) require memo + human approval
- Town-Hermes Feedback Protocol: post-h20d phase (h20d 2026-05-26 elapsed) — manual reviewed sync only; automated export gated on two clean manual cycles + operator approval
- Only `crt_resolution_watcher` holds `mutate_data` authority
- Lane A agents must not depend on LLM gateway tokens
- PIT rule: never call set "true PIT" unless archived raw inputs + archived code + archived artifacts all exist

---

## 2026-06-24 Session Updates (supersede where conflicting)

- **Architecture freeze: LIFTED 2026-05-26** (h20d passed). Supersedes "Architecture Freeze: ACTIVE" above.
- **Town-Hermes feedback freeze: LIFTED 2026-06-24** (operator decision). Town-sourced content may land via reviewed PRs. STILL GATED: automated `.learnings/` write paths + automated memory sync need their own spec + approval; read-only Skills MCP unchanged.
- **Town skill sync (pilot):** 9 Town skills mapped to `docs/knowledge/*.md` as knowledge-layer references (NOT agents). Open PRs #35-43 (#35 = financial-health + CLAUDE.md freeze-text lift; merge #35 first). Awaiting operator merge.
- **High-churn skills** (institutional-signal, screener-ops) synced framework-only with live-state banners; volatile state excluded — fetch live via MCP.
- **SEC Filing Monitor (Town routine):** schedule fixed to single 7 PM ET run (was 9 AM + 7 PM; 9 AM dropped to match prompt).
- **CNTA:** Eli Lilly acquisition closed 2026-06-24; ADS delisted; coinvest watchlist 17 → 16.
- **VRDN:** veligrotug PDUFA 2026-06-30 (highest-priority active watch; FM 14.04% + DT 5.4M sh).

---

## Forward Monitor

- Accumulating since 2026-04-03. ~35+ trading days as of 2026-05-22.
- coinvest_score_z pooled mean IC = -0.031 (14 dates, 28.6% hit rate) — OBSERVE verdict
- Ranker IC: UNMEASURED (Spec 095 scope bug; blocked until Spec 100)
- Post-13F refresh IC decomposition: pending (gate: quarantine cleared ✓)

---

## Open Items — Skills Learning Sweep 2026-06-24 (operator decision needed)

Logged from a full read-only sweep of all 40 Town skills (repo Issues are disabled, so tracked here). No model/ranker/selector/scorer/sizing change; observe-only.

1. **Stalled self-improvement loop (failure-patterns PENDING past threshold).** Two entries past the >=3 / one-cycle threshold, blocked on unresolved outages not missing rules:
   - F-2026-005 Herald dark ~10 weeks (since ~2026-04-14). Code fixes merged; terminal recovery verification never confirmed.
   - F-2026-006 CI red ~47 days (since ~2026-05-08, PR #285 open). operational-health-baselines own SLA = block merges after 5 red days; freeze exception now moot.
   - DECISION: for each, confirm recovery from host (terminal) → mark RESOLVED, OR formally accept as known-open with a target date.
2. **Checklist v2 battery rerun vs final_score — NOT executed (~29d post-freeze-lift).** Highest-priority unblocked research action. Spec 100 tooling fix landed (2faa88e6); ranker IC stays UNMEASURED until the rerun runs. Forward shadow ~61+ trading days, evidence ready.
3. **Doc-only cleanup (done same session):** catalyst-resolution CRL CING-pending wording reconciled. Still open elsewhere: v1.14.0 signal-rename back-propagation to GitHub model docs + .docx (F-2026-001); agent-count drift cleanup (F-2026-008); decision-audit-trail D-2026-001/004 rationale backfill.

---

## Stalled-Loop Verdicts (FILL IN — operator sign-off required) 2026-06-24

Hermes-side mirrors applied via PR #391 (Cursor). Patch-efficacy tracking (harvest_log "2-week post-merge" check) cannot start until these two are RESOLVED — you cannot measure "0 recurrence since fix" on an outage whose recovery was never confirmed from the host. Town cannot read the host (crontab/logs/smoke test), so it cannot self-close these. Pick ONE per entry:

- **F-2026-005 Herald:** [ ] RESOLVED — recovery confirmed from host on ____; verify deduped_{date}.jsonl + classified_{date}.jsonl present  |  [ ] KNOWN-OPEN — target date ____
- **F-2026-006 CI:** [ ] RESOLVED — CI green on main confirmed ____ (PR #285 merged?)  |  [ ] KNOWN-OPEN — target date ____

On RESOLVED: set the failure-patterns entry to PROMOTED/RESOLVED and add the harvest_log 2-week verification block. On KNOWN-OPEN: record the target date so it stops reading as a silently-stalled loop.

## Self-Improvement Loop — Town↔Hermes alignment note (for Hermes Rule 12) 2026-06-24

When Hermes adds the Rule 12 promotion checklist, point it at the SHARED definition, do not fork it:
- **Threshold:** reuse the `self-improving` skill's canonical `>= 3` occurrences (failure modes all-time; behavioral patterns 7-day window). A parallel Hermes threshold = definition drift (F-2026-001-class) and the two sides will disagree on what "promotable" means.
- **Feed:** source promotion candidates from the Town Correction Ledger (`content://collections/self-improvement/correction-ledger`) `recurrence_count >= 3` rows — already-counted, deterministic — rather than re-deciding from ad-hoc chat corrections.
- **Audit-count note:** `audit_hermes_skills.py` 32/32 is expected, not a discrepancy. Town has 40 skills; 8 (SFO / family-office / real-estate framework skills) have no Hermes mirror by design. Worth one line in the audit output so a future reader does not chase a phantom 8-skill drift.

## Skills Corrections Backlog (audit 2026-06-24)

Correction-worthy items found in the skills audit (distinct from expected stale operational state). Each notes who can fix it — none is a fabricated-fact error a Town session can correct without a primary source.

- **FIXED — catalyst-resolution CRL count line.** "0 PENDING (CING 8-K pending)" contradiction reconciled to "CING CRL-inferred, official 8-K still pending verification" (Town doc edit, 2026-06-24). No further action.
- **OPEN — financial-health composite weights (W1).** V3 Enhanced (24%), V3 Partial (28%), Baker-Style (22%) do not sum to 100%; remaining 72-78% unspecified, so Gate 7 cannot validate them. Fix: source the full weight vectors from production `module_5_composite.py` (or the deployed weight artifact) and document. Repo/code, not a Town edit — do not invent the missing allocations.
- **OPEN — decision-audit-trail rationale backfill.** D-2026-001 ($5 penny-stock gate) and D-2026-004 (20-day contamination window) carry `evidence: MISSING`. Fix: operator supplies the original rationale; until then leave marked MISSING (do not fabricate).
- **OPEN — document-lineage cron-schedule row (W5).** Lists screener-ops "5:30 PM" as a possible stale copy vs. `crontab -l` ground truth. Needs the live host crontab — host-gated.
- **OPEN — v1.14.0 signal rename back-propagation (F-2026-001).** Rule promoted into coding-standards; actual rename to GitHub model docs + .docx not yet propagated. Repo-side.
- **OPEN — agent-count drift cleanup (F-2026-008).** Rule promoted into hermes-runtime (cite agent_governance.md, dated); downstream stale counts (17/26/27/28) remain in other docs. Repo-side.

These surface in the monthly Self-Learning Loop Review digest until closed.
