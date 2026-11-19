# Research Opportunity Queue — week of 2026-11-19

**Run date:** Thursday, November 19, 2026
**Routine:** X Intelligence — Weekly Research Opportunity Queue
**Governance:** DIAGNOSTIC_ONLY / NO_MODEL_CHANGE / NO_AUTOMATIC_SCORE_WRITE
**Captures reviewed:** 8 daily AI digests (2026-11-12 through 2026-11-19), meeting the 3-digest minimum. All 8 were dispositioned "no qualifying item" (novelty none, ROI 1). X API unavailable; web sources used. Prior ROQs read: 2026-11-12 (full), 2026-08-13 (full), 2026-08-06 (size/structure only).
**Candidates qualified:** 5 (5 filled Top-5; 1 additional item held, not re-ranked). Another thin week: the digests surfaced no new qualifying item, so the queue is carryover plus re-verification of primary sources.

---

## Top-5 Ranked Experiments

| Rank | Title | Effort | Evidence | ROI | Composite | Rec |
|------|-------|--------|----------|-----|-----------|-----|
| 1 | Codex CLI 0.167.0 "Agent Command Center" — Observability Mapping | 30 min | High | 2 | 12.0 | **Run** |
| 2 | Green Street GreenStreetAI MCP Server — CRE Underwriting Pilot (carryover) | ~1 hr (contingent) | High | 4 | 12.0 | **Wait** |
| 3 | METR Review of Anthropic Risk Report "Automated R&D" Section (Nov 5) — Read-and-Map | 30 min | Medium | 2 | 8.0 | **Run** |
| 4 | NVIDIA Nemotron 3.5 / NeMo Switchyard Cost-Aware Routing (carryover) | ~2 hrs | Medium | 3 | 3.0 | **Wait** |
| 5 | Canary Susceptibility Rate (CSR) Harness (carryover) | ~2 hrs | Low | 4 | 2.0 | **Wait** |

*Composite = (Expected ROI x Evidence score [High=3/Med=2/Low=1]) / Effort in hours. Ties broken toward items advancing a named bottleneck (EDGAR/PDF parsing, catalyst monitoring, entity resolution, memo drafting, benchmarking; agent governance/observability). Rank 1 vs 2 tie (12.0) broken toward agent-governance/observability and because Rank 1 is runnable now while Rank 2 is blocked on access. High evidence was given only where the primary source was fetched this run (Codex release, Green Street press release).*

---

## Rank 1 — Codex CLI 0.167.0 "Agent Command Center": Observability Mapping

**Capability/Tool:** OpenAI Codex CLI 0.167.0 (stable, rust-v0.167.0): `codex agents --no-daemon` agent command center that flags agents with unread results; backend switching from the session picker without losing drafts.
**Primary source:** https://github.com/openai/codex/releases/tag/rust-v0.167.0 — **fetched and resolves this run**; page shows release date "06 Nov" (day/month only) and confirms the command-center and backend-switching notes. Upgrades the 2026-11-12 ROQ rating (secondary sources only).

**Estimated effort:** 30 minutes
**Expected payoff:** Low-Medium
**Stack impact:** hermes-agent multi-agent visibility / heartbeat design (agent-status surfacing)
**Evidence quality:** High for existence and the quoted features (vendor release page). Payoff for Hermes remains an assumption.

**Similar tools already tested:** None. Carried from 2026-11-12 Rank 1 (Run); no completion record exists in the files reviewed, so this ROQ makes no claim that it was done.

**Success metric:** One-page mapping of each command-center signal (unread-result marking, per-agent status) to an existing Hermes artifact (`agents_list(include_heartbeat=true)` fields). Pass = every signal has a Hermes equivalent or an explicit "no equivalent" note.

**Smallest shadow test:** Read the full rust-v0.167.0 notes and write the mapping note. Read-only; no install, no config change, no new lane.

**Ladder move:** primary_source_found -> internal_experiment (mapping note)

**Recommendation: Run.** Cheapest item, reading-only, and the primary source is now verified. Nothing is adopted.

---

## Rank 2 — Green Street GreenStreetAI MCP Server: CRE Underwriting Pilot (carryover)

**Capability/Tool:** Green Street MCP Server (GreenStreetAI) connecting Green Street research/data to corporate instances of Claude, ChatGPT and Gemini; tools cover Research, Company Data, Sector Data, Market Data, Market Forecast, Sales Comps and single-property AVM.
**Primary source:** Green Street press release, Aug 11 2026 (https://www.prnewswire.com/news-releases/green-street-launches-its-mcp-server-powered-by-greenstreetai-connecting-cre-intelligence-directly-to-corporate-instances-of-claude-chatgpt-gemini-and-other-ai-platforms-302848322.html) — **fetched and resolves this run.** The release is promotional; its efficiency claims are the company's own and unverified.

**Estimated effort:** ~1 hour (contingent on subscription/trial access)
**Expected payoff:** High, if access exists
**Stack impact:** real-estate-intel skill (Wake Robin multifamily / 55+ underwriting); comp monitoring
**Evidence quality:** High for the release and its scope; no independent output-quality review found, so payoff is unproven.

**Similar tools already tested:** None. Same item as 2026-11-12 Rank 2 and 2026-08-13 Rank 4 (Wait). No new evidence this week beyond source re-verification.

**Success metric:** Re-run one underwriting question already answered manually this quarter through the MCP-connected instance; compare accuracy and citation quality.

**Smallest shadow test:** Confirm subscription/trial access; if available, connect and re-run one already-answered question. Read-only queries.

**Ladder move:** primary_source_found -> internal_experiment -> measured_improvement

**Recommendation: Wait.** Blocker is access, not evidence; unchanged.

---

## Rank 3 — METR Review of Anthropic's Risk Report "Automated R&D" Section (Nov 5): Read-and-Map

**Capability/Tool:** METR post "Review of the 'Risks from automated R&D' section in Anthropic's Risk Report (August 2026)", dated 2026-11-05. **Correction to the 2026-11-12 ROQ:** that ROQ ranked a METR "Is AI Accelerating AI Development?" report as unverified. The Nov 5 METR item that exists on metr.org is this review; this ROQ replaces the earlier unverified title with it and does not confirm the "~2x pace" claim from that ROQ.
**Primary source:** https://metr.org/blog/2026-11-05-rd-section-anthropic-risk-report-august-2026-review/ — listed on the metr.org blog index fetched this run (title and date confirmed; the post body was **not read**).

**Estimated effort:** 30 minutes
**Expected payoff:** Low-Medium (context for capability-trend and agent-governance assumptions; no direct tool)
**Stack impact:** none direct; informs benchmarking and agent-governance assumptions
**Evidence quality:** Medium — primary index entry confirmed, content not yet read.

**Similar tools already tested:** METR Reliability Gate checklist (2026-08-06) and METR Expenditure Horizon (2026-07-23) are different METR outputs.

**Success metric:** 5-line note extracting METR's main findings and caveats on the R&D-acceleration section, with the quantitative claims quoted exactly.

**Smallest shadow test:** Read the post and write the note. Read-only.

**Ladder move:** primary_source_found -> internal_experiment (reading note)

**Recommendation: Run.** Primary source now resolves; reading-only, 30 minutes.

---

## Rank 4 — NVIDIA Nemotron 3.5 / NeMo Switchyard Cost-Aware Routing (carryover)

**Capability/Tool:** Cost-aware escalation routing (~70-75% cost reduction at mid-single-digit accuracy cost per implementer benchmarks).
**Primary source:** As cited in the 2026-08-13 ROQ (Also Considered #10); **not re-fetched this run**.

**Estimated effort:** ~2 hours
**Expected payoff:** Medium
**Stack impact:** hermes-agent multi-model routing (cost baseline)
**Evidence quality:** Medium — implementer benchmarks from interested parties; not re-verified.

**Similar tools already tested:** None.

**Success metric:** Replay one logged set of routed calls offline through the published routing policy; compare projected vs actual cost.

**Smallest shadow test:** Offline replay of logged calls only; no routing change.

**Ladder move:** independent_confirmation -> internal_experiment

**Recommendation: Wait.** No new evidence in 8 digests; source unverified.

---

## Rank 5 — Canary Susceptibility Rate (CSR) Harness (carryover)

**Capability/Tool:** Tool-selection reliability evaluation harness (Anand & Chattaraj; 36x model variance claimed).
**Primary source:** Not located as of 2026-08-13; no targeted search was made this run.

**Estimated effort:** ~2 hours
**Expected payoff:** High (targets the benchmarking bottleneck)
**Stack impact:** benchmarking
**Evidence quality:** Low — secondary coverage only.

**Similar tools already tested:** None.

**Success metric:** Primary paper located, then one tool-selection eval reproduced on a toy set.

**Smallest shadow test:** Search arXiv/SSRN for the paper; stop if absent. Read-only.

**Ladder move:** unverified_lead -> primary_source_found

**Recommendation: Wait.** Strong bottleneck fit; blocked on source verification.

---

## Also Considered / Held (not ranked)

- **Claude Code changelog 2.1.317–2.1.323 (sandbox escape fix, MCP OAuth redirect secrets fix, read-only Bash sandbox fix)** — **Held, not re-ranked.** Hold until 2026-11-25 per the 2026-11-11 digest unless an advisory/CVE appears; none was reported in the 8 digests. The related read-only version inventory remains the relevant diagnostic. Re-elevate on/after 2026-11-25.
- **METR "Red-Teaming OpenAI's Internal Agent Monitoring Systems" (Oct 22)** — title/date confirmed on the metr.org index this run; post not read. Relevant to agent-governance observability; not ranked this week (older than the window, no stack tie established). Candidate for a future read-and-map.
- **Aggregator-only leads from digests (DeepSeek coding agent / Pi 1.5.0, GPT-6 Cyber restricted release, Google ADK 2.14.0, AlphaProof CodeAgentic, Cursor/OpenAI supply cutoff)** — no primary source found; not qualified.

---

## Dropped This Week

- **Unfilled prior-ROQ Run items (Semgrep scan, C2PA provenance, encrypted-CoT routing test, Agent Plugins 1.0.0 manifest mapping)** — not re-ranked; no record of completion exists in the files reviewed, so no claim is made either way. The operator can re-surface any of them.

---

## Carryover Status

- 2026-11-12 items re-ranked: Codex (Rank 1, evidence upgraded to High), Green Street (Rank 2, evidence upgraded to High), METR (Rank 3, retitled/corrected, evidence upgraded to Medium), Nemotron (Rank 4), CSR (Rank 5). Their hold windows had no stated expiry beyond "Wait"; status otherwise unchanged.
- Claude Code changelog items remain on hold until 2026-11-25.

---

## Self-Check

- Captures reviewed: 8 daily AI digests (2026-11-12 to 2026-11-19); all "no qualifying item".
- Primary sources verified this run (WebFetch): Codex rust-v0.167.0 release page; Green Street press release; metr.org blog index. Not verified: Nemotron/Switchyard, CSR, METR post body.
- Candidates qualified: 5 (2 High-evidence; 2 Run / 3 Wait)
- All shadow tests are read-only/diagnostic; no production change, cron, lane, model or score change; nothing was adopted.
- Deliverables: this file only.
