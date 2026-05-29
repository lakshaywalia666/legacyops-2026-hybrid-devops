# Legacy Retail Operations System — Developer Code Handoff

This repository contains only the application code for the LegacyOps 2026 DevOps modernization project.

The DevOps engineer will add and own:
- Dockerfiles
- Docker Compose
- Kubernetes/K3s manifests
- Helm chart
- Terraform
- Ansible
- GitHub Actions
- Jenkins pipelines
- Argo CD
- Prometheus/Grafana/Loki
- Backup/restore automation

## Application stack

- Frontend: React + Vite
- Backend: Python FastAPI
- Database: PostgreSQL
- Queue/cache: Redis
- Worker: Python background worker

## Application features

- Dashboard summary
- Product management
- Inventory tracking
- Customer management
- Order management
- Billing-style order records
- Health endpoint
- Readiness endpoint
- Prometheus metrics endpoint
- Simple Redis job queue integration

## Repository structure

```text
legacyops_application_code_handoff/
├── app/
│   ├── backend/
│   ├── frontend/
│   └── worker/
├── docs/
│   ├── API_CONTRACT.md
│   ├── DATABASE_SCHEMA.md
│   └── DEVOPS_HANDOFF_NOTES.md
├── .env.example
├── .gitignore
└── README.md
```

## Local backend run without Docker

```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL="postgresql+psycopg2://legacyops:legacyops@localhost:5432/legacyops"
export REDIS_URL="redis://localhost:6379/0"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend docs:
- Swagger UI: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Readiness: http://localhost:8000/ready
- Metrics: http://localhost:8000/metrics

## Local frontend run without Docker

```bash
cd app/frontend
npm install
npm run dev
```

Frontend default:
- http://localhost:5173

Set backend API URL:

```bash
export VITE_API_URL="http://localhost:8000"
```

## Local worker run without Docker

```bash
cd app/worker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export REDIS_URL="redis://localhost:6379/0"
python worker.py
```

## Seed demo data

Start the backend and call:

```bash
curl -X POST http://localhost:8000/admin/seed
```

## Minimal backend tests

```bash
cd app/backend
pip install -r requirements.txt
pytest
```

Tests use SQLite by default through `tests/conftest.py`, so they do not require PostgreSQL.

## Important handoff note

This code is intentionally simple. It is built as the workload for a DevOps portfolio project. The value of the project comes from how it is containerized, deployed, monitored, secured, backed up, and operated.
