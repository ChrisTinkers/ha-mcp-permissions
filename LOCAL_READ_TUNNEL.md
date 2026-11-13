# Historical local read tunnel and migration

The previous **OpenAI MCP Tunnel (lokal)** v0.1.0 was installed from `/local_apps/openai_tunnel/`.

On 2026-11-13 a new app, **HA MCP Read Tunnel** v0.1.1, was installed from this GitHub repository under the distinct slug `ha_mcp_read_tunnel`, allowing both installations to coexist during transition. Its `host_network` setting was reduced from `true` to `false`.

**Current state:** The new app is running. The previous local app is stopped and remains installed as a rollback option. A Home Assistant read call succeeded after the change. The direct end-to-end route through the read tunnel and clean restoration after a failure have not been independently verified.

The original source files were inspected without publishing local settings. The three assignment lines of `run.sh` were confirmed to load values through `bashio::config`, but their precise byte-for-byte text was not compared with the reconstructed GitHub script.

Rollback, if needed: stop the GitHub-managed read app first, then start the local app with its existing protected configuration, and validate the read connection. **Do not run two clients concurrently against the same tunnel ID.**

See [HA MCP Read Tunnel documentation](ha_mcp_read_tunnel/DOCS.md).
