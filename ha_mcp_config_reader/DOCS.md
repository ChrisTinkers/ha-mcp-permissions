# HA MCP Config Reader 1.1.1 (experimental)

Read-only MCP server for the Home Assistant `packages` folder and optionally
the top-level `configuration.yaml`. Existing read/write MCP tunnels are not changed.

## Configuration

Create a unique 32+ character random `access_key` in the Home Assistant
app options (never commit or paste it into chat). The default allowlist is:

```yaml
allowed_files:
  - "packages/*.yaml"
  - "configuration.yaml"
```

The wildcard covers **only direct `.yaml` files** in `packages/`, not
subdirectories, `.yml` files, hidden files, or `secrets.yaml`.
A literal `hauswartung.yaml` entry is also accepted for backward
compatibility and means `packages/hauswartung.yaml`.

Tools: `list_config_files` returns paths relative to `/homeassistant`;
`read_config_file(filename)` accepts those exact paths.

## Security and deployment

The app mounts Home Assistant config as read-only (`config:ro`), has no
Home Assistant API permissions, and does not publish a host port. File reads
use directory-relative file descriptors with `O_NOFOLLOW` and reject
non-regular files, path traversal, symlinks, and files over 128 KiB.
A conservative heuristic blocks common credential keys and credential URLs.
**This heuristic cannot guarantee that all secrets are detected.** Carefully
review files before allowing them, especially `configuration.yaml`. The
wildcard intentionally allows future package files automatically, so do not
place credentials or other sensitive content in that directory.

Start only after configuring the key. A **separate** MCP tunnel and connection
must be provisioned to `http://<addon-internal-host>:8766/<access_key>/mcp`;
do not reuse an existing tunnel's credentials. The existing read tunnel does
not automatically expose these new tools.

Rollback: stop this app and its dedicated tunnel; existing MCP apps remain
unchanged.
