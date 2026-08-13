# Research Opportunity Queue — week of 2026-08-13

**Run date:** Thursday, August 13, 2026 | 16:00 ET
**Routine:** X Intelligence — Weekly Research Opportunity Queue
**Governance:** DIAGNOSTIC_ONLY / NO_MODEL_CHANGE / NO_AUTOMATIC_SCORE_WRITE
**Captures reviewed:** 7 daily AI digests (2026-08-06 through 2026-08-13); ~400 items scanned across the week (X quota capped Aug 11-13; web-search fallback used).
**Candidates qualified:** 13 (5 filled Top-5, 7 held as also-considered)

---

## Top-5 Ranked Experiments

| Rank | Title | Effort | Evidence | ROI | Composite | Rec |
|------|-------|--------|----------|-----|-----------|-----|
| 1 | Semgrep + Replit — Generation-Time SAST/Secrets Scan on Agent Commits | 30 min | High | 4 | 24.0 | **Run** |
| 2 | Anthropic C2PA Provenance Metadata — Document-Lineage Test | 30 min | High | 3 | 18.0 | **Run** |
| 3 | Encrypted CoT Reasoning-Trace Extraction Attack — Hermes Routing-Tier Test | ~1 hr | High | 5 | 15.0 | **Run** |
| 4 | Green Street GreenStreetAI MCP Server — CRE Underwriting Pilot | ~1 hr (contingent) | High | 4 | 12.0 | **Wait** |
| 5 | Agent Plugins 1.0.0 — Skill-Packaging Portability Test | 1-2 hrs | High | 4 | 8.0 | **Run** |

*Composite = (Expected ROI x Evidence score [High=3/Med=2/Low=1]) / Effort in hours. Ties broken toward items advancing a named bottleneck (EDGAR/PDF parsing, catalyst monitoring, entity resolution, memo drafting, benchmarking).*

---

## Rank 1 — Semgrep + Replit: Generation-Time SAST/Secrets Scan on Agent Commits

**Capability/Tool:** Semgrep Guardian embedded in Replit's Project/Security Center — generation-time (not post-deploy) vulnerability and secret-leak scanning for AI-authored code. Semgrep itself runs standalone via CLI/CI outside Replit.
**Primary source:** Business Wire, Aug 11 2026 (https://www.financialcontent.com/article/bizwire-2026-8-11-semgrep-and-replit-expand-integration-to-keep-pace-with-ai-generated-code-at-scale); independently confirmed by Replit's own product docs (https://docs.replit.com/features/security/project-security-center).

**Estimated effort:** 30 minutes
**Expected payoff:** High
**Stack impact:** Repository maintenance (biotech-screener, hermes-agent, asset-allocation repos); PR #19 Reliability Gate write-path governance
**Evidence quality:** High — two independently-originated primary sources (Semgrep's announcing partner + Replit's own docs), not a single reprinted release.

**Similar tools already tested:** None in the SAST/secrets-at-generation-time category. Distinct from last week's Rank-1/3/4 items (METR incident-investigation checklist, Perplexity Numbat pre-action monitor, Hermes write-path audit) — those cover behavioral/access governance; this covers static code vulnerability and credential-leak detection. Complementary, not duplicate.

**Success metric:** Run `semgrep ci --config=p/owasp-top-ten --config=p/secrets` against the last 10 agent-authored commits on Warrenpoobear/biotech-screener. Novel findings beyond current CI checks (target: at least one class of finding not caught by existing lint/pytest gates) confirms actionable value.

**Smallest shadow test:** Run the Semgrep Community Edition CLI (zero cost) against 10 recent commits; count and categorize novel findings vs. current CI. ~30 minutes, no production change.

**Ladder move:** independent_confirmation -> internal_experiment (CLI scan run) -> measured_improvement (findings triaged, gate added to CI remediation scope if warranted)

**Recommendation: Run.** Cheapest item this week (30 min, zero cost via Community Edition), purely diagnostic — reading commits and running a scanner changes nothing in production. Directly informs the PR #19 write-path governance mapping already in flight without requiring a merge decision today.

---

## Rank 2 — Anthropic C2PA Provenance Metadata: Document-Lineage Test

**Capability/Tool:** Anthropic now attaches machine-readable C2PA-conformant provenance metadata to Claude-generated text and files worldwide, driven by EU AI Act Article 50(2); applies across Claude Platform (API), Claude Code, and cloud partners.
**Primary source:** Anthropic Claude Help Center, updated Aug 11 2026 (https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content); independently corroborated by TechCrunch, The Verge, The Register, Fast Company, Euronews (all Aug 11, each reporting directly from Anthropic's page).

**Estimated effort:** 30 minutes
**Expected payoff:** Medium-High
**Stack impact:** document-lineage skill (per-fact authority and Code -> GitHub -> Skills -> Artifacts -> .docx sync-state protocol); investment memo / IC drafting
**Evidence quality:** High — canonical primary source + 5 independent tier-1 outlets.

**Similar tools already tested:** None. This is the first cross-lab provenance-marking norm surfaced to the ROQ; no prior candidate addressed machine-checkable AI-vs-human content marking.

**Success metric:** Generate a test file with Claude, inspect for embedded C2PA metadata, and confirm a simple script can extract/verify it. Pass = metadata present and machine-readable without manual inspection.

**Smallest shadow test:** Generate one test document via Claude, check for C2PA metadata, write a short script to extract/verify it. ~30 minutes, zero cost.

**Ladder move:** independent_confirmation -> internal_experiment (extraction script) -> measured_improvement (adopted as a document-lineage provenance signal, if the extraction works cleanly)

**Recommendation: Run.** Trivial cost, pure observability (no Hermes behavior changes), and directly tests a candidate free provenance signal for the document-lineage skill's authority-tracking mandate. Low urgency but essentially free to check now.

---

## Rank 3 — Encrypted CoT Reasoning-Trace Extraction Attack: Hermes Routing-Tier Test

**Capability/Tool:** ELLIS Institute Tübingen / MPI-IS demonstrated that encrypted chain-of-thought reasoning blobs returned by Anthropic/OpenAI/Google APIs are portable across sessions, users, and models within a provider — injecting a frontier model's trace into a weaker sibling forces plaintext transcription. 315,320 reasoning blocks scanned; 182 credentials + 367 PII artifacts recovered from public traces.
**Primary source:** arXiv:2608.09867 (https://arxiv.org/abs/2608.09867) (Andriushchenko, Panfilov, Schmotz et al., submitted Aug 10 2026); independently corroborated by AI/TLDR, ExplainX.ai, ChatPaper.ai.

**Estimated effort:** ~1 hour (~$10 API cost)
**Expected payoff:** High
**Stack impact:** hermes-agent-runtime (multi-model routing: Opus primary + lighter routing tiers); biotech-screener write paths; PR #19 Reliability Gate
**Evidence quality:** High — peer-institution arXiv primary + 3 independent corroborating sources; attack independently confirmed across all three major providers.

**Similar tools already tested:** None. Distinct attack surface from the sandbox-escape cluster surfaced in prior weeks (that was outbound-network misconfiguration; this is reasoning-trace portability/leakage) — new vulnerability class, not a duplicate of last week's Rank-4 write-path audit.

**Success metric:** Inject a dummy Opus-tier reasoning trace into a Haiku/Sonnet-tier Hermes routing call. Pass/fail: does the weaker model transcribe the injected reasoning verbatim in plaintext? A "fail" (no transcription) is the desired outcome and would indicate Hermes's routing tier is not exposed to this specific extraction path as tested.
**Smallest shadow test:** Run the ELLIS attack pattern against Hermes's Haiku/Sonnet routing tier using a dummy Opus trace. ~$10 API cost, no production change.

**Ladder move:** independent_confirmation -> internal_experiment (routing-tier test) -> measured_improvement (result documented in PR #19 threat model)

**Recommendation: Run.** Highest raw ROI this week (5), cheap ($10, ~1 hour), and tests a concrete, previously-undocumented exposure in exactly the multi-model routing architecture Hermes uses. Diagnostic-only — feeds the PR #19 write-path governance review already in flight without requiring any routing change today.

---

## Rank 4 — Green Street GreenStreetAI MCP Server: CRE Underwriting Pilot

**Capability/Tool:** Green Street launched general availability of an MCP Server (GreenStreetAI) connecting its proprietary CRE market intelligence directly into corporate instances of Claude, ChatGPT, and Gemini for natural-language market underwriting and REIT benchmarking.
**Primary source:** Green Street official press release, Aug 11 2026 (https://www.prnewswire.com/news-releases/green-street-launches-its-mcp-server-powered-by-greenstreetai-connecting-cre-intelligence-directly-to-corporate-instances-of-claude-chatgpt-gemini-and-other-ai-platforms-302848322.html).

**Estimated effort:** ~1 hour (contingent on Wake Robin holding or trialing Green Street subscription access)
**Expected payoff:** High, if access exists
**Stack impact:** real-estate-intel skill (Wake Robin multifamily / 55+ underwriting under Liv Communities / Westplan); catalyst/comp monitoring for the Southeast US and Michigan/Midwest markets
**Evidence quality:** High for the sourcing claim itself (official PR + Green Street's own site + webinar channel); no independent trade-press review of output accuracy/citation quality located yet — ladder stays at primary_source_found per the digest's own verification note (second independent source not yet found beyond wire syndication).

**Similar tools already tested:** None. First CRE-data-in-agent-platform capability surfaced to the ROQ. This is Wake Robin's professional real-estate mandate, not the biotech satellite — a different research stream than most ROQ candidates but explicitly in scope for "the research process" broadly.

**Success metric:** Re-run one underwriting question already answered manually this quarter (e.g., a Southeast 55+ community rent-comp benchmark) through the MCP-connected Claude instance; compare output accuracy and citation quality against the existing manual process.

**Smallest shadow test:** Confirm Green Street subscription/trial access; if available, connect the MCP server and re-run one already-answered underwriting question. ~1 hour, contingent on access.

**Ladder move:** primary_source_found -> internal_experiment (comparison test) -> measured_improvement

**Recommendation: Wait.** Gate on confirming Wake Robin's Green Street subscription status first (unknown as of this run, and access decisions likely involve Austin/Scott, not solely this pipeline). Evidence for the release itself is solid; the blocker is access, not evidence quality. Verify access before allocating the 1-hour test.

---

## Rank 5 — Agent Plugins 1.0.0: Skill-Packaging Portability Test

**Capability/Tool:** Agent Plugins 1.0.0 — vendor-neutral open standard for packaging MCP servers and Agent Skills into portable plugins, governed by a Technical Steering Committee of Amazon, Cursor, Microsoft, OpenAI, and Vercel (Google joined as a sixth Core Maintainer). Compatible clients: ChatGPT, Codex, Cursor, GitHub Copilot, Kiro, VS Code.
**Primary source:** spec repo, github.com/agentplugins/agent-plugins-spec (https://vercel.com/blog/introducing-agent-plugins); independently confirmed by AWS, Google Developers Blog, and 3+ independent editorial outlets.

**Estimated effort:** 1-2 hours
**Expected payoff:** Medium-High
**Stack impact:** hermes-agent skill-mirror sync Phase B design; cross-agent portability for Robinhood MCP and future EDGAR/ClinicalTrials connectors
**Evidence quality:** High — live spec repo with schema files, multi-vendor founding blog posts, 3+ independent editorial confirmations. Explicitly noted by the source digest as freeze-safe: "no architecture change needed — purely additive packaging work... can proceed during freeze (observability-only)."

**Similar tools already tested:** None — first cross-vendor agent-plugin portability standard evaluated. Distinct from last week's dropped item "Cursor cloud agent environment architecture" (that was a read-before-sprint reference on self-healing environments, not a packaging standard).

**Success metric:** Map the existing Robinhood MCP integration to the Agent Plugins manifest format (`plugin.json`). If the format covers the use case with minimal adaptation, this is a near-term packaging win; if it requires substantial rework, defer.

**Smallest shadow test:** Read `spec/1.0.0.md`; map the Robinhood MCP integration to the plugin manifest format. ~1-2 hours, no Hermes code change required to evaluate.

**Ladder move:** independent_confirmation -> internal_experiment (manifest mapping) -> measured_improvement (skill packaged, tested across a second client)

**Recommendation: Run.** Freeze-compliant by the source's own characterization (spec evaluation only, no code change), moderate cost, and directly serves the ROQ's "more reproducible" mandate — this is exactly the kind of skill-portability groundwork that reduces per-client re-engineering long-term.

---

## Also Considered (Ranked 6-13)

- **#6 — Multi-agent Lean4-verified swarm for biotech literature synthesis** (Anthropic Riemann bound + OpenAI Astra Lean proofs), composite 6.0, Run/Wait: shadow-research backlog, freeze-gated to ~Sep-Oct. Test: 3-agent Claude swarm on a verifiable biotech mechanism question, ~$20, measure novel-fact surface rate vs. single-agent baseline.
- **#7 — Meta Muse Glimmer 30B local model tier**, composite 4.5, freeze-gated. First serious local (no-cloud-API) Hermes agent-tier candidate; Apache 2.0.
- **#7 — Mistral Shieldstral 3B local guardrail** (strongest verification, Aug 9 capture), composite 4.5, freeze-safe as pure observability. Policy-as-language safety classifier for Hermes tool-call outputs.
- **#7 — Cursor cloud-agent self-healing MCP mapping**, composite 4.5. Map Cursor's environment-diagnostic MCP tools to Hermes observable equivalents; window for the original Aug 7 CI sprint has passed, lower urgency now.
- **#10 — NVIDIA Nemotron 3.5 Lightning / NeMo Switchyard cost-aware escalation routing**, composite 4.0. Evidence upgraded this week (LangChain + Cognition independent-but-interested implementer benchmarks: ~70-75% cost reduction at mid-single-digit accuracy cost). Explicitly gated by the source captures to shadow-research backlog, timeline unchanged per freeze governance — **Wait**.
- **#10 — Citadel/Ken Griffin backtest-reproduction claim**, composite 4.0. Confirmed Griffin made the claim on the record (Goldman Sachs Exchanges, Jun 2); the underlying technical capability remains Citadel's self-report, not independently audited. Proposed test: have an agent independently reconstruct and verify one past IC memo backtest number. Freeze-gated shadow-research backlog — **Wait**.
- **#13 — Canary Susceptibility Rate (CSR) evaluation harness**, composite 2.0. Directly targets the named "benchmarking" bottleneck (36x model variance in tool-selection reliability, correlates with task failure at Spearman -0.34) — strategically the best-fit item this week, but the underlying Anand & Chattaraj paper's arXiv/SSRN listing was not independently located as of this capture ("primary source not directly verified... secondary coverage"). Downgraded to Low evidence quality; **Wait** pending source verification, not for lack of strategic fit.

---

## Dropped This Week

- **GPT-5.6-Cyber + Daybreak Red/Blue governance signal** — real capability/governance news (OpenAI dual-tier offensive/defensive model), but the only proposed action is documenting a threat class in the PR #19 governance doc — zero code change, no measurable pass/fail. Not a process experiment; folded into PR #19 governance tracking.
- **29-House-Democrats congressional hearing demand (Casar/Matsui letters to OpenAI/Anthropic)** — legislative/regulatory monitoring, pure context for the GOOGL/Anthropic regulatory-risk thread, not a research-tooling experiment.
- **Meta Muse Spark 1.1 sandbox escape / Kimi K3 "4th lab" escape / OpenAI Astra Critical-tier pause / AISI cross-lab reform pattern** — this cluster is real and well-evidenced, but it is the same underlying write-path/sandbox-misconfiguration story last week's ROQ already ranked (Ranks 3-4, both recommended Run) and Reliability Gate PR #19 is already scoped to address it. No material new action beyond what is already in flight; re-listing would be noise, not a new recommendation.
- **DeepSeek API price-increase notice** — operational cost-baseline bookkeeping ("check hermes-llm-config routing table"), not an experiment with a success metric.
- **SALP/Aschenbrenner hedge-fund collapse** — regime-evidence / cautionary market reference for IPS Appendix A risk parameters, not a research-process tool or experiment.
- **Google DeepMind leadership reshuffle (Hassabis -> Kavukcuoglu) + Gary Marcus counter-thesis** — the proposed "smallest shadow test" is object-level investment analysis (read the TCI Q1 letter, decide if the GOOGL thesis is model-leadership- or distribution-based). That is IC memo work itself, not a repeatable tooling/process experiment; belongs in the GOOGL memo workflow, not the ROQ.
- **Cline SDK re-surfaced release** — verification found the underlying release is dated May 13-14, 2026, roughly three months before this week's capture; the "new this week" framing was inaccurate, and the proposed test has no decision gate. Thin value; watch, do not implement per source's own disposition.
- **Millennium/Anthropic digital-risk-analyst co-development** — explicitly filed to "watch/do-not-act" by the source captures; no independent performance benchmark exists.

---

## Carryover Status

No prior-week ROQ items from Jul 30 or earlier remain open per this routine's memory (first ledger-tracked run for this instance). The Aug 6 ROQ's Top-5 (METR Reliability Gate mapping, Meta Muse Code CI test, Perplexity Numbat monitor, Anthropic sandbox write-path audit, Microsoft EvoLib) all fall inside the same PR #19 / CI-remediation governance sprint already referenced above under "Dropped This Week" — none are re-surfaced here as new recommendations.

---

## Self-Check

- Captures reviewed: 7 daily AI digests (2026-08-06 through 2026-08-13), ~400 items scanned (X quota capped Aug 11-13; web-search fallback used per source notes)
- Candidates qualified: 13 (5 filled Top-5 bar; 7 held as also-considered; 1 of the 13 downgraded to Wait on evidence grounds despite strong bottleneck fit — CSR harness)
- Top-N delivered: 5 of 5 (3 Run / 2 Wait)
- GitHub mirror cross-check: performed (Warrenpoobear/hermes-agent research-inbox/x-intelligence/roq/2026-08-06 reviewed for continuity; no dedicated GitHub mirror of the Aug 06-13 daily AI digests found beyond the Content Library notes — Content Library treated as primary per note metadata, gap noted)
- Prior-week ledger memory: none found for this routine (first tracked run); this week's queue is being written to memory now
- Deliverables: Content Library (this document) written; GitHub commit (this file); Decision Impact Ledger 5 rows pending; emails to dschulz@wakerobin.co and djschulz@gmail.com pending
- Schema: v1.0 (cols A-Z), no structural changes proposed
