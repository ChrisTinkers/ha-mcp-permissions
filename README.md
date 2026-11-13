# Home Assistant / ChatGPT MCP suite

A self-hosted Home Assistant MCP setup with **separate read-only and narrowly scoped write connections**. The write gateway manages **only** `todo.ha_weiterentwicklung`.

> **Status (2026-11-13):** All three tunnel/gateway apps are installed and running. The local read tunnel's three source files have now been reconstructed from the running system and are tracked. Its start script uses confirmed `bashio::config` sources, but the exact three original assignment lines have not yet been compared byte-for-byte; deployment parity and a clean-install test remain open. Version 1.0.0 is proposed but **not yet released**.

## Architecture

```text
ChatGPT
  |-- Read connection --> OpenAI MCP Tunnel (lokal) --> HA MCP Server 9.2.0
  |                                                (read_only_mode=true)
  |
  `-- Write connection --> HA MCP Write Tunnel --> HA MCP Permissions
                                                    |
                                                    `--> todo.ha_weiterentwicklung
```

Both connections are independent. No generic Home Assistant service caller is exposed by the write gateway.

## Components

| App | Source | Installed version (2026-11-13) | Role |
| --- | --- | --- | --- |
| HA MCP Permissions | [ha_mcp_permissions/](ha_mcp_permissions/) | 0.1.4 | Restricts write operations to one to-do list |
| HA MCP Write Tunnel | [ha_mcp_write_tunnel/](ha_mcp_write_tunnel/) | 0.1.1 | Dedicated OpenAI tunnel to the limited gateway |
| OpenAI MCP Tunnel (lokal) | [openai_mcp_tunnel_local/](openai_mcp_tunnel_local/); [verification notes](LOCAL_READ_TUNNEL.md) | 0.1.0 | Local tunnel to the existing read-only MCP server |
| Home Assistant MCP Server | External dependency | 9.2.0 | Existing read-only MCP integration |

Installed component versions are independent; there is not yet a unified 1.0 release.

## Approved operations

The write gateway exposes exactly four tools:

- `list_development_tasks`: `todo.get_items`
- `add_development_task`: `todo.add_item`
- `rename_development_task`: `todo.update_item` with a new name
- `complete_development_task`: `todo.update_item` with completed status

The target `todo.ha_weiterentwicklung` is hard-coded. Users cannot provide another entity, domain, service or arbitrary URL. The server imposes input validation and a fixed service allowlist.

## Installation and recovery

1. Install and verify the upstream Home Assistant MCP Server in `read_only_mode=true`.
2. The local read tunnel's source is now tracked in sanitized form. Its exact start-script equivalence and restore procedure still require [verification](LOCAL_READ_TUNNEL.md).
3. Add this repository to the Home Assistant app store and install HA MCP Permissions and HA MCP Write Tunnel.
4. Follow the [permissions app notes](ha_mcp_permissions/DOCS.md) and [write tunnel notes](ha_mcp_write_tunnel/DOCS.md). Configure credentials only in Home Assistant's local app options.
5. Confirm the four write tools operate exclusively on the development to-do list; verify denial of other actions and entities.
6. Maintain a separate secure backup of local configuration, credentials and app data. GitHub does **not** replace a secret-bearing backup.

Default configuration does not publish the permission gateway's port to the host (`8765/tcp: null`), and the write tunnel exposes no incoming port. Never add a router port forward to the MCP gateway.

## Security and limitations

- Only requests to the secret `/<access_key>/mcp` path reach the gateway. **The complete URL is itself a secret.**
- The write tunnel restricts its upstream to the internal permissions app hostname.
- **Important residual risk:** HA MCP Permissions has a privileged Supervisor-issued Home Assistant API token. Scope restrictions are enforced by application code, not a separately scoped Home Assistant credential. A compromised container could theoretically exceed its intended scope.
- Code review and mocked tests are not proof that a deployed container matches the repository or that the deployment is free of vulnerabilities.
- Review and pin dependencies and base images, rotate previously exposed tokens and perform live negative tests before a 1.0 release.

**Never commit or publish** `access_key`, `api_key`, Supervisor tokens, tunnel credentials, complete secret MCP URLs, `options.json`, `.env`, logs containing secrets or Home Assistant backups. Use placeholders such as `YOUR_ACCESS_KEY` in examples. Also review Git history, not just current files.

## Automated checks

```bash
python -m pip install -r ha_mcp_permissions/requirements.txt
python -m unittest discover -s tests -v
sh -n ha_mcp_write_tunnel/run.sh
```

CI is configured in [policy-tests.yml](.github/workflows/policy-tests.yml). Mock tests complement but do not replace live validation.

**Live observations on 2026-11-13:** three relevant apps running, four write tools exposed and exercised successfully. Server-side restrictions are supported by source review and tests, but exact deployed-image correspondence is not yet proven.

## Roadmap to 1.0.0

See [RELEASE.md](RELEASE.md). Before publishing 1.0.0, verify the reconstructed local read tunnel source against the running instance, align app versions/build metadata, run security/history checks, verify fresh installation and backup recovery, and perform live authorization-denial tests.

New write scopes must be implemented as separately reviewed, narrowly constrained capabilities — never as unrestricted Home Assistant service calls.

Maintained by [ChrisTinkers](https://github.com/ChrisTinkers).
