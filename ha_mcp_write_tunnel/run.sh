#!/bin/sh
set -eu
CONFIG=/data/options.json

# Never print, log, or interpolate secrets into a shell command.
CONTROL_PLANE_TUNNEL_ID="$(jq -er '.tunnel_id | select(type=="string" and startswith("tunnel_"))' "$CONFIG")"
CONTROL_PLANE_API_KEY="$(jq -er '.api_key | select(type=="string" and length >= 20)' "$CONFIG")"
MCP_SERVER_URL="$(jq -er '.mcp_url | select(type=="string" and startswith("http://9cf2e9bf-ha-mcp-permissions:8765/") and endswith("/mcp"))' "$CONFIG")"
export CONTROL_PLANE_TUNNEL_ID CONTROL_PLANE_API_KEY MCP_SERVER_URL

echo "Starting isolated MCP write tunnel; upstream host restricted to HA MCP Permissions"
exec /usr/local/bin/tunnel-client run --log.level=info
