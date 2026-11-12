# HA MCP Permissions

Planned separate, least-privilege MCP write service for Home Assistant.

## Architecture
- Existing Home Assistant MCP server and its tunnel remain **read-only**.
- An independent MCP service and tunnel will expose only explicitly allowed actions.
- Server-side allowlists deny every unapproved action/entity; AI instructions are not access controls.

## Permission stages
| Stage | Scope | Status |
| --- | --- | --- |
| 0 | Existing read-only Home Assistant integration | Active, unchanged |
| 1 | Manage items in `todo.ha_weiterentwicklung` | Planned |
| 2 | Specifically approved additional lists and helpers | Disabled |
| 3 | Specifically approved configuration changes | Disabled |
| 4 | Specifically approved device controls | Disabled |

## Requirements
- Stage 1 never accepts client-supplied `entity_id`, `service`, `domain` or arbitrary URLs.
- Only narrowly defined MCP tools; no generic Home Assistant service-call tool.
- Validate and bound input; no secrets in repository or logs.
- Test that modifying any other list or device is denied.
- Replace the previously exposed OpenAI API key before enabling a new write connection.
- Verify ChatGPT's write-tool availability before deployment.

## Status
**Not installable yet.** This repository currently contains planning files only; the actual service, Home Assistant app and connection must still be implemented and tested.

Never paste access tokens, API keys, or private MCP URLs into issues or chats.
