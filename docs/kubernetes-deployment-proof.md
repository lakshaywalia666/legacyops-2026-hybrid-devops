# LegacyOps 2026 Kubernetes Deployment Proof

## Status

LegacyOps 2026 was successfully deployed on Kubernetes using GHCR container images.

## Verified Results

### Frontend NodePort

URL: http://localhost:30080

Result:

HTTP/1.1 200 OK

### Backend NodePort

URL: http://localhost:30081/health

Result:

{"status":"ok","service":"Legacy Retail Operations System","version":"1.0.0","environment":"kubernetes"}

## Kubernetes Result

All LegacyOps pods, services, and deployments are running successfully in the legacyops namespace.

## Images Used

backend  -> ghcr.io/lakshaywalia666/legacyops-2026-hybrid-devops/legacyops-backend:latest
frontend -> ghcr.io/lakshaywalia666/legacyops-2026-hybrid-devops/legacyops-frontend:latest
redis    -> redis:7-alpine
postgres -> postgres:16-alpine
