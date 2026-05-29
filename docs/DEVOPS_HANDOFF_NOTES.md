# DevOps Handoff Notes

This application was written as a realistic workload for the LegacyOps 2026 hybrid DevOps project.

## What the developer gives

- React frontend source
- FastAPI backend source
- Python worker source
- API contract
- Database schema
- `.env.example`
- Minimal tests

## What the DevOps engineer should add

- Dockerfiles for frontend, backend, and worker
- Docker Compose with frontend, backend, worker, PostgreSQL, and Redis
- Kubernetes deployments/services/statefulset/configmaps/secrets
- Helm chart and environment values
- Terraform AWS infra
- Ansible server automation
- CI/CD workflows
- Argo CD app manifests
- Jenkins operational pipelines
- Prometheus/Grafana/Loki monitoring
- Backup and restore automation

## Backend health endpoints

Use these in Docker, Kubernetes, Helm, Argo CD, Jenkins, Uptime Kuma, and monitoring:

```text
GET /health
GET /ready
GET /metrics
```

Recommended Kubernetes probes:
- Liveness: `/health`
- Readiness: `/ready`

## Service ports

| Service | Port |
|---|---:|
| frontend | 5173 in dev, 80/3000 after containerization |
| backend | 8000 |
| PostgreSQL | 5432 |
| Redis | 6379 |

## Environment variables

Backend:

```text
APP_NAME
APP_ENV
APP_VERSION
DATABASE_URL
REDIS_URL
REDIS_REQUIRED
CORS_ORIGINS
```

Frontend:

```text
VITE_API_URL
```

Worker:

```text
REDIS_URL
LEGACYOPS_JOB_QUEUE
WORKER_POLL_TIMEOUT_SECONDS
```

## Important note for portfolio honesty

Say this in interviews:

> The application code was treated as a developer-provided workload. My main contribution was the DevOps implementation: containerization, infrastructure, automation, Kubernetes, CI/CD, monitoring, logging, backup, and incident recovery.
