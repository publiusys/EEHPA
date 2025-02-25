#!/bin/bash

#set -x

tar -xf kube-prometheus-0.13.0.tar.gz

echo "🟢 apply prometheus manifests 🟢"
kubectl apply --server-side -f kube-prometheus-0.13.0/manifests/setup

sleep 1
until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
sleep 1

kubectl apply -f kube-prometheus-0.13.0/manifests/

echo "🟢 wait 60 secs 🟢"
sleep 60
kubectl get pods --all-namespaces
