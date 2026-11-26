# Research Opportunity Queue — week of 2026-11-26

**Run date:** Thursday, November 26, 2026
**Routine:** X Intelligence — Weekly Research Opportunity Queue
**Governance:** DIAGNOSTIC_ONLY / NO_MODEL_CHANGE / NO_AUTOMATIC_SCORE_WRITE
**Captures reviewed:** 8 daily AI digests (2026-11-19 through 2026-11-26), meeting the 3-digest minimum. 7 were dispositioned "no qualifying item" (novelty none, ROI 1); 1 (2026-11-25, METR pretraining-loss post) was filed to backlog with a hold until 2026-12-09. X API unavailable; web sources used. Prior ROQs read: 2026-11-19 (full), 2026-11-12 (full).
**Candidates qualified:** 5 (5 filled Top-5; 2 additional items held/not re-ranked). Another thin week: no new qualifying item in the digests, so the queue is carryover plus re-verification of primary sources. One evidence upgrade (CSR paper located).

---

## Top-5 Ranked Experiments

| Rank | Title | Effort | Evidence | ROI | Composite | Rec |
|------|-------|--------|----------|-----|-----------|-----|
| 1 | Codex CLI 0.167.0 "Agent Command Center" — Observability Mapping (carryover) | 30 min | High | 2 | 12.0 | **Run** |
| 2 | METR Review of Anthropic Risk Report "Automated R&D" Section (Nov 5) — Read-and-Map (carryover) | 30 min | High | 2 | 12.0 | **Run** |
| 3 | Green Street GreenStreetAI MCP Server — CRE Underwriting Pilot (carryover) | ~1 hr (contingent) | High | 4 | 12.0 | **Wait** |
| 4 | Canary Susceptibility Rate (CSR) / Canary Tools — Paper Read-and-Verify (carryover, source now found) | ~2 hrs | High | 4 | 6.0 | **Run** |
| 5 | NVIDIA Nemotron 3.5 / NeMo Switchyard Cost-Aware Routing (carryover) | ~2 hrs | Medium | 3 | 3.0 | **Wait** |

*Composite = (Expected ROI x Evidence score [High=3/Med=2/Low=1]) / Effort in hours. Ties broken toward items advancing a named bottleneck (EDGAR/PDF parsing, catalyst monitoring, entity resolution, memo drafting, benchmarking; agent governance/observability). Ranks 1-3 tie at 12.0: Codex and METR are runnable now and advance agent governance/observability; Green Street is blocked on access. Codex ranked above METR because its mapping targets an existing Hermes artifact. High evidence was given only where the primary source was fetched this run (Codex release, METR post, Green Street release, arXiv abstract).*

---

## Rank 1 — Codex CLI 0.167.0 "Agent Command Center": Observability Mapping (carryover)

**Capability/Tool:** OpenAI Codex CLI 0.167.0 (rust-v0.167.0): `codex agents --no-daemon` opens an agent command center; it and the session picker flag unread results; backend switching from the session picker keeps drafts.
**Primary source:** https://github.com/openai/codex/releases/tag/rust-v0.167.0 — **fetched this run**; page partially loaded (some sections showed GitHub load errors) but the release notes, "06 Nov" date, command-center and backend-switching notes were readable.

**Estimated effort:** 30 minutes
**Expected payoff:** Low-Medium
**Stack impact:** hermes-agent multi-agent visibility / heartbeat design (agent-status surfacing)
**Evidence quality:** High for existence and the quoted features (vendor release page). Payoff for Hermes remains an assumption.

**Similar tools already tested:** None. Carried from 2026-11-12 and 2026-11-19 (Run); no completion record exists in the files reviewed, so this ROQ makes no claim that it was done.

**Success metric:** One-page mapping of each command-center signal (unread-result marking, per-agent status) to an existing Hermes artifact (`agents_list(include_heartbeat=true)` fields). Pass = every signal has a Hermes equivalent or an explicit "no equivalent" note.

**Smallest shadow test:** Read the full rust-v0.167.0 notes and write the mapping note. Read-only; no install, no config change, no new lane.

**Ladder move:** primary_source_found -> internal_experiment (mapping note)

**Recommendation: Run.** Cheapest item, reading-only, source verified. Nothing is adopted.

---

## Rank 2 — METR Review of Anthropic's Risk Report "Automated R&D" Section (Nov 5): Read-and-Map (carryover)

**Capability/Tool:** METR post "Review of the 'Risks from automated R&D' section in Anthropic's Risk Report (August 2026)", 2026-11-05.
**Primary source:** https://metr.org/blog/2026-11-05-rd-section-anthropic-risk-report-august-2026-review/ — **fetched and read this run** (upgrade from index-only last week). Points the fetch summary surfaced, to be quoted exactly from the post when the note is written: METR says it is "plausible that they had crossed their early warning threshold"; Anthropic's public report says acceleration "by less than a factor of 2" while METR computes 1.97 from the private report with an estimated range of "between 1.3 and 2.8"; METR cites "around 1.5x" (original data) and "1.9x" (with more benchmarks) for AECI acceleration; METR "cannot rule out a substantial further acceleration in the pace of capabilities progress over the next 6 months." Caveats noted by METR: Anthropic had redaction rights and review scope was negotiated.

**Estimated effort:** 30 minutes
**Expected payoff:** Low-Medium (context for capability-trend and agent-governance assumptions; no direct tool)
**Stack impact:** none direct; informs benchmarking and agent-governance assumptions
**Evidence quality:** High — primary post fetched and read via fetch summary (not independently line-checked).

**Similar tools already tested:** METR Reliability Gate checklist (2026-08-06) and METR Expenditure Horizon (2026-07-23) are different METR outputs. The 2026-11-24 METR pretraining-loss post is a separate item on hold until 2026-12-09 (not re-ranked here).

**Success metric:** 5-line note extracting METR's main findings and caveats, with quantitative claims quoted exactly from the post text.

**Smallest shadow test:** Re-read the post and write the note. Read-only.

**Ladder move:** primary_source_found -> internal_experiment (reading note)

**Recommendation: Run.** Reading-only, 30 minutes.

---

## Rank 3 — Green Street GreenStreetAI MCP Server: CRE Underwriting Pilot (carryover)

**Capability/Tool:** Green Street MCP Server (GreenStreetAI) connecting Green Street research/data to corporate instances of Claude, ChatGPT and Gemini (Research, Company Data, Sector Data, Market Data, Market Forecast, Sales Comps, single-property AVM).
**Primary source:** Green Street press release, Aug 11 2026 (https://www.prnewswire.com/news-releases/green-street-launches-its-mcp-server-powered-by-greenstreetai-connecting-cre-intelligence-directly-to-corporate-instances-of-claude-chatgpt-gemini-and-other-ai-platforms-302848322.html) — **fetched and resolves this run** (dated Aug 11, 2026). Promotional; efficiency claims are the company's own and unverified.

**Estimated effort:** ~1 hour (contingent on subscription/trial access)
**Expected payoff:** High, if access exists
**Stack impact:** real-estate-intel skill (Wake Robin multifamily / 55+ underwriting); comp monitoring
**Evidence quality:** High for the release and its scope; no independent output-quality review found, so payoff is unproven.

**Similar tools already tested:** None. Same item as 2026-11-19 Rank 2, 2026-11-12 Rank 2, 2026-08-13 Rank 4 (Wait).

**Success metric:** Re-run one underwriting question already answered manually this quarter through the MCP-connected instance; compare accuracy and citation quality.

**Smallest shadow test:** Confirm subscription/trial access; if available, connect and re-run one already-answered question. Read-only queries.

**Ladder move:** primary_source_found -> internal_experiment -> measured_improvement

**Recommendation: Wait.** Blocker is access, not evidence; unchanged.

---

## Rank 4 — Canary Tools / Canary Susceptibility Rate (CSR): Paper Read-and-Verify (carryover, source now found)

**Capability/Tool:** "Diagnosing Tool-Selection Reasoning in LLM Agents with Canary Tools" (Atul Anand, Sourav Chattaraj): diagnostic "canary" probe tools planted in an agent's tool set, six-type taxonomy of tool-selection weaknesses; CSR = share of tool calls landing on canary tools. Abstract: eight models, 120 tasks; susceptibility drops as capability rises but tier is not a reliable guide; softening probe phrasing leaves frontier-model results nearly unchanged.
**Primary source:** https://arxiv.org/abs/2608.04719 (submitted Aug 5, 2026) — **fetched and resolves this run; abstract confirmed.** **Correction to prior ROQs:** earlier ROQs listed the source as "not located"; it is located now. The "36x model variance" figure and per-model CSR numbers appear only in secondary write-ups, differ between them, and were **not confirmed** against the paper text; do not cite them until the paper is read.

**Estimated effort:** ~2 hours (read paper, check figures; no harness build)
**Expected payoff:** High (targets the benchmarking bottleneck; relevant to MCP tool-selection reliability)
**Stack impact:** benchmarking; MCP tool-set design review
**Evidence quality:** High for existence and abstract; secondary-only for headline numbers.

**Similar tools already tested:** None. Carried from 2026-11-12/2026-11-19 (Rank 5, Wait; evidence Low).

**Success metric:** Note recording the paper's actual CSR definition, per-model figures and limitations, and whether the 36x claim holds; plus a paper-only assessment of whether the probe design could be replayed on a logged Hermes tool-call transcript.

**Smallest shadow test:** Read the paper; if it provides probe definitions, dry-run them offline against an already-logged transcript only. No tools are added to any live agent, no harness is deployed.

**Ladder move:** primary_source_found -> independent_confirmation (paper read) -> internal_experiment (offline transcript replay)

**Recommendation: Run (paper read only).** The earlier blocker (source verification) is cleared; the offline replay step is optional and gated on what the paper provides.

---

## Rank 5 — NVIDIA Nemotron 3.5 / NeMo Switchyard Cost-Aware Routing (carryover)

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

## Also Considered / Held (not ranked)

- **METR "Interpreting a recent acceleration in pretraining loss" (2026-11-24)** — **Held, not re-ranked.** Filed in the 2026-11-25 digest with a hold until 2026-12-09 unless OpenAI's source post or a third-party replication is reviewed; neither surfaced. The related read-only eval re-baseline staleness listing (model IDs and last re-baseline dates) remains the relevant diagnostic.
- **Claude Code changelog 2.1.317–2.1.326 (sandbox/MCP OAuth fixes)** — the hold expired 2026-11-25. No advisory/CVE appeared in the 2026-11-19–26 digests, and official changelogs were not checked this run, so it is **not ranked**. The read-only version inventory is the diagnostic if the operator wants to re-elevate.
- **METR "Red-Teaming OpenAI's Internal Agent Monitoring Systems" (Oct 22)** — title/date seen on the metr.org index per digests; not read; no stack tie established. Candidate for a future read-and-map.
- **Aggregator-only leads (DeepSeek coding agent / Pi 1.5.0, GPT-6 Cyber restricted release, Google ADK 2.14.0, Codex CLI untrusted-directory config change, SWE-CI arXiv 2603.03823 background)** — no primary source confirmed this run; not qualified.

---

## Dropped This Week

- **Unfilled prior-ROQ Run items (Semgrep scan, C2PA provenance, encrypted-CoT routing test, Agent Plugins 1.0.0 manifest mapping)** — not re-ranked; no record of completion exists in the files reviewed, so no claim is made either way.

---

## Carryover Status

- 2026-11-19 items re-ranked: Codex (Rank 1), METR (Rank 2, evidence upgraded Medium -> High after reading the post), Green Street (Rank 3), CSR (Rank 4, source located, evidence upgraded Low -> High for existence, Wait -> Run for the paper read), Nemotron (Rank 5).
- METR pretraining-loss item remains on hold until 2026-12-09.

---

## Self-Check

- Captures reviewed: 8 daily AI digests (2026-11-19 to 2026-11-26); 7 "no qualifying item", 1 held backlog item.
- Primary sources verified this run (WebFetch): Codex rust-v0.167.0 release page (partial load); METR 2026-11-05 post; Green Street press release; arXiv 2608.04719 abstract. Not verified: Nemotron/Switchyard, CSR headline figures, Claude Code official changelogs.
- Candidates qualified: 5 (4 High-evidence; 3 Run / 2 Wait)
- All shadow tests are read-only/diagnostic; no production change, cron, lane, model or score change; nothing was adopted.
- Deliverables: this file only.
