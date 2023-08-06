# Global Water Watch Service
Backend API for synchronous operations within Global Water Watch

## Testing
```bash
docker-compose up
pytest
```

## Local deployment

Currently, I have 2 ways of deploying locally

### Debugging
For debugging, it is best to debug the main.py file in python, and use `docker-compose` to get the database running:
```docker-compose up```

Get earthengine credentials:
```make get_secrets```

And add the following environment variables (to your launch.json in VSCode) and .env:
```json
{
    "EE_SA": "dagster-workloads@global-water-watch.iam.gserviceaccount.com",
    "EE_PK": "${workspaceFolder}/gcloud_dist/privatekey.json"
}
```

We can then use `psql` to create the postgis extension:
```psql -U testuser -h localhost -d testdb```
using the `testpassword`.

Then use (for example) VSCode to debug main.py.

### Local kubernetes

To test kubernetes (later for some extra functionality like workflows), you can deploy a local cluster.
This is simplified in the `Makefile`. 
- Install [kind](https://kind.sigs.k8s.io/).
- Install [kubectl](https://kubernetes.io/docs/tasks/tools/)
- Install [helm](https://helm.sh/)

```
make build-docker
make deploy-local
```

Check out the database:
in one terminal:
```
export PGMASTER=$(kubectl get pods -o jsonpath={.items..metadata.name} -l application=spilo,cluster-name=gwwuser-gww,spilo-role=master -n gww)
kubectl port-forward $PGMASTER 6432:5432 -n gww
```
in another:
```
export PGPASSWORD=$(kubectl get secret -n gww gwwuser.gwwuser-gww.credentials.postgresql.acid.zalan.do -o 'jsonpath={.data.password}' | base64 -d)
export PGSSLMODE=require
psql -U gwwuser -h localhost -p 6432 -d gwwdb
```

Check out the api:
```
kubectl port-forward -n gww svc/gww-api 8080:80
```

After you are done:
```
kind delete clusters waterwatch
```

> Note: This is to test working with other software, for debugging, using VSCode together with
> docker-compose and FastAPI's `--reload` option helps developing quickly.

## Deploy on kubernetes

This repository contains a helm chart that deploys the API to kubernetes.
For example values, check out [the values file](helm/gww-api/values.yaml).
