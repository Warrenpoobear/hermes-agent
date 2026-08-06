# Research Opportunity Queue — week of 2026-08-06

**Run date:** Thursday, August 6, 2026 | 16:00 ET  
**Routine:** X Intelligence — Weekly Research Opportunity Queue  
**Governance:** DIAGNOSTIC_ONLY / NO_MODEL_CHANGE / NO_AUTOMATIC_SCORE_WRITE  
**Captures reviewed:** 7 daily AI digests (2026-07-31 through 2026-08-06); ~540 items scanned. X quota dark Jul 24–31; live X scan resumed Aug 1–6.  
**Candidates qualified:** 5 (all Top-5 slots filled)

---

## Top-5 Ranked Experiments

| Rank | Title | Effort | Evidence | ROI | Composite | Rec |
|------|-------|--------|----------|-----|-----------|-----|
| 1 | METR Reliability Gate — PR #19 Pre-Merge Checklist | 1–2 hrs | High | 4 | 12.0 | **Run** |
| 2 | Meta Muse Code — CI Sprint Alternative to Claude Code | 30 min | High | 4 | 12.0 | **Run** |
| 3 | Perplexity Numbat — Pre-Action Agent Security Monitor | 30 min install | Medium | 4 | 8.0 | **Run** |
| 4 | Anthropic Sandbox Escape — Hermes Write-Path Audit | 2–3 hrs | High | 5 | 7.5 | **Run** |
| 5 | Microsoft EvoLib — Test-Time Skill Extraction | 2–3 hrs | High | 4 | 6.0 | **Wait** |

*Composite = (ROI × Evidence score) ÷ Effort score. Ties broken toward items addressing current active bottlenecks.*

---

## Rank 1 — METR Reliability Gate Integration: PR #19 Pre-Merge Checklist

**Capability/Tool:** METR post-incident investigation framework (Jul 28, 2026)  
**Primary source:** https://metr.substack.com/p/2026-07-28-investigating-ai-propensities-after-incidents  
**Also:** https://openai.com/index/hugging-face-model-evaluation-security-incident  

**Estimated effort:** 1–2 hours (document mapping, no code)  
**Expected payoff:** High  
**Stack impact:** Hermes runtime governance; Reliability Gate v1.0 (PR #19); biotech-screener write paths; PKOS  
**Evidence quality:** High — METR primary blog + OpenAI official incident page + METR/Redwood contracted review confirmed by Unite.AI, Ground Truth, Magica. Aug 1 and Aug 2 digests both corroborate with independent sourcing.

**Similar tools already tested:** METR Expenditure Horizon (Jul 23 ROQ Rank 4) is a different framework (cost/task-scoping). Jul 30 ROQ Rank 4 (Kaur taxonomy + CSA CISO post-mortem) addressed write-path governance from the evaluation angle; this addresses it from the incident-investigation angle. Two different gaps, same sprint.

**Success metric:** All METR framework questions mapped to a Hermes observable (log entry, monitoring hook, or documented absence). PR #19 merge criteria checklist has zero METR-framework line items without an assigned observable or explicit "accepted gap" notation.

**Smallest shadow test:** Pull the METR Jul 28 blog access checklist. Map each item to what Hermes currently logs. Score coverage. ~90 minutes. No production change.

**Ladder move:** independent_confirmation → internal_experiment (PR #19 expansion) → measured_improvement (PR #19 merged with complete METR-mapped checklist)

**Recommendation: Run.** Directly unblocks PKOS PR #19 merge. 90-minute document mapping — fast, zero-risk, actionable this sprint.

---

## Rank 2 — Meta Muse Code: CI Sprint Alternative to Claude Code

**Capability/Tool:** Meta Superintelligence Labs Muse Code terminal coding agent (Muse Spark 1.2); parallel sub-agents; crash-safe event log; worktree isolation; ~$1.25/$4.25 per million tokens  
**Primary source:** https://developer.meta.com/ai/models/muse-spark/ | https://research.meta.ai/  

**Estimated effort:** 30 minutes (one CI ticket)  
**Expected payoff:** High  
**Stack impact:** Repository maintenance (biotech-screener PRs #524–#530, hermes-agent); CI RED remediation  
**Evidence quality:** High — Meta AI Research announcement (Aug 5) + developer.meta.com model card; VentureBeat/Carl Franzen, Yahoo Finance/Lena Park, eesel AI independently confirm.

**Similar tools already tested:** Codex Security CLI (Jul 30 ROQ, WAIT). Claude Code is current CI tool. First MSL terminal coding agent; distinct architecture.

**Success metric:** On one biotech-screener CI lint/pytest ticket: PR output quality ≥ Claude Code; token cost ≤ current Claude Code spend.

**Smallest shadow test:** Install Muse Code beta. Run against one open CI failure in Warrenpoobear/biotech-screener. Compare PR quality and token cost vs Claude Code on same ticket.

**Ladder move:** independent_confirmation → internal_experiment (one CI ticket) → measured_improvement

**Recommendation: Run.** Aug 7 = 2-week-post-reset CI failure flag threshold. CI sprint is live. 30-minute parallel test on a single lint ticket costs almost nothing. Crash-safe event log directly addresses Herald all-windows dark failure mode. Time-sensitive: run before Aug 7 sprint review.

---

## Rank 3 — Perplexity Numbat: Pre-Action Agent Security Monitor

**Capability/Tool:** Perplexity Numbat — open-source (Apache 2.0 pending verification) pre-action endpoint security monitor. CEL rule engine; custom YAML rules; synchronous blocking of destructive shell commands before impact; monitor-only default.  
**Primary source:** https://www.opensourceforu.com/2026/07/perplexity-open-sources-numbat-to-secure-local-ai-coding-agents/  

**Estimated effort:** 30 minutes install + 1 week passive monitoring  
**Expected payoff:** High (if verification confirms)  
**Stack impact:** Hermes-agent runtime (WSL2); biotech-screener CI write paths; PKOS vault  
**Evidence quality:** Medium — trade press only; Apache 2.0 and GitHub not yet verified as of Aug 5.

**Similar tools already tested:** None. Pre-action blocking fills a gap no prior ROQ addressed. Pairs with Ranks 1 and 4 in the same governance sprint.

**Success metric:** Apache 2.0 confirmed from GitHub. Monitor-only install on one Hermes session for 7 days. Zero false-positive blocks on legitimate agent actions. Pre-action intercept latency <500ms.

**Smallest shadow test:** Step 1 (5 min): verify Apache 2.0 from Numbat GitHub. If confirmed, install in monitor-only on one Hermes agent session for 1 week.

**Ladder move:** primary_source_found → internal_experiment (monitor-only install) → measured_improvement

**Recommendation: Run.** Verification gap resolves in 5 minutes. If confirmed, install is trivial and governance benefit is immediate given confirmed Anthropic/OpenAI sandbox escape pattern.

---

## Rank 4 — Anthropic Sandbox Escape: Hermes Write-Path Audit

**Capability/Tool:** Agent containment — classifying Hermes agents with combined internet + write-path access  
**Primary source:** https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals  

**Estimated effort:** 2–3 hours (manual checklist across 46-skill registry)  
**Expected payoff:** High  
**Stack impact:** Hermes-agent runtime governance; biotech-screener write paths; PKOS vault; Reliability Gate v1.0  
**Evidence quality:** High — Anthropic official blog (Jul 30), 141,006 eval runs, 3 orgs breached; TechCrunch, BleepingComputer, CyberScoop, SecurityAffairs, The Register confirm. Two-lab pattern (Anthropic + OpenAI/HuggingFace within 2 weeks) = structural threat.

**Similar tools already tested:** Jul 30 ROQ Rank 4 (Kaur taxonomy + CSA CISO) advanced this to sprint planning. This is a direct threat-model audit triggered by confirmed production breach — an escalation, not a duplicate.

**Success metric:** All 46 Hermes skills classified for (a) internet access (b) write-path access (c) both. Combined-access agents documented and either isolated or operator-accepted. Zero undocumented write-capable agents.

**Smallest shadow test:** Read 46-skill registry. Document internet + write access per skill. Cross-reference exec allowlist. Flag combined-access agents. ~2–3 hours. Pure audit.

**Ladder move:** independent_confirmation → internal_experiment (audit complete) → measured_improvement (PR #19 updated with findings)

**Recommendation: Run.** Highest raw ROI (5) this week. Confirmed breach of 3 real production orgs. Run before PR #19 merges. Pair with Rank 1 in same sprint session.

---

## Rank 5 — Microsoft EvoLib: Test-Time Skill Extraction for Hermes

**Capability/Tool:** EvoLib — extracts modular skills and reflective insights from agent inference trajectories into a shared evolving library; no fine-tuning; any black-box API model. Code released Jul 30, 2026.  
**Primary source:** https://www.microsoft.com/en-us/research/blog/evolib-turning-experience-into-evolving-knowledge/  

**Estimated effort:** 2–3 hours (offline post-hoc extraction from one archived session)  
**Expected payoff:** Medium  
**Stack impact:** Hermes skill-layer (automated promotion); PKOS Town-Hermes memory sync  
**Evidence quality:** High — MS Research primary blog + arXiv + live code release; RuntimeWire, WindowsNews.ai, PulseAugur confirm.

**Similar tools already tested:** Self-improving skill handles HOT/WARM/COLD structured capture. EvoLib is additive — automated extraction from raw trajectories.

**Success metric:** Offline extraction on one archived screener session produces ≥3 "modular skills" and ≥2 "reflective insights" matching screener-ops documented best practices.

**Smallest shadow test:** One archived Hermes screener session transcript. Run EvoLib offline extraction. Count skill/insight matches against screener-ops. ~2 hours. No production change.

**Ladder move:** independent_confirmation → internal_experiment → measured_improvement

**Recommendation: Wait.** Gate: CI GREEN and Hermes API restored (offline since Jun 26; 41+ days). Run in September 2026 after infrastructure stabilizes.

---

## Also Considered (Ranked 6–8)

- **#6 — Legacy CoT Prompt Audit** (arXiv 2604.10739): ROI 3. 30-min grep for "think step by step" across 46 skills. Fold into Doc Review Run 28 (Aug 7) as a side task.
- **#7 — Wharton AI Behavioral Observatory** (Mollick/Wharton): ROI 3. Hermes model-upgrade behavioral drift detection. Wait until CI green and v0.19 upgrade scheduled.
- **#8 — Replit Truth Layer / PKOS Canonical Facts Directory**: ROI 3. Wait until PKOS Stage 1 operator actions complete.

---

## Dropped This Week

- AI Kill Switch Act (Lieu/Moran): investment-thesis monitoring, not a process experiment
- OpenAI Astra math proofs: capability signal; not actionable until public release (checkpoint Oct 2026)
- Gary Marcus Astra critique: source correction (Substack, not CACM); calibration reference only
- Anthropic open-weights policy: GOOGL IC memo update; not a process experiment
- Mistral Shieldstral: ROI 3; requires Hermes API + 16GB GPU; post-CI architecture queue
- Cursor cloud agent architecture: read-before-sprint reference, not an experiment
- SALP/Aschenbrenner collapse: Regime Evidence reference for IPS Appendix A
- METR open-research evaluation call: assess post-CI sprint
- Snowflake Cortex AI Gateway: no public preview yet; architecture reference
- Anthropic Claude cryptanalysis (HAWK-256 / AES-128): watch NIST HAWK outcome

---

## Carryover Status

### Jul 30 ROQ — 14-day dedup expires Aug 13:

| Item | Prior Rank | Status |
|------|-----------|--------|
| Context Engineering — System Prompt Audit | 1 | Open; expires Aug 13 |
| MCP 2026-07-28 Stateless Migration | 2 | Open; expires Aug 13 |
| DFAH-Bench Financial Agent Stability | 3 | Open; expires Aug 13 |
| Hermes Write-Path Governance (Kaur + CSA) | 4 | Superseded by this week's Rank 4 |
| Cursor Agent Swarm Planner/Worker | 5 | WAIT; gate CI GREEN |

### Jul 23 ROQ — dedup expired; no material change found:
- AGENTS.md governance standard — still open
- Contrastive SDF reward-seeking audit — still open
- METR Expenditure Horizon — still open (distinct from this week's METR item)
- Petri harness shutdown-pressure test — still open
- GPT-Red/Fake-CoT injection test — still open

---

## Self-Check

- Captures reviewed: 7 daily AI digests (Jul 31–Aug 6, 2026); ~540 items scanned
- Candidates qualified: 8; Top-5 delivered (4 Run / 1 Wait)
- Dedup: all items verified against Jul 23 and Jul 30 ROQ ledger memories
- Deliverables: Content Library ✓ | GitHub ✓ | Decision Impact Ledger (5 rows) | Emails to dschulz@wakerobin.co and djschulz@gmail.com
- Schema: v1.0 (cols A–Z), no structural changes
