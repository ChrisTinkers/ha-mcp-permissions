# Changelog

All notable changes to the Home Assistant / ChatGPT MCP Suite are recorded here. App versions are independent until the first suite release.

## 1.0.0 — Release candidate (not published)

The first unified version is prepared in source control; production installations remain on their last tested versions until the final acceptance checks. A tag or GitHub release is deliberately withheld pending remaining verification.

### Release preparation
- Set all three Home Assistant app manifests and Docker build defaults to version 1.0.0.
- Added automated version-consistency test.
- No runtime or permissions changes intended.

## Pre-release history — 2026-11-13

- Documented three-part architecture: read tunnel, restricted permissions gateway and separate write tunnel.
- Migrated the read tunnel from a local Home Assistant app to the GitHub-managed **HA MCP Read Tunnel**, version **0.1.1**.
- Disabled host networking on the new read tunnel; Home Assistant security score observed at 7/8.
- Verified new read tunnel is running and the old locally installed tunnel is stopped.
- Documented migration, rollback, sensitive configuration handling and a detailed release acceptance checklist.
- Full security review, restore test, consistent version bump and release tag remain outstanding.

## Previously deployed app versions (2026-11-13)

### HA MCP Permissions 0.1.4
- Four scoped to-do list tools for `todo.ha_weiterentwicklung`.
- Fixed entity, restricted service allowlist, input validation and private route guard.
- Home Assistant service-call correction for write actions.

### HA MCP Write Tunnel 0.1.1
- Separate write-side tunnel app using fixed internal permissions server host.
- OAuth discovery disabled for backend using a private access-key route.

### HA MCP Read Tunnel 0.1.1
- GitHub-managed replacement for the former local app.
- Client runtime v0.0.19 download with SHA-256 verification.
- `host_network: false`; app slug `ha_mcp_read_tunnel`.

No stable `v1.0.0` tag has been published.
