#  Aerospike + Datadog Agent Integration (Kubernetes)

This document describes two approaches for integrating an **Aerospike cluster on Kubernetes** with **Datadog monitoring** using **OpenMetrics Integration** and **Aerospike Integration**


## 1. **Openmetrics Integration**
There are two ways to implement this integration:  
**(i). Sidecar Setup** — Deploy Datadog Agent as a sidecar alongside the Aerospike Prometheus Exporter.  
**(ii). DaemonSet Setup** — Run Datadog Agent as a cluster-wide DaemonSet using Autodiscovery annotations.

## (i).Sidecar Setup
###  Overview
This method deploys:
- An **Aerospike server** container
- A **Prometheus Exporter** as a sidecar
- A **Datadog Agent** as a sidecar
- Secret management for Datadog credentials
###  Setup Instructions
#### Step 1: Create Namespace
```bash
kubectl create namespace aerospike
```
#### Step 2: Create Kubernetes Secret for Datadog
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
#### Step 3: Deploy Aerospike Cluster
Update `Aerospike_CR_DD_Sidecar_Openmetrics.yaml` as needed and apply:
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
Apply the manifest:
```bash
kubectl apply -f Aerospike_CR_DD_Sidecar_Openmetrics.yaml -n aerospike
```
#### Step 4: Verify Resources
```bash
kubectl get pods -n aerospike
```
Go to [Datadog Metrics Explorer](https://app.datadoghq.com/metrics/explorer) and search for:
```
aerospike.*
```

## (ii). DaemonSet Setup
### Overview
This method deploys:
- An **Aerospike server** container
- A **Prometheus Exporter** as a sidecar
- A **Datadog Agent** as a DaemonSet
- Autodiscovery-based OpenMetrics configuration
### Setup Instructions
#### Step 1: Create Namespace
```bash
kubectl create namespace aerospike
```
#### Step 2: Create Datadog API Key Secret
```bash
kubectl create secret generic datadog-api-key \
  --namespace aerospike \
  --from-literal=api-key=<your-datadog-api-key>
```
#### Step 3: Deploy Aerospike Cluster with Exporter
Update `Aerospike_CR_DD_Daemonset_Openmetrics.yaml` with cluster configuration and Datadog annotations.
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
- Datadog Aerospike integration reference: [Official Docs](https://docs.datadoghq.com/containers/kubernetes/integrations/?tab=annotations)
  
```yaml
      annotations:
        ad.datadoghq.com/aerospike-prometheus-exporter.check_names: '["openmetrics"]'  
        ad.datadoghq.com/aerospike-prometheus-exporter.init_configs: '[{}]'
        ad.datadoghq.com/aerospike-prometheus-exporter.instances: |
          [
            {
              "prometheus_url": "http://%%host%%:9145/metrics",
              "namespace": "aerospike",
              "metrics": ["*"],
              "labels_mapper": {
                "cluster_name": "aerospike_cluster",
                "service": "aerospike_service"
              },
              "tags": ["env:dev123"]
            }
          ]
```
##  Notes
- If you use  `init_config [{}]`, the check will use the global Datadog Agent settings. 
- Override this to customize behavior, such as: 
  - Add scrape timeout: `[{ "timeout": 10 }]` 
  - Skip SSL verification: `[{ "ssl_verify": false }]`  
  - Use bearer token: `[{ "bearer_token": "your-token-here" }]` 
  
Apply the manifest:
```bash
kubectl apply -f Aerospike_CR_DD_Daemonset_Openmetrics.yaml -n aerospike
```
#### Step 4: Install Datadog Agent via Helm

Create `values.yaml` and install the agent:
```yaml
datadog:
  site: us5.datadoghq.com
  prometheusScrape:
    enabled: true
  apiKeyExistingSecret: datadog-api-key
```
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
You should see: 
  - Aerospike pods 
  - Datadog Agent pods (1 per node) 

Search in Datadog Metrics Explorer for:
```
aerospike.*
```
---

## 2. **Aerospike Integration**

There are two ways to implement this integration:  
**(i). Sidecar Setup** — Deploy Datadog Agent as a sidecar alongside the Aerospike Prometheus Exporter.  
**(ii). DaemonSet Setup** — Run Datadog Agent as a cluster-wide DaemonSet using Autodiscovery annotations.

## (i). Sidecar Setup
###  Overview
This method deploys:
- An **Aerospike server** container
- A **Prometheus Exporter** as a sidecar
- A **Datadog Agent** as a sidecar
- Secret management for Datadog credentials
###  Setup Instructions
#### Step 1: Create Namespace
```bash
kubectl create namespace aerospike
```
#### Step 2: Create Kubernetes Secret for Datadog
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
#### Step 3: Deploy Aerospike Cluster with Sidecars
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
#### Step 4: Verify Resources
```bash
kubectl get pods -n aerospike
```
Go to [Datadog Metrics Explorer](https://app.datadoghq.com/metrics/explorer) and search:
```
aerospike.*
```
##  (ii). DaemonSet Setup

###  Overview
This method deploys:
- An **Aerospike server** container
- A **Prometheus Exporter** as a sidecar
- A **Datadog Agent** as a DaemonSet
- Datadog Autodiscovery with Aerospike integration
###  Setup Instructions
#### Step 1: Create Namespace
```bash
kubectl create namespace aerospike
```
#### Step 2: Create Datadog API Key Secret
```bash
kubectl create secret generic datadog-api-key \
  --namespace aerospike \
  --from-literal=api-key=<your-datadog-api-key>
```
#### Step 3: Deploy Aerospike Cluster with Exporter
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
#### Step 4: Install Datadog Agent via Helm
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
You should see: 
Aerospike pods 
Datadog Agent pods (1 per node) 

Search in Datadog Metrics Explorer for:
```
aerospike.*
```
