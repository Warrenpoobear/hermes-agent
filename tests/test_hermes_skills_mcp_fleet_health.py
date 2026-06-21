"""Fleet health snapshot tests for registry-only and inactive-agent handling."""

import json
from datetime import datetime, timedelta, timezone

import pytest


@pytest.fixture
def snapshot_env(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    home = tmp_path / "home"
    repo.mkdir()
    home.mkdir()
    monkeypatch.setenv("HERMES_REPO", str(repo))
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.delenv("HERMES_AGENTS_DIR", raising=False)

    import hermes_skills_mcp as mcp

    monkeypatch.setattr(mcp, "_gateway_reachable", lambda: False)
    return repo, home, mcp


def _write_registry(agents_dir, entries: dict) -> None:
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "AGENT_REGISTRY.json").write_text(
        json.dumps(entries, indent=2),
        encoding="utf-8",
    )


def _write_learnings(repo):
    learnings = repo / ".learnings"
    learnings.mkdir()
    (learnings / "memory.md").write_text("# Memory\n", encoding="utf-8")


def _write_knowledge(repo):
    knowledge = repo / "artifacts" / "ops" / "knowledge_layer"
    knowledge.mkdir(parents=True)
    (knowledge / "latest_state.md").write_text("# Latest State\n", encoding="utf-8")
    held = repo / "artifacts" / "ops" / "held_spec_ledger"
    held.mkdir(parents=True)
    (held / "latest.md").write_text(
        "# Held Specification Ledger\n\n- HELD: example constraint\n",
        encoding="utf-8",
    )


def test_registry_only_skips_stale_heartbeat_false_alarms(snapshot_env):
    repo, _home, mcp = snapshot_env
    agents_dir = repo / "agents"
    _write_registry(
        agents_dir,
        {
            "herald": {
                "lane": "A",
                "status": "active",
                "authority": "write_artifacts",
            },
            "bioshort_watch": {
                "lane": "B",
                "status": "deprecated",
                "suppressed": True,
                "authority": "observe_only",
            },
        },
    )
    _write_learnings(repo)
    _write_knowledge(repo)

    snapshot = mcp.build_fleet_context_snapshot(summary=True)
    health = mcp.build_agent_health_summary()

    assert snapshot["registry_only"] is True
    assert snapshot["stale_heartbeats"] == []
    assert health["status"] == "ok"
    assert health["registry_only"] is True
    assert any("registry-only" in w for w in health["warnings"])


def test_inactive_agents_excluded_from_heartbeat_checks(snapshot_env):
    repo, _home, mcp = snapshot_env
    agents_dir = repo / "agents"
    _write_registry(
        agents_dir,
        {
            "herald": {
                "lane": "A",
                "status": "active",
                "authority": "write_artifacts",
            },
            "company_news_ingest": {
                "lane": "B",
                "status": "deprecated",
                "retired": True,
                "authority": "write_artifacts",
            },
            "shadow_watch": {
                "lane": "B",
                "status": "shadow",
                "suppressed": True,
                "authority": "observe_only",
            },
        },
    )
    herald_dir = agents_dir / "herald"
    herald_dir.mkdir(parents=True)
    (herald_dir / "HEARTBEAT.md").write_text("ok\n", encoding="utf-8")
    _write_learnings(repo)
    _write_knowledge(repo)

    snapshot = mcp.build_fleet_context_snapshot(summary=True)

    assert snapshot["registry_only"] is False
    assert snapshot["stale_heartbeats"] == []


def test_stale_active_agent_reported_when_runtime_present(snapshot_env):
    repo, _home, mcp = snapshot_env
    agents_dir = repo / "agents"
    _write_registry(
        agents_dir,
        {
            "herald": {
                "lane": "A",
                "status": "active",
                "authority": "write_artifacts",
            },
        },
    )
    herald_dir = agents_dir / "herald"
    herald_dir.mkdir(parents=True)
    heartbeat = herald_dir / "HEARTBEAT.md"
    heartbeat.write_text("stale\n", encoding="utf-8")
    stale_time = datetime.now(timezone.utc) - timedelta(days=2)
    heartbeat.touch()
    import os

    os.utime(heartbeat, (stale_time.timestamp(), stale_time.timestamp()))
    _write_learnings(repo)
    _write_knowledge(repo)

    snapshot = mcp.build_fleet_context_snapshot(summary=True)
    health = mcp.build_agent_health_summary()

    assert len(snapshot["stale_heartbeats"]) == 1
    assert snapshot["stale_heartbeats"][0]["agent"] == "herald"
    assert snapshot["stale_heartbeats"][0]["status"] == "stale"
    assert health["status"] == "attention"


def test_held_specs_do_not_count_as_health_anomalies(snapshot_env):
    repo, _home, mcp = snapshot_env
    agents_dir = repo / "agents"
    _write_registry(
        agents_dir,
        {
            "herald": {
                "lane": "A",
                "status": "active",
                "authority": "write_artifacts",
            },
        },
    )
    _write_learnings(repo)
    _write_knowledge(repo)

    health = mcp.build_agent_health_summary()
    brief = mcp.build_town_brief()

    assert health["status"] == "ok"
    assert health["held_spec_flags_count"] >= 1
    assert brief["status"] == "ok"
    assert any(issue["kind"] == "held_specs" for issue in brief["active_issues"])
