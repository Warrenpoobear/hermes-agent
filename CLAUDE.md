# Hermes Agent - Claude Code Guide

This file is the Claude Code entry point for this repository. The canonical,
more complete agent/developer guide is `AGENTS.md`; use it as the source of
truth when details differ.

## Start Here

- Work from the current git branch unless the user asks you to switch.
- Prefer the repo's existing patterns and helper APIs over new abstractions.
- Do not revert unrelated user changes in the working tree.
- Keep edits scoped to the request and the affected subsystem.

## Environment

```bash
source .venv/bin/activate  # or: source venv/bin/activate
```

`scripts/run_tests.sh` is the required test wrapper. It probes `.venv`, `venv`,
and the shared Hermes checkout venv, then runs pytest with CI-like environment
settings.

## Test Commands

```bash
scripts/run_tests.sh
scripts/run_tests.sh tests/gateway/
scripts/run_tests.sh tests/tools/test_delegate.py::TestBlockedTools
.venv/bin/ruff check .
```

Do not call `pytest` directly unless there is no alternative; the wrapper
normalizes credentials, HOME, timezone, locale, and worker count.

## Important Project Invariants

- Profile-aware state paths must use `get_hermes_home()` from
  `hermes_constants`; user-facing path text should use `display_hermes_home()`.
- Tests must not write to a real `~/.hermes/`; use the existing fixtures and set
  `HERMES_HOME` when mocking home directories.
- Prompt caching must not be broken mid-conversation. Slash commands that alter
  tools, skills, memory, or system prompt state should defer invalidation unless
  an explicit `--now` flow exists.
- Built-in tools require both registration in `tools/*.py` and exposure through
  `toolsets.py`.
- Plugin capabilities should use generic plugin hooks/surfaces; do not hardcode
  plugin-specific logic into core files.

## High-Value Files

- `run_agent.py` - `AIAgent`, conversation loop, interrupts, compression.
- `model_tools.py` - tool discovery, schema filtering, function dispatch.
- `toolsets.py` - toolset definitions and platform bundles.
- `cli.py` - classic CLI and slash-command dispatch.
- `gateway/run.py` - messaging gateway runner.
- `hermes_cli/config.py` - default config and config migration.
- `tools/` - built-in tool implementations.
- `plugins/` - plugin systems and bundled plugins.
- `tests/` - pytest suite.

## Recent CI/PR Notes

This branch contains audit fixes around:

- subagent blocked-tool enforcement,
- `AIAgent.close()` cleanup of shared terminal/background resources,
- Google Chat plugin platform registration and Pub/Sub handoff,
- setup-provider config resync,
- gateway runtime env reload authority,
- concurrent interrupt test scaffolding.

When touching these areas, rerun the focused tests listed in the PR body before
committing.
