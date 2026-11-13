#!/command/with-contenv bashio
set -euo pipefail

export CONTROL_PLANE_TUNNEL_ID="$(bashio::config 'tunnel_id')"
export CONTROL_PLANE_API_KEY="$(bashio::config 'api_key')"
export MCP_SERVER_URL="$(bashio::config 'mcp_url')"

if [[ -z "${CONTROL_PLANE_TUNNEL_ID}" || -z "${CONTROL_PLANE_API_KEY}" || -z "${MCP_SERVER_URL}" ]]; then
  bashio::log.error "Tunnel-ID, API-Key und MCP-URL muessen gesetzt sein."
  exit 1
fi

bashio::log.info "Starte OpenAI Secure MCP Tunnel."
exec /usr/local/bin/tunnel-client-runtime run --log.level=info
