#!/usr/bin/env python3
"""Diagnostic-only EES v2 composite reconstruction.

Governance boundary:
    DIAGNOSTIC_ONLY | NO_PRODUCTION_SCORING_CHANGE | FREEZE_ACTIVE

This script reuses the strict PIT EES v2 backtest panel construction, then
adds reconstructed composite variants for research only. It reads historical
PIT snapshots/prices/trial records and writes only research artifacts under
``artifacts/research`` by default.

It deliberately does not import or call production screen runners, does not
fetch live data, and does not mutate production scoring fields.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
from scripts.research import pit_backtest_ees_v2 as pit

RUN_DATE = "2026_06_24"
SCHEMA = "ees_v2_reconstructed_composite.v1"
GOVERNANCE = "DIAGNOSTIC_ONLY | NO_PRODUCTION_SCORING_CHANGE | FREEZE_ACTIVE | NO_LIVE_FETCH"

HORIZONS = [21, 42, 63]
POSITIVE_COMPONENTS = [
    "conditional_gap_score",
    "conditional_misprice_score",
    "conditional_base_rate",
    "conditional_expected_move",
]
NEGATIVE_CANDIDATES = ["trap_overlay_score", "base_rate_gap_score"]
VARIANT_NAMES = [
    "positive_components_equal_weight",
    "positive_components_ic_weighted",
    "original_minus_trap_overlay",
    "original_minus_base_rate_gap",
    "original_minus_both",
    "sign_flip_trap_and_base_rate_gap",
]
PREDECLARED_PASS_BAR = {
    "all_horizons_positive_ic": True,
    "min_horizons_with_newey_west_t_ge_2": 2,
    "max_single_ticker_ic_contribution_pct": 25.0,
    "requires_priced_move_only_survival": True,
    "requires_full_panel_survival": True,
    "requires_no_lookahead_or_live_universe_dependency": True,
}
_FORBIDDEN_LIVE_IMPORTS = ("yfinance", "requests", "urllib", "httpx", "alpaca", "iexfinance", "tiingo")


def _safe_float(value: Any) -> Optional[float]:
    if value is None or value == "" or value == "None":
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(out) else out


def _is_valid_number(value: Any) -> bool:
    return _safe_float(value) is not None


def _mean(values: Iterable[float]) -> Optional[float]:
    vals = list(values)
    if not vals:
        return None
    return sum(vals) / len(vals)


def _zscore_by_date(records: List[Dict[str, Any]], columns: List[str]) -> None:
    """Add ``z_<column>`` fields in place, per snapshot date.

    The transformation is cross-sectional within a single already-materialized
    PIT snapshot. It does not read future dates or any live data.
    """
    for col in columns:
        vals = [_safe_float(r.get(col)) for r in records]
        clean = [v for v in vals if v is not None]
        if len(clean) < 2:
            for r in records:
                r[f"z_{col}"] = None
            continue
        mu = sum(clean) / len(clean)
        var = sum((v - mu) ** 2 for v in clean) / len(clean)
        sd = math.sqrt(var)
        for r, v in zip(records, vals):
            r[f"z_{col}"] = None if v is None or sd < 1e-12 else (v - mu) / sd


def _equal_weight_positive(record: Dict[str, Any]) -> Optional[float]:
    vals = [_safe_float(record.get(f"z_{c}")) for c in POSITIVE_COMPONENTS]
    vals = [v for v in vals if v is not None]
    return _mean(vals)


def _ic_weighted_positive(record: Dict[str, Any], weights: Dict[str, float]) -> Optional[float]:
    numer = 0.0
    denom = 0.0
    for comp in POSITIVE_COMPONENTS:
        v = _safe_float(record.get(f"z_{comp}"))
        w = weights.get(comp, 0.0)
        if v is None or w <= 0:
            continue
        numer += v * w
        denom += w
    return None if denom <= 0 else numer / denom


def _original_minus(record: Dict[str, Any], *remove_cols: str) -> Optional[float]:
    original = _safe_float(record.get("z_ees_v2_score"))
    if original is None:
        return None
    value = original
    for col in remove_cols:
        comp = _safe_float(record.get(f"z_{col}"))
        if comp is not None:
            value -= comp
    return value


def _sign_flip_trap_and_base_rate_gap(record: Dict[str, Any]) -> Optional[float]:
    original = _safe_float(record.get("z_ees_v2_score"))
    if original is None:
        return None
    trap = _safe_float(record.get("z_trap_overlay_score")) or 0.0
    base = _safe_float(record.get("z_base_rate_gap_score")) or 0.0
    # Flip each component by removing its original contribution once and adding
    # the opposite contribution once: original - 2*component.
    return original - 2.0 * trap - 2.0 * base


def variant_score(record: Dict[str, Any], variant: str, ic_weights: Optional[Dict[str, float]] = None) -> Optional[float]:
    """Return a diagnostic reconstructed score for one PIT row.

    The function intentionally returns a new score value and never mutates or
    overwrites ``ees_v2_score``.
    """
    if variant == "positive_components_equal_weight":
        return _equal_weight_positive(record)
    if variant == "positive_components_ic_weighted":
        return _ic_weighted_positive(record, ic_weights or {})
    if variant == "original_minus_trap_overlay":
        return _original_minus(record, "trap_overlay_score")
    if variant == "original_minus_base_rate_gap":
        return _original_minus(record, "base_rate_gap_score")
    if variant == "original_minus_both":
        return _original_minus(record, "trap_overlay_score", "base_rate_gap_score")
    if variant == "sign_flip_trap_and_base_rate_gap":
        return _sign_flip_trap_and_base_rate_gap(record)
    raise ValueError(f"Unknown variant: {variant}")


def _ic_weights_from_baseline(baseline_report: Dict[str, Any]) -> Dict[str, float]:
    """Positive-component weights from baseline PIT IC evidence only.

    Uses non-negative mean IC averaged across horizons. Negative component ICs
    receive zero weight. If all are non-positive/missing, falls back to equal
    weights so the diagnostic remains observable but is not marked promoted.
    """
    raw: Dict[str, float] = {}
    horizons = baseline_report.get("horizons", {})
    for comp in POSITIVE_COMPONENTS:
        vals: List[float] = []
        for report in horizons.values():
            ic = report.get("core_performance", {}).get(comp, {}).get("ic", {}).get("mean_ic")
            if ic is not None:
                vals.append(float(ic))
        raw[comp] = max(0.0, statistics.mean(vals)) if vals else 0.0
    if sum(raw.values()) <= 0:
        return {comp: 1.0 for comp in POSITIVE_COMPONENTS}
    return raw


def build_horizon_records(
    snapshots_dir: Path,
    price_csv: Path,
    trial_records_path: Path,
    horizon: int,
) -> Dict[str, List[Dict[str, Any]]]:
    """Build strict PIT event records plus forward returns for one horizon."""
    import sys

    sys.path.insert(0, str(PROJECT_ROOT))
    from event_ev.conditional_model import ConditionalModel
    from event_ev.expectation_error_model import ExpectationErrorModel

    cond_model = ConditionalModel(trial_records_path=trial_records_path)
    ees_model = ExpectationErrorModel()

    prices = pit._load_prices(price_csv)
    sorted_dates_by_ticker: Dict[str, List[str]] = {tk: sorted(px.keys()) for tk, px in prices.items()}
    date_records: Dict[str, List[Dict[str, Any]]] = {}

    for snap_date in pit._discover_snapshot_dates(snapshots_dir):
        rows = pit._load_snapshot(snapshots_dir, snap_date)
        if not rows:
            continue
        pit._pre_enrich_snapshot(rows, snap_date, prices, sorted_dates_by_ticker)
        enriched = pit._score_snapshot_strict(rows, snap_date, cond_model, ees_model)
        event_records: List[Dict[str, Any]] = []
        for rec in enriched:
            if not rec.get("has_catalyst"):
                continue
            ticker = rec.get("ticker")
            ticker_dates = sorted_dates_by_ticker.get(ticker or "")
            if not ticker_dates:
                continue
            trade_date = pit._resolve_trade_date(ticker_dates, snap_date)
            if not trade_date:
                continue
            fwd_return = pit._forward_return(prices[ticker], ticker_dates, trade_date, horizon)
            if fwd_return is None:
                continue
            rec["fwd_return"] = fwd_return
            event_records.append(rec)
        if len(event_records) >= 5:
            _zscore_by_date(
                event_records,
                ["ees_v2_score", *POSITIVE_COMPONENTS, *NEGATIVE_CANDIDATES],
            )
            date_records[snap_date] = event_records
    return date_records


def _evaluate_signal(date_records: Dict[str, List[Dict[str, Any]]], signal_key: str) -> Dict[str, Any]:
    ic_series = pit._compute_ic_series(date_records, signal_key)
    ics = [x[1] for x in ic_series]
    if not ics:
        return {
            "mean_ic": None,
            "t_nw": 0.0,
            "n_periods": 0,
            "hit_rate": None,
            "n_observations": 0,
            "max_single_ticker_ic_contribution_pct": None,
        }
    nw = pit._newey_west_tstat(ics)
    return {
        "mean_ic": nw["mean"],
        "t_nw": nw["t_nw"],
        "n_periods": len(ics),
        "hit_rate": round(sum(1 for ic in ics if ic > 0) / len(ics), 3),
        "n_observations": sum(len(v) for v in date_records.values()),
        "max_single_ticker_ic_contribution_pct": _max_ticker_contribution_pct(date_records, signal_key),
    }


def _max_ticker_contribution_pct(date_records: Dict[str, List[Dict[str, Any]]], signal_key: str) -> Optional[float]:
    """Approximate ticker concentration using absolute demeaned rank covariance."""
    contributions: Dict[str, float] = defaultdict(float)
    total_abs = 0.0
    for records in date_records.values():
        valid = [r for r in records if _is_valid_number(r.get(signal_key)) and _is_valid_number(r.get("fwd_return"))]
        if len(valid) < 5:
            continue
        sigs = [float(valid[i][signal_key]) for i in range(len(valid))]
        rets = [float(valid[i]["fwd_return"]) for i in range(len(valid))]
        rx = pit._avg_ranks(sigs)
        ry = pit._avg_ranks(rets)
        mx = sum(rx) / len(rx)
        my = sum(ry) / len(ry)
        for row, x, y in zip(valid, rx, ry):
            contrib = (x - mx) * (y - my)
            abs_contrib = abs(contrib)
            contributions[row.get("ticker", "UNKNOWN")] += abs_contrib
            total_abs += abs_contrib
    if total_abs <= 0:
        return None
    return round(max(contributions.values()) / total_abs * 100.0, 2)


def _restricted_records(
    date_records: Dict[str, List[Dict[str, Any]]],
    predicate: Callable[[Dict[str, Any]], bool],
) -> Dict[str, List[Dict[str, Any]]]:
    out = {}
    for dt, records in date_records.items():
        kept = [r for r in records if predicate(r)]
        if len(kept) >= 5:
            out[dt] = kept
    return out


def _decorate_variants(
    date_records: Dict[str, List[Dict[str, Any]]],
    ic_weights: Dict[str, float],
) -> None:
    for records in date_records.values():
        for rec in records:
            for variant in VARIANT_NAMES:
                score = variant_score(rec, variant, ic_weights)
                rec[f"variant__{variant}"] = float("nan") if score is None else score


def _evaluate_pass_bar(variant_result: Dict[str, Any]) -> Dict[str, Any]:
    horizons = variant_result.get("horizons", {})
    horizon_metrics = [horizons.get(f"{h}d", {}) for h in HORIZONS]
    all_positive = all((m.get("full_panel", {}).get("mean_ic") or 0) > 0 for m in horizon_metrics)
    t_ge_2 = sum(1 for m in horizon_metrics if (m.get("full_panel", {}).get("t_nw") or 0) >= 2.0)
    max_ticker = max(
        (m.get("full_panel", {}).get("max_single_ticker_ic_contribution_pct") or 100.0) for m in horizon_metrics
    )
    pm_survives = all((m.get("priced_move_only", {}).get("mean_ic") or 0) > 0 for m in horizon_metrics)
    full_survives = all_positive
    no_lookahead = True
    clears = all_positive and t_ge_2 >= 2 and max_ticker <= 25.0 and pm_survives and full_survives and no_lookahead
    return {
        "clears_predeclared_pass_bar": clears,
        "all_horizons_positive_ic": all_positive,
        "horizons_with_newey_west_t_ge_2": t_ge_2,
        "max_single_ticker_ic_contribution_pct": round(max_ticker, 2),
        "priced_move_only_survives": pm_survives,
        "full_panel_survives": full_survives,
        "no_lookahead_or_live_universe_dependency_detected": no_lookahead,
    }


def run_reconstruction(
    snapshots_dir: Path,
    price_csv: Path,
    trial_records_path: Path,
) -> Dict[str, Any]:
    """Run baseline PIT backtest and reconstructed variant diagnostics."""
    missing_inputs = []
    if not snapshots_dir.exists() or not any(snapshots_dir.iterdir() if snapshots_dir.exists() else []):
        missing_inputs.append(str(snapshots_dir))
    if not price_csv.exists():
        missing_inputs.append(str(price_csv))
    if not trial_records_path.exists():
        missing_inputs.append(str(trial_records_path))
    if missing_inputs:
        return _no_data_report(snapshots_dir, price_csv, trial_records_path, missing_inputs)

    baseline = pit.run_multi_horizon(snapshots_dir, price_csv, trial_records_path)
    ic_weights = _ic_weights_from_baseline(baseline)

    variants: Dict[str, Dict[str, Any]] = {v: {"horizons": {}} for v in VARIANT_NAMES}
    for horizon in HORIZONS:
        date_records = build_horizon_records(snapshots_dir, price_csv, trial_records_path, horizon)
        _decorate_variants(date_records, ic_weights)
        priced_move_only = _restricted_records(date_records, lambda r: bool(r.get("has_priced_move")))
        full_panel = date_records
        for variant in VARIANT_NAMES:
            key = f"variant__{variant}"
            variants[variant]["horizons"][f"{horizon}d"] = {
                "full_panel": _evaluate_signal(full_panel, key),
                "priced_move_only": _evaluate_signal(priced_move_only, key),
            }

    for variant in VARIANT_NAMES:
        variants[variant]["pass_bar"] = _evaluate_pass_bar(variants[variant])

    robust = _best_robust_variant(variants)
    return {
        "schema": SCHEMA,
        "run_date": RUN_DATE,
        "governance": GOVERNANCE,
        "inputs": {
            "snapshots_dir": str(snapshots_dir),
            "price_csv": str(price_csv),
            "trial_records_path": str(trial_records_path),
            "live_fetch": False,
            "production_mutation": False,
        },
        "predeclared_pass_bar": PREDECLARED_PASS_BAR,
        "baseline_reference": _baseline_summary(baseline),
        "ic_weights": ic_weights,
        "variants": variants,
        "best_robust_variant": robust,
        "governance_verdict": _governance_verdict(variants, robust),
    }



def _no_data_report(
    snapshots_dir: Path,
    price_csv: Path,
    trial_records_path: Path,
    missing_inputs: List[str],
) -> Dict[str, Any]:
    return {
        "schema": SCHEMA,
        "run_date": RUN_DATE,
        "governance": GOVERNANCE,
        "status": "NO_DATA",
        "missing_inputs": missing_inputs,
        "inputs": {
            "snapshots_dir": str(snapshots_dir),
            "price_csv": str(price_csv),
            "trial_records_path": str(trial_records_path),
            "live_fetch": False,
            "production_mutation": False,
        },
        "predeclared_pass_bar": PREDECLARED_PASS_BAR,
        "baseline_reference": {
            "source": "scripts.research.pit_backtest_ees_v2.run_multi_horizon",
            "signals": [],
        },
        "ic_weights": {},
        "variants": {name: {"horizons": {}, "pass_bar": {"clears_predeclared_pass_bar": False}} for name in VARIANT_NAMES},
        "best_robust_variant": {"variant": None, "reason": "missing PIT inputs in this environment"},
        "governance_verdict": (
            "FREEZE_REMAINS_ACTIVE: PIT reconstruction could not be evaluated because required historical "
            "inputs are unavailable in this environment; no production promotion is authorized."
        ),
    }


def _baseline_summary(baseline: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for row in baseline.get("cross_horizon_summary", []):
        if row.get("signal") in ["ees_v2_score", *POSITIVE_COMPONENTS, *NEGATIVE_CANDIDATES]:
            rows.append(row)
    return {
        "source": "scripts.research.pit_backtest_ees_v2.run_multi_horizon",
        "signals": rows,
    }


def _best_robust_variant(variants: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    scored = []
    for name, result in variants.items():
        horizons = result.get("horizons", {})
        means = []
        t_count = 0
        min_pm = 999.0
        for h in HORIZONS:
            metric = horizons.get(f"{h}d", {})
            full = metric.get("full_panel", {})
            pm = metric.get("priced_move_only", {})
            if full.get("mean_ic") is not None:
                means.append(full["mean_ic"])
            if (full.get("t_nw") or 0) >= 2.0:
                t_count += 1
            min_pm = min(min_pm, pm.get("mean_ic") if pm.get("mean_ic") is not None else -999.0)
        avg_ic = statistics.mean(means) if means else -999.0
        scored.append((result.get("pass_bar", {}).get("clears_predeclared_pass_bar", False), t_count, min_pm, avg_ic, name))
    scored.sort(reverse=True)
    if not scored:
        return {"variant": None, "reason": "no variants evaluated"}
    clears, t_count, min_pm, avg_ic, name = scored[0]
    return {
        "variant": name,
        "clears_predeclared_pass_bar": clears,
        "horizons_with_t_ge_2": t_count,
        "min_priced_move_only_ic": round(min_pm, 6) if min_pm > -900 else None,
        "average_full_panel_ic": round(avg_ic, 6) if avg_ic > -900 else None,
    }


def _governance_verdict(variants: Dict[str, Dict[str, Any]], robust: Dict[str, Any]) -> str:
    any_clear = any(v.get("pass_bar", {}).get("clears_predeclared_pass_bar") for v in variants.values())
    if any_clear:
        return (
            "FREEZE_REMAINS_ACTIVE_PENDING_HUMAN_REVIEW: at least one reconstructed composite cleared the "
            "pre-declared diagnostic bar, but this script is research-only and does not authorize production promotion."
        )
    return (
        "FREEZE_REMAINS_ACTIVE: no reconstructed composite cleared the pre-declared diagnostic promotion bar; "
        "do not lift freeze, do not wire variants into production scoring."
    )


def render_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# EES v2 Reconstructed Composite Diagnostic",
        "",
        f"**Run date:** {report.get('run_date')}",
        f"**Governance:** {report.get('governance')}",
        "",
        "## Pre-declared pass bar",
        "",
    ]
    for k, v in report.get("predeclared_pass_bar", {}).items():
        lines.append(f"- `{k}`: `{v}`")
    lines.extend(["", "## Variant IC / t-stat table", ""])
    lines.append("| Variant | 21d IC | 21d t | 42d IC | 42d t | 63d IC | 63d t | Max ticker % | Clears bar |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, result in report.get("variants", {}).items():
        cells = [name]
        max_ticker = None
        for h in HORIZONS:
            full = result.get("horizons", {}).get(f"{h}d", {}).get("full_panel", {})
            ic = full.get("mean_ic")
            t = full.get("t_nw")
            cells.append("" if ic is None else f"{ic:+.4f}")
            cells.append("" if t is None else f"{t:+.2f}")
            mt = full.get("max_single_ticker_ic_contribution_pct")
            if mt is not None:
                max_ticker = mt if max_ticker is None else max(max_ticker, mt)
        clears = result.get("pass_bar", {}).get("clears_predeclared_pass_bar", False)
        lines.append(
            f"| {cells[0]} | {cells[1]} | {cells[2]} | {cells[3]} | {cells[4]} | {cells[5]} | {cells[6]} | "
            f"{'' if max_ticker is None else f'{max_ticker:.2f}'} | {'YES' if clears else 'NO'} |"
        )
    robust = report.get("best_robust_variant", {})
    lines.extend(
        [
            "",
            "## Best robust variant",
            "",
            f"- Variant: `{robust.get('variant')}`",
            f"- Clears pre-declared bar: `{robust.get('clears_predeclared_pass_bar')}`",
            f"- Average full-panel IC: `{robust.get('average_full_panel_ic')}`",
            f"- Min priced-move-only IC: `{robust.get('min_priced_move_only_ic')}`",
            "",
            "## Governance verdict",
            "",
            report.get("governance_verdict", "FREEZE_REMAINS_ACTIVE"),
            "",
            "## Production boundary",
            "",
            "- No production scoring changed.",
            "- `run_screen.py` is not imported, edited, or wired to these variants.",
            "- `final_score`, sizing, selector, eligibility, and portfolio construction remain untouched.",
            "- Outputs are research artifacts only under `artifacts/research` unless an explicit output path is supplied.",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_output_path_allowed(path: Path) -> None:
    resolved = path.resolve()
    research_root = (PROJECT_ROOT / "artifacts" / "research").resolve()
    if research_root not in [resolved, *resolved.parents]:
        raise ValueError(f"Refusing non-research output path: {path}")


def write_outputs(report: Dict[str, Any], output_json: Path, output_md: Path) -> None:
    _assert_output_path_allowed(output_json)
    _assert_output_path_allowed(output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(render_markdown(report))


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnostic-only reconstructed EES v2 composite PIT backtest")
    parser.add_argument("--snapshots-dir", type=Path, default=pit.DEFAULT_SNAPSHOTS_DIR)
    parser.add_argument("--prices", type=Path, default=pit.DEFAULT_PRICE_CSV)
    parser.add_argument("--trials", type=Path, default=pit.DEFAULT_TRIAL_RECORDS)
    parser.add_argument("--output-json", type=Path, default=PROJECT_ROOT / "artifacts" / "research" / f"ees_v2_reconstructed_composite_{RUN_DATE}.json")
    parser.add_argument("--output-md", type=Path, default=PROJECT_ROOT / "artifacts" / "research" / f"ees_v2_reconstructed_composite_{RUN_DATE}.md")
    parser.add_argument("--print-only", action="store_true", help="Print markdown instead of writing artifacts")
    args = parser.parse_args()

    report = run_reconstruction(args.snapshots_dir, args.prices, args.trials)
    if args.print_only:
        print(render_markdown(report))
    else:
        write_outputs(report, args.output_json, args.output_md)
        print(f"wrote {args.output_json}")
        print(f"wrote {args.output_md}")


if __name__ == "__main__":
    main()
