# Home Assistant / ChatGPT MCP Suite

Self-hosted MCP integration with **separate read-only and narrowly restricted write paths**, plus an optional, separately isolated YAML configuration reader. This repository is a Home Assistant app repository, **not** a complete backup of a deployed installation.

## Verified installation (2026-11-14)

The following versions and running states were queried directly from Home Assistant. Source versions match the app manifests on GitHub.

| Component | Installed version | Observed state | Source |
| --- | --- | --- | --- |
| HA MCP Permissions | 1.0.0 | Running | [ha_mcp_permissions](ha_mcp_permissions/) |
| HA MCP Write Tunnel | 1.0.0 | Running; restricted task list read passed | [ha_mcp_write_tunnel](ha_mcp_write_tunnel/) |
| HA MCP Read Tunnel | 1.0.2 | Running; live state read passed | [ha_mcp_read_tunnel](ha_mcp_read_tunnel/) |
| HA MCP Config Reader | 1.1.3 | Running; allowed YAML read passed | [ha_mcp_config_reader](ha_mcp_config_reader/) |
| HA MCP Config Tunnel | 1.0.0 | Running; connected to Config Reader | [ha_mcp_config_tunnel](ha_mcp_config_tunnel/) |
| External Home Assistant MCP Server | 9.2.0 | Running | External integration |
| Old OpenAI MCP Tunnel (local) | 0.1.0 | Stopped; retained for rollback | Former local app |

Observed live smoke tests: the general read connector returned the state of `sun.sun`; the restricted write connector listed items from `todo.ha_weiterentwicklung` without mutation; the Config Reader listed approved files and returned the content of `packages/pollenflug.yaml`. A request for `secrets.yaml` was rejected. These tests do **not** establish comprehensive write authorization, credential isolation, recovery, or deployed-image provenance.

## Architecture

```text
ChatGPT
  |-- HA MCP Read Tunnel (1.0.2) --> Home Assistant MCP Server (9.2.0)
  |                                      read-only mode
  |
  |-- HA MCP Write Tunnel (1.0.0) --> HA MCP Permissions (1.0.0)
  |                                      todo.ha_weiterentwicklung only
  |
  +-- HA MCP Config Tunnel (1.0.0) --> HA MCP Config Reader (1.1.3)
                                         packages/*.yaml
                                         configuration.yaml
```

All three tunnels are separate and running. The user confirmed separate OpenAI API keys for each; secret values cannot be independently compared because Home Assistant masks them. The read tunnel validates its internal target as `http://81f33d0f-ha-mcp:9583/<secret-path>` (the secret path is already the complete endpoint; do not append `/mcp`). Never publish the actual secret path.

