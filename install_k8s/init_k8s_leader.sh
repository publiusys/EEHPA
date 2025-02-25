#!/bin/bash

#set -x

echo "🟢 initialize cluster 🟢"
sudo kubeadm init --pod-network-cidr=10.10.0.0/16

echo "🟢 assuming init runs correctly 🟢"
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

echo "🟢 setup calico 🟢"
kubectl create -f calico/tigera-operator.yaml
kubectl create -f calico/custom-resources.yaml

echo "🟢 wait 120 seconds 🟢"
sleep 120
kubectl get pods --all-namespaces

echo "⚠️  ⚠️  Make sure a node join the cluster with the command below before continuing ⚠️  ⚠️ "
kubeadm token create --print-join-command

