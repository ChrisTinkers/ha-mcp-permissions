# Release policy and v1.0.0 readiness

A live system working successfully is not sufficient evidence for reproducible deployment or secure release.

## Versions as installed (2026-11-13)

| Component | Version | State |
| --- | --- | --- |
| HA MCP Permissions | 0.1.4 | Running |
| HA MCP Write Tunnel | 0.1.1 | Running |
| HA MCP Read Tunnel | 0.1.1 | Running, GitHub-managed |
| Old OpenAI MCP Tunnel (lokal) | 0.1.0 | Stopped, rollback |
| External HA MCP Server | 9.2.0 | Running |

Versioning policy: semantic versioning per app; an optional suite-wide `v1.0.0` release tag only when the whole installation passes the acceptance criteria. App versions and matching Docker build metadata should be aligned before release.

## Verification checklist

- [x] Four write tools present and functional in the allowed development list
- [x] Fixed-target write gateway and restricted-service implementation inspected
- [x] Unit and mocked runtime/service-scope tests in repository
- [x] GitHub Actions checks on latest read-tunnel v0.1.1 changes reported successful
- [x] GitHub-managed read tunnel installed and running; old local app stopped
- [x] App reports security rating 7/8 with host networking disabled
- [x] Home Assistant read operation succeeded after read tunnel switchover
- [x] README and deployment/migration documentation updated
- [ ] Full live end-to-end verification explicitly via each tunnel connection
- [x] Gitleaks full-history scan succeeded on 2026-11-13; no scanner findings. This is not a guarantee that all possible secret types were detected; rotate credentials if independent evidence of exposure appears
- [ ] Demonstrate the running container image corresponds to reviewed source
- [x] Live input-validation negative test: blank task title rejected and all 13 existing tasks unchanged (2026-11-13)
- [ ] Independently verify denied writes against other entities/services (mocked scope tests pass; live scope escape test not conducted)
- [ ] Dependency and base-image vulnerability review, plus version pinning strategy
- [x] Existing pre-release app versions and Docker build defaults are internally consistent (0.1.4 / 0.1.1 / 0.1.1)
- [ ] Consistent 1.0.0 versions in three app configs and Docker build labels
- [x] Documented recovery and rollback in [RECOVERY.md](RECOVERY.md)
- [x] User confirmed in Home Assistant UI that the prior successful backup contains HA MCP Permissions, HA MCP Write Tunnel, and the old local read tunnel (2026-11-13). This provides a rollback source for those apps, not for the newly installed GitHub-managed read tunnel.
- [ ] Test clean install, upgrade/rollback and actual restoration from backup; direct backup listing through read-only MCP is deliberately blocked by HA MCP Server setting enable_snapshot_actions=false
- [x] User verified on 2026-11-13: UniFi Dream Router has no manual port forwarding and UPnP is disabled
- [ ] Confirm exact Home Assistant Core/OS versions and any other external access paths or firewall/ingress restrictions
- [ ] Publish final release notes and tag only after all required checks

## Residual risk

HA MCP Permissions uses `homeassistant_api: true`, which supplies a privileged Supervisor-issued API token. The service/action/entity restriction is enforced in application code, not by a restricted token. An application compromise could breach that boundary.

Do not commit keys, tunnel IDs, private URLs or populated Home Assistant app options. The GitHub repository does not include the credentials needed to restore the installation.

## Release decision

**Not released as v1.0.0 yet.** See [CHANGELOG.md](CHANGELOG.md) and [README.md](README.md). Release only after the remaining checks are confirmed, rather than equating working functionality with audited security.
