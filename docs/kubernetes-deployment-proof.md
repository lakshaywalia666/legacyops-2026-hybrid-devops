# Kubernetes Deployment Proof

## Cluster Workloads
NAME                                      READY   STATUS    RESTARTS   AGE
pod/legacyops-backend-85dc6b6749-ck5dz    1/1     Running   0          173m
pod/legacyops-frontend-859ff74fb8-cxk8t   1/1     Running   0          173m
pod/legacyops-postgres-5d4fd765fb-dnnfq   1/1     Running   0          4h27m
pod/legacyops-redis-7b75dd7d5c-9tcqw      1/1     Running   0          4h27m

NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/legacyops-backend    NodePort    10.43.55.68     <none>        8000:30081/TCP   4h27m
service/legacyops-frontend   NodePort    10.43.251.8     <none>        80:30080/TCP     4h27m
service/legacyops-postgres   ClusterIP   10.43.145.61    <none>        5432/TCP         4h27m
service/legacyops-redis      ClusterIP   10.43.238.104   <none>        6379/TCP         4h27m

NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/legacyops-backend    1/1     1            1           4h27m
deployment.apps/legacyops-frontend   1/1     1            1           4h27m
deployment.apps/legacyops-postgres   1/1     1            1           4h27m
deployment.apps/legacyops-redis      1/1     1            1           4h27m

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/legacyops-backend-559d66659     0         0         0       4h15m
replicaset.apps/legacyops-backend-849876b55     0         0         0       4h27m
replicaset.apps/legacyops-backend-85dc6b6749    1         1         1       173m
replicaset.apps/legacyops-frontend-57d9b65d64   0         0         0       4h16m
replicaset.apps/legacyops-frontend-859ff74fb8   1         1         1       173m
replicaset.apps/legacyops-frontend-bccbf564f    0         0         0       4h27m
replicaset.apps/legacyops-postgres-5d4fd765fb   1         1         1       4h27m
replicaset.apps/legacyops-redis-7b75dd7d5c      1         1         1       4h27m

## Frontend NodePort Test
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Fri, 29 May 2026 15:28:36 GMT
Content-Type: text/html
Content-Length: 416
Last-Modified: Fri, 29 May 2026 11:40:56 GMT
Connection: keep-alive
ETag: "6a197b48-1a0"
Accept-Ranges: bytes


## Backend Health Test
{"status":"ok","service":"Legacy Retail Operations System","version":"1.0.0","environment":"kubernetes"}

## Backend Readiness Test
{"status":"ready","dependencies":{"database":"ok","redis":"ok"}}
