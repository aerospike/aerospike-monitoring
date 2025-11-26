# Datadog Aerospike Enterprise Integration on Kubernetes 

This guide explains how to deploy **Aerospike Server**, **Aerospike Prometheus Exporter**, and set up **Datadoga Aerospike Enterprise Integration** monitoring on a Kubernetes cluster using the Aerospike Kubernetes Operator (AKO).

---

## 🧩 Prerequisites

- A working **Kubernetes cluster** (v1.25+)
- `kubectl` installed and configured
- Internet access to pull container images and apply manifests
- Sufficient permissions to create namespaces, CRDs, and cluster-wide roles
- Aerospike server configuration and feature files

---

## 🧠 Step 1 — Install Operator Lifecycle Manager (OLM)

OLM manages the installation and upgrades of Kubernetes operators.

```bash
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.38.0/install.sh | bash -s v0.38.0
```

Verify that OLM pods are running:

```bash
kubectl get pods -n olm
```

---

## 🧰 Step 2 — Install Aerospike Kubernetes Operator (AKO)

The Aerospike Operator automates Aerospike cluster management in Kubernetes.
For reference, see [Aerospike AKO Installation Docs](https://aerospike.com/docs/kubernetes/install/olm/).

```bash
kubectl create -f https://operatorhub.io/install/aerospike-kubernetes-operator.yaml
```

Check operator status (may take a few seconds):

```bash
kubectl get csv -n operators aerospike-kubernetes-operator.v4.1.1 -w
```

---

## 🏗️ Step 3 — Configure Aerospike Namespace, ServiceAccount & Secrets

Create required namespaces, service accounts, role bindings, and secrets.  
For reference, see [Aerospike AKO Installation Docs](https://aerospike.com/docs/kubernetes/install/olm/).

```bash
# Create application namespace
kubectl create namespace aerospike

# Service account for operator controller
kubectl -n aerospike create serviceaccount aerospike-operator-controller-manager

kubectl create clusterrolebinding aerospike-cluster   --clusterrole=aerospike-cluster   --serviceaccount=aerospike:aerospike-operator-controller-manager

# NOTE: Copy your features.conf file 'secrets' folder

# Create secrets
kubectl -n aerospike create secret generic aerospike-secret --from-file=secrets
kubectl -n aerospike create secret generic auth-secret --from-literal=password='admin123'

# Create secret key to 
kubectl -n aerospike create secret generic datadog-secret --from-literal=api-key='<DATADOG_API_KEY'
```

---

## 🚀 Step 4 — Deploy Aerospike Server & Exporter

Apply the **Aerospike cluster custom resource** manifest.

```bash
kubectl apply -f dim_nostorage_cluster_skip_validation_cr.yaml
```

This YAML typically contains:
- Aerospike cluster configuration (namespace, service, storage)
- Prometheus exporter configuration for metrics
- Authentication reference to secrets created above

> 📘 Example file: `dim_nostorage_cluster_skip_validation_cr.yaml`

Verify deployment:

```bash
kubectl -n aerospike get pods
kubectl -n aerospike logs aerocluster-0-0
kubectl -n aerospike get aerospikecluster
kubectl describe pod aerocluster-0-0 -n aerospike
```

Look for the message:
```
service ready: soon there will be cake
```

---

Login to Datadog UI https://app.datadoghq.com and verify that metrics are 

---

## 🧾 Files Used in This Setup

| File Name | Purpose |
|------------|----------|
| `dim_nostorage_cluster_skip_validation_cr.yaml` | Aerospike cluster and exporter deployment (CR) |

---

## 🔍 Verification Commands

```bash
# Aerospike pods
kubectl -n aerospike get pods

# Datadog side car logs
kubectl -n aerospike logs aerocluster-0-0 -c datadog-agent --tail=50
```

---

## 🧹 Cleanup

To remove all components:

```bash
kubectl delete namespace aerospike
kubectl delete namespace operators
```

---

## 📚 References

- [Aerospike Kubernetes Operator Documentation](https://aerospike.com/docs/kubernetes)
- [Operator Lifecycle Manager](https://github.com/operator-framework/operator-lifecycle-manager)

---
