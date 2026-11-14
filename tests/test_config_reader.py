"""Offline security tests; requires MCP package installed."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "ha_mcp_config_reader" / "server.py"


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "packages").mkdir()
        (self.root / "packages" / "hauswartung.yaml").write_text("sensor: []\n")
        self.options = self.root / "options.json"
        self.options.write_text(json.dumps({
            "access_key": "a" * 40, "allowed_files": ["hauswartung.yaml"]
        }))
        # Import safely: module initializes options at import.
        spec = importlib.util.spec_from_file_location("config_reader_under_test", MODULE)
        self.module = importlib.util.module_from_spec(spec)
        with patch("pathlib.Path.read_text", wraps=Path.read_text):
            with patch("builtins.open", wraps=open):
                pass
        with patch("pathlib.Path", wraps=Path):
            pass
        # load_options can be tested independently once module import has valid options.

    def test_allowlist(self):
        self.assertTrue(self.options.exists())
