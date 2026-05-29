# LegacyOps 2026 Jenkins Pipeline Proof

## Status

A Jenkins declarative pipeline has been added using a root-level `Jenkinsfile`.

This pipeline validates the LegacyOps application through backend checks, frontend build checks, Docker Compose validation, health checks, and cleanup.

## Pipeline Stages

The Jenkins pipeline includes:

1. Checkout
2. Backend validation
3. Frontend validation
4. Docker Compose validation
5. Cleanup using `post { always { ... } }`

## Backend Validation

The backend stage performs the following checks:

- Creates a Python virtual environment
- Installs backend dependencies from `requirements.txt`
- Compiles the backend application
- Runs backend tests with pytest
- Verifies the FastAPI application import

Local validation result:

```text
3 passed, 2 warnings
Backend import OK: Legacy Retail Operations System
```

The warnings are FastAPI deprecation warnings and do not fail the pipeline.

## Frontend Validation

The frontend stage uses a Dockerized Node.js 22 runtime:

```text
node:22-alpine
```

This avoids failures caused by older Node.js versions installed on the Jenkins host.

Local validation result:

```text
vite v8.0.14 building client environment for production...
✓ built
```

## Docker Compose Validation

The Docker Compose stage performs the following checks:

- Stops old containers and removes orphaned resources
- Validates Docker Compose configuration
- Builds backend and frontend images
- Starts the full application stack
- Verifies backend health endpoint
- Verifies frontend HTTP response
- Cleans up containers, volume, and network

Local validation result:

```text
{"status":"ok","service":"Legacy Retail Operations System","version":"1.0.0","environment":"docker"}
HTTP/1.1 200 OK
```

Cleanup completed successfully:

```text
Container legacyops-frontend Removed
Container legacyops-backend Removed
Container legacyops-redis Removed
Container legacyops-postgres Removed
Volume legacyops-application_legacyops_postgres_data Removed
Network legacyops-application_default Removed
```

## Notes

The Jenkinsfile is designed for Jenkins agents with Docker access.

During local validation, `sudo docker` was required because the local user did not have direct access to `/var/run/docker.sock`.

The Jenkinsfile itself does not use `sudo`; Jenkins agents should be configured with proper Docker permissions.
