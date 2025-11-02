# Aerospike Monitoring Stack on Kubernetes 

This guide explains how to deploy **Aerospike Server**, **Aerospike Prometheus Exporter**, and set up **Prometheus + Grafana** monitoring on a Kubernetes cluster using the Aerospike Kubernetes Operator (AKO).

---

## 🧩 Prerequisites

- A working **Kubernetes cluster** (v1.25+)
- `kubectl` installed and configured
- Internet access to pull container images and apply manifests
- Sufficient permissions to create namespaces, CRDs, and cluster-wide roles
- Aerospike server configuration and feature files

---

## ⚙️ Step 1 — Install Cert-Manager

Cert-manager provides automatic certificate management for Kubernetes components.

```bash
# Create the namespace (harmless if it already exists)
kubectl create namespace cert-manager --dry-run=client -o yaml | kubectl apply -f -

# Install the latest stable cert-manager (includes CRDs)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml
```

Verify installation:

```bash
kubectl get pods -n cert-manager
```

---

## 🧠 Step 2 — Install Operator Lifecycle Manager (OLM)

OLM manages the installation and upgrades of Kubernetes operators.

```bash
curl -L https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.36.0/install.sh -o olm36_install.sh
chmod +x olm36_install.sh
./olm36_install.sh v0.36.0
```

Verify that OLM pods are running:

```bash
kubectl get pods -n olm
```

---

## 🧰 Step 3 — Install Aerospike Kubernetes Operator (AKO)

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

## 🏗️ Step 4 — Configure Aerospike Namespace, ServiceAccount & Secrets

Create required namespaces, service accounts, role bindings, and secrets.  
For reference, see [Aerospike AKO Installation Docs](https://aerospike.com/docs/kubernetes/install/olm/).

```bash
# Create application namespace
kubectl create namespace aerospike

# Service account for operator controller
kubectl -n aerospike create serviceaccount aerospike-operator-controller-manager

# Bind service account to roles
kubectl -n aerospike create rolebinding aerospike-cluster   --clusterrole=aerospike-cluster   --serviceaccount=aerospike:aerospike-operator-controller-manager

kubectl create clusterrolebinding aerospike-cluster   --clusterrole=aerospike-cluster   --serviceaccount=aerospike:aerospike-operator-controller-manager

# NOTE: Copy your features.conf file 'secrets' folder

# Create secrets
kubectl -n aerospike create secret generic aerospike-secret --from-file=secrets
kubectl -n aerospike create secret generic auth-secret --from-literal=password='admin123'

```

---

## 🚀 Step 5 — Deploy Aerospike Server & Exporter

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
```

Look for the message:
```
service ready: soon there will be cake
```

---

## 📊 Step 6 — Set Up Monitoring (Prometheus & Grafana)

### 6.1 Create Monitoring Namespace
```bash
kubectl create namespace monitoring
```

---

### 6.2 Deploy Prometheus

```bash
# Prometheus configuration
kubectl apply -f prometheus-config.yaml

# Prometheus deployment
kubectl apply -f prometheus-deploy.yaml

# Prometheus alerting rules
kubectl apply -f prometheus-rules.yaml
```

Verify: if Prometheus monitoring pod are UP

```bash
kubectl -n monitoring get pods
```

Access Prometheus UI via port-forwarding:
```bash
kubectl -n monitoring port-forward svc/prometheus 8090:9090
```
Open [http://localhost:8090](http://localhost:8090)

---

### 6.3 Deploy Grafana

In **File:** `grafana-deploy.yaml`, modify <b>PROVIDE_REAL_PATH_TO_DASHBOARDS</b> to the path where your grafana dashboards are synced

```bash
# Grafana deployment
kubectl apply -f grafana-deploy.yaml

# Default Prometheus Datasource 'Aerospike Prometheus'
kubectl apply -f grafana-datasource.yaml

# Load all existing Aerospike Grafana Dashboards
kubectl apply -f grafana-dashboard-provider.yaml
```

Verify that Prometheus and Grafana pods are running:

```bash
kubectl get pods -n monitoring
```

Port-forward Grafana:
```bash
kubectl -n monitoring port-forward svc/grafana 13090:3000
```
Access Grafana at [http://localhost:13090](http://localhost:13090)

> Default credentials (unless changed):  
> **Username:** `admin`  
> **Password:** `admin`

Once logged in, import the **Aerospike Dashboards** (JSON files available in Aerospike’s Grafana repo or bundled with this setup).

---

## 🧾 Files Used in This Setup

| File Name | Purpose |
|------------|----------|
| `dim_nostorage_cluster_skip_validation_cr.yaml` | Aerospike cluster and exporter deployment (CR) |
| `prometheus-config.yaml` | Prometheus scrape configuration |
| `prometheus-deploy.yaml` | Prometheus Deployment |
| `prometheus-rules.yaml` | Prometheus alert and rule configuration |
| `grafana-deploy.yaml` | Grafana Deployment |
| `grafana-datasource.yaml` | Prometheus datasource for Grafana |
| `grafana-dashboard-provider.yaml` | Grafana dashboard configuration |

---

## 🔍 Verification Commands

```bash
# Aerospike pods
kubectl -n aerospike get pods

# Monitoring pods
kubectl -n monitoring get pods

# Check metrics endpoint
kubectl -n aerospike port-forward svc/aerospike-prometheus-exporter 9145:9145
curl http://localhost:9145/metrics | head
```

---

## 🧹 Cleanup

To remove all components:

```bash
kubectl delete namespace aerospike
kubectl delete namespace monitoring
kubectl delete namespace cert-manager
kubectl delete namespace operators
```

---

## 📚 References

- [Aerospike Kubernetes Operator Documentation](https://aerospike.com/docs/kubernetes)
- [Aerospike Prometheus Exporter](https://github.com/aerospike/aerospike-prometheus-exporter)
- [Operator Lifecycle Manager](https://github.com/operator-framework/operator-lifecycle-manager)
- [Cert-Manager](https://cert-manager.io)

---
