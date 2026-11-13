# Recovery runbook – Home Assistant MCP Suite

Last documented operational status: **2026-11-13**. This is a procedure, **not a passed disaster-recovery test**.

## Scope

| App | Source directory | Working version |
| --- | --- | --- |
| HA MCP Permissions | `ha_mcp_permissions/` | 0.1.4 |
| HA MCP Write Tunnel | `ha_mcp_write_tunnel/` | 0.1.1 |
| HA MCP Read Tunnel | `ha_mcp_read_tunnel/` | 0.1.1 |

External dependency: Home Assistant MCP Server 9.2.0, configured `read_only_mode: true`. The old local read tunnel v0.1.0 remains **stopped** and is not part of the GitHub-managed suite.

## What must be backed up outside GitHub

- A protected Home Assistant backup containing app data and configuration, including the MCP app options, stored according to the household's backup policy.
- Separate securely stored tunnel IDs, API keys, access-key secret and private MCP endpoints. The **complete private MCP URL is confidential**.
- A note of how the OpenAI tunnel connections are configured and identified; don't publish their identifiers.
- The version of the upstream Home Assistant MCP Server and the Home Assistant Core/OS versions used.

Do not put credentials, populated `options.json`, private URLs or backups into GitHub, issues or logs. A Git clone alone **cannot** restore a working deployment.

## Initial recovery

1. Recover Home Assistant OS and app data from a verified backup.
2. Restore the external Home Assistant MCP Server; confirm it is `read_only_mode=true`.
3. Add the existing repository `https://github.com/ChrisTinkers/ha-mcp-permissions` to the Home Assistant App Store and refresh its catalog.
4. Install HA MCP Permissions first. Supply the original `access_key` **privately in the app options**; do not enable its TCP port on the host. Confirm its fixed `todo.ha_weiterentwicklung` target and the four expected MCP tools.
5. Install HA MCP Write Tunnel and configure its tunnel ID, API key and internal MCP URL privately; the internal target is the Permissions app's hostname, not a user-selectable arbitrary service.
6. Install HA MCP Read Tunnel and configure its independent read-tunnel ID, API key and internal URL to the external **read-only** MCP Server. Keep `host_network: false`.
7. Do not run the old local tunnel and the new read tunnel simultaneously with the same tunnel ID.
8. Test read access and the allowed to-do operations independently; confirm other entities and services cannot be written through the write gateway.
9. Confirm no external router port forwarding and review UPnP/firewall policies.
10. Verify logs for connection errors without sharing or publishing secret-bearing values.

## Rollback

- If the **new read tunnel** fails, stop it before starting the old stopped local read tunnel. Check that its original credentials remain safely stored. Verify read-only access before considering removal of the new app.
- If the **write tunnel** fails, stop only the write tunnel; leave the existing read connection active. Restore the previous working write-tunnel version and private settings.
- If the **permissions gateway** fails, disable the write tunnel and restore the previously tested gateway version. Do not replace it with a generic writable MCP server.

## Release gate

A dry-run or full fresh restore has **not yet been completed**. A successful app status or single read call does not prove a full recovery. Before v1.0.0, perform a safe backup/restore test, check deployed-image provenance, test read and write paths end-to-end, and validate authorization denial without affecting unrelated entities.
