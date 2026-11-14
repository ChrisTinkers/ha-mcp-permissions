# HA MCP Config Tunnel 1.0.0

Separate OpenAI Secure MCP tunnel for the **HA MCP Config Reader**. This app
does not change either existing read or write tunnel.

## Installation and setup

1. Install this app from the existing GitHub Home Assistant app repository.
2. Create a **new** tunnel/ChatGPT connection with a new tunnel ID and API key.
   Never reuse credentials of an existing read or write tunnel.
3. Enter the new `tunnel_id` and `api_key` only in the private app options.
4. Set `mcp_url` to
   `http://9cf2e9bf-ha-mcp-config-reader:8766/<reader-access-key>/mcp`.
   Replace the placeholder privately with the existing 32+-character Config
   Reader `access_key`. The complete URL is confidential.
5. Save and start the tunnel. Check logs without sharing secrets.
6. Connect the new tunnel to ChatGPT. Test `list_config_files`, reading a
   reviewed harmless YAML file, and denial of unlisted files.

The launcher accepts only the fixed internal Config Reader host and port
with a single URL-path key of at least 32 characters. This is an application
routing check, not a network firewall or complete security proof.

## Security

- `host_network: false`; no published ports or HA/Supervisor API access.
- Independent credentials and manually controlled initial startup.
- The official tunnel-client-runtime v0.0.19 download is SHA-256 verified.
- The Config Reader still uses a read-only configuration mount and file
  allowlist. Its secret detection is heuristic and cannot guarantee that
  sensitive content is absent. Review YAML before connecting ChatGPT.
- Installing the app does not itself create a ChatGPT tunnel connection.

## Rollback

Stop this new tunnel and disconnect its ChatGPT connection. Existing
read/write tunnels and the Config Reader need no changes.
