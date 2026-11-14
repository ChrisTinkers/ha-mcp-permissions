# HA MCP Config Reader (experimental)

An independent, read-only MCP server for explicitly approved files under
`/homeassistant/packages/`. It does not modify the existing HA read tunnel,
HA MCP Server, or write gateway.

## Installation and connection

1. Review the source and tests. Install the new app from the existing GitHub
   Home Assistant app repository; do not upgrade the existing tunnels.
2. Generate a unique random access key of at least 32 characters in the app's
   private options. Set `allowed_files` to an explicit list of package filenames.
3. The app mounts the Home Assistant config read-only and has no host-published
   port. It serves internal port 8766.
4. Connect a **separate** read-only MCP tunnel to the internal service URL
   `http://<internal-addon-host>:8766/<access_key>/mcp`. Use the actual
   internal host name resolved in your HA installation. Do not reuse a running
   tunnel ID. A third ChatGPT MCP connector must be added for this endpoint.
5. Verify `list_config_files` and `read_config_file("hauswartung.yaml")`
   through ChatGPT. Verify disallowed paths and files fail.

Never publish access keys, internal secret-bearing URLs or app options.
Do not forward port 8766 through your router.

## Security limitations

- Only listed filenames can be accessed. No path separators, traversal or
  symlinks; the package directory is also checked for symlinks.
- Files above 128 KiB and YAML containing common sensitive-key names are
  rejected in full (not redacted).
- This is a conservative heuristic, **not** a complete secret detector.
  Do not allowlist files with embedded credentials or personal information.
- The app's mount is read-only, but its process can potentially read other
  mounted config files if compromised. Review the container and exposure.
- The new app is NOT automatically connected to the existing read tunnel.
  Its installation alone will not make tools appear in ChatGPT.
- Rollback: stop/uninstall this new app and its separate tunnel. The previous
  HA read/write integrations remain unchanged.
