# Read tunnel migration notes

The existing **OpenAI MCP Tunnel (lokal)** is still installed and running. Its GitHub-managed successor is **[HA MCP Read Tunnel](ha_mcp_read_tunnel/DOCS.md)**.

Source files were reconstructed from the read-only inspection of the local app in `/local_apps/openai_tunnel/`. The exact text of three credential-loading assignment lines was not disclosed; the versioned start script uses the confirmed `bashio::config` mechanism, but byte-for-byte equivalence has not been established.

The new app has a distinct slug, `ha_mcp_read_tunnel`, allowing controlled migration with rollback. Preserve the local app and configure all secrets only in Home Assistant. Do not remove it until the new tunnel is running and read-only operation is verified.

See [migration steps](ha_mcp_read_tunnel/DOCS.md) and [release requirements](RELEASE.md).
