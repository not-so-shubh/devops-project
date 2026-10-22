# Docker and Compose

[Documentation hub](../docs/README.md) · [Quick start](../README.md#quick-start) · [Deployment](../docs/DEPLOYMENT.md#local-compose)

Canonical definitions are [`backend/Dockerfile`](../backend/Dockerfile), [`frontend/Dockerfile`](../frontend/Dockerfile) and [`docker-compose.yml`](../docker-compose.yml). This guide maps the coursework's `docker/` deliverable without duplicating build contexts.

| Service | Behavior |
|---|---|
| PostgreSQL | Private network, health check and persistent named volume |
| Migration | One-shot Alembic upgrade after database health |
| Backend | Starts after migration, UID 10001, port 8000, database-aware readiness |
| Frontend | Node builder/Nginx runtime, UID 101, internal 8080 mapped to loopback 3000 |

Both application runtimes have read-only filesystems, temporary writable mounts, dropped capabilities and no privilege escalation. Base images are digest-pinned and dependencies locked.

After the secure root setup, from the repository root:

```bash
docker compose config --quiet
docker compose up --build -d --wait --wait-timeout 180
docker compose ps
python3 scripts/smoke.py
```

`docker compose down` retains database data. Deleting volumes with `down -v` is destructive and should be an explicit local-demo decision. Changing `.env` does not change the password already stored in an initialized database volume.

CI also runs [`verify-compose-persistence.py`](../scripts/verify-compose-persistence.py): it creates a synthetic product/movement, restarts PostgreSQL, verifies both records and cleans up its catalog probe. [Source-pinned result](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/persistence-ci.txt).
