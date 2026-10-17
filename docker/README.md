# Docker deliverable

Canonical build definitions: [`backend/Dockerfile`](../backend/Dockerfile), [`frontend/Dockerfile`](../frontend/Dockerfile) and [`docker-compose.yml`](../docker-compose.yml). This directory supplies the homework PDF's `docker/` entry while keeping build contexts with their component sources.

Run commands from the repository root. Copy `.env.example` to `.env`, replace the local password, then `docker compose config --quiet` and `docker compose up --build -d --wait --wait-timeout 180`. Inspect `docker compose ps`, run `python3 scripts/smoke.py`, and open http://localhost:3000. The migration service completes before the backend starts; PostgreSQL uses a named persistent volume. Both application runtimes run as non-root with read-only filesystems and dropped capabilities; frontend uses a Node builder and unprivileged Nginx runtime.

See [deployment and cleanup](../docs/DEPLOYMENT.md), [persistence verification](../scripts/verify-compose-persistence.py) and [real CI evidence](../docs/EVIDENCE.md).
