# Aerospike Kubernetes Operator Setup with Datadog and Prometheus Monitoring

This repository provides step-by-step instructions for deploying the [Aerospike Kubernetes Operator](https://aerospike.com/docs/cloud/kubernetes/operator/) in a local or cloud-based Kubernetes cluster. It also includes optional integration with **Datadog** and **Prometheus/Grafana** for monitoring.

---
##  Prerequisites

- Kubernetes cluster (local like `k3d`, `minikube` or any cloud provider)
- `kubectl` and `helm` CLI installed
- Datadog API key (for Datadog monitoring)
---
##  Quick Start: Set Up a Local Kubernetes Cluster

Choose one of the following tools to spin up a local Kubernetes cluster:

1. **Install k3d**  
    [Installation Guide](https://k3d.io/#installation)  
   Or run:
   ```bash
   wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
   curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
   ```
---

##  Clone the Aerospike Kubernetes Operator Repository

```bash
git clone https://github.com/aerospike/aerospike-kubernetes-operator.git
cd aerospike-kubernetes-operator
```

---

##  Step 1: Install Operator Lifecycle Manager (OLM)

```bash
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.25.0/install.sh | bash -s v0.25.0
```

---

##  Step 2: Deploy the Aerospike Kubernetes Operator

```bash
kubectl create -f https://operatorhub.io/install/aerospike-kubernetes-operator.yaml
```

Verify operator installation:

```bash
kubectl get csv -n operators aerospike-kubernetes-operator.v4.0.1 -w
```
Check operator logs

```bash
kubectl -n operators logs -f deployment/aerospike-operator-controller-manager manager
```
---

##  Step 3: Set Up Namespace and Permissions

```bash
kubectl create namespace aerospike

kubectl -n aerospike create serviceaccount aerospike-operator-controller-manager

kubectl create clusterrolebinding aerospike-cluster   --clusterrole=aerospike-cluster   --serviceaccount=aerospike:aerospike-operator-controller-manager
```

Verify the permissions:

```bash
kubectl edit clusterrolebinding aerospike-cluster
```

Ensure `serviceAccount` references the `aerospike` namespace.

---

##  Step 4: Create Secrets

Copy features.conf file to secrets directory:

```bash
cp $features.conf path  /aerospike-kubernetes-operator/config/samples/secrets
```

Create Kubernetes secrets:

```bash
cd /aerospike-kubernetes-operator/config/samples
kubectl -n aerospike create secret generic aerospike-secret --from-file=secrets
kubectl -n aerospike create secret generic auth-secret --from-literal=password='admin123'
```

---

##  Step 5: Deploy Aerospike Cluster

### Option A: Aerospike Cluster with Datadog Agent as Sidecar

###  Overview
This method deploys:
- An **Aerospike server** container
- A **Prometheus Exporter** as a sidecar
- A **Datadog Agent** as a sidecar
- Secret management for Datadog credentials
###  Setup Instructions

#### (i) Create Kubernetes Secret for Datadog
Update `datadog-secret.yaml` with your Datadog credentials:
```yaml
DD_API_KEY: <your-datadog-api-key>
DD_SITE: <your-datadog-site> # e.g., us5.datadoghq.com
metadata:
  name: datadog-secret
  namespace: aerospike
```
Apply the secret:
```bash
kubectl apply -f datadog-secret.yaml
```
#### (ii) Deploy Aerospike Cluster with Sidecars
Update and apply `Aerospike_CR_DD_Sidecar_Aerospike.yaml`:
```
# name: Name of the Aerospike cluster (e.g., test-env) 
# namespace: Namespace where the cluster and related resources will be deployed (e.g., aerospike) 
# size: Number of Aerospike nodes (e.g., 1, 3) 
# image: Aerospike server image and version (e.g., aerospike/aerospike-server-enterprise:8.0.0.5) 
# image: Prometheus exporter image and version (e.g., aerospike/aerospike-prometheus-exporter:1.22.0) 
# image: Datadog Agent image (e.g., gcr.io/datadoghq/agent:latest) 
# DD_API_KEY: Your Datadog API key (store in Kubernetes Secret) 
# - name: secret name  
# DD_SITE: Your Datadog site (e.g., us5.datadoghq.com) 
# - name: secret name  
# prometheus_url: Prometheus exporter endpoint (e.g., http://localhost:9145/metrics) 
# cluster_name: Custom tag for identifying your Aerospike cluster in Datadog (e.g., aerospike_cluster) 
# service: Custom tag for identifying the service (e.g., aerospike_service) 
# name: Name of the Datadog scrape config ConfigMap (e.g., datadog-scrape-config) 
# path: Path where the config will be mounted inside the Datadog Agent container (e.g., /etc/datadog-agent/conf.d/openmetrics.d/) 
# secretName: Name of the secret containing the Aerospike feature key (e.g., aerospike-secret) 
```
```bash
kubectl apply -f Aerospike_CR_DD_Sidecar_Aerospike.yaml -n aerospike
```
#### (iii) Verify Resources
```bash
kubectl get pods -n aerospike
```
Go to [Datadog Metrics Explorer](https://app.datadoghq.com/metrics/explorer) and search:
```
aerospike.*
```
```bash
kubectl apply -f config/samples/dim_nostorage_cluster_cr.yaml -n aerospike
```

## Option B: Aerospike Cluster with Datadog Agent as Daemonset

###  Overview
This method deploys:
- An **Aerospike server** container
- A **Prometheus Exporter** as a sidecar
- A **Datadog Agent** as a DaemonSet
- Datadog Autodiscovery with Aerospike integration
###  Setup Instructions
#### (i) Create Datadog API Key Secret
```bash
kubectl create secret generic datadog-api-key \
  --namespace aerospike \
  --from-literal=api-key=<your-datadog-api-key>
```
#### (ii) Deploy Aerospike Cluster with Exporter
Update `Aerospike_CR_DD_Daemonset_Aerospike.yaml` with cluster configuration and annotations:
```
# name: Name of the Aerospike cluster (e.g., testenv) 
# namespace: Namespace where the cluster and related resources will be deployed (e.g., aerospike) 
# size: Number of Aerospike nodes (e.g., 1, 3) 
# image: Aerospike server image and version (e.g., aerospike/aerospike-server-enterprise:8.0.0.5) 
# multiPodPerHost: Allow multiple Aerospike pods to run on a single Kubernetes node 
# name (sidecar): Name of the Prometheus exporter sidecar container 
# image (sidecar): Prometheus exporter image and version (e.g., aerospike/aerospike-prometheus-exporter:1.22.0) 
# secretName: Name of the Kubernetes Secret containing Aerospike config (e.g., aerospike-secret) 
```
Use the following annotations in your Yaml file as per integration 
- Datadog Aerospike integration reference: [Official Docs](https://docs.datadoghq.com/integrations/aerospike/?tab=containerized)

```yaml
annotations:
  ad.datadoghq.com/aerospike-prometheus-exporter.checks: |
    {
      "aerospike": {
        "init_config": {},
        "instances": [
          {
            "openmetrics_endpoint": "http://%%host%%:9145/metrics"
          }
        ],
        "tags": ["env:dev123"]
      }
    }
```
##  Notes

- If you use  `init_config [{}]`, the check will use the global Datadog Agent settings. 
- Override this to customize behavior, such as: 
  - Add scrape timeout: `[{ "timeout": 10 }]` 
  - Skip SSL verification: `[{ "ssl_verify": false }]`  
  - Use bearer token: `[{ "bearer_token": "your-token-here" }]` 

Apply the manifest:
```bash
kubectl apply -f Aerospike_CR_DD_Daemonset_Aerospike.yaml -n aerospike
```
#### (iii) Install Datadog Agent via Helm

Create `values.yaml`:
```yaml
datadog:
  site: us5.datadoghq.com
  prometheusScrape:
    enabled: true
  apiKeyExistingSecret: datadog-api-key
```

Install the Agent:
```bash
helm repo add datadog https://helm.datadoghq.com
helm repo update

helm install datadog-agent datadog/datadog \
  --namespace aerospike \
  -f values.yaml
```

#### Step 5: Verify Resources
```bash
kubectl get pods -n aerospike
```

Search in Datadog Metrics Explorer for:
```
aerospike.*
```

---
##  Files List

| File | Description |
|------|-------------|
| `datadog-secret.yaml` | Datadog API key + site Kubernetes Secret |
| `Aerospike_CR_DD_Sidecar_Aerospike.yaml` | Aerospike Cluster with Prometheus + Datadog sidecars |
| `Aerospike_CR_DD_Daemonset_Aerospike.yaml` | Aerospike Cluster with Prometheus sidecar + DaemonSet Agent |
| `values.yaml` | Helm config for installing Datadog Agent as DaemonSet |

---
##  Step 6: Set Up Prometheus and Grafana Monitoring

### 6.1 Add Helm Repo

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### 6.2 Install kube-prometheus-stack

Use your custom `prom_values.yaml` file for fine-tuned configuration.

```bash
helm install prometheus prometheus-community/kube-prometheus-stack   -n monitoring --create-namespace -f prom_values.yaml
```

### 6.3 Access Grafana Dashboard

```bash
kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80
```

Visit: [http://localhost:3000](http://localhost:3000)

**Default credentials:**

- Username: `admin`
- Password: `prom-operator` *(unless overridden in values file)*

---

##  Observability Notes

- Aerospike metrics will be exposed under the `aerospike_*` family.
- With Datadog integration, metrics appear under the `aerospike.*` namespace.
- You can import Aerospike dashboards into Grafana from:  
  [https://github.com/aerospike/aerospike-monitoring](https://github.com/aerospike/aerospike-monitoring)

---
##  References

- [Aerospike Kubernetes Operator Docs](https://aerospike.com/docs/cloud/kubernetes/operator/)
- [OperatorHub Aerospike Operator](https://operatorhub.io/operator/aerospike-kubernetes-operator)
- [Datadog Kubernetes Monitoring Guide](https://docs.datadoghq.com/agent/kubernetes/)
- [kube-prometheus-stack Helm Chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)

---
