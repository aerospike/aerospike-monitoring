# Aerospike Monitoring Stack
This repo contains the contains examples for deploying the [Aerospike Monitoring Stack](https://aerospike.com/docs/monitorstack) including [Grafana dashboards](./config/grafana/), [Prometheus Aerospike server alerts](./config/prometheus/aerospike_rules.yml) and  [Prometheus Aerospike connector alerts](./config/prometheus/aerospike_connector_rules.yml)

For more details about installing Aerospike Monitoring Stack see [Aerospike see the product documentation](https://www.aerospike.com/docs/tools/monitorstack).

## Additional Plugin depedencies
Some of the dashboard depends on external grafana plugins to render the panels, each dashboard and the plug-in dependency is mentioned below
### Multi-cluster-view dashboard
This dashboard uses 2 grafana external plugin 
#### [grafana-polystat-panel](https://grafana.com/grafana/plugins/grafana-polystat-panel)
Installation
```
grafana-cli plugins install grafana-polystat-panel
```
#### [jdbranham-diagram-panel](https://grafana.com/grafana/plugins/jdbranham-diagram-panel)
Installation
```
grafana-cli plugins install jdbranham-diagram-panel
```

## Examples for Testing
If you need to test dashboard changes the following examples will setup
an Aerospike cluster, plus Prometheus, Grafana, and Alert Manager. 

### Easy single node Aerospike cluster

A single command is needed to deploy containers for the entire monitoring stack for a single node cluster.
```
$ cd examples/docker-compose
$ docker-compose up
```
See [documentation](examples/docker-compose/).

### Open Telemetry

[Open Telemetry](https://opentelemetry.io/) makes it easier to integrate with partner solutions like Datadog,
New Relic, or Cloudwatch. See the [OTEL reference architecture](examples/otel/) for
more details. 

### AeroLab

Deploy monitoring stack using [AeroLab](https://github.com/aerospike/aerolab).  See [documentation](examples/aerolab/).
