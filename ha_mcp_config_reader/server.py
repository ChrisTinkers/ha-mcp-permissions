"""Read-only MCP access to selected Home Assistant YAML configuration files."""
import json
import os
import re
import secrets
import stat
from pathlib import Path

import uvicorn
from mcp.server import MCPServer

CONFIG_ROOT = Path("/homeassistant")
MAX_BYTES = 131072
PORT = 8766
SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.ya?ml\Z")
PACKAGE_PATTERN = "packages/*.yaml"
ROOT_FILE = "configuration.yaml"
# Deny known secret-bearing names even if a future allowlist is broadened.
DENIED_NAMES = frozenset({"secrets.yaml", "secrets.yml"})
# Conservative heuristic, not a substitute for manual review of allowed files.
SENSITIVE = re.compile(
    r'(?im)(?:^|[,\\{])\\s*["\\\']?(?:password|passwd|token|'
    r'(?:api|access|refresh|bearer|client|private)[_-]?(?:key|token|secret)|'
    r'secret|authorization|credential|webhook_id)["\\\']?\\s*:'
)
SENSITIVE_URL = re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s/@]+:[^\s/@]+@")
SENSITIVE_AUTH = re.compile(r"(?i)\b(?:bearer|basic)\s+[A-Za-z0-9+/=_-]{12,}")


def valid_name(name):
    return isinstance(name, str) and SAFE_NAME.fullmatch(name) is not None and name.lower() not in DENIED_NAMES


def load_options(path="/data/options.json"):
    options = json.loads(Path(path).read_text(encoding="utf-8"))
    key = options.get("access_key")
    if not isinstance(key, str) or len(key) < 32:
        raise RuntimeError("access_key must contain at least 32 characters")
    names = options.get("allowed_files", [])
    if not isinstance(names, list) or not names or len(names) > 100:
        raise RuntimeError("allowed_files must contain 1-100 entries")
    for entry in names:
        if not isinstance(entry, str) or not (
            entry in {PACKAGE_PATTERN, ROOT_FILE} or valid_name(entry)
        ):
            raise RuntimeError("Only package YAML filenames, packages/*.yaml or configuration.yaml are allowed")
    return key, frozenset(names)


def is_allowed(filename, allowed):
    if filename == ROOT_FILE:
        return ROOT_FILE in allowed
    if not isinstance(filename, str) or not filename.startswith("packages/"):
        return False
    name = filename[len("packages/"):]
    return valid_name(name) and (
        PACKAGE_PATTERN in allowed or name in allowed or filename in allowed
    )


def _read_regular_file(root, filename):
    # Open root and each path component relative to an open directory descriptor.
    # O_NOFOLLOW protects against symlinks and races on both directory and file.
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    root_fd = os.open(root, directory_flags)
    try:
        if filename == ROOT_FILE:
            directory_fd = root_fd
            name = ROOT_FILE
        else:
            directory_fd = os.open("packages", directory_flags, dir_fd=root_fd)
            name = filename[len("packages/"):]
        try:
            fd = os.open(name, flags, dir_fd=directory_fd)
            try:
                if not stat.S_ISREG(os.fstat(fd).st_mode):
                    raise ValueError("Not a regular file")
                with os.fdopen(fd, "rb", closefd=False) as handle:
                    raw = handle.read(MAX_BYTES + 1)
            finally:
                os.close(fd)
        finally:
            if directory_fd != root_fd:
                os.close(directory_fd)
    finally:
        os.close(root_fd)
    if len(raw) > MAX_BYTES:
        raise ValueError("File exceeds 128 KiB limit")
    content = raw.decode("utf-8")
    if SENSITIVE.search(content) or SENSITIVE_URL.search(content) or SENSITIVE_AUTH.search(content):
        raise ValueError("Potential secret detected; file refused")
    return content


def read_config(filename, allowed, root=CONFIG_ROOT):
    if not is_allowed(filename, allowed):
        raise ValueError("File is not on the explicit allowlist")
    return _read_regular_file(root, filename)


def list_files(allowed, root=CONFIG_ROOT):
    result = []
    if ROOT_FILE in allowed:
        try:
            if (root / ROOT_FILE).is_file() and not (root / ROOT_FILE).is_symlink():
                result.append(ROOT_FILE)
        except OSError:
            pass
    package_dir = root / "packages"
    if package_dir.is_dir() and not package_dir.is_symlink():
        try:
            for entry in package_dir.iterdir():
                if is_allowed("packages/" + entry.name, allowed) and entry.is_file() and not entry.is_symlink():
                    result.append("packages/" + entry.name)
        except OSError:
            pass
    return sorted(result)


ACCESS_KEY, ALLOWED = load_options()
server = MCPServer("HA YAML Reader", instructions=(
    "Read-only access to approved Home Assistant YAML files. "
    "Never request credentials or secrets."
))


@server.tool()
async def list_config_files() -> dict:
    """List currently available approved YAML files."""
    return {"files": list_files(ALLOWED)}


@server.tool()
async def read_config_file(filename: str) -> dict:
    """Read an approved packages/<name>.yaml or configuration.yaml file."""
    return {"filename": filename, "content": read_config(filename, ALLOWED)}


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
