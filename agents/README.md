# Agent Registry

This directory is intentionally registry-first in this checkout.

`AGENT_REGISTRY.json` is the local source of truth for the Hermes fleet index:
agent names, descriptions, lanes, tiers, authorities, status, cron metadata, and
dependencies.

Runtime identity documents such as `SOUL.md`, `IDENTITY.md`, and `HEARTBEAT.md`
are not checked in here by default. Tools that need those files should read them
from a mounted runtime directory such as `HERMES_AGENTS_DIR`, then fall back to
`agents/<name>/` only if those files are actually present.

Do not generate placeholder identity layers from registry metadata. The registry
can describe what an agent is allowed to do, but it cannot replace the canonical
runtime identity contract.

When editing `AGENT_REGISTRY.json`, keep all declared dependencies resolvable to
other registry entries unless the dependency is intentionally external and that
exception is documented with the change.
