# HA MCP Write Tunnel

Installed version verified on 2026-11-13: **0.1.1**, running.

This app connects the separate **restricted write MCP gateway** to an OpenAI tunnel. It does not replace the existing local read-only tunnel.

## Configuration (local only)

The Home Assistant app requires:

- `tunnel_id`: tunnel identifier provided for this write connection
- `api_key`: runtime tunnel credential
- `mcp_url`: private upstream URL for HA MCP Permissions

**Never commit these values.** Do not paste the complete `mcp_url` into a public issue or screenshot: its path includes an access credential.

The startup script accepts only the internal gateway host `9cf2e9bf-ha-mcp-permissions` on port `8765` and a URL ending in `/mcp`. The actual secret path belongs exclusively in local app options.

This app has `ports: {}` and does not request Home Assistant Core or Supervisor API access. OAuth metadata discovery is disabled for this secret-path backend.

## Security and operations

- No public port forwarding.
- Keep the read and write tunnels separate and independently revocable.
- Rotate credentials after suspected exposure.
- Review changes to `run.sh` and the pinned tunnel-client image before upgrading.
- Reconfirm four-tool availability after upgrades.
- The upstream Permissions app still has a privileged Supervisor-issued token; see [its security model](../ha_mcp_permissions/DOCS.md).

See [release checklist](../RELEASE.md). A running service is not proof of authorization isolation or a tested recovery.
