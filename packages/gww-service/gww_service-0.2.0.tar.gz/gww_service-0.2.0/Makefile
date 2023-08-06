SHELL := /bin/bash

sa_key_name = privatekey.json
version = $(shell cat gww_service/__init__.py | grep -oP "\d+\.\d+\.\d+")
TWINE_PASSWORD = ${TWINE_PASSWORD}

.PHONY: build push deploy get_secrets deploy-local

build-docker:
	docker build . -t gww-api:${version}
	
push-docker: build-docker
	docker tag gww-api:${version} us.gcr.io/global-water-watch/gww-api:${version}
	docker push us.gcr.io/global-water-watch/gww-api:${version}

build-python:
	pip install flit wheel twine
	flit build

push-python: build-python
	python -m twine check dist/*
	python -m twine upload dist/*

push-python-test: build-python
	python -m twine check dist/*
	@python -m twine upload --repository testpypi -u __token__ dist/*

test: build-docker
	docker-compose run --rm api hack/testing-entrypoint.sh pytest tests \
		--doctest-modules \
		--junitxml=junit/test-results.xml \
		--cov=gww_service \
		--cov-report=xml \
		--cov-report=html

deploy:
	helm upgrade gww-api ./helm/gww-api -i \
		--namespace gww \
		--atomic \
		--create-namespace

get_secrets:
	mkdir -p gcloud_dist
	gcloud secrets versions access "latest" --secret="gww-private-key" --format='get(payload.data)' | tr '_-' '/+' | base64 -d > gcloud_dist/$(sa_key_name)

deploy-local: get_secrets
	if ! [[ $$(kind get clusters | grep gww) ]]; \
	then \
		kind create cluster --config kind.yaml; \
	fi;
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
	sleep 20
	kubectl wait --namespace ingress-nginx \
		--for=condition=ready pod \
		--selector=app.kubernetes.io/component=controller \
		--timeout=90s
	docker build . -t gww-api:${version}
	kind load docker-image gww-api:${version} --name gww
	helm repo add postgres-operator-charts https://opensource.zalando.com/postgres-operator/charts/postgres-operator
	helm repo update
	kubectl create namespace gww --dry-run=client -o yaml | kubectl apply -f -
	kubectl create secret -n gww generic ee-sa-credentials \
		--from-file=gcloud_dist/$(sa_key_name) \
		--dry-run -o yaml | kubectl apply -f -
	helm upgrade postgresql postgres-operator-charts/postgres-operator -i --namespace gww
	helm upgrade gww-api ./helm/gww-api -i \
		--namespace gww \
		--set "image.repository=gww-api" \
		--set "image.tag=${version}" \
		--set image.pullPolicy=IfNotPresent \
		--set "postgresql.resources.requests.cpu=250m" \
		--set "postgresql.resources.requests.memory=512Mi" \
		--set "postgresql.resources.limits.cpu=500m" \
		--set "postgresql.resources.limits.memory=1Gi" \
		--set "postgresql.storageClass=null" \
		--set "postgresql.volumeSize=5Gi" \
		--set "postgresql.createNodeSelector=false" \
		--set "postgresql.useNodeAffinity=false"
