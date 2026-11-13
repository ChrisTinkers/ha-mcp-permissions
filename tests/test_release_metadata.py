"""Check consistency of the three app version declarations.

This validates source metadata only; it does not prove deployment provenance.
"""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
APPS = ("ha_mcp_permissions", "ha_mcp_write_tunnel", "ha_mcp_read_tunnel")
EXPECTED = "1.0.0"


class ReleaseMetadataTests(unittest.TestCase):
    def test_version_matches_docker_build_default(self):
        for app in APPS:
            with self.subTest(app=app):
                config = (ROOT / app / "config.yaml").read_text(encoding="utf-8")
                docker = (ROOT / app / "Dockerfile").read_text(encoding="utf-8")
                c = re.search(r'^version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)', config, re.M)
                d = re.search(r'^ARG BUILD_VERSION=([0-9]+\.[0-9]+\.[0-9]+)', docker, re.M)
                self.assertIsNotNone(c, "Missing app version")
                self.assertIsNotNone(d, "Missing Docker build version")
                self.assertEqual(c.group(1), d.group(1))
                self.assertEqual(c.group(1), EXPECTED)


if __name__ == "__main__":
    unittest.main()
