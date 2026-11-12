# HA MCP Write Tunnel

This is an independent Home Assistant app for the separate write-only MCP connection.

- The existing read-only tunnel and original HA MCP server remain unchanged.
- Do not start this app before verifying the HA MCP Permissions endpoint and authorization behavior.
- Options are local secrets. Never paste the `api_key` or the private `mcp_url` into chat.
- Set `tunnel_id` to the newly created OpenAI Platform tunnel.
- Set `api_key` to a **runtime** API key with Tunnels Read + Use permissions.
- Set `mcp_url` to the internal endpoint `http://9cf2e9bf-ha-mcp-permissions:8765/<ACCESS_KEY>/mcp`. Obtain ACCESS_KEY from the HA MCP Permissions app's local configuration; do not share it.

The launch script accepts only the internal HA MCP Permissions hostname and port for its MCP target, preventing accidental redirection to the existing read-only server or an external URL.

**Limitation:** The target MCP app currently holds a Home Assistant Supervisor API token. Restriction is enforced in the MCP code; it is not a separately scope-limited HA credential. Review and test before enabling writes. Tool access in ChatGPT is subject to plan/workspace permissions.

No public ingress or host port is created for this tunnel app.
