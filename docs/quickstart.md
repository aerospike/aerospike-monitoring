# Install with Docker

This document describes how to install and run the Aerospike monitoring stack components using Docker containers.

## Prerequisites

- A running Aerospike instance. See [Install Aerospike](https://aerospike.com/docs/operations/install) for deployment instructions for your platform.
- If you want to monitor an Aerospike outbound connector, but you do not have an instance deployed, see [Streaming from Aerospike](https://aerospike.com/docs/connectors/enterprise/streaming) for deployment instructions.

## 1. Run Aerospike Prometheus Exporter

Aerospike provides docker images for the Aerospike Prometheus Exporter on Docker Hub.

Run Aerospike Prometheus Exporter and connect to an Aerospike database. This example command assumes that the Aerospike database was deployed in a container named `aerospike` on the same system:

```bash
docker run -itd --name exporter \
  --link="aerospike" \
  -e AS_HOST=aerospike \
  -e AS_PORT=3000 \
  -e METRIC_LABELS="type='development',source='aerospike'" \
  -p 9145:9145 \
  aerospike/aerospike-prometheus-exporter:latest
```

Configuration parameters:
- `AS_HOST`: The IP address of a node of the Aerospike database
- `AS_PORT`: The client-access port for the database

## 2. Run Prometheus

Run a Prometheus container and configure the exporter as a scrape target.

1. Create `prometheus.yml` with this content:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'aerospike'
    static_configs:
      - targets: ['exporter:9145']
```

2. Run the Prometheus container:

```bash
docker run -tid --name prometheus \
  --link="exporter" \
  -p 9090:9090 \
  -v <Path_of_prometheus.yml>:/etc/prometheus/prometheus.yml \
  prom/prometheus:latest
```

View metrics on a Prometheus dashboard at http://localhost:9090.

## 3. Run Grafana

Grafana's default port is 3000, however Aerospike is already bound to ports 3000, 3001, and 3002. To avoid a conflict, you must use the `-p` flag to rebind Grafana to a new port outside this range. The following example rebinds it to `3003`:

```bash
docker run -d --name grafana -p 3003:3000 grafana/grafana
```

Visit http://localhost:3003/ to access the dashboard.

> **Note**: The previous steps describing how to run Grafana in a Docker container represent a general process useful for getting to know the software. For a video tutorial and more information about less commonly-used command line options, see [Run Grafana Docker image](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/) in the Grafana documentation.

You can import dashboards for monitoring your Aerospike database from the [Aerospike Monitoring repository](https://github.com/aerospike/aerospike-monitoring) on GitHub.

## Additional Resources

- [Aerospike Monitoring Stack](https://github.com/aerospike/aerospike-monitoring)
- [Prometheus Docker Documentation](https://prometheus.io/docs/prometheus/latest/installation/)
- [Grafana Docker Documentation](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/) 