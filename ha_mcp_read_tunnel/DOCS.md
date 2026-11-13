# HA MCP Read Tunnel

GitHub-managed read tunnel for the existing Home Assistant MCP Server, which must operate in `read_only_mode=true`.

**Installed and running:** v0.1.1 (verified 2026-11-13). The former **OpenAI MCP Tunnel (lokal)** v0.1.0 is stopped but retained for rollback.

## Configuration

The Home Assistant app has three secret settings:

- `tunnel_id`: identifier of the read-side tunnel
- `api_key`: runtime credential for the tunnel client
- `mcp_url`: internal URL of the existing **read-only** Home Assistant MCP Server

Enter these only in Home Assistant's private app configuration. **Do not save real values in GitHub, issues or screenshots.** Treat a full MCP URL as sensitive when it contains private paths or credentials.

The script loads fields using `bashio::config` and exports them to the tunnel client. The app uses `host_network: false`; an app security score of **7/8** was observed after this change.

The Dockerfile fetches tunnel-client-runtime v0.0.19 from the official release URL and verifies the archive's SHA-256. Its base image is `ghcr.io/home-assistant/base:3.24`.

## Controlled migration (completed 2026-11-13)

1. Add the GitHub repository to the Home Assistant App Store and refresh it.
2. Install HA MCP Read Tunnel v0.1.1, with the new distinct slug.
3. Copy the three settings privately from the old local app configuration.
4. Stop **OpenAI MCP Tunnel (lokal)** before starting the new app, especially if reusing the same tunnel ID.
5. Start HA MCP Read Tunnel and inspect sanitized logs.
6. Check that the read connection can access Home Assistant and that the existing read-side MCP Server remains read-only.

**Observed:** The new app started successfully; the old app is stopped; a Home Assistant read operation succeeded. A full tunnel-specific end-to-end check and clean reinstall/restore test remain outstanding.

## Rollback and limitations

To roll back, stop the new app before starting the old app; avoid simultaneous connections with the same tunnel ID. Retain the old app and its credentials until the new deployment has passed recovery tests.

The reconstructed `run.sh` uses the previously verified `bashio::config` mechanism, but exact byte-for-byte equivalence with the old script's credential assignment lines has not been established.

See [release checklist](../RELEASE.md) for remaining stability and security work.
