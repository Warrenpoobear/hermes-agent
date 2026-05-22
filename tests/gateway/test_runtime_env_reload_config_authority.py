"""Regression tests for gateway per-turn env reload preserving config authority.

Issue #19158: startup bridges config.yaml agent.max_turns into
HERMES_MAX_ITERATIONS, but a later per-turn load_dotenv(..., override=True)
can restore a stale .env HERMES_MAX_ITERATIONS value before the next turn.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from gateway import run as gateway_run


def test_reload_runtime_env_preserves_config_max_turns(tmp_path: Path, monkeypatch) -> None:
    hermes_home = tmp_path / ".hermes"
    hermes_home.mkdir()
    (hermes_home / "config.yaml").write_text(
        yaml.safe_dump({"agent": {"max_turns": 9000}}),
        encoding="utf-8",
    )
    (hermes_home / ".env").write_text(
        "HERMES_MAX_ITERATIONS=90\nOPENROUTER_API_KEY=fresh-key\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(gateway_run, "_hermes_home", hermes_home)
    monkeypatch.setenv("HERMES_MAX_ITERATIONS", "9000")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    gateway_run._reload_runtime_env_preserving_config_authority()

    assert os.environ["OPENROUTER_API_KEY"] == "fresh-key"
    assert os.environ["HERMES_MAX_ITERATIONS"] == "9000"


def test_reload_runtime_env_reapplies_all_gateway_config_bridges(
    tmp_path: Path, monkeypatch
) -> None:
    hermes_home = tmp_path / ".hermes"
    hermes_home.mkdir()
    (hermes_home / "config.yaml").write_text(
        yaml.safe_dump(
            {
                "agent": {
                    "gateway_timeout": 321,
                    "gateway_timeout_warning": 123,
                    "gateway_notify_interval": 45,
                    "restart_drain_timeout": 67,
                    "gateway_auto_continue_freshness": 89,
                },
                "display": {
                    "busy_input_mode": "queue",
                    "busy_ack_enabled": False,
                },
                "timezone": "UTC",
                "security": {"redact_secrets": False},
            }
        ),
        encoding="utf-8",
    )
    (hermes_home / ".env").write_text(
        "\n".join(
            [
                "HERMES_AGENT_TIMEOUT=1",
                "HERMES_AGENT_TIMEOUT_WARNING=2",
                "HERMES_AGENT_NOTIFY_INTERVAL=3",
                "HERMES_RESTART_DRAIN_TIMEOUT=4",
                "HERMES_AUTO_CONTINUE_FRESHNESS=5",
                "HERMES_GATEWAY_BUSY_INPUT_MODE=interrupt",
                "HERMES_GATEWAY_BUSY_ACK_ENABLED=true",
                "HERMES_TIMEZONE=America/Los_Angeles",
                "HERMES_REDACT_SECRETS=true",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(gateway_run, "_hermes_home", hermes_home)

    gateway_run._reload_runtime_env_preserving_config_authority()

    assert os.environ["HERMES_AGENT_TIMEOUT"] == "321"
    assert os.environ["HERMES_AGENT_TIMEOUT_WARNING"] == "123"
    assert os.environ["HERMES_AGENT_NOTIFY_INTERVAL"] == "45"
    assert os.environ["HERMES_RESTART_DRAIN_TIMEOUT"] == "67"
    assert os.environ["HERMES_AUTO_CONTINUE_FRESHNESS"] == "89"
    assert os.environ["HERMES_GATEWAY_BUSY_INPUT_MODE"] == "queue"
    assert os.environ["HERMES_GATEWAY_BUSY_ACK_ENABLED"] == "False"
    assert os.environ["HERMES_TIMEZONE"] == "UTC"
    assert os.environ["HERMES_REDACT_SECRETS"] == "false"


def test_reload_runtime_env_keeps_env_max_iterations_when_config_omits_key(
    tmp_path: Path, monkeypatch
) -> None:
    hermes_home = tmp_path / ".hermes"
    hermes_home.mkdir()
    (hermes_home / "config.yaml").write_text(yaml.safe_dump({"agent": {}}), encoding="utf-8")
    (hermes_home / ".env").write_text("HERMES_MAX_ITERATIONS=123\n", encoding="utf-8")

    monkeypatch.setattr(gateway_run, "_hermes_home", hermes_home)
    monkeypatch.delenv("HERMES_MAX_ITERATIONS", raising=False)

    gateway_run._reload_runtime_env_preserving_config_authority()

    assert os.environ["HERMES_MAX_ITERATIONS"] == "123"
