# Aerospike on Kubernetes (Server + Prometheus Exporter)

This document describes how to run **Aerospike Server** and the **Aerospike Prometheus Exporter** on Kubernetes, using the manifests in this repo. It covers:
1. Namespace / prerequisites
2. Deploying Aerospike
3. Deploying the exporter
4. Verifying metrics
5. (Optional) Wiring to Datadog / Prometheus
6. Troubleshooting

> **Note:** This README assumes you already have a working Kubernetes cluster (`kubectl` configured) and an image registry accessible by the cluster.

---

## 1. Prerequisites

- Kubernetes **1.25+** (adjust if yours is different)
- `kubectl` installed and pointing to the correct cluster
- Storage provisioner available (for Aerospike persistence) – or you can run in-memory
- (Optional) Access to container registry for custom images
- (Optional) Prometheus / Datadog in the cluster

Create a namespace (or use `default`):

```sh
kubectl create namespace aerospike

