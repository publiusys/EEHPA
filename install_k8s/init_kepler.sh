#!/bin/bash

set -x

tar -xf kepler.tar.gz

currdir=$(pwd)

## bad hack - ignore
#sed -i "s#PROJECT_ROOT=\"\$(git rev-parse --show-toplevel)\"#PROJECT_ROOT=\"$currdir/kepler-0.7.2/\"#" kepler-0.7.2/hack/tools.sh
#sed -i "s#PROJECT_ROOT=\"\$(git rev-parse --show-toplevel)\"#PROJECT_ROOT=\"$currdir/kepler-0.7.2/\"#" kepler-0.7.2/hack/build-manifest.sh

echo "🟢 building kepler manifests 🟢"
cd kepler
make build-manifest OPTS="BM_DEPLOY PROMETHEUS_DEPLOY"
kubectl apply -f _output/generated-manifest/deployment.yaml
cd $currdir

echo "🟢 wait 60 secs 🟢"
sleep 60

kubectl get pods --all-namespaces
kubectl config set-context --current --namespace=kepler
