# Release policy and readiness

**Documentation status: 2026-11-14.** The Permissions gateway and Write Tunnel run at 1.0.0; the Read Tunnel runs at 1.0.2; the Config Reader runs at 1.1.3 and its dedicated Config Tunnel at 1.0.0. App version numbers are independent. A suite-wide `v1.0.0` GitHub release/tag is **not documented as published**.

## Directly observed Home Assistant state

| Component | Installed version | Observed state |
| --- | --- | --- |
| HA MCP Permissions | 1.0.0 | Running |
| HA MCP Write Tunnel | 1.0.0 | Running; task list read passed |
| HA MCP Read Tunnel | 1.0.2 | Running; live entity read passed |
| HA MCP Config Reader | 1.1.3 | Running; YAML content read passed |
| HA MCP Config Tunnel | 1.0.0 | Running; connected |
| External Home Assistant MCP Server | 9.2.0 | Running |
| Old OpenAI MCP Tunnel (local) | 0.1.0 | Stopped, retained for rollback |

The Config Reader's separate tunnel and ChatGPT connection are configured and operational. The three tunnel IDs differ; the user confirmed independent API keys, although the key values are masked in Home Assistant.

## Release verification checklist

### Completed or previously documented

- [x] Restricted write gateway implements four scoped tools for `todo.ha_weiterentwicklung`.
- [x] Unit, service-scope and mocked runtime tests exist in the repository.
- [x] Permissions and Write Tunnel 1.0.0, Read Tunnel 1.0.2, Config Reader 1.1.3 and Config Tunnel 1.0.0 reported running on 2026-11-14.
- [x] Config Reader 1.1.3 and its separate Config Tunnel are installed and running.
- [x] Automated tests and Docker build for Config Reader 1.1.1 implementation passed on GitHub Actions.
- [x] Full Git-history secret scan passed on the implementation commit; a scan cannot guarantee absence of every secret.
- [x] Read Tunnel 1.0.2 live state read succeeded after correcting the secret-path URL (no extra `/mcp`).
- [x] Recovery/rollback instructions exist in [RECOVERY.md](RECOVERY.md).
- [x] Earlier user confirmation of a Home Assistant backup covering the original core apps was documented; it does **not** prove a restore.
- [x] Earlier user verification documented no manual UniFi port forwarding and disabled UPnP.

### Still outstanding

- [x] Config Reader 1.1.3: approved file listing and YAML content read passed; `secrets.yaml` access was rejected.
- [x] Dedicated Config Reader tunnel and ChatGPT connection verified.
- [x] General read connection tested via `sun.sun`; restricted write connection tested via non-mutating task list retrieval.
- [ ] Exercise an explicitly authorized write operation end-to-end and confirm the intended change only.
- [ ] Independently verify denied writes to other entities/services without affecting unrelated entities.
- [ ] Demonstrate deployed container images correspond to reviewed source.
- [ ] Perform a clean install, upgrade/rollback and **actual restoration** from backup.
- [ ] Review dependencies/base images and decide on version pinning.
- [ ] Confirm Home Assistant Core/OS versions and external access boundaries.
- [ ] Verify final suite release criteria before creating a suite-wide GitHub tag/release.

## Security constraints and residual risk

The Permissions gateway uses `homeassistant_api: true` and receives a privileged Supervisor-issued token. Restrictions are implemented in the gateway code, not in a least-privileged Supervisor credential; process compromise could bypass them.

The Config Reader mounts the Home Assistant configuration read-only and checks allowed paths, but its credential detection is heuristic. The `packages/*.yaml` wildcard includes future direct package files automatically. Review source files and avoid embedding credentials.

Never commit populated app options, tunnel IDs, keys, private MCP URLs, tokens, logs containing secrets or backups. Keep protected credential and Home Assistant backups separately.

## Release decision

**No new suite-wide release is being published as part of this documentation update.** All three live connections have passed non-mutating smoke tests. Finish the remaining authorization, security and recovery checks before declaring a complete suite release.

See [README.md](README.md), [CHANGELOG.md](CHANGELOG.md) and [RECOVERY.md](RECOVERY.md).
