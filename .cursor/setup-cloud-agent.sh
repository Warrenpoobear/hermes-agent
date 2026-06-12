#!/usr/bin/env bash
# Cursor Cloud bootstrap for Hermes development/test sessions.
#
# Keep this focused on agent-readiness: install the repository's existing
# dev extra so scripts/run_tests.sh can run pytest-based tests immediately.

set -euo pipefail

ROOT="${1:-${CURSOR_WORKSPACE:-$(pwd)}}"
cd "$ROOT"

export UV_NO_CONFIG=1

find_uv() {
  if command -v uv >/dev/null 2>&1; then
    command -v uv
  elif [ -x "$HOME/.local/bin/uv" ]; then
    printf '%s\n' "$HOME/.local/bin/uv"
  elif [ -x "$HOME/.cargo/bin/uv" ]; then
    printf '%s\n' "$HOME/.cargo/bin/uv"
  fi
}

UV_CMD="$(find_uv || true)"
if [ -z "$UV_CMD" ]; then
  echo "Installing uv for Cursor Cloud setup..."
  uv_installer="$(mktemp 2>/dev/null || printf '/tmp/hermes-uv-installer.%s.sh' "$$")"
  curl -LsSf https://astral.sh/uv/install.sh -o "$uv_installer"
  sh "$uv_installer"
  rm -f "$uv_installer"
  UV_CMD="$(find_uv || true)"
fi

if [ -z "$UV_CMD" ]; then
  echo "error: uv installer completed but uv was not found" >&2
  exit 1
fi

"$UV_CMD" sync --extra dev

if [ -x "$ROOT/.venv/bin/hermes" ]; then
  "$ROOT/.venv/bin/hermes" --version
else
  "$UV_CMD" run hermes --version
fi
