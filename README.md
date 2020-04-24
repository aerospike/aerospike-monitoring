# Aerospike Monitoring Stack
This is now in **beta**. If you're an enterprise customer feel free to reach out to support with any questions.
We appreciate feedback from community members on the [issues](https://github.com/aerospike/aerospike-monitoring/issues).


## Aerospike Monitoring Stack On Kubernetes

[Aerospike Helm Chart](https://hub.helm.sh/charts/aerospike/aerospike-enterprise) provides Aerospike Monitoring Stack which includes an Aerospike prometheus exporter (sidecar), Prometheus statefulset, Grafana statefulset and an Alertmanager statefulset.

Aerospike Helm Chart automatically configures the entire monitoring stack including dynamic discovery of prometheus exporters.

### Quick Start Guide

- Add Aerospike repository,
    ```sh
    helm repo add aerospike https://aerospike.github.io/aerospike-kubernetes-enterprise
    ```

- Deploy an Aerospike cluster with complete monitoring stack which includes Aerospike Prometheus Exporter (sidecar), Prometheus, Grafana and Alertmanager,
    ```sh
    helm install aerospike-release aerospike/aerospike-enterprise \
                --set-file featureKeyFilePath=/secrets/aerospike/features.conf \
                --set rbac.create=true \
                --set enableAerospikeMonitoring=true
    ```
    For Helm v2,
    ```sh
    helm install --name aerospike-release aerospike/aerospike-enterprise \
                --set-file featureKeyFilePath=/secrets/aerospike/features.conf \
                --set rbac.create=true \
                --set enableAerospikeMonitoring=true
    ```

    To deploy an Aerospike cluster with Aerospike Prometheus Exporter (only) (without Prometheus/Grafana/Alertmanager statefulsets),

    ```sh
    helm install aerospike-release aerospike/aerospike-enterprise \
                --set-file featureKeyFilePath=/secrets/aerospike/features.conf \
                --set enableAerospikePrometheusExporter=true
    ```
    For Helm v2,
    ```sh
    helm install --name aerospike-release aerospike/aerospike-enterprise \
                --set-file featureKeyFilePath=/secrets/aerospike/features.conf \
                --set enableAerospikePrometheusExporter=true
    ```

- To check the status of all created resources,
  ```sh
  kubectl get all,configmap --namespace default -l "release=aerospike-release, chart=aerospike-enterprise-4.8.0"
  ```

- Aerospike Helm Chart comes with a basic set of alert rules configured, which can trigger and send alerts to the Alertmanager Pods.

    To apply a custom rules configuration, use option `--set-file prometheus.aerospikeAlertRulesFilePath=<FILE_PATH>` with `helm install`.

    To add an alertmanager configuration file, use option `--set-file alertmanager.alertmanagerConfFilePath=<FILE_PATH>` with `helm install`.

- Prometheus and Grafana dashboards can be viewed on localhost using `kubectl port-forward`,
  ```sh
  # To view Prometheus dashboard at http://localhost:9090
  kubectl port-forward service/aerospike-release-prometheus 9090:9090

  # To view Grafana dashboard at http://localhost:8080
  kubectl port-forward service/aerospike-release-grafana 8080:80
  ```

- To uninstall or delete the release (cleanup all resources associated with the release),
  ```sh
  helm uninstall aerospike-release
  ```
  For Helm v2,

  ```sh
  helm delete aerospike-release --purge
  ```

- [Aerospike Helm Chart Configuration Section](https://github.com/aerospike/aerospike-kubernetes-enterprise/tree/master/helm#configuration) contains a list of other configurable options that can be used with `helm install`.

- Additional references

  - Aerospike Helm Chart : https://hub.helm.sh/charts/aerospike/aerospike-enterprise
  - Install Helm : https://helm.sh/docs/intro/install/
  - `kubectl` usage : https://kubernetes.io/docs/reference/kubectl/cheatsheet/

## Installing Aerospike Prometheus Exporter

Aerospike Prometheus Exporter can be compiled and built from the source [aerospike/aerospike-prometheus-exporter](https://github.com/aerospike/aerospike-prometheus-exporter) GitHub repository.

- Use [build/docker-compose.yaml](build/docker-compose.yaml) file to quickly build `aerospike-prometheus-exporter` binary for `linux` and `osx` platforms.
    ```
    git clone https://github.com/aerospike/aerospike-monitoring.git
    cd aerospike-monitoring/

    docker-compose -f build/docker-compose.yaml up
    ```

- Aerospike Prometheus Exporter requires a configuration file to run. Here's a [sample configuration file](https://raw.githubusercontent.com/aerospike/aerospike-prometheus-exporter/master/aeroprom.conf.dev).
    ```
    curl https://raw.githubusercontent.com/aerospike/aerospike-prometheus-exporter/master/aeroprom.conf.dev -o ./build/ape.toml
    ```

### Aerospike Prometheus Exporter Configuration

- As a minimum required configuration, edit `./build/ape.toml` to add `db_host` and `db_port` to point to an Aerospike server IP and port.
    ```toml
    [Aerospike]

    db_host="localhost"
    db_port=3000
    ```
- Update Aerospike security and TLS configurations (if applicable),
    ```toml
    [Aerospike]

    # certificate file
    cert_file=""

    # key file
    key_file=""

    # Passphrase for encrypted key_file. Supports below formats,
    # 1. Passphrase directly                 - "<passphrase>"
    # 2. Passphrase via file                 - "file:<file-that-contains-passphrase>"
    # 3. Passphrase via environment variable - "env:<environment-variable-that-holds-passphrase>"
    key_file_passphrase=""

    # node TLS name for authentication
    node_tls_name=""

    # root certificate file
    root_ca=""

    # authentication mode: internal (for server), external (LDAP, etc.)
    auth_mode=""

    # database user
    user=""

    # database password
    password=""
    ```

- Update exporter's bind address and port (default: `0.0.0.0:9145`), and add tags.
    ```toml
    [Agent]

    bind=":9145"

    tags=['agent', 'aerospike']
    ```

- Use metrics whitelist to filter out required metrics (optional). The whitelist supports standard wildcards (globbing patterns which include - `? (question mark)`, `* (asterisk)`, `[ ] (square brackets)`, `{ } (curly brackets)`, `[!]` and `\ (backslash)`) for bulk whitelisting. For example,
    ```toml
    [Aerospike]

    # Metrics Whitelist - If specified, only these metrics will be scraped. An empty list will exclude all metrics.
    # Commenting out the below whitelist configs will disable whitelisting (all metrics will be scraped).

    # Namespace metrics whitelist
    namespace_metrics_whitelist=[
    "client_read_[a-z]*",
    "stop_writes",
    "storage-engine.file.defrag_q",
    "client_write_success",
    "memory_*_bytes",
    "objects",
    "*_available_pct"
    ]

    # Set metrics whitelist
    set_metrics_whitelist=[
    "objects",
    "tombstones"
    ]

    # Node metrics whitelist
    node_metrics_whitelist=[
    "uptime",
    "cluster_size",
    "batch_index_*",
    "xdr_ship_*"
    ]

    # XDR metrics whitelist (only for server versions 5.0 and above)
    xdr_metrics_whitelist=[
    "success",
    "latency_ms",
    "throughput",
    "lap_us"
    ]
    ```

- To enable basic HTTP authentication and/or enable HTTPS between the Prometheus server and the exporter, use the below configurations keys (optional),

  ```toml
  [Agent]

  # File paths should be double quoted.

  # Certificate file for the metric servers for prometheus
  cert_file = ""

  # Key file for the metric servers for prometheus
  key_file = ""

  # Basic HTTP authentication for '/metrics'.
  basic_auth_username=""
  basic_auth_password=""
  ```

### Installation

- Add the `aerospike-prometheus-exporter` binary to `/usr/local/bin` and add `ape.toml` file to `/etc/aerospike-prometheus-exporter/ape.toml`.
    ```sh
    cp ./build/aerospike-prometheus-exporter-linux /usr/local/bin/aerospike-prometheus-exporter
    mkdir /etc/aerospike-prometheus-exporter
    cp ./build/ape.toml /etc/aerospike-prometheus-exporter/ape.toml
    ```

- Create a systemd unit file for `aerospike-prometheus-exporter.service`,
    ```
    # cat /usr/lib/systemd/system/aerospike-prometheus-exporter.service

    [Unit]
    Description=Aerospike Prometheus Exporter Service
    Documentation=https://github.com/aerospike/aerospike-prometheus-exporter
    Wants=network.target
    After=network.target

    [Service]
    ExecStart=/usr/local/bin/aerospike-prometheus-exporter --config /etc/aerospike-prometheus-exporter/ape.toml

    [Install]
    WantedBy=multi-user.target
    ```
    ```
    systemctl daemon-reload
    ```

- Run `aerospike-prometheus-exporter`,
    ```sh
    systemctl start aerospike-prometheus-exporter.service
    ```


## Prometheus Configuration

This section covers the configuration of Prometheus server to scrape metrics from Aerospike Prometheus Exporter, send alerts to an Alertmanager instance and add an Aerospike alert rules configuration file.


### Install Prometheus

https://prometheus.io/docs/prometheus/latest/installation/

### Configuration

Create a Prometheus configuration file `/etc/prometheus/prometheus.yml`,
- Add `scrape_configs` with `targets` pointing to each instance of `aerospike-prometheus-exporter`.
    ```yaml
    scrape_configs:
      - job_name: 'aerospike'
        static_configs:
          - targets: ['172.20.0.2:9145', '172.20.0.3:9145']
    ```
- To enable `alerting`, add alertmanager instance's `IP:Port` target.
    ```yaml
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - "alertmanager:9093"
    ```
- Add [aerospike rules configuration file](config/prometheus/aerospike_rules.yml) to path `/etc/prometheus/aerospike_rules.yaml` and configure `rule_files` to point to the same.
    ```yaml
    rule_files:
      - "/etc/prometheus/aerospike_rules.yaml"
    ```

    ```yaml
    # /etc/prometheus/prometheus.yml

    # Global Configuration
    global:
      scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
      evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.

    # Alertmanager Configuration
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - "alertmanager:9093"

    # Add Aerospike Rules YAML File
    rule_files:
    - "/etc/prometheus/aerospike_rules.yaml"

    # Scrape Configuration. Must point to Aerospike Prometheus Exporter
    scrape_configs:
    # The job name 'aerospike' is added as a label `job=aerospike` to any timeseries scraped from this config.
    - job_name: 'aerospike'

        # metrics_path defaults to '/metrics'
        # scheme defaults to 'http'.
      static_configs:
        - targets: ['172.20.0.2:9145', '172.20.0.3:9145']
    ```

- Create a data directory for Prometheus to store the metrics data,
    ```sh
    mkdir /var/lib/prometheus
    ```

### Start Prometheus Server

- Start Prometheus server.
    ```sh
    /usr/local/bin/prometheus --config.file /etc/prometheus/prometheus.yml \
                              --storage.tsdb.path /var/lib/prometheus/
    ```
  OR,

- (Optional) Create a systemd unit file for `prometheus.service`,
    ```
    # cat /usr/lib/systemd/system/prometheus.service

    [Unit]
    Description=Prometheus Service
    Documentation=https://prometheus.io/docs/introduction/overview/
    Wants=network.target
    After=network.target

    [Service]
    ExecStart=/usr/local/bin/prometheus --config.file /etc/prometheus/prometheus.yml --storage.tsdb.path /var/lib/prometheus/

    [Install]
    WantedBy=multi-user.target
    ```
    ```sh
    systemctl daemon-reload
    ```
    ```sh
    systemctl start prometheus.service
    ```

### Prometheus Dashboard

An example query to compute and view Read TPS is shown below.

The query selects data with `aerospike_namespace_client_read_success` metric name that has `job` label as `aerospike` and `cluster_name` as `aerospike-release-aerospike-enterprise` and passes it into `rate()` function which returns per second average rate of increase.

```sh
rate(aerospike_namespace_client_read_success{job="aerospike", cluster_name="aerospike-release-aerospike-enterprise"}[1m])+
rate(aerospike_namespace_client_read_not_found{job="aerospike", cluster_name="aerospike-release-aerospike-enterprise"}[1m])
```

![Prometheus Dashboard Example Console](resources/prometheus_query_console.png)

![Prometheus Dashboard Example Graph](resources/prometheus_query_graph.png)

Other than querying data, there are few additional things that can also be checked on the dashboard like status of scrape targets, alert rules, configuration etc.

![Prometheus Dashboard Example](resources/prometheus_dashboard.png)

References:

  - https://prometheus.io/docs/prometheus/latest/querying/basics/
  - https://prometheus.io/docs/prometheus/latest/querying/examples/


## Grafana Configuration

This section covers the configuration of Grafana server to add Prometheus datasource, Alertmanager datasource and Aerospike dashboards.

### Install Grafana

https://grafana.com/docs/grafana/latest/installation/

### Configuration

- Add `provisioning` config directory path in `/etc/grafana/grafana.ini`.  If installing on an Aerospike cluster node change the default Grafana HTTP port in addition to changes listed below.

    ```ini
    [paths]
    provisioning = /etc/grafana/provisioning/
    ```

- Create two directories `dashboards` and `datasources` under `provisioning` path.
    ```
    mkdir -p /etc/grafana/provisioning/datasources
    mkdir -p /etc/grafana/provisioning/dashboards
    ```

- Create a file `all.yaml` in `/etc/grafana/provisioning/dashboards/` directory to add a dashboard provider that will load dashboards into Grafana from the local filesystem. Here, the path to dashboard files is configured as `/var/lib/grafana/dashboards`.
    ```yaml
    # /etc/grafana/provisioning/dashboards/all.yaml

    apiVersion: 1

    providers:
    # <string> an unique provider name
    - name: 'default'
        # <int> org id. will default to orgId 1 if not specified
        # orgId: 1

        # <string, required> name of the dashboard folder. Required
        folder: 'Aerospike'

        # <string, required> provider type. Required
        type: file

        # <bool> disable dashboard deletion
        disableDeletion: false

        # <bool> enable dashboard editing
        editable: true

        # <int> how often Grafana will scan for changed dashboards
        updateIntervalSeconds: 10

        options:
        # <string, required> path to dashboard files on disk. Required
          path: /var/lib/grafana/dashboards
    ```

- Create a file `all.yaml` in `/etc/grafana/provisioning/datasources/` directory to define datasources.
    ```yaml
    # /etc/grafana/provisioning/datasources/all.yaml

    apiVersion: 1

    datasources:
    - name: "Aerospike Prometheus Alertmanager"
      type: camptocamp-prometheus-alertmanager-datasource
      access: proxy
      url: http://alertmanager:9093
      editable: true
      isDefault: false

    - name: "Aerospike Prometheus"
      type: prometheus
      access: proxy
      url: http://prometheus:9090
      editable: true
      isDefault: false

    ```

- Install `camptocamp-prometheus-alertmanager-datasource` plugin for Alertmanager datasource.
    ```sh
    grafana-cli plugins install camptocamp-prometheus-alertmanager-datasource
    ```

- Add [dashboard files from this repository](config/grafana/dashboards/) to `/var/lib/grafana/dashboards/` directory.

### Start Grafana Server

- Start Grafana server.
    ```sh
    systemctl start grafana-server
    ```

### Grafana Dashboards

To view [Aerospike Dashboards](config/grafana/dashboards/),

- Once logged into grafana, click on dashboards icon on left top corner (which also says "Home" with a drop-down)

  ![Navigate to dashboards](resources/navigate_to_dashboards.png)

- Select Aerospike folder, and select any one of the dashboard to view.

  ![Select Aerospike dashboards](resources/select_aerospike_dashboards.png)

- Screenshot - Cluster overview dashboard

  ![Cluster overview](resources/cluster_overview_dashboard.png)

- Screenshot - Node overview dashboard

  ![Node overview](resources/node_overview_dashboard.png)


## Alertmanager Configuration

Alertmanager supports various configuration depending on where the notifications need to be sent.

An example configuration for generating notifications to a slack channel is shown below.

```yaml
# This is an example alertmanager.yaml which sends alert notifications to a slack channel.

global:
  slack_api_url: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
route:
  group_by: ['alertname', 'cluster', 'service']
  receiver: slack_general

receivers:
- name: slack_general
  slack_configs:
  - channel: '#channel'
    text: "summary: {{ .CommonAnnotations.summary }}\ndescription: {{ .CommonAnnotations.description }}"
```

For more details, check [Alertmanager Documentation](https://prometheus.io/docs/alerting/configuration/#configuration).

## Deploy Prometheus, Grafana and Alertmanager using `docker-compose`

An example [docker-compose.yml](docker-compose.yml) file is included in this repository which deploys Prometheus, Grafana and Alertmanager and uses dashboards, alert rules and other configurations defined in [config](config/) directory.


## Other Examples

For other quick examples, check [examples/](examples/) directory.
