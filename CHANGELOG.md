# Changelog

This file documents all notable changes to Aerospike Monitoring Stack

## [v1.1.0](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.1.0)

- Add description info to each dashboard panel.
- Add `clock_skew_stop_writes` to `Namespace View` and `Cluster View` dashboards.
- Add dashboard support for the new latency metrics change in [Aerospike Prometheus Exporter v1.1.0](https://github.com/aerospike/aerospike-prometheus-exporter/releases/tag/v1.1.0).
- Remove `aerospike_node_info` metric as per [Aerospike Prometheus Exporter v1.1.0](https://github.com/aerospike/aerospike-prometheus-exporter/releases/tag/v1.1.0).
- Show Primary index usage for namespaces using `index-type` `flash` or `pmem`.
- Increase default Grafana refresh rate to `1m`.
- Fix primary index usage panel to show values in `MiB`/`GiB`.


## [v1.0.0](https://github.com/aerospike/aerospike-monitoring/releases/tag/v1.0.0)

- Initial Release