# Release policy and v1.0.0 readiness

A successful live setup does not by itself mean the project is reproducible, secure or ready for a stable release.

## Versioning

- Use semantic versions `MAJOR.MINOR.PATCH` for each Home Assistant app.
- The repository may additionally carry a suite-wide tag once all components are present and verified.
- Current **installed** versions: HA MCP Permissions 0.1.4, HA MCP Write Tunnel 0.1.1, local read tunnel 0.1.0 (2026-11-13).
- **Proposed first stable version:** 1.0.0. **Not released yet.**
- Document and test upgrades with a rollback path; do not automatically alter running installations as part of documentation work.

## v1.0.0 acceptance checklist

- [x] Four write MCP tools exposed; functional add/rename/complete/list smoke checks done
- [x] Source review: fixed to-do entity, action allowlist and internal tunnel destination
- [x] Mocked authorization tests exist in `tests/`
- [x] Repository documentation updated to distinguish design from deployed state
- [ ] Recover the actual **local read tunnel** implementation, sanitized and documented
- [ ] Inspect current Git history for leaked credentials; rotate and purge any exposed secret
- [ ] Verify running container image corresponds to reviewed source/commit
- [ ] Verify live negative authorization tests without changing unrelated Home Assistant resources
- [ ] Pin/review runtime dependencies and base images as appropriate; confirm CI is green
- [ ] Align version numbers in `config.yaml`, Docker build metadata and changelog
- [ ] Test fresh installation, upgrade and restoration from backups
- [ ] Record tested Home Assistant Core, OS and upstream MCP server versions
- [ ] Confirm local firewall/ingress controls and no router port forwarding
- [ ] Publish release tag and notes only after checks above complete

## Security assumptions

The Permissions app requests `homeassistant_api: true`. The resulting Supervisor token is powerful; the least-privilege boundary is implemented in the application. It is not equivalent to a Home Assistant-scoped API credential. Any compromise of the app process could bypass its own policy.

A secret URL path is an access credential, **not** a substitute for reviewing network and key handling. Treat URLs, app options and logs as sensitive; keep credential values only in local secret stores.

## Change control

Changes adding write scopes require explicit review, threat model updates, additional negative tests and an independent release. Do not quietly add arbitrary domain/entity/service arguments.
