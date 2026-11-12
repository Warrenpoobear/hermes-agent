# Research Opportunity Queue — week of 2026-11-12

**Run date:** Thursday, November 12, 2026
**Routine:** X Intelligence — Weekly Research Opportunity Queue
**Governance:** DIAGNOSTIC_ONLY / NO_MODEL_CHANGE / NO_AUTOMATIC_SCORE_WRITE
**Captures reviewed:** 2 daily AI digests (2026-11-11, 2026-11-12) — fewer than the 3 required; queue built from these plus targeted WebSearch/WebFetch confirmation. X API unavailable; web sources used. No digests exist in the repo between 2026-08-31 and 2026-11-11, and the last ROQ is 2026-08-13 (a ~13-week gap).
**Candidates qualified:** 5 (5 filled Top-5; 1 additional item held, not re-ranked). This is a thin week: both digests were low-yield, and 2 of the 5 slots are carryover Wait items from the 2026-08-13 ROQ.

---

## Top-5 Ranked Experiments

| Rank | Title | Effort | Evidence | ROI | Composite | Rec |
|------|-------|--------|----------|-----|-----------|-----|
| 1 | Codex CLI 0.167.0 "Agent Command Center" — Observability Mapping | 30 min | Medium | 2 | 8.0 | **Run** |
| 2 | Green Street GreenStreetAI MCP Server — CRE Underwriting Pilot (carryover) | ~1 hr (contingent) | Medium | 4 | 8.0 | **Wait** |
| 3 | METR "Is AI Accelerating AI Development?" Report (Nov 5) — Read-and-Map | 30 min | Low | 2 | 4.0 | **Wait** |
| 4 | NVIDIA Nemotron 3.5 / NeMo Switchyard Cost-Aware Routing (carryover) | ~2 hrs | Medium | 3 | 3.0 | **Wait** |
| 5 | Canary Susceptibility Rate (CSR) Harness (carryover) | ~2 hrs | Low | 4 | 2.0 | **Wait** |

*Composite = (Expected ROI x Evidence score [High=3/Med=2/Low=1]) / Effort in hours. Ties broken toward items advancing a named bottleneck (EDGAR/PDF parsing, catalyst monitoring, entity resolution, memo drafting, benchmarking). Rank 1 vs 2 tie broken toward agent-governance/observability. No item received High evidence this run: carryover primary sources were not re-fetched this run (the 2026-08 URLs were not re-verified), and the new items rest on secondary or unverified sources.*

---

## Rank 1 — Codex CLI 0.167.0 "Agent Command Center": Observability Mapping

**Capability/Tool:** OpenAI Codex CLI 0.167.0 (stable, GitHub tag rust-v0.167.0, published ~Nov 6 2026): `codex agents --no-daemon` agent command center marking agents with unread results; backend switching in the session picker without losing drafts; Vertex AI setup wizard; opt-in system proxy.
**Primary source:** GitHub release rust-v0.167.0 (openai/codex) — **not directly fetched**; the release is described by secondary sources only: https://codex.danielvaughan.com/2026/11/06/codex-v0167-stable-agent-command-center-multi-backend-image-attachments-gcp-vertex/ and https://ai-tldr.dev/releases/openai-codex-cli-0-167/ (dates differ Nov 5 vs Nov 6).

**Estimated effort:** 30 minutes
**Expected payoff:** Low-Medium
**Stack impact:** hermes-agent multi-agent visibility / heartbeat design (agent-status surfacing); CI-remediation agent tooling comparison
**Evidence quality:** Medium — multiple summary sites agree on features, but the canonical GitHub release was not fetched and the 2026-11-12 digest flagged this only as an aggregator lead. Not High until the release page is read.

**Similar tools already tested:** None directly. Related by theme to the 2026-08-06 ROQ Rank 2 (Meta Muse Code CI alternative) as a competing coding-agent surface, but this is a UI/observability feature, not a CI-quality comparison.

**Success metric:** Written one-page mapping of each command-center signal (unread-result marking, per-agent status) to an existing Hermes artifact (`agents_list(include_heartbeat=true)` fields). Pass = every signal has a Hermes equivalent or an explicit "no equivalent" note.

**Smallest shadow test:** Fetch the rust-v0.167.0 release notes, read them, and write the mapping note. Read-only, no install, no config change, no new lane.

**Ladder move:** secondary_sources_only -> primary_source_found (fetch GitHub release) -> internal_experiment (mapping note)

**Recommendation: Run.** Cheapest item this week, reading-only, and the first step doubles as the primary-source verification the evidence rating needs. Low payoff expected; nothing is adopted.

---

## Rank 2 — Green Street GreenStreetAI MCP Server: CRE Underwriting Pilot (carryover)

**Capability/Tool:** Green Street MCP Server (GreenStreetAI) connecting CRE market intelligence to Claude/ChatGPT/Gemini for market underwriting and REIT benchmarking.
**Primary source:** Green Street press release, Aug 11 2026 (https://www.prnewswire.com/news-releases/green-street-launches-its-mcp-server-powered-by-greenstreetai-connecting-cre-intelligence-directly-to-corporate-instances-of-claude-chatgpt-gemini-and-other-ai-platforms-302848322.html) — carried from the 2026-08-13 ROQ; **not re-fetched this run**.

**Estimated effort:** ~1 hour (contingent on subscription/trial access)
**Expected payoff:** High, if access exists
**Stack impact:** real-estate-intel skill (Wake Robin multifamily / 55+ underwriting); comp monitoring
**Evidence quality:** Medium — previously High for the release itself, downgraded this run because the source was not re-verified and no independent output-quality review was found.

**Similar tools already tested:** None. Same item as 2026-08-13 Rank 4 (Wait); no new evidence surfaced this week. Hold window from that ROQ has expired, so it is re-ranked, but without a change in status.

**Success metric:** Re-run one underwriting question already answered manually this quarter through the MCP-connected instance; compare accuracy and citation quality.

**Smallest shadow test:** Confirm subscription/trial access; if available, connect and re-run one already-answered question. Read-only queries.

**Ladder move:** primary_source_found -> internal_experiment -> measured_improvement

**Recommendation: Wait.** Blocker is access, not evidence; unchanged since Aug 13.

---

## Rank 3 — METR "Is AI Accelerating AI Development?" (Nov 5): Read-and-Map

**Capability/Tool:** METR report (reported Nov 5 2026) concluding capability growth on well-specified tasks is likely ~2x the Mar 2024–Oct 2025 pace as of Oct 2026, with Anthropic redacting much of the evidence in the public version.
**Primary source:** **Not verified.** A WebSearch summary described the report, but a WebFetch of https://metr.org/research listed nothing newer than Aug 26 2026 and no Nov 5 item. The 2026-11-12 digest also listed METR studies as an unconfirmed aggregator lead (fourweekmba.com returned 403).

**Estimated effort:** 30 minutes
**Expected payoff:** Low-Medium (context for capability-trend assumptions; no direct tool)
**Stack impact:** none direct; informs the benchmarking bottleneck and IPS capability-trend assumptions
**Evidence quality:** Low — no primary source resolved.

**Similar tools already tested:** METR Reliability Gate checklist (2026-08-06 Rank 1) and METR Expenditure Horizon (2026-07-23) are different METR outputs; this is a trend report, not an evaluation framework.

**Success metric:** Locate the primary report URL; extract its quantitative claim and caveats into a 5-line note.

**Smallest shadow test:** Locate the report on metr.org or via METR's channels; if it cannot be found, record "unverified" and drop. Read-only.

**Ladder move:** unverified_lead -> primary_source_found

**Recommendation: Wait.** Do not act until a primary source is located.

---

## Rank 4 — NVIDIA Nemotron 3.5 / NeMo Switchyard Cost-Aware Routing (carryover)

**Capability/Tool:** Cost-aware escalation routing (~70-75% cost reduction at mid-single-digit accuracy cost per implementer benchmarks).
**Primary source:** As cited in the 2026-08-13 ROQ (Also Considered #10); **not re-fetched this run**.

**Estimated effort:** ~2 hours
**Expected payoff:** Medium
**Stack impact:** hermes-agent multi-model routing (cost baseline)
**Evidence quality:** Medium — implementer benchmarks from interested parties; not re-verified.

**Similar tools already tested:** None.

**Success metric:** Replay one logged set of routed calls offline through the published routing policy and compare projected cost vs actual.

**Smallest shadow test:** Offline replay of logged calls only; no routing change.

**Ladder move:** independent_confirmation -> internal_experiment

**Recommendation: Wait.** No new evidence this week; remains gated by prior disposition.

---

## Rank 5 — Canary Susceptibility Rate (CSR) Harness (carryover)

**Capability/Tool:** Tool-selection reliability evaluation harness (Anand & Chattaraj; 36x model variance claimed).
**Primary source:** Not located as of 2026-08-13; **no new primary source found this run** (no targeted search was made for it).

**Estimated effort:** ~2 hours
**Expected payoff:** High (targets the named benchmarking bottleneck)
**Stack impact:** benchmarking
**Evidence quality:** Low — secondary coverage only.

**Similar tools already tested:** None.

**Success metric:** Primary paper located, then one tool-selection eval reproduced on a toy set.

**Smallest shadow test:** Search arXiv/SSRN for the paper; stop if absent. Read-only.

**Ladder move:** unverified_lead -> primary_source_found

**Recommendation: Wait.** Strong bottleneck fit; blocked on source verification.

---

## Also Considered / Held (not ranked)

- **Claude Code changelog 2.1.317–2.1.322 (sandbox escape fix in 2.1.319; MCP OAuth redirect secrets fix, read-only Bash sandbox fix, mods changes in 2.1.321)** — **Held, not re-ranked.** The 2026-11-11 and 2026-11-12 digests set a hold until 2026-11-25 unless an advisory/CVE is published or an internal version inventory is run. This run re-fetched the vendor changelog and confirmed the wording: newest entry 2.1.322 (Nov 10); 2.1.319 "Fixed a sandbox escape when creating a worktree"; 2.1.321 fixes for MCP OAuth redirect secrets and a read-only Bash command running outside the sandbox. Only the first ~100k of ~1.2M characters were read. Mods wording was only partly confirmed (listed under "Changed" in 2.1.321, not as a bug fix, so the 11-11 digest's phrasing was imprecise). No advisory was located. Re-elevate on/after 2026-11-25.
- **DeepSeek coding agent / Pi 1.5.0** — single-source/aggregator only per 2026-11-11 digest; not qualified.

---

## Dropped This Week

- **Unfilled prior-ROQ Run items (Semgrep scan, C2PA provenance, encrypted-CoT routing test, Agent Plugins 1.0.0 manifest mapping)** — not re-ranked; no record of their completion or status exists in the files reviewed, so this ROQ makes no claim either way. The operator can re-surface any of them.

---

## Carryover Status

- 2026-08-13 Wait items re-ranked above: Green Street (Rank 2), Nemotron/Switchyard (Rank 4), CSR (Rank 5). Hold windows have expired; status unchanged.
- Claude Code changelog items from 2026-11-11/12 remain on hold until 2026-11-25.

---

## Self-Check

- Captures reviewed: 2 daily AI digests (2026-11-11, 2026-11-12) — below the 3-digest minimum, stated in header. Prior ROQs read: 2026-08-13 (full), 2026-08-06 and 2026-07-30 (head).
- Primary sources verified this run: Claude Code changelog (WebFetch, partial read). Not verified: Codex GitHub release, METR Nov 5 report (not found on metr.org), all carryover URLs.
- Candidates qualified: 5 (0 High-evidence; 1 Run / 4 Wait)
- All shadow tests are read-only/diagnostic; no production change, cron, lane, model or score change; nothing was adopted.
- Deliverables: this file only.
