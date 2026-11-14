"""Regression checks for isolated Config Reader tunnel metadata."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "ha_mcp_config_tunnel"


class ConfigTunnelTests(unittest.TestCase):
    def test_version_and_slug(self):
        config = (APP / "config.yaml").read_text()
        docker = (APP / "Dockerfile").read_text()
        self.assertIn('slug: "ha_mcp_config_tunnel"', config)
        self.assertIn('version: "1.0.0"', config)
        self.assertIn("ARG BUILD_VERSION=1.0.0", docker)

    def test_isolation(self):
        config = (APP / "config.yaml").read_text()
        for item in ("host_network: false", "homeassistant_api: false",
                     "hassio_api: false", "auth_api: false",
                     "docker_api: false", "ports: {}", "boot: manual"):
            with self.subTest(item=item):
                self.assertIn(item, config)
        self.assertNotIn("map:", config)

    def test_fixed_upstream(self):
        script = (APP / "run.sh").read_text()
        self.assertIn("9cf2e9bf-ha-mcp-config-reader:8766", script)
        self.assertIn("bashio::config 'tunnel_id'", script)
        self.assertIn("bashio::config 'api_key'", script)
        self.assertIn("bashio::config 'mcp_url'", script)
        self.assertIn("MCP-URL muss auf den internen", script)
        self.assertNotIn("set -x", script)

    def test_client_checksum(self):
        docker = (APP / "Dockerfile").read_text()
        self.assertIn("tunnel-client-runtime-v0.0.19-linux-amd64.zip", docker)
        self.assertIn("sha256sum -c -", docker)
