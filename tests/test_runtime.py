"""Runtime smoke tests: imports the actual MCP SDK and boots ASGI."""
import importlib.util
import json
import os
import pathlib
import unittest
from unittest.mock import patch

from starlette.testclient import TestClient

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "ha_mcp_permissions" / "server.py"


class RuntimeTests(unittest.TestCase):
    def test_server_boot_and_unauthorized_route(self):
        read_text = pathlib.Path.read_text

        def fake_options(path, *args, **kwargs):
            if str(path) == "/data/options.json":
                return json.dumps({"access_key": "a" * 48})
            return read_text(path, *args, **kwargs)

        spec = importlib.util.spec_from_file_location("gateway_under_test", SOURCE)
        module = importlib.util.module_from_spec(spec)
        with patch.dict(os.environ, {"SUPERVISOR_TOKEN": "test-only-token"}), patch.object(
            pathlib.Path, "read_text", fake_options
        ):
            spec.loader.exec_module(module)

        app = module.build_app()
        with TestClient(app) as client:
            denied = client.post("/not-permitted/mcp", json={})
            self.assertEqual(denied.status_code, 404)
            denied2 = client.post("/" + "a"*48 + "/wrong", json={})
            self.assertEqual(denied2.status_code, 404)


if __name__ == "__main__":
    unittest.main()
