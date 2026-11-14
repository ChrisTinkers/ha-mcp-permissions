# Release policy and readiness

**Documentation status: 2026-11-14.** The three core apps run on version 1.0.0, and the experimental Config Reader is installed at 1.1.1 but stopped. App version numbers are independent. A suite-wide `v1.0.0` GitHub release/tag is **not documented as published**.

## Directly observed Home Assistant state

| Component | Installed version | Observed state |
| --- | --- | --- |
| HA MCP Permissions | 1.0.0 | Running |
| HA MCP Write Tunnel | 1.0.0 | Running |
| HA MCP Read Tunnel | 1.0.0 | Running |
| HA MCP Config Reader | 1.1.1 | Stopped |
| External Home Assistant MCP Server | 9.2.0 | Running |
| Old OpenAI MCP Tunnel (local) | 0.1.0 | Stopped, retained for rollback |

The Config Reader requires a separate tunnel and ChatGPT connection; its installation alone does not expose the new tools.

## Release verification checklist

### Completed or previously documented

- [x] Restricted write gateway implements four scoped tools for `todo.ha_weiterentwicklung`.
- [x] Unit, service-scope and mocked runtime tests exist in the repository.
- [x] Core apps 1.0.0 are installed and reported running on 2026-11-14.
- [x] Config Reader 1.1.1 is installed and reported stopped on 2026-11-14.
- [x] Automated tests and Docker build for Config Reader 1.1.1 implementation passed on GitHub Actions.
- [x] Full Git-history secret scan passed on the implementation commit; a scan cannot guarantee absence of every secret.
- [x] Earlier read-tunnel migration and successful read call were documented.
- [x] Recovery/rollback instructions exist in [RECOVERY.md](RECOVERY.md).
- [x] Earlier user confirmation of a Home Assistant backup covering the original core apps was documented; it does **not** prove a restore.
- [x] Earlier user verification documented no manual UniFi port forwarding and disabled UPnP.

### Still outstanding

- [ ] Start and smoke-test the Config Reader 1.1.1 with a reviewed allowlist.
- [ ] Provision a separate Config Reader tunnel and ChatGPT connection; test allowed and denied reads end-to-end.
- [ ] Re-verify both existing read and restricted-write paths end-to-end after deployment changes.
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

**No new suite-wide release is being published as part of this documentation update.** Continue operating the existing core apps without changes. Finish live Config Reader connectivity and the remaining security/recovery checks before declaring a complete release.

See [README.md](README.md), [CHANGELOG.md](CHANGELOG.md) and [RECOVERY.md](RECOVERY.md).
