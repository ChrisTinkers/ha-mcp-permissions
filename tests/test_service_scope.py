"""Runtime tests of the gateway's hard-coded HA service scope."""
import asyncio
import importlib.util
import json
import os
import pathlib
import unittest
from unittest.mock import patch

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "ha_mcp_permissions" / "server.py"


def load_gateway():
    original = pathlib.Path.read_text

    def fake_options(path, *args, **kwargs):
        if str(path) == "/data/options.json":
            return json.dumps({"access_key": "a" * 48})
        return original(path, *args, **kwargs)

    spec = importlib.util.spec_from_file_location("scope_gateway", SOURCE)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(os.environ, {"SUPERVISOR_TOKEN": "test-token"}), patch.object(
        pathlib.Path, "read_text", fake_options
    ):
        spec.loader.exec_module(module)
    return module


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"success": True}


class FakeClient:
    calls = []

    def __init__(self, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def post(self, url, *, json, headers):
        self.calls.append((url, json, headers))
        return FakeResponse()


class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.gateway = load_gateway()
        FakeClient.calls.clear()

    def test_action_allowlist_rejects_unapproved_services(self):
        for action in ("turn_on", "remove_item", "reload", "delete", "call_service"):
            with self.subTest(action=action):
                with self.assertRaises(ValueError):
                    asyncio.run(self.gateway._ha_call(action, {}))
        self.assertEqual(FakeClient.calls, [])

    def test_target_cannot_be_overridden(self):
        with patch.object(self.gateway.httpx, "AsyncClient", FakeClient):
            asyncio.run(self.gateway._ha_call("add_item", {
                "entity_id": "todo.einkaufsliste",
                "item": "Scope test only",
            }))
        self.assertEqual(len(FakeClient.calls), 1)
        url, payload, headers = FakeClient.calls[0]
        self.assertTrue(url.endswith("/services/todo/add_item?return_response"))
        self.assertEqual(payload["entity_id"], "todo.ha_weiterentwicklung")
        self.assertEqual(payload["item"], "Scope test only")

    def test_no_other_domain_endpoint_can_be_called(self):
        with patch.object(self.gateway.httpx, "AsyncClient", FakeClient):
            asyncio.run(self.gateway._ha_call("update_item", {
                "entity_id": "light.wohnzimmer",
                "item": "some-task",
                "status": "completed",
            }))
        self.assertEqual(len(FakeClient.calls), 1)
        url, payload, _ = FakeClient.calls[0]
        self.assertIn("/services/todo/update_item", url)
        self.assertEqual(payload["entity_id"], "todo.ha_weiterentwicklung")


if __name__ == "__main__":
    unittest.main()
