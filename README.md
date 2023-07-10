# Aerospike Monitoring Stack
This repo contains the contains examples for deploying the [Aerospike Monitoring Stack](https://www.aerospike.com/docs/tools/monitorstack/index.html) including [Grafana dashboards](./config/grafana/) and [Prometheus alerts](./config/prometheus/aerospike_rules.yml).

For more details about installing Aerospike Monitoring Stack see [Aerospike see the product documentation](https://www.aerospike.com/docs/tools/monitorstack/index.html).


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
