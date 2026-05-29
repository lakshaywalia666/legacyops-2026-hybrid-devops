# LegacyOps 2026 Helm Deployment Proof

## Status

LegacyOps 2026 was successfully deployed using the Helm chart in helm/legacyops.

## Helm Validation

Helm lint passed successfully.

Result:

1 chart(s) linted, 0 chart(s) failed

Helm template rendering also completed successfully.

## Helm Install Test

A temporary Helm release was installed for validation.

Release name: legacyops-helm-test
Test namespace: legacyops-helm-test
Frontend NodePort: 31080
Backend NodePort: 31081

Result:

STATUS: deployed
REVISION: 1

## Kubernetes Result

All Helm-managed LegacyOps pods reached Running state.

backend  -> 1/1 Running
frontend -> 1/1 Running
postgres -> 1/1 Running
redis    -> 1/1 Running

## Frontend Verification

URL: http://localhost:31080

Result:

HTTP/1.1 200 OK

## Backend Verification

URL: http://localhost:31081/health

Result:

{"status":"ok","service":"Legacy Retail Operations System","version":"1.0.0","environment":"kubernetes"}

## Cleanup

The temporary Helm release was removed after validation.

Result:

release "legacyops-helm-test" uninstalled
namespace/legacyops-helm-test condition met
