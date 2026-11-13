# HA MCP Permissions

Installed version verified on 2026-11-13: **0.1.4**, running.

## Purpose

A separate MCP gateway for one Home Assistant task list. It provides four tools to read, add, rename and complete entries in `todo.ha_weiterentwicklung`.

## Configuration

Set `access_key` to an independently generated random secret of **at least 32 characters** in the Home Assistant app configuration. It forms part of the private MCP endpoint path. Never publish the full URL or the access key in GitHub, chat, issues, logs or screenshots.

The default app configuration does not map its TCP port 8765 to the host (`8765/tcp: null`). **Do not enable that port or create a router port forward.**

## Security model

The code permits only `todo.get_items`, `todo.add_item` and `todo.update_item`, with target `todo.ha_weiterentwicklung` fixed in the server. The MCP client cannot select a different service or entity. Invalid request routes receive HTTP 404.

**Residual risk:** `homeassistant_api: true` provides a powerful Supervisor token. Least privilege is enforced by this Python gateway's code and is not enforced by the token itself. A compromised app could potentially exceed these restrictions.

## Validation and recovery

- Check the installed app version and source/image correspondence.
- Run `python -m unittest discover -s tests -v` from the repository with its dependencies installed.
- Confirm the four actions against the approved list.
- Test denial of other services and lists without touching unrelated Home Assistant resources.
- Store secret-containing app options in a protected local backup, **never in Git**.
- See [release readiness](../RELEASE.md) before tagging a stable release.

The original Home Assistant MCP Server and read tunnel remain separate and read-only.
