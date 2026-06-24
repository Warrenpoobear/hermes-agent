# EES v2 Reconstructed Composite Diagnostic

**Run date:** 2026_06_24
**Governance:** DIAGNOSTIC_ONLY | NO_PRODUCTION_SCORING_CHANGE | FREEZE_ACTIVE | NO_LIVE_FETCH

## Pre-declared pass bar

- `all_horizons_positive_ic`: `True`
- `min_horizons_with_newey_west_t_ge_2`: `2`
- `max_single_ticker_ic_contribution_pct`: `25.0`
- `requires_priced_move_only_survival`: `True`
- `requires_full_panel_survival`: `True`
- `requires_no_lookahead_or_live_universe_dependency`: `True`

## Variant IC / t-stat table

| Variant | 21d IC | 21d t | 42d IC | 42d t | 63d IC | 63d t | Max ticker % | Clears bar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| positive_components_equal_weight |  |  |  |  |  |  |  | NO |
| positive_components_ic_weighted |  |  |  |  |  |  |  | NO |
| original_minus_trap_overlay |  |  |  |  |  |  |  | NO |
| original_minus_base_rate_gap |  |  |  |  |  |  |  | NO |
| original_minus_both |  |  |  |  |  |  |  | NO |
| sign_flip_trap_and_base_rate_gap |  |  |  |  |  |  |  | NO |

## Best robust variant

- Variant: `None`
- Clears pre-declared bar: `None`
- Average full-panel IC: `None`
- Min priced-move-only IC: `None`

## Governance verdict

FREEZE_REMAINS_ACTIVE: PIT reconstruction could not be evaluated because required historical inputs are unavailable in this environment; no production promotion is authorized.

## Production boundary

- No production scoring changed.
- `run_screen.py` is not imported, edited, or wired to these variants.
- `final_score`, sizing, selector, eligibility, and portfolio construction remain untouched.
- Outputs are research artifacts only under `artifacts/research` unless an explicit output path is supplied.
