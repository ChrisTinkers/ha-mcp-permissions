# HA MCP Read Tunnel

Repository-managed replacement for the previously local **OpenAI MCP Tunnel (lokal)**.

**Migration status:** Source prepared; **not yet installed or cut over**. The old local app stays active until the new app is installed, its credentials are entered locally, and read-only operation is confirmed.

## Purpose

Connect the existing Home Assistant MCP Server (`read_only_mode=true`) to the OpenAI MCP tunnel. This is the **read** side only; the separate [write tunnel](../ha_mcp_write_tunnel/) connects to the restricted [permissions gateway](../ha_mcp_permissions/).

## Configuration

Home Assistant prompts for `tunnel_id`, `api_key`, and `mcp_url`. All values must be set inside the app options; **no real secrets belong in GitHub**.

The startup script reads these values using `bashio::config` and exports them for the pinned tunnel-client runtime.

- The upstream `mcp_url` must refer to the **existing read-only Home Assistant MCP Server** endpoint.
- The app still uses `host_network: true`, matching the functioning local version. Whether this can be reduced should be tested independently after migration.
- The Dockerfile pins tunnel-client runtime v0.0.19 by download URL and SHA-256 integrity check. Review and upgrade separately, not during cutover.
- `config.yaml` uses a new app slug (`ha_mcp_read_tunnel`) so both old and new apps can temporarily coexist.

## Safe migration

1. Review and merge the GitHub pull request before refreshing the repository in the Home Assistant app store.
2. Refresh the existing GitHub app repository source in Home Assistant; confirm **HA MCP Read Tunnel** appears.
3. Install the new app, but **do not stop or uninstall the local tunnel yet**.
4. In the new app's private configuration, manually enter the read-side tunnel ID, runtime API key, and read-only MCP upstream URL. Never publish, paste, or commit these values.
5. If the OpenAI tunnel service allows only one active client for the tunnel ID, **stop the old local app immediately before starting the new app** (controlled cutover); otherwise avoid duplicate connections.
6. Start the new app, inspect sanitized logs, and validate a real read-only tool call from ChatGPT. Confirm no write tools came through the read connection.
7. Only after successful operation disable auto-start or uninstall the old local app. Keep rollback available until tests are complete.

## Pre-release checks

- Verify the three reconstructed source files against the local originals, especially the actual `bashio::config` assignment lines in `run.sh`.
- Build on the HA machine and validate the downloaded binary/checksum.
- Test clean install, read-only connection, rollback and backup restore.
- Review secret-handling, any runtime logs and existing Git history before releasing v1.0.0.

The new app is kept at version **0.1.0** for this migration. There is **no stable release yet**.
