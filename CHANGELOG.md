# Changelog — Home Assistant / ChatGPT MCP Suite

Each Home Assistant app has its **own version**. The versions below are app versions, not a suite-wide release. The currently installed state was checked live on 2026-11-14.

## 2026-11-14 — Three MCP connections verified

- **HA MCP Read Tunnel 1.0.2:** corrected upstream URL validation to the Home Assistant MCP Server's complete secret-path endpoint (without a trailing `/mcp`); restricts the upstream to the internal host and port. Running; live `sun.sun` state read passed.
- **HA MCP Write Tunnel 1.0.0 / HA MCP Permissions 1.0.0:** running; listing tasks from the restricted `todo.ha_weiterentwicklung` succeeded without changes. No new write-operation test was performed.
- **HA MCP Config Tunnel 1.0.0 / Config Reader 1.1.3:** running; approved file listing and content read for `packages/pollenflug.yaml` passed. Attempt to read `secrets.yaml` was rejected.
- **Config Reader 1.1.2:** fixed read-only Home Assistant configuration directory mapping. **1.1.3:** changed file-read tool output to plain MCP text, resolving empty content responses.
- Three distinct tunnel IDs were observed; the user confirmed three separate API keys. Key equality cannot be independently verified from masked app options.
- The earlier 1.0.1 Read Tunnel URL restriction incorrectly required `/mcp`, causing an incompatible path requirement; fixed in 1.0.2.
- No suite-wide release/tag, complete write-permission penetration test, container provenance attestation, or backup restore is claimed.

## 2026-11-14 — Config Reader 1.1.1

- Added read-only access to direct `packages/*.yaml` files and `configuration.yaml`.
- Improved filename, path and symlink restrictions, plus heuristic credential detection.
- Added/extended automated reader tests and verified successful CI checks for the implementation.
- Added an app-specific [CHANGELOG.md](ha_mcp_config_reader/CHANGELOG.md).
- Historical status at that point: Config Reader **1.1.1 installed but stopped**; dedicated tunnel was not yet provisioned. See the newer verified deployment above.

## 2026-11-14 — Config Reader 1.1.0

- Introduced the separately installed, read-only YAML MCP server with explicit package-file allowlisting, private access key and file-size limit.
- Initial 1.1.0 installation was kept stopped while the wildcard/root-file enhancement was developed.

## Initial core app versions — 1.0.0

- HA MCP Permissions: restricted to four operations on `todo.ha_weiterentwicklung`.
- HA MCP Write Tunnel: separate connection to the restricted permissions gateway.
- HA MCP Read Tunnel: separate connection to the external read-only Home Assistant MCP Server.
- Home Assistant reported all three apps running on 2026-11-14.

## 2026-11-13 — Earlier deployment and release preparation

- Migrated the read tunnel from a local Home Assistant app to a GitHub-managed app, with host networking disabled.
- Kept the old local tunnel stopped as a rollback option.
- Added policy, service-scope and runtime tests, recovery guidance and a release acceptance checklist.
- Prepared 1.0.0 versions for the three core apps; these versions are now installed. **No suite-wide v1.0.0 GitHub release/tag is asserted here.**

## Historical versions

- Permissions 0.1.4: four scoped to-do tools and restricted service/entity handling.
- Write Tunnel 0.1.1: separate tunnel for the permissions gateway.
- Read Tunnel 0.1.1: GitHub-managed replacement of the local tunnel, without host networking.

**Release caveat:** successful CI and running apps are not equivalent to an independently verified security boundary or tested disaster recovery. See [RELEASE.md](RELEASE.md).
