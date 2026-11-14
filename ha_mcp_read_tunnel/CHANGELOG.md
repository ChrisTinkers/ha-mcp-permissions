# HA MCP Read Tunnel – Changelog

## 1.0.1 – 2026-11-14
- Restrict `mcp_url` to the internal Home Assistant MCP Server host `81f33d0f-ha-mcp` on port `9583` using HTTP and a single private path segment followed by `/mcp`.
- Reject invalid upstream URLs before launching the tunnel; do not log the secret-bearing URL.
- Preserve existing tunnel ID, API key, secret path, and MCP runtime version.
- **Compatibility:** installations using a different internal hostname or URL path will fail to start until adjusted; verify the configured URL before upgrading.
- This hardening does not itself repair an existing HTTP connectivity or authentication failure.

## 1.0.0
- Initial dedicated OpenAI MCP read tunnel.
