# LegacyOps 2026 — Hybrid DevOps Modernization Platform

[![LegacyOps CI](https://github.com/lakshaywalia666/legacyops-2026-hybrid-devops/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/lakshaywalia666/legacyops-2026-hybrid-devops/actions/workflows/ci.yml)

LegacyOps 2026 is a full-stack retail operations application used as a production-style DevOps modernization project.

The goal of this project is to demonstrate real-world DevOps skills across containerization, CI/CD, infrastructure automation, Kubernetes, monitoring, and hybrid cloud operations.

---

## Project status

Completed so far:

- Backend containerization with Docker
- Frontend containerization with Docker
- Full local stack using Docker Compose
- PostgreSQL service
- Redis service
- FastAPI backend service
- React/Vite frontend service served through Nginx
- GitHub Actions CI pipeline
- Pull request based workflow
- CI validation for backend, frontend, and Docker Compose stack
- GHCR container image publishing
- Kubernetes base manifests
- Kubernetes deployment using K3s
- Frontend and backend verified through Kubernetes NodePort services
- Kubernetes deployment proof documented in docs/kubernetes-deployment-proof.md

Planned next milestones:

- Helm chart
- Jenkins pipeline
- Terraform infrastructure
- Ansible automation
- Prometheus, Grafana, and Loki observability
- Backup and restore automation
- Argo CD GitOps deployment

---

## Architecture

```text
User Browser
    |
    v
Frontend Container
React + Vite + Nginx
Port 3000
    |
    v
Backend Container
Python FastAPI
Port 8000
    |
    +------------------+
    |                  |
    v                  v
PostgreSQL          Redis
Port 5432           Port 6379
```

---

## Application stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Nginx |
| Backend | Python, FastAPI, Uvicorn |
| Database | PostgreSQL |
| Cache / Queue | Redis |
| Containerization | Docker |
| Local orchestration | Docker Compose |
| CI/CD | GitHub Actions |
| Source control | Git, GitHub |

---

## Repository structure

```text
legacyops-application/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── backend/
│   │   ├── app/
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   ├── package.json
│   │   └── package-lock.json
│   └── worker/
├── docs/
├── docker-compose.yml
└── README.md
```

---

## Run locally with Docker Compose

### 1. Start the full stack

```bash
docker compose up -d
```

This starts:

- PostgreSQL
- Redis
- Backend
- Frontend

### 2. Check container status

```bash
docker compose ps
```

Expected result:

```text
legacyops-postgres   healthy
legacyops-redis      healthy
legacyops-backend    healthy
legacyops-frontend   healthy
```

### 3. Test backend health

```bash
curl -s http://localhost:8000/health && echo
```

Expected response:

```json
{
  "status": "ok",
  "service": "Legacy Retail Operations System",
  "version": "1.0.0",
  "environment": "docker"
}
```

### 4. Test frontend

```bash
curl -I http://localhost:3000
```

Expected response:

```text
HTTP/1.1 200 OK
```

Open the frontend in browser:

```text
http://localhost:3000
```

---

## Useful local URLs

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend health | http://localhost:8000/health |
| Backend readiness | http://localhost:8000/ready |
| Backend Swagger docs | http://localhost:8000/docs |
| Backend metrics | http://localhost:8000/metrics |

---

## Docker Compose services

| Service | Container name | Port |
|---|---|---|
| postgres | legacyops-postgres | 5432 |
| redis | legacyops-redis | 6379 |
| backend | legacyops-backend | 8000 |
| frontend | legacyops-frontend | 3000 |

---

## Stop the stack

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

---

## Rebuild after code changes

```bash
docker compose build
docker compose up -d
```

Or rebuild and start together:

```bash
docker compose up -d --build
```

---

## GitHub Actions CI

The project includes a GitHub Actions workflow at:

```text
.github/workflows/ci.yml
```

The CI pipeline runs on:

- Pushes to `main`
- Pushes to `feature/**` branches
- Pull requests targeting `main`

CI validates:

1. Backend Python dependencies
2. Backend source compilation
3. FastAPI application import
4. Frontend dependency installation
5. Frontend production build
6. Docker Compose config
7. Docker image builds
8. Full stack startup
9. Backend health endpoint
10. Frontend HTTP response

---

## Local backend run without Docker

```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL="postgresql+psycopg2://legacyops:legacyops@localhost:5432/legacyops"
export REDIS_URL="redis://localhost:6379/0"
export REDIS_REQUIRED="false"

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Local frontend run without Docker

```bash
cd app/frontend
npm install
export VITE_API_URL="http://localhost:8000"
npm run dev
```

Frontend dev server:

```text
http://localhost:5173
```

---

## Seed demo data

Start the backend first, then run:

```bash
curl -X POST http://localhost:8000/admin/seed
```

---

## DevOps portfolio purpose

This repository is designed as a DevOps portfolio project, not just an application codebase.

The main DevOps value comes from:

- Containerizing legacy-style services
- Creating repeatable local environments
- Building CI/CD pipelines
- Deploying to Kubernetes
- Managing infrastructure with Terraform
- Automating servers with Ansible
- Adding monitoring and logging
- Practicing backup and recovery
- Operating a hybrid cloud + home server setup

---

## Current milestone

The project currently supports a complete local Dockerized workflow:

```bash
docker compose up -d
```

One command starts the full application stack:

```text
postgres + redis + backend + frontend
```
