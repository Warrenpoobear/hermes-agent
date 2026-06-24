from pathlib import Path

import pytest

from scripts.research import reconstruct_ees_v2_composite as recon


def _row():
    return {
        "ees_v2_score": 0.5,
        "z_ees_v2_score": 0.5,
        "z_conditional_gap_score": 1.0,
        "z_conditional_misprice_score": 0.5,
        "z_conditional_base_rate": 0.25,
        "z_conditional_expected_move": 0.75,
        "z_trap_overlay_score": -0.2,
        "z_base_rate_gap_score": -0.4,
    }


def test_variant_score_does_not_mutate_original_ees_score():
    row = _row()
    before = row["ees_v2_score"]

    score = recon.variant_score(row, "positive_components_equal_weight")

    assert score == pytest.approx(0.625)
    assert row["ees_v2_score"] == before
    assert "variant__positive_components_equal_weight" not in row


def test_sign_flip_variant_flips_only_diagnostic_components():
    row = _row()

    score = recon.variant_score(row, "sign_flip_trap_and_base_rate_gap")

    assert score == pytest.approx(0.5 - 2 * (-0.2) - 2 * (-0.4))
    assert row["ees_v2_score"] == 0.5


def test_output_path_guard_allows_only_research_artifacts(tmp_path, monkeypatch):
    project = tmp_path / "repo"
    allowed = project / "artifacts" / "research" / "out.json"
    forbidden = project / "production_data" / "out.json"
    monkeypatch.setattr(recon, "PROJECT_ROOT", project)

    recon._assert_output_path_allowed(allowed)
    with pytest.raises(ValueError):
        recon._assert_output_path_allowed(forbidden)


def test_script_source_has_no_live_data_imports():
    source = Path(recon.__file__).read_text(encoding="utf-8")
    for forbidden in recon._FORBIDDEN_LIVE_IMPORTS:
        assert f"import {forbidden}" not in source
        assert f"from {forbidden}" not in source


def test_reconstruction_module_does_not_import_run_screen_or_production_mutators():
    source = Path(recon.__file__).read_text(encoding="utf-8")
    assert "import run_screen" not in source
    assert "from run_screen" not in source
    assert "final_score" not in "\n".join(
        line for line in source.splitlines() if not line.strip().startswith(("#", "\"", "-"))
    )
    assert "portfolio construction" in source
