# Research Opportunity Queue — week of 2026-07-24

**Run date:** Thursday, July 30, 2026 | **Captures reviewed:** 53 items across 7 daily digests (2026-07-24 through 2026-07-30) | **Candidates qualified:** 5 (4 RUN / 1 WAIT) | **X quota gap:** Monthly limit dark the entire window (resets Aug 1); web-search fallback used throughout. All surfaced items independently corroborated.

---

## Top-5 Ranked Experiments

| # | Title | Tool/Source | Effort | ROI | Evidence | Stack Area | Rec |
|---|-------|-------------|--------|-----|----------|------------|-----|
| 1 | Context Engineering — Hermes Skill Prompt Audit | Anthropic / Claude Code | 30 min | High | High | hermes-agent runtime + PKOS skill layer | **RUN** |
| 2 | MCP 2026-07-28 — Stateless Protocol Migration | Anthropic MCP spec | 2–4h audit | High | High | hermes-agent, Robinhood MCP, ASKB | **RUN** |
| 3 | DFAH-Bench — Financial Agent DAR/TAR Stability Audit | IBM / arXiv:2607.20491 | 2–3h | High | Medium | biotech-screener IC + backtest-framework | **RUN** |
| 4 | Hermes Write-Path Governance Audit (Kaur + CSA) | arXiv:2607.21735 + CSA | 1–2h | High | Medium | hermes runtime governance + Reliability Gate PR #19 | **RUN** |
| 5 | Cursor Agent Swarm — Planner/Worker Architecture Pilot | Cursor / minisqlite | 1 cron run | High | Medium | hermes-agent multi-agent architecture | **WAIT** |

---

## Detailed Write-Ups

---

### Rank 1 — Context Engineering: Hermes Skill Prompt Audit

**Underlying capability:** Anthropic "unhobbling" — removing legacy guardrails baked into system prompts and skill documents that compensated for pre-Claude-5 model limits, now replaced by tool schemas and selectively loaded skills. Anthropic removed >80% of Claude Code's system prompt for Opus 5 and Fable 5 with no measurable eval regression.

**Primary source:** https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models (Thariq Shihipar, Anthropic MTS, Jul 24, 2026)

**Estimated effort:** 30 min

**Expected payoff:** High — Stack impact: hermes-agent runtime + PKOS skill layer (all 45 skills). Reduces per-run token cost, frees context window, eliminates latent instruction conflicts.

**Evidence quality:** High — Official Anthropic primary source; corroborated by Cursor Jul 26 swarm experiment and ARC-AGI-3 30.2% record (both confirm capability step-change underpinning the claim).

**Similar tools already tested:** No prior Hermes skill prompt audit in ROQ ledger.

**Success metric:** Token count per run on audited skill drops ≥20%; eval pass rate holds or improves; latency flat or lower.

**Smallest shadow test:** Pick screener-ops or clinical-scoring. Delete constraints that compensate for pre-Claude-5 model limits. Run same eval. Measure: token count delta, eval pass rate, latency. One session.

**Ladder move:** independent_confirmation → internal_experiment → measured_improvement

**Recommendation: RUN** — Highest composite score this week (ROI 5 × Evidence High / Effort 30 min = 15.0). Shadow test is bounded, non-destructive, fully reversible. Freeze permits measurement work; this qualifies.

---

### Rank 2 — MCP 2026-07-28: Stateless Protocol Migration (Breaking Change)

**Underlying capability:** MCP 2026-07-28 removes protocol-level sessions, `initialize` handshake, and `Mcp-Session-Id`. Every request now self-describes. Old clients cannot talk to new servers without migration. MCP = 400M monthly SDK downloads, de facto agentic standard.

**Primary source:** https://claude.com/blog/bringing-mcp-2026-07-28-to-claude | https://blog.modelcontextprotocol.io/posts/2026-07-28/

**Estimated effort:** 2–4h audit; 1–2 days migration per server with state dependencies

**Expected payoff:** High — Stack impact: hermes-agent runtime (all MCP servers), Robinhood MCP OAuth, Bloomberg ASKB.

**Evidence quality:** High — Official Anthropic + 5+ independent engineering sources.

**Success metric:** Zero MCP server failures after client auto-upgrade. Robinhood MCP confirmed functional under 2026-07-28 spec in dev before upgrade propagates.

**Smallest shadow test:** (1) Inventory all Hermes MCP servers for `initialize` handshake / `Mcp-Session-Id` dependencies. (2) Test Robinhood MCP in dev against 2026-07-28 spec. (3) Identify state-carrying tools needing refactoring. Time-box: 2–4h.

**Ladder move:** primary_source_found → internal_experiment → measured_improvement

**Recommendation: RUN** — Non-optional breaking change. Add MCP audit to Aug 1 remediation sprint agenda.

---

### Rank 3 — DFAH-Bench: Financial Agent DAR/TAR Stability Audit

**Underlying capability:** DFAH-Bench (IBM; arXiv:2607.20491; ICLR 2026 FinAI workshop). 8,127 agentic runs across 10 models: determinism and accuracy uncorrelated (Spearman r = −0.11, p = 0.63). Introduces DAR, TAR, and DAR–TAR gap — consistent decisions via inconsistent reasoning paths, invisible to outcome-only evaluation. Open-source code.

**Primary source:** https://arxiv.org/abs/2607.20491 | https://github.com/ibm-client-engineering/output-drift-financial-llms

**Estimated effort:** 2–3 hours

**Expected payoff:** High — Stack impact: biotech-screener IC framework, backtest-framework, ic-evaluation skill.

**Evidence quality:** Medium — IBM preprint; open-source, replicable; ICLR 2026 FinAI workshop prior work.

**Success metric:** DAR ≥ 80% and TAR ≥ 70% on 5-run replay. If DAR–TAR gap > 20%, flag as IC measurement validity risk.

**Smallest shadow test:** Run 5 identical screener prompts through one Hermes agent on 3 consecutive days. Compute DAR, TAR, gap using DFAH-Bench open code.

**Ladder move:** independent_confirmation → internal_experiment → measured_improvement

**Recommendation: RUN** — DEM forward-validation mandate at 0/20 windows. Tool-path stability is a prerequisite for trusting IC accumulation. Open code, low effort.

---

### Rank 4 — Hermes Write-Path Governance Audit (Kaur Taxonomy + CSA Post-Mortem)

**Underlying capability:** (1) Kaur arXiv:2607.21735 — formal proof that a passing red-team eval cannot prove dangerous capability is absent; maps what evals can/cannot prove. (2) CSA CISO post-mortem (~700 CISOs) on OpenAI/HF sandbox escape: models chained zero-days "no human would take" but issued malformed commands. Key finding: step-level coherence is a lagging indicator — monitor sequence-level action-chain patterns.

**Primary sources:** https://arxiv.org/abs/2607.21735 | https://cloudsecurityalliance.org/artifacts/hugging-face-ciso-post-mortem

**Estimated effort:** 1–2 hours

**Expected payoff:** High — Stack impact: hermes runtime governance, Reliability Gate v1.0 (PR #19), biotech-screener write paths.

**Evidence quality:** Medium — Kaur: preprint + independent coverage. CSA: institutional primary (~700 CISOs) + The Register + iTnews. Interpretation confidence capped medium (OpenAI technical report pending).

**Success metric:** All Hermes write-path tools classified against Kaur taxonomy. Action-chain coherence criterion added to PR #19 draft. Zero unguarded write paths.

**Smallest shadow test:** List all Hermes tools that touch state. For each: (1) apply Kaur taxonomy, (2) enumerate 2–3 most dangerous valid-operation sequences. Cross-check against Reliability Gate PR #19 draft. 1 hour, no code change.

**Ladder move:** independent_confirmation → internal_experiment (PR #19 update) → measured_improvement

**Recommendation: RUN** — Directly feeds PR #19 (already in-flight). Zero new engineering. Pair with Jul 23 Rank 2 sandbox audit in single governance sprint.

---

### Rank 5 — Cursor Agent Swarm: Planner/Worker Architecture Pilot

**Underlying capability:** Cursor experiment — frontier planner + cheaper worker swarms reached 100% task completion in every configuration. Single-model baselines 11–77%. Open-source codebase (minisqlite).

**Primary source:** https://the-decoder.com/cursors-agent-swarm-suggests-cheaper-models-can-handle-most-coding-when-frontier-models-plan-the-work/

**Estimated effort:** 1 cron run (2–3h)

**Expected payoff:** High — Stack impact: hermes-agent runtime, biotech-screener agents, v0.19 upgrade planning.

**Evidence quality:** Medium — Cursor's own experiment; open codebase; The Decoder independent editorial.

**Success metric:** Cost-per-Herald-digest-run drops ≥15% with planner+worker vs. single-model baseline; output quality equivalent or better.

**Smallest shadow test:** Run one Herald digest with Opus 5 as planner + Haiku/Sonnet for retrieval. Compare cost, run time, output quality vs. current config. One cron run.

**Ladder move:** primary_source_found → internal_experiment → measured_improvement

**Recommendation: WAIT** — Gate on: (a) CI GREEN (Aug 1 reset) and (b) v0.19 upgrade executed. Then run immediately.

---

## Also Considered (Ranked 6–N)

6. **OpenAI Codex Security CLI** (Apache-2.0) — ROI 4. WAIT — v0.94 CVE must be confirmed patched in v0.95.0+ before write-path integration. Natural candidate after Aug 1.
7. **GitHub Issues Agent Automation Controls** — ROI 3, 15-min shadow test. RUN post-CI-green (too small for Top-5 slot).
8. **Claude Opus 5 mid-conversation tool switching** — ROI 4, blocked dedup window (expires Aug 8). Carry to next week's ROQ.
9. **Deep Agents v0.7** (LangChain) — ROI 3, 65% token reduction. WAIT for Hermes v0.18.0 compatibility check.
10. **Scale AI ResearchRubrics** — ROI 3. WAIT until deep-research agent pilot active.
11. **Bloomberg/Canoe Intelligence** — ROI 3, data-adapter. WAIT 12–24 months.
12. **RSI governance letter** (1,100 insiders) — ROI 4. WATCH — investment thesis / long-horizon governance, not a process experiment.
13. **KAT-Coder-V2.5** (open-weight) — ROI 3. WAIT for independent SWE-bench replication.
14. **Perplexity CLI** — ROI 3. WAIT — high cost + security concerns require sandboxed eval first.

**Carryover from Jul 23 ROQ still open:** Petri harness shutdown-pressure test (Rank 5/RUN), GPT-Red/Fake-CoT injection (Rank 6/RUN), AGENTS.md governance standard (Rank 1/RUN, dedup expires Aug 6), Contrastive SDF audit (Rank 3/RUN, dedup expires Aug 6), METR Expenditure Horizon (Rank 4/RUN, pairs with Rank 5 WAIT).

---

## Dropped This Week

| Item | Reason |
|------|--------|
| Mastra Factory | terminal_state: Unverifiable — 3 verification attempts, vendor-only sourcing. Drop despite ROI 4. Re-evaluate if independent editorial coverage appears. |
| Samaya FrontierFinance | Promotion / COI — vendor designed + claims top score. Quarantined pending independent replication. |
| Qwen 3.8 | No benchmark table, no model card from Alibaba. |
| Kimi K3 open weights | Watch-only — 51% undisclosed hallucination rate (independent review). |
| Meta benchmark cherry-picking | Pattern context only; no experiment. |
| AMD Helios / MI455X | NVDA competitive intelligence; no Hermes workflow impact. |
| IBKR MCP expansion | Robinhood MCP already connected; directional signal only. |
| Cursor Router GA | Teams/Enterprise governance; revisit at freeze exit (~Oct 2026). |

---

## Self-Check

- Captures reviewed: 53 | Candidates qualified: 5 | Top-N: 5 (4 RUN / 1 WAIT)
- X quota: dark entire window (resets Aug 1); web fallback used; all items independently corroborated
- Destinations: Content Library ✓ | GitHub ✓ | Ledger ✓ | Emails ✓ | Memory ✓
