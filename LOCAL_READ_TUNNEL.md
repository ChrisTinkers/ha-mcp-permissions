# OpenAI MCP Tunnel (lokal): source migration

**Current status:** The local read tunnel is running in Home Assistant at version 0.1.0, but its implementation is **not** currently present in this repository. Do not infer that the source for `ha_mcp_write_tunnel` can replace it.

## Capture from the running system

1. Locate the local Home Assistant app directory for `local_openai_mcp_tunnel` using Home Assistant's supported file access.
2. Copy only non-secret implementation files (typically `config.yaml`, `Dockerfile`, startup script and documentation) into a new directory `openai_mcp_tunnel_local/`.
3. **Before staging or committing, inspect every file** for hard-coded tokens, URLs containing secret paths, user identifiers and local configuration.
4. Keep actual `/data/options.json`, local runtime configuration, tunnel IDs, `api_key`, logs and backups **outside Git**. Document required option *names*, not their values.
5. Verify that the upstream is the existing Home Assistant MCP Server configured with `read_only_mode=true`, and that the local tunnel is not given an arbitrary configurable external destination.
6. Validate a clean install and read-only behavior; keep the current deployed tunnel running during review.

## Recovery requirements

Record supported Home Assistant and upstream MCP Server versions, deployment steps, service hostname, connectivity checks and rollback instructions after inspecting the actual source.

**Do not mark this component reproduced or ready for a unified v1.0.0 until the above steps have been completed and independently checked.**
