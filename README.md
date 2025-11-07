# kub8s_setup
# Kubernetes Setup using Multipass (Control Plane + Worker)

This guide documents how I set up a **Kubernetes cluster** using **Multipass** on macOS, with a Linux VM serving as the **control plane**, and optionally connecting **Raspberry Pi devices** or other VMs as worker nodes.

---

## 🧰 Requirements

- **macOS** with [Multipass](https://multipass.run) installed  
- Minimum resources for control plane:
  - 2 CPUs
  - 2 GB RAM
  - 10 GB Disk
- Internet access for package installation

---

## ⚙️ What I Did

1. **Installed Multipass** on macOS:
   ```bash
   brew install --cask multipass
Launched a Linux VM for the Control Plane:

multipass launch --name k8s-control --cpus 2 --mem 2G --disk 10G


Checked the status of the VM:

multipass list


Accessed the Control Plane VM:

multipass shell k8s-control


Installed Kubernetes prerequisites inside the VM:

sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] \
https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl


Initialized the Kubernetes Control Plane:

sudo kubeadm init --pod-network-cidr=10.244.0.0/16


Configured kubectl access:

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config


Installed the Flannel CNI plugin:

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml


(Optional) Added worker nodes using the join command from kubeadm init output:

sudo kubeadm join <control-plane-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>

💻 How to Login to the Control Plane VM

To log back into the control plane node:

multipass shell k8s-control


This opens an interactive shell session inside the control plane VM.
🔍 Useful Multipass Commands
Command	Description
multipass list	List all running VMs
multipass stop <name>	Stop a VM
multipass start <name>	Start a stopped VM
multipass delete <name>	Delete a VM
multipass purge	Remove all deleted VMs

🧩 Next Steps

Add worker nodes (e.g., Raspberry Pi devices) using the kubeadm join command.

Deploy test workloads with kubectl.

Configure persistent storage or ingress if needed.

Author: Keerthi Pitchaimani
Date: November 2025


---

