from unittest.mock import MagicMock, patch

from run_agent import AIAgent


def test_close_cleans_current_session_and_resolved_terminal_task_ids():
    agent = AIAgent.__new__(AIAgent)
    agent.session_id = "session-123"
    agent._current_task_id = "turn-456"
    agent._active_children_lock = MagicMock()
    agent._active_children_lock.__enter__.return_value = None
    agent._active_children_lock.__exit__.return_value = None
    agent._active_children = []
    agent.client = None

    killed = []
    cleaned_vm = []
    cleaned_browser = []
    registry = MagicMock()
    registry.kill_all.side_effect = lambda task_id=None: killed.append(task_id) or 0

    with (
        patch("tools.process_registry.process_registry", registry),
        patch("run_agent.cleanup_vm", side_effect=lambda task_id: cleaned_vm.append(task_id)),
        patch("run_agent.cleanup_browser", side_effect=lambda task_id: cleaned_browser.append(task_id)),
        patch("tools.terminal_tool._resolve_container_task_id", return_value="default"),
    ):
        agent.close()

    assert killed == ["turn-456", "session-123", "default"]
    assert cleaned_vm == ["turn-456", "session-123", "default"]
    assert cleaned_browser == ["turn-456", "session-123", "default"]
