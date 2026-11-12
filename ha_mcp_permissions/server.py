"""Minimal, default-deny Home Assistant to-do MCP gateway.

The MCP client cannot choose an entity, domain, service, or URL.
There are NO arbitrary Home Assistant service-call tools.
"""
import json
import os
import secrets
from pathlib import Path

import httpx
import uvicorn
from mcp.server import MCPServer

TARGET = "todo.ha_weiterentwicklung"
API_ROOT = "http://supervisor/core/api"
PORT = 8765


def _access_key() -> str:
    options_path = Path("/data/options.json")
    options = json.loads(options_path.read_text(encoding="utf-8"))
    key = options.get("access_key", "")
    if not isinstance(key, str) or len(key) < 32:
        raise RuntimeError("access_key must be at least 32 characters")
    return key


ACCESS_KEY = _access_key()
SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN", "")
if not SUPERVISOR_TOKEN:
    raise RuntimeError("SUPERVISOR_TOKEN missing")


def _clean(value: str, limit: int) -> str:
    if not isinstance(value, str):
        raise ValueError("Expected a text value")
    value = value.strip()
    if not value or len(value) > limit or any(ord(c) < 32 for c in value):
        raise ValueError(f"Text must contain 1–{limit} printable characters")
    return value


async def _ha_call(action: str, data: dict) -> dict:
    # Hard-coded map, not an arbitrary service caller.
    if action not in {"get_items", "add_item", "update_item"}:
        raise ValueError("Action not allowed")
    payload = {"entity_id": TARGET, **data}
    url = f"{API_ROOT}/services/todo/{action}?return_response"
    headers = {"Authorization": f"Bearer {SUPERVISOR_TOKEN}"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()


server = MCPServer("HA Weiterentwicklung", instructions=(
    "This server only manages todo.ha_weiterentwicklung. "
    "Other Home Assistant resources are never writable through this server."
))


@server.tool()
async def list_development_tasks() -> dict:
    """List all tasks from the one explicitly allowed Home Assistant to-do list."""
    return await _ha_call("get_items", {})


@server.tool()
async def add_development_task(summary: str, description: str = "") -> dict:
    """Add a task exclusively to HA Weiterentwicklung."""
    data = {"item": _clean(summary, 180)}
    if description:
        data["description"] = _clean(description, 2000)
    return await _ha_call("add_item", data)


@server.tool()
async def rename_development_task(item: str, new_name: str) -> dict:
    """Rename a task in the allowed list; use the UID when possible."""
    return await _ha_call("update_item", {
        "item": _clean(item, 180), "rename": _clean(new_name, 180)
    })


@server.tool()
async def complete_development_task(item: str) -> dict:
    """Mark a task in the allowed list completed; use the UID when possible."""
    return await _ha_call("update_item", {
        "item": _clean(item, 180), "status": "completed"
    })


class ProtectedMCP:
    """Reject all paths except /<secret>/mcp; never forward arbitrary routes.

    This is a shared-secret URL to support a tunnel that cannot send custom headers.
    Keep the URL confidential and do not publish the app's port.
    """

    def __init__(self, application):
        self.application = application

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            return await self.application(scope, receive, send)
        if scope["type"] != "http":
            return await self._reject(send)
        path = scope.get("path", "")
        valid_path = "/" + ACCESS_KEY + "/mcp"
        if not secrets.compare_digest(path, valid_path):
            return await self._reject(send)
        scope = dict(scope)
        scope["path"] = "/mcp"
        scope["raw_path"] = b"/mcp"
        await self.application(scope, receive, send)

    @staticmethod
    async def _reject(send):
        await send({"type": "http.response.start", "status": 404, "headers": []})
        await send({"type": "http.response.body", "body": b"Not found"})


if __name__ == "__main__":
    app = ProtectedMCP(server.streamable_http_app(
        host="0.0.0.0", stateless_http=True, json_response=True
    ))
    uvicorn.run(app, host="0.0.0.0", port=PORT, access_log=False)
