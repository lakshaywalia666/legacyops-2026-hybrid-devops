# Kubernetes Home Lab Validation

Date: 2026-05-29T11:20:16+00:00
Server: lwlabs
Server IP: 192.168.1.12

## Pods and Services
```
NAME                                      READY   STATUS    RESTARTS   AGE     IP           NODE     NOMINATED NODE   READINESS GATES
pod/legacyops-backend-559d66659-dr8ht     1/1     Running   0          7m12s   10.42.0.15   lwlabs   <none>           <none>
pod/legacyops-frontend-57d9b65d64-bzw2r   1/1     Running   0          8m10s   10.42.0.14   lwlabs   <none>           <none>
pod/legacyops-postgres-5d4fd765fb-dnnfq   1/1     Running   0          19m     10.42.0.13   lwlabs   <none>           <none>
pod/legacyops-redis-7b75dd7d5c-9tcqw      1/1     Running   0          19m     10.42.0.11   lwlabs   <none>           <none>

NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE   SELECTOR
service/legacyops-backend    NodePort    10.43.55.68     <none>        8000:30081/TCP   19m   app.kubernetes.io/managed-by=kustomize,app.kubernetes.io/name=legacyops-backend
service/legacyops-frontend   NodePort    10.43.251.8     <none>        80:30080/TCP     19m   app.kubernetes.io/managed-by=kustomize,app.kubernetes.io/name=legacyops-frontend
service/legacyops-postgres   ClusterIP   10.43.145.61    <none>        5432/TCP         19m   app.kubernetes.io/managed-by=kustomize,app.kubernetes.io/name=legacyops-postgres
service/legacyops-redis      ClusterIP   10.43.238.104   <none>        6379/TCP         19m   app.kubernetes.io/managed-by=kustomize,app.kubernetes.io/name=legacyops-redis
```

## Backend Health
```
HTTP/1.1 200 OK
date: Fri, 29 May 2026 11:20:15 GMT
server: uvicorn
content-length: 104
content-type: application/json

{"status":"ok","service":"Legacy Retail Operations System","version":"1.0.0","environment":"kubernetes"}
```

## Backend Readiness
```
HTTP/1.1 200 OK
date: Fri, 29 May 2026 11:20:15 GMT
server: uvicorn
content-length: 64
content-type: application/json

{"status":"ready","dependencies":{"database":"ok","redis":"ok"}}
```

## Frontend
```
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Fri, 29 May 2026 11:20:16 GMT
Content-Type: text/html
Content-Length: 416
Last-Modified: Fri, 29 May 2026 11:08:17 GMT
Connection: keep-alive
ETag: "6a1973a1-1a0"
Accept-Ranges: bytes

```

## Browser URLs
- Frontend: http://192.168.1.12:30080
- Backend readiness: http://192.168.1.12:30081/ready
