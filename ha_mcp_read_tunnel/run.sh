#!/command/with-contenv bashio
set -euo pipefail

export CONTROL_PLANE_TUNNEL_ID="$(bashio::config 'tunnel_id')"
export CONTROL_PLANE_API_KEY="$(bashio::config 'api_key')"
export MCP_SERVER_URL="$(bashio::config 'mcp_url')"

if [[ -z "${CONTROL_PLANE_TUNNEL_ID}" || -z "${CONTROL_PLANE_API_KEY}" || -z "${MCP_SERVER_URL}" ]]; then
  bashio::log.error "Tunnel-ID, API-Key und MCP-URL muessen gesetzt sein."
  exit 1
fi

# Permit only the installed Home Assistant MCP server on its internal port.
# Do not log the URL: its path contains a private MCP access secret.
if [[ ! "${MCP_SERVER_URL}" =~ ^http://81f33d0f-ha-mcp:9583/[^/?#]+$ ]]; then
  bashio::log.error "Ungueltige MCP-Zieladresse: nur der interne HA MCP Server auf Port 9583 mit einem einzelnen geheimen Pfadsegment ist erlaubt."
  exit 1
fi

bashio::log.info "Starte OpenAI Secure MCP Read Tunnel (Zielhost geprueft)."
exec /usr/local/bin/tunnel-client-runtime run --log.level=info
