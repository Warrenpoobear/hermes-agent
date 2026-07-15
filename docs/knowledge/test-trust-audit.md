# Test-Trust Audit (Knowledge Reference)

<!--
SYNC PROVENANCE
  Source: Town skill `test-trust-audit`
  Source maturity (per skill-maturity-metadata): DRAFT (new build; first run 2026-07-14)
  Synced to Hermes: 2026-07-14 (manual, operator-approved; pushed direct-to-main per operator instruction 2026-07-14)
  Sync owner: Darren Schulz (dschulz@wakerobin.co)
  Type: knowledge-layer reference (NOT an agent; no AGENT_REGISTRY.json entry, no cron, no authority)
  Batch: Town -> Hermes mapping pipeline.
  NOTE: Reference knowledge a SOUL.md may cite. It does not execute, mutate data, or write to .learnings/.
-->

> **READ-ONLY / ADVISORY — this wraps existing code, it does not fork it.**
> The authority for detection is the repo's own `tools/test_trust_audit.py` (v1, read-only, advisory).
> This reference documents how to DRIVE that tool and how to cover the checks its v1 does not yet make.
> Do NOT restate or re-implement the detector logic here — if the detectors change, change the tool,
> not this file.

## Purpose
Drive the repo's own deterministic test-trust auditor, `tools/test_trust_audit.py`, and turn its output into a go/no-go trust verdict. The tool owns detection; this reference explains how to run it, escalate the findings that actually block trust, cover the checks the tool's v1 does not yet make, and state whether "green" can be believed. It changes nothing — the tool is read-only and advisory.

## When to use
- CI is red and you need to know which green is real before trusting it.
- Before a freeze-lift, or a ranker / selector / scorer promotion, that leans on "the tests pass."
- Periodically (e.g., monthly) as a standing hygiene pass, distinct from signal sweeps.

## The engine is the authority: `tools/test_trust_audit.py`
Do not re-derive detection heuristics — the tool is the single source of truth. It is read-only, advisory-only, and deterministic (emits a findings SHA and a trust score; `SCHEMA_VERSION = test_trust_audit.v1`).

Run it:
```
python -m tools.test_trust_audit --mode static --tests-root tests --out reports/
```
Optional: `--as-of YYYY-MM-DD` (audit date; defaults from the repo HEAD commit date). It writes a markdown + JSON report to `--out` and prints JSON with the report paths, trust score, severity counts, and the delta versus the prior run.

Active detectors (v1):

| Detector | What it catches | Severity |
| --- | --- | --- |
| T2 | no effective assertion | HIGH |
| T3 | tautological assertion (`assert x == x`) | HIGH |
| T4 | mock of the subject-under-test; when the mocked target is on a frozen model path (per `FrozenPolicy` / `frozen_markers`) it is flagged `model_path=True`, `report_only=True` | CRITICAL |
| T5 | swallowed failure (`try/…/except: pass` or broad except) | HIGH |
| T6 | vacuous parametrize | MEDIUM |
| T7 | silent skip / xfail | MEDIUM |
| T12 | broad snapshot / weak assert (`len`- or type-only) | LOW-MEDIUM |

Disabled stubs in v1 — DO NOT assume these are covered:
- T8 stale-golden detector
- T9 PIT-leakage detector
- T10 coverage cross-check (L2)
- L3 mutation probe

## Procedure
1. **Run the tool** (command above) and read the JSON payload + markdown report.
2. **Escalate the blockers first:** every `T4` with `model_path=True` — a frozen-path test that passes without running the frozen logic. These are the freeze-lift blockers. List them before anything else.
3. **Read the trust score, severity counts, and delta** vs the prior run (a regression matters more than the absolute level).
4. **Cover the v1 gaps the tool does not yet detect** (these stay manual until T8/T9/T10 are enabled):
   - **PIT-leakage (T9 off):** spot-check that PIT/staleness modules assert rejection of future-dated or stale input (`pytest.raises` / reject / empty), not just shape.
   - **Stale-golden (T8 off):** confirm golden/snapshot tests cannot be silently regenerated to match current output.
   - **Decimal-leakage (no detector):** scan scoring/rank/sizing tests for `pytest.approx`/`assertAlmostEqual` that could pass even if the `Decimal` mandate were violated.
   - **Byte-identity:** confirm determinism claims are backed by `sha256`/`hexdigest`, not only object/DataFrame equality.
5. **Emit the verdict** (below).

## Output
- **Suite trust verdict** — one line: can green be trusted for a freeze-lift / promotion — yes / no / partial — naming the blocking set.
- **Blocker list** — the `T4 model_path=True` findings (and any other CRITICAL), each as `file::test · detector · why`.
- **Tool summary** — trust score + severity counts + delta vs prior run, with the report path cited.
- **Gap-check results** — the four manual checks from step 4.

## Governance guardrails (hard)
- **Observe-only.** Run the tool (it is read-only) and read its reports; never edit, add, or delete a test, and never touch frozen `scoring / ranker / selector / sizing / final_score / PIT` paths.
- **Advisory only.** The tool and this reference are `report_only`. Do not fail CI on findings and do not open fix PRs without explicit authorization.
- **Do not enable** the T8 / T9 / T10 / L3 stubs, and do not make any detector CI-blocking, without an explicit go-ahead — they are gated deliberately.
- **One task per session. No broad refactors.** Respect the active architecture freeze and the `.cursorrules` Judgment Capital principle: a test that codifies judgment must actually exercise it, or it is a lossy compression masquerading as coverage.

## Notes
- The engine already encodes the taxonomy deterministically; this reference's value is (a) running it, (b) escalating frozen-path CRITICALs, and (c) covering the v1 gaps (PIT-leakage, stale-golden, Decimal-leakage, byte-identity) that remain manual.
- First run: 2026-07-14 against `biotech-screener` (722 test files / 17,461 test functions). Verdict PARTIAL — no systemic rot; CI-red is not explained by suite dishonesty. Findings report lives in the Town Content Library (self-improvement collection).
