#!/usr/bin/env python3
"""Skill execution logging with redaction, environment tagging, and safety guards.

Ported from the biotech-screener repo. Hermes adaptation:
- Default logs_dir: get_hermes_home() / "skills_learning" (respects HERMES_HOME)
- Zero biotech-specific imports; stdlib only (plus hermes_constants).

Features:
- Automatic PII/sensitive data scrubbing before logging
- Environment tagging (test vs production)
- Minimum sample-size rules (5+ executions before skill evaluation)
- Advisory-only recommendations (no auto-apply)
- One-week observation before routing changes
"""

import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Patterns for redaction (PII, credentials, internal IDs)
REDACT_PATTERNS = [
    (r"(api[_-]?key|apikey|token|password)\s*[:=]\s*['\"]?[^\s'\"]+", "[REDACTED_KEY]"),
    (r"(email|from|to)\s*[:=]\s*[\w\.-]+@[\w\.-]+", "[REDACTED_EMAIL]"),
    (r"(ticker|symbol)\s*[:=]\s*[A-Z]{1,5}", "[REDACTED_TICKER]"),
    (r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b", "[REDACTED_DATE]"),
    (r"(\d{1,3}\.){3}\d{1,3}", "[REDACTED_IP]"),
    (r"authorization\s*[:=]\s*Bearer\s+\S+", "[REDACTED_AUTH]"),
]


def scrub_sensitive_data(text: str) -> str:
    """Redact PII and credentials from text."""
    if not isinstance(text, str):
        return text
    result = text
    for pattern, replacement in REDACT_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def scrub_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively scrub sensitive data from dict values."""
    if not isinstance(data, dict):
        return data
    scrubbed = {}
    for key, value in data.items():
        if isinstance(value, str):
            scrubbed[key] = scrub_sensitive_data(value)
        elif isinstance(value, dict):
            scrubbed[key] = scrub_dict(value)
        elif isinstance(value, list):
            scrubbed[key] = [
                scrub_dict(v)
                if isinstance(v, dict)
                else scrub_sensitive_data(v)
                if isinstance(v, str)
                else v
                for v in value
            ]
        else:
            scrubbed[key] = value
    return scrubbed


def _default_logs_dir() -> Path:
    """Return the default ledger directory, respecting HERMES_HOME override."""
    try:
        from hermes_constants import get_hermes_home

        return get_hermes_home() / "skills_learning"
    except Exception:
        return Path.home() / ".hermes" / "skills_learning"


class SkillExecutionLoggerV2:
    """Log skill executions with redaction, environment tagging, and safety guards."""

    def __init__(self, logs_dir: Optional[Path] = None):
        self.logs_dir = Path(logs_dir) if logs_dir is not None else _default_logs_dir()
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def log_execution(
        self,
        skill_name: str,
        task_context: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        latency_ms: float,
        tokens_in: int = 0,
        tokens_out: int = 0,
        cost_usd: float = 0.0,
        success: bool = True,
        error: Optional[str] = None,
        environment: str = "prod",
    ) -> str:
        """Log a skill execution with redaction and environment tagging.

        Returns:
            execution_id (for later feedback)
        """
        exec_id = str(uuid.uuid4())[:8]

        task_context_scrubbed = scrub_sensitive_data(task_context)
        inputs_scrubbed = scrub_dict(inputs)
        outputs_scrubbed = scrub_dict(outputs)
        error_scrubbed = scrub_sensitive_data(error) if error else None

        record = {
            "execution_id": exec_id,
            "skill_name": skill_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "environment": environment,
            "task_context": task_context_scrubbed,
            "inputs": inputs_scrubbed,
            "outputs": outputs_scrubbed,
            "metrics": {
                "latency_ms": latency_ms,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "cost_usd": cost_usd,
            },
            "outcome": {
                "success": success,
                "error": error_scrubbed,
                "user_feedback": None,
            },
        }

        month_str = datetime.utcnow().strftime("%Y-%m")
        log_file = self.logs_dir / f"execution_log_{environment}_{month_str}.jsonl"

        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(record) + "\n")
        except OSError as e:
            print(f"Warning: Could not log skill execution: {e}")

        return exec_id

    def record_feedback(
        self,
        execution_id: str,
        verdict: str,
        notes: str = "",
        environment: str = "prod",
    ) -> None:
        """Record feedback on a previous execution."""
        feedback = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "execution_id": execution_id,
            "verdict": verdict,
            "notes": scrub_sensitive_data(notes),
            "environment": environment,
        }

        month_str = datetime.utcnow().strftime("%Y-%m")
        log_file = self.logs_dir / f"feedback_log_{environment}_{month_str}.jsonl"

        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(feedback) + "\n")
        except OSError as e:
            print(f"Warning: Could not record feedback: {e}")


# Module-level singleton — lazily initialized so HERMES_HOME is read at
# first use, not at import time (important for test isolation via conftest).
_skill_logger: Optional[SkillExecutionLoggerV2] = None


def get_logger() -> SkillExecutionLoggerV2:
    """Get or create the module-level logger instance."""
    global _skill_logger
    if _skill_logger is None:
        _skill_logger = SkillExecutionLoggerV2()
    return _skill_logger


def reset_logger() -> None:
    """Reset the module-level singleton (test helper)."""
    global _skill_logger
    _skill_logger = None


def log_skill(
    skill_name: str,
    task_context: str,
    inputs: Dict[str, Any],
    outputs: Dict[str, Any],
    latency_ms: float,
    tokens_in: int = 0,
    tokens_out: int = 0,
    cost_usd: float = 0.0,
    success: bool = True,
    error: Optional[str] = None,
    environment: str = "prod",
) -> str:
    """Log a skill execution. Returns execution_id for later feedback."""
    return get_logger().log_execution(
        skill_name=skill_name,
        task_context=task_context,
        inputs=inputs,
        outputs=outputs,
        latency_ms=latency_ms,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost_usd=cost_usd,
        success=success,
        error=error,
        environment=environment,
    )


def record_feedback(
    execution_id: str, verdict: str, notes: str = "", environment: str = "prod"
) -> None:
    """Record feedback on a skill execution."""
    get_logger().record_feedback(execution_id, verdict, notes, environment)
