# Home Assistant / ChatGPT MCP Suite

Self-hosted MCP integration with **separate read and narrowly restricted write connections**. The only writable Home Assistant entity exposed by the custom write gateway is `todo.ha_weiterentwicklung`.

## Current deployment (2026-11-13)

| Component | Installed version | Status | Source |
| --- | --- | --- | --- |
| HA MCP Permissions | 0.1.4 | Running | [ha_mcp_permissions](ha_mcp_permissions/) |
| HA MCP Write Tunnel | 0.1.1 | Running | [ha_mcp_write_tunnel](ha_mcp_write_tunnel/) |
| HA MCP Read Tunnel | 0.1.1 | Running; GitHub-managed replacement | [ha_mcp_read_tunnel](ha_mcp_read_tunnel/) |
| Home Assistant MCP Server | 9.2.0 | Running, configured as read-only | External integration |
| OpenAI MCP Tunnel (lokal) | 0.1.0 | **Stopped; rollback only** | Former locally installed app |

The GitHub-managed read tunnel has been successfully installed and started with `host_network: false` (Home Assistant app security score observed: 7/8). A Home Assistant read-tool call succeeded after migration. The old local tunnel remains installed but stopped.

> **Release status:** v1.0.0 is planned, not yet tagged or published. A successful installation does not replace security review, disaster-recovery testing or an end-to-end tunnel-path verification.

## Architecture

```text
ChatGPT
  |-- Read connection --> HA MCP Read Tunnel --> Home Assistant MCP Server
  |                                              (read_only_mode=true)
  |
  `-- Write connection --> HA MCP Write Tunnel --> HA MCP Permissions
                                                    |
                                                    `--> todo.ha_weiterentwicklung
```

Both connections use separate tunnel configurations. The write gateway has no general-purpose Home Assistant service tool.

## Allowed write gateway operations

| MCP tool | HA service |
| --- | --- |
| `list_development_tasks` | `todo.get_items` |
| `add_development_task` | `todo.add_item` |
| `rename_development_task` | `todo.update_item` |
| `complete_development_task` | `todo.update_item` |

The entity `todo.ha_weiterentwicklung` is hard-coded server-side. Clients cannot choose another entity, domain, service or upstream URL.

## Setup and recovery

1. Install and configure the external Home Assistant MCP Server with **read-only mode enabled**.
2. Install **HA MCP Permissions** and **HA MCP Write Tunnel** from this app repository. Read [permissions documentation](ha_mcp_permissions/DOCS.md) and [write tunnel documentation](ha_mcp_write_tunnel/DOCS.md).
3. Install **HA MCP Read Tunnel**, configure its read-side tunnel values **only in Home Assistant app options**, and check its read-only upstream. Follow the [migration/rollback guide](ha_mcp_read_tunnel/DOCS.md).
4. Verify the read and write tunnel connections independently; validate the write scope against `todo.ha_weiterentwicklung`.
5. Keep a separate protected backup of Home Assistant app options and credentials. **GitHub is not a backup of runtime secrets.**

The old locally installed read tunnel has deliberately been retained in the stopped state until recovery tests are complete.

## Security model

- The write gateway checks a private `/<access_key>/mcp` route, limits its services, validates inputs and overwrites any client-supplied `entity_id`.
- The write gateway's port is not mapped to the host by default; the write tunnel has no inbound port mapping.
- The read tunnel no longer needs `host_network: true`; its source is at `host_network: false`.
- **Residual privilege risk:** the permissions gateway obtains a powerful Home Assistant Supervisor token (`homeassistant_api: true`). Restrictions are enforced by the gateway application itself, **not** by a least-privileged Supervisor credential. A compromise of this process could bypass its in-process policy.
- No firewall, gateway hardening or source check alone is proof of full security.

**Never publish** API keys, access keys, tunnel IDs, private endpoint URLs, Supervisor tokens, populated `options.json`, app runtime logs or backup archives. Public examples must use placeholders. Before release, examine **all Git history**, not just tracked current files, for exposed secrets.

## Tests

The repository contains tests under `tests/` and a GitHub Actions workflow at [.github/workflows/policy-tests.yml](.github/workflows/policy-tests.yml).

```bash
python -m pip install -r ha_mcp_permissions/requirements.txt
python -m unittest discover -s tests -v
sh -n ha_mcp_read_tunnel/run.sh
sh -n ha_mcp_write_tunnel/run.sh
```

Recent GitHub Actions security-policy runs have succeeded (2026-11-13). Tests use mocked calls and cannot prove the entire live deployment boundary.

See [Recovery and rollback](RECOVERY.md), [Release readiness](RELEASE.md) and [Changelog](CHANGELOG.md). No `v1.0.0` tag has been published.
