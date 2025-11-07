#!/bin/bash
# ----------------------------
# Kubernetes Control Plane Setup
# Ubuntu 22.04 (Jammy) VM -- Multipass
# ----------------------------
set -e

echo "=== Updating Ubuntu packages ==="
sudo apt update && sudo apt upgrade -y

echo "=== Disabling swap ==="
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab

echo "=== Installing containerd ==="
sudo apt install -y containerd
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

echo "=== Setting up Kubernetes repository (pkgs.k8s.io) ==="
# Remove old repository definitions if present
sudo rm -f /etc/apt/sources.list.d/kubernetes.list
sudo rm -f /usr/share/keyrings/kubernetes-apt-keyring.gpg

sudo apt install -y apt-transport-https ca-certificates curl gnupg

# Create keyrings directory (if not exists)
sudo mkdir -p /etc/apt/keyrings

# Download the GPG key from pkgs.k8s.io for the desired K8s version (replace v1.34 with your target version)
TARGET_VERSION="v1.34"
curl -fsSL "https://pkgs.k8s.io/core:/stable:/${TARGET_VERSION}/deb/Release.key" | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add repository
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/${TARGET_VERSION}/deb/ /" | \
  sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update

echo "=== Installing kubelet, kubeadm, kubectl ==="
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

echo "=== Initializing Kubernetes control plane ==="
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

echo "=== Configuring kubectl for your user ==="
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

echo "=== Installing Flannel CNI plugin ==="
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

echo "=== Cluster setup complete! ==="
echo ""
echo "Use the following command on worker nodes to join this cluster:"
kubeadm token create --print-join-command
echo ""
echo "Check cluster status:"
kubectl get nodes -o wide
kubectl get pods -n kube-system
