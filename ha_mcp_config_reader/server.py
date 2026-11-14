"""Explicit-allowlist, read-only MCP access to Home Assistant package YAML.

Never expose a general file path or a write tool.
"""
import json
import os
import re
import secrets
from pathlib import Path

import uvicorn
from mcp.server import MCPServer

CONFIG_ROOT = Path("/homeassistant")
MAX_BYTES = 131072
PORT = 8766
SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.ya?ml\Z")
SENSITIVE = re.compile(
    r"(?im)^\s*(?:[- ]*\s*)?(?:password|passwd|token|api[_-]?key|"
    r"access[_-]?key|secret|client[_-]?secret|authorization|private[_-]?key)"
    r"\s*:"
)


def load_options(path="/data/options.json"):
    options = json.loads(Path(path).read_text(encoding="utf-8"))
    key = options.get("access_key")
    if not isinstance(key, str) or len(key) < 32:
        raise RuntimeError("access_key must contain at least 32 characters")
    names = options.get("allowed_files", [])
    if not isinstance(names, list) or not names or len(names) > 100:
        raise RuntimeError("allowed_files must contain 1-100 filenames")
    if any(not isinstance(n, str) or not SAFE_NAME.fullmatch(n)
           or n.lower() in {"secrets.yaml", "secrets.yml"} for n in names):
        raise RuntimeError("Only simple YAML filenames may be allowed")
    return key, frozenset(names)


def read_package(filename, allowed, root=CONFIG_ROOT):
    if filename not in allowed:
        raise ValueError("File is not on the explicit allowlist")
    if not SAFE_NAME.fullmatch(filename):
        raise ValueError("Invalid filename")
    package_dir = root / "packages"
    # Do not follow symlinks in the directory or the file.
    if package_dir.is_symlink():
        raise ValueError("Package directory symlink denied")
    target = package_dir / filename
    if target.is_symlink() or not target.is_file():
        raise FileNotFoundError("File unavailable or not a regular file")
    # O_NOFOLLOW protects the final component against symlink races.
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(target, flags)
    try:
        import stat
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("Not a regular file")
        with os.fdopen(fd, "rb", closefd=False) as handle:
            raw = handle.read(MAX_BYTES + 1)
    finally:
        os.close(fd)
    if len(raw) > MAX_BYTES:
        raise ValueError("File exceeds 128 KiB limit")
    content = raw.decode("utf-8")
    if SENSITIVE.search(content):
        raise ValueError("File contains potentially sensitive YAML keys; refused")
    return content


ACCESS_KEY, ALLOWED = load_options()
server = MCPServer("HA YAML Reader", instructions=(
    "Read-only access to explicitly approved Home Assistant package YAML files. "
    "Never use this tool for credentials or secrets."
))


@server.tool()
async def list_config_files() -> dict:
    """List explicitly approved YAML package filenames (not arbitrary paths)."""
    return {"files": sorted(ALLOWED)}


@server.tool()
async def read_config_file(filename: str) -> dict:
    """Read one approved packages/*.yaml file, rejecting sensitive YAML keys."""
    return {"filename": filename, "content": read_package(filename, ALLOWED)}


class ProtectedMCP:
    def __init__(self, application):
        self.application = application

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            return await self.application(scope, receive, send)
        if scope["type"] != "http" or not secrets.compare_digest(
            scope.get("path", ""), "/" + ACCESS_KEY + "/mcp"
        ):
            await send({"type": "http.response.start", "status": 404, "headers": []})
            await send({"type": "http.response.body", "body": b"Not found"})
            return
        scope = dict(scope, path="/mcp", raw_path=b"/mcp")
        await self.application(scope, receive, send)


def build_app():
    return ProtectedMCP(server.streamable_http_app(
        host="0.0.0.0", stateless_http=True, json_response=True,
        max_request_body_size=8192
    ))


if __name__ == "__main__":
    uvicorn.run(build_app(), host="0.0.0.0", port=PORT, access_log=False)
