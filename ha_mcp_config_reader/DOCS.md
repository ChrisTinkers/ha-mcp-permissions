# HA MCP Config Reader 1.1.0 (experimental)

This new app adds **read-only**, explicitly allowlisted access to YAML files
inside `/homeassistant/packages/`. Existing MCP read and write connections
remain unchanged.

## Deployment

1. Install the new app from the GitHub app repository after refreshing its store.
2. Set a unique 32+ character `access_key` in the private app options.
3. Set `allowed_files` to explicitly reviewed filenames such as
   `hauswartung.yaml`. Avoid files containing credentials or personal data.
4. The app mounts `config:ro` and exposes TCP 8766 **inside the app network
   only**; no host port is published.
5. To reach it from ChatGPT, provision a **separate MCP tunnel and connection**
   with unique tunnel credentials, forwarding to the internal app address
   `http://<addon-internal-host>:8766/<access_key>/mcp`.
   Determine the actual internal host from Supervisor networking before use.
   Do not reuse the credentials of the running read tunnel.
6. Verify list/read tools, denylisted paths and files, and that existing
   read/write tunnels still work.

## Limits

- Only explicitly listed package filenames are allowed; paths are not accepted.
- Symlinks, files over 128 KiB and common secret-like YAML keys are rejected.
- Secret detection is heuristic and not a guarantee. Do not allowlist files
  containing embedded credentials or sensitive information.
- The app cannot modify config files. A read-only mount does not prevent an
  exploited process from reading other mounted files.
- No existing tunnel automatically picks up the new tools.
- Rollback: stop/remove this app and its separate tunnel. Existing apps are
  unaffected.
