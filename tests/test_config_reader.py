"""Offline tests for the separate YAML reader; requires mcp and uvicorn."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "ha_mcp_config_reader" / "server.py"


class ReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        (cls.root / "packages").mkdir()
        cls.options = cls.root / "options.json"
        cls.options.write_text(json.dumps({
            "access_key": "a" * 40, "allowed_files": ["hauswartung.yaml"]
        }))
        original_read_text = Path.read_text

        def mocked_read_text(path, *args, **kwargs):
            if str(path) == "/data/options.json":
                return original_read_text(cls.options, *args, **kwargs)
            return original_read_text(path, *args, **kwargs)

        spec = importlib.util.spec_from_file_location("config_reader_test", MODULE)
        cls.reader = importlib.util.module_from_spec(spec)
        with patch.object(Path, "read_text", mocked_read_text):
            spec.loader.exec_module(cls.reader)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_read_allowed_file(self):
        (self.root / "packages" / "hauswartung.yaml").write_text("sensor: []\n")
        self.assertEqual(self.reader.read_package(
            "hauswartung.yaml", {"hauswartung.yaml"}, self.root), "sensor: []\n")

    def test_reject_unlisted_and_traversal(self):
        for filename in ("other.yaml", "../secrets.yaml", "/etc/passwd"):
            with self.subTest(filename=filename):
                with self.assertRaises(ValueError):
                    self.reader.read_package(filename, {"hauswartung.yaml"}, self.root)

    def test_reject_symlink(self):
        target = self.root / "packages" / "hauswartung.yaml"
        target.unlink(missing_ok=True)
        target.symlink_to(self.options)
        with self.assertRaises(ValueError):
            self.reader.read_package("hauswartung.yaml", {"hauswartung.yaml"}, self.root)
        target.unlink()

    def test_reject_secret_keys(self):
        (self.root / "packages" / "hauswartung.yaml").write_text(
            "api_key: abc\n")
        with self.assertRaises(ValueError):
            self.reader.read_package("hauswartung.yaml", {"hauswartung.yaml"}, self.root)

    def test_reject_large_file(self):
        (self.root / "packages" / "hauswartung.yaml").write_text(
            "x" * (self.reader.MAX_BYTES + 1))
        with self.assertRaises(ValueError):
            self.reader.read_package("hauswartung.yaml", {"hauswartung.yaml"}, self.root)

    def test_reject_invalid_allowlist(self):
        self.options.write_text(json.dumps({
            "access_key": "a" * 40, "allowed_files": ["../secrets.yaml"]
        }))
        with self.assertRaises(RuntimeError):
            self.reader.load_options(self.options)


if __name__ == "__main__":
    unittest.main()
