# Home Assistant / ChatGPT MCP Suite

Self-hosted MCP integration with **separate read-only and narrowly restricted write paths**, plus an optional, separately isolated YAML configuration reader. This repository is a Home Assistant app repository, **not** a complete backup of a deployed installation.

## Verified installation (2026-11-14)

The following versions and running states were queried directly from Home Assistant. Source versions match the app manifests on GitHub.

| Component | Installed version | Observed state | Source |
| --- | --- | --- | --- |
| HA MCP Permissions | 1.0.0 | Running | [ha_mcp_permissions](ha_mcp_permissions/) |
| HA MCP Write Tunnel | 1.0.0 | Running | [ha_mcp_write_tunnel](ha_mcp_write_tunnel/) |
| HA MCP Read Tunnel | 1.0.0 | Running | [ha_mcp_read_tunnel](ha_mcp_read_tunnel/) |
| HA MCP Config Reader | 1.1.1 | **Stopped**; not connected to ChatGPT | [ha_mcp_config_reader](ha_mcp_config_reader/) |
| External Home Assistant MCP Server | 9.2.0 | Running | External integration |
| Old OpenAI MCP Tunnel (local) | 0.1.0 | Stopped; retained for rollback | Former local app |

A running state is not proof of a complete end-to-end authorization or recovery test. The new YAML reader has passed automated repository tests but its live tunnel connection and live file-read behavior remain unverified.

## Architecture

```text
ChatGPT
  |-- Existing read connection --> HA MCP Read Tunnel --> External HA MCP Server
  |                                                       (read-only upstream)
  |
  |-- Restricted write connection --> HA MCP Write Tunnel --> HA MCP Permissions
  |                                                              |
  |                                                              +--> todo.ha_weiterentwicklung only
  |
  +-- Planned YAML reader connection --> [separate tunnel, not provisioned]
                                              |
                                              +--> HA MCP Config Reader (stopped)
                                                    |-- packages/*.yaml
                                                    +-- configuration.yaml
```

The YAML reader does **not** automatically join the existing read tunnel. Its own tunnel and ChatGPT connection must be configured and verified separately before use.

## Restricted write operations

| MCP tool | Home Assistant service |
| --- | --- |
| `list_development_tasks` | `todo.get_items` |
| `add_development_task` | `todo.add_item` |
| `rename_development_task` | `todo.update_item` |
| `complete_development_task` | `todo.update_item` |

The write gateway fixes the target to `todo.ha_weiterentwicklung` and enforces a service allowlist in application code. It does not expose a generic write tool.

## YAML configuration reader (experimental)

Version 1.1.1 supports a private `access_key` (32+ characters) and an allowlist, normally:

```yaml
allowed_files:
  - "packages/*.yaml"
  - "configuration.yaml"
```

The wildcard covers only direct `.yaml` files under `packages/`, not nested directories or `.yml` files. The reader rejects symlinks, path traversal, non-regular files, `secrets.yaml`, oversized files and common secret-like patterns. **Secret detection is heuristic, not a guarantee.** Review the files before connecting the reader, especially the root `configuration.yaml` and any newly added package.

See [Config Reader documentation](ha_mcp_config_reader/DOCS.md) and its [app changelog](ha_mcp_config_reader/CHANGELOG.md).

## Deployment and security

1. Configure the external Home Assistant MCP Server as read-only.
2. Keep read and write tunnel credentials independent and private in Home Assistant app options.
3. Verify the restricted write target and the existing read connection independently.
4. Configure and start the Config Reader only after reviewing its allowlist and secret handling. Its dedicated tunnel/ChatGPT connection remains **outstanding**.
5. Keep protected Home Assistant backups and private copies of credentials. GitHub contains neither runtime secrets nor a proven recovery image.

The write gateway uses `homeassistant_api: true` and receives a privileged Home Assistant token. Its narrow write policy is enforced **in process**, not by a least-privilege Supervisor token. Compromise of the process could bypass this policy.

Never commit or publish access keys, API keys, tunnel IDs, populated options, private endpoint URLs, Supervisor tokens, sensitive logs or backups.

## Testing and release status

GitHub Actions builds the write tunnel and Config Reader images, runs Python unit/policy/runtime tests and checks Git history for secrets. Automated checks passed for the Config Reader 1.1.1 implementation; they do not prove live isolation, backup restoration or tunnel-to-ChatGPT connectivity.

```bash
python -m pip install -r ha_mcp_permissions/requirements.txt -r ha_mcp_config_reader/requirements.txt
python -m compileall -q ha_mcp_permissions/server.py ha_mcp_config_reader/server.py
python -m unittest discover -s tests -v
sh -n ha_mcp_write_tunnel/run.sh
```

The installed apps have their own version numbers. **Do not infer a published suite-wide v1.0.0 release from installed 1.0.0 app versions.** A suite release/tag is gated on outstanding checks documented in [RELEASE.md](RELEASE.md).

See also [central changelog](CHANGELOG.md) and [recovery procedure](RECOVERY.md). The recovery procedure documents intended steps, not a completed restore test.
