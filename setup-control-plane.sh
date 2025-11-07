#!/bin/bash

# ----------------------------
# Kubernetes Control Plane Setup
# Multipass Ubuntu 22.04 VM
# ----------------------------

# Step 0: Update OS
echo "Updating Ubuntu packages..."
sudo apt update && sudo apt upgrade -y

# Step 1: Disable swap
echo "Disabling swap..."
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab

# Step 2: Install containerd
echo "Installing containerd..."
sudo apt install -y containerd
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

# Step 3: Add Kubernetes apt repository
echo "Adding Kubernetes repository..."
sudo apt install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg \
  https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] \
https://apt.kubernetes.io/ kubernetes-xenial main" | \
  sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update

# Step 4: Install Kubernetes components
echo "Installing kubelet, kubeadm, kubectl..."
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Step 5: Initialize Kubernetes control plane
echo "Initializing Kubernetes control plane..."
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Step 6: Configure kubectl for current user
echo "Setting up kubectl configuration..."
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Step 7: Install Flannel CNI
echo "Installing Flannel CNI plugin..."
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

# Step 8: Display join command for worker nodes
echo "Control plane setup complete!"
echo "Use the following command on worker nodes to join this cluster:"
kubeadm token create --print-join-command

# Step 9: Display node status
kubectl get nodes -o wide
kubectl get pods -n kube-system
