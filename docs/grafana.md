# Configure Grafana

This document describes how to configure a Grafana server to add the Prometheus datasource, Alertmanager datasource, and Aerospike dashboards.

## Overview

The configuration involves:
1. Editing the `grafana.ini` file
2. Adding Prometheus and AlertManager datasources
3. Adding or upgrading dashboards

## Edit the `grafana.ini` file

1. Open the file `/etc/grafana/grafana.ini` for editing.

> **Note**: If you are running Grafana in a Docker container, log in to the running container as root. Only the root user has permission to write to this file.

2. Make the file writeable:
```bash
chmod 664 /etc/grafana/grafana.ini
```

3. Configure the provisioning directory in the `[paths]` section:
```ini
[paths]
# folder that contains provisioning config files that grafana will apply on startup and while running.
provisioning = /etc/grafana/provisioning
```

4. If you installed Grafana on an Aerospike cluster node, change the HTTP port (default is 3000, which conflicts with Aerospike):
```ini
[server]
# The http port to use
http_port = 3100
```

## Add Prometheus and AlertManager Datasources

1. Install the Alertmanager plugin:
```bash
grafana-cli plugins install camptocamp-prometheus-alertmanager-datasource
```

2. Create the datasources directory:
```bash
mkdir -p /etc/grafana/provisioning/datasources
cd /etc/grafana/provisioning/datasources
```

3. Download Aerospike's example configuration:
```bash
wget https://raw.githubusercontent.com/aerospike/aerospike-monitoring/master/config/grafana/provisioning/datasources/all.yaml
```

4. Edit the URLs in the file to point to your Prometheus and AlertManager servers with their respective ports.

## Add or Upgrade Dashboards

> **Caution**: The following procedure overwrites any changes you have made to your dashboards. To preserve existing dashboards, rename them and change their ID before proceeding.

1. Download the latest version of the monitoring stack:
```bash
wget https://github.com/aerospike/aerospike-monitoring/archive/refs/tags/v3.8.0.tar.gz
```

2. Extract the downloaded archive:
```bash
tar -xvf v3.8.0.tar.gz
```

3. Copy the dashboards folder to the provisioning directory:
```bash
cp -R ./aerospike-monitoring/config/grafana/dashboards /var/lib/grafana/dashboards
```

4. Restart Grafana to apply all changes.

## Additional Resources

- [Aerospike Monitoring Stack](https://github.com/aerospike/aerospike-monitoring)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus AlertManager Datasource Plugin](https://grafana.com/grafana/plugins/camptocamp-prometheus-alertmanager-datasource/) 