"""Regression tests for the read-only Home Assistant YAML reader."""
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
            "access_key": "a" * 40,
            "allowed_files": ["packages/*.yaml", "configuration.yaml"]
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

    def setUp(self):
        for item in (self.root / "packages").iterdir():
            if item.is_dir() and not item.is_symlink():
                item.rmdir()
            else:
                item.unlink()
        (self.root / "configuration.yaml").unlink(missing_ok=True)

    @property
    def allowed(self):
        return {"packages/*.yaml", "configuration.yaml"}

    def test_package_wildcard_and_root_configuration(self):
        (self.root / "packages" / "hauswartung.yaml").write_text("sensor: []\\n")
        (self.root / "packages" / "lueftung.yml").write_text("fan: []\\n")
        (self.root / "configuration.yaml").write_text("homeassistant: {}\\n")
        self.assertEqual(self.reader.read_config("packages/hauswartung.yaml", self.allowed, self.root), "sensor: []\\n")
        self.assertEqual(self.reader.read_config("configuration.yaml", self.allowed, self.root), "homeassistant: {}\\n")
        self.assertEqual(self.reader.list_files(self.allowed, self.root), [
            "configuration.yaml", "packages/hauswartung.yaml"
        ])
        with self.assertRaises(ValueError):
            self.reader.read_config("packages/lueftung.yml", self.allowed, self.root)

    def test_single_file_legacy_allowlist(self):
        (self.root / "packages" / "hauswartung.yaml").write_text("sensor: []")
        self.assertEqual(self.reader.read_config("packages/hauswartung.yaml", {"hauswartung.yaml"}, self.root), "sensor: []")

    def test_reject_traversal_and_unlisted(self):
        for name in ("../secrets.yaml", "packages/../secrets.yaml", "packages/secrets.yaml",
                     "packages/secrets.yml", "/etc/passwd", "automations.yaml",
                     "packages/sub/child.yaml", "packages/.hidden.yaml",
                     "packages/other.yml"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.reader.read_config(name, self.allowed, self.root)

    def test_symlinks_rejected(self):
        target = self.root / "packages" / "linked.yaml"
        target.symlink_to(self.options)
        with self.assertRaises((ValueError, OSError)):
            self.reader.read_config("packages/linked.yaml", self.allowed, self.root)
        target.unlink()
        (self.root / "configuration.yaml").symlink_to(self.options)
        with self.assertRaises((ValueError, OSError)):
            self.reader.read_config("configuration.yaml", self.allowed, self.root)

    def test_directory_symlink_rejected(self):
        (self.root / "packages").rmdir()
        (self.root / "packages").symlink_to(self.root, target_is_directory=True)
        try:
            with self.assertRaises((ValueError, OSError)):
                self.reader.read_config("packages/other.yaml", self.allowed, self.root)
        finally:
            (self.root / "packages").unlink()
            (self.root / "packages").mkdir()

    def test_sensitive_values_rejected(self):
        for content in ("api_key: abc", "access_token: abc", "secret: abc",
                        "headers: {authorization: Bearer foo}", "url: https://bob:password@example.com",
                        "authorization: Bearer abcdefghijklmnop"):
            with self.subTest(content=content):
                (self.root / "configuration.yaml").write_text(content)
                with self.assertRaises(ValueError):
                    self.reader.read_config("configuration.yaml", self.allowed, self.root)

    def test_secret_reference_is_not_expanded(self):
        (self.root / "configuration.yaml").write_text("password: !secret my_password")
        with self.assertRaises(ValueError):
            self.reader.read_config("configuration.yaml", self.allowed, self.root)

    def test_large_file_rejected(self):
        (self.root / "configuration.yaml").write_text("x" * (self.reader.MAX_BYTES + 1))
        with self.assertRaises(ValueError):
            self.reader.read_config("configuration.yaml", self.allowed, self.root)

    def test_invalid_allowlist(self):
        for entries in (["../secrets.yaml"], ["packages/../secrets.yaml"], ["secrets.yaml"],
                        ["packages/*.yml"], ["*.yaml"], []):
            with self.subTest(entries=entries):
                self.options.write_text(json.dumps({"access_key": "a" * 40, "allowed_files": entries}))
                with self.assertRaises(RuntimeError):
                    self.reader.load_options(self.options)

    def test_valid_allowlist(self):
        self.options.write_text(json.dumps({"access_key": "a" * 40, "allowed_files": list(self.allowed)}))
        _, entries = self.reader.load_options(self.options)
        self.assertEqual(entries, frozenset(self.allowed))


if __name__ == "__main__":
    unittest.main()
