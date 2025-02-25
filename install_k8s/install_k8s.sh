#!/bin/bash

set -x

sudo apt-get update

# taken from https://www.cherryservers.com/blog/install-kubernetes-on-ubuntu

# disable swap
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab
lsblk

# Set up the IPV4 bridge on all nodes
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter

# sysctl params required by setup, params persist across reboots
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system

# Install kubelet, kubeadm, and kubectl on each node
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo mkdir /etc/apt/keyrings
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --yes --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sleep 1
sudo apt-get update -y
sudo apt-get install -y kubelet kubeadm kubectl
#sudo apt install -y kubelet=1.28.2-00 kubeadm=1.28.2-00 kubectl=1.28.2-00

# prevents them from being updated, upgraded, etc
sudo apt-mark hold kubeadm kubelet kubectl

# install docker
sudo apt install -y docker.io
sudo mkdir /etc/containerd
sudo sh -c "containerd config default > /etc/containerd/config.toml"
sudo sed -i 's/ SystemdCgroup = false/ SystemdCgroup = true/' /etc/containerd/config.toml

# may need to disable apparmor
sudo systemctl stop apparmor
sudo systemctl disable apparmor 

sudo systemctl restart containerd.service
sudo systemctl enable kubelet.service
sudo systemctl restart kubelet.service
sudo systemctl enable kubelet.service

# initialize kubernetes services
sudo kubeadm config images pull

# install golang for kepler
sudo apt-get install -y golang

# disable HyperThreads
#echo off | sudo tee /sys/devices/system/cpu/smt/control

# disable TurboBoost
#echo "1" | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

# disable irq rebalance
#sudo killall irqbalance
